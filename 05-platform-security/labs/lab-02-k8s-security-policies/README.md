# Lab 02: Kubernetes Security Policies

Implement defense-in-depth K8s security: RBAC least-privilege, NetworkPolicies, Pod Security Standards, and OPA/Kyverno admission control. Terraform provisions the cluster and policy infrastructure.

## Objectives

- Provision a local K8s cluster with Terraform (minikube)
- Implement Pod Security Standards (restricted profile)
- Create NetworkPolicies for microsegmentation
- Deploy Kyverno with custom security policies
- Build RBAC roles with least-privilege access
- Test each control by attempting policy violations

## Prerequisites

```bash
minikube start --driver=docker --memory=4096 --cpus=2
# Install Kyverno
kubectl apply -f https://github.com/kyverno/kyverno/releases/latest/download/install.yaml
```

## Exercises

### Exercise 1: Terraform Cluster Setup

Provision the lab environment with Terraform:

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

This creates:
- Namespaces with Pod Security Standards labels
- ServiceAccounts with scoped RBAC
- ResourceQuotas and LimitRanges
- NetworkPolicy baseline

### Exercise 2: RBAC Least Privilege

Three personas, three levels of access:

| Role | Namespace | Permissions |
|------|-----------|-------------|
| `developer` | `app-team` | get/list pods, logs, exec (no secrets) |
| `security-auditor` | ALL | get/list everything (no write) |
| `deployer` | `app-team` | create/update deployments (no RBAC changes) |

```bash
# Test as developer — should succeed
kubectl auth can-i get pods -n app-team --as=system:serviceaccount:app-team:developer

# Test as developer — should fail
kubectl auth can-i get secrets -n app-team --as=system:serviceaccount:app-team:developer
```

### Exercise 3: NetworkPolicies

Implement zero-trust networking:

```bash
kubectl apply -f policies/network/

# Test: app can reach database
kubectl exec -n app-team deploy/frontend -- wget -qO- http://backend.app-team:8080

# Test: app CANNOT reach kube-system
kubectl exec -n app-team deploy/frontend -- wget -qO- http://kube-dns.kube-system:53
```

### Exercise 4: Kyverno Admission Policies

Deploy custom policies and test enforcement:

```bash
kubectl apply -f policies/kyverno/

# This should be BLOCKED (no resource limits)
kubectl apply -f test-manifests/violation-no-limits.yaml

# This should be BLOCKED (privileged container)
kubectl apply -f test-manifests/violation-privileged.yaml

# This should be BLOCKED (latest tag)
kubectl apply -f test-manifests/violation-latest-tag.yaml

# This should PASS
kubectl apply -f test-manifests/compliant-deployment.yaml
```

### Exercise 5: Audit and Report

Generate a security posture report:

```bash
# Check RBAC permissions matrix
kubectl auth can-i --list --as=system:serviceaccount:app-team:developer -n app-team

# Validate all policies are enforcing
kubectl get clusterpolicy -o wide

# Run kube-bench CIS check
kubectl apply -f k8s/kube-bench-job.yaml
kubectl logs job/kube-bench
```

## Success Criteria

- [ ] Terraform provisions full lab environment in one `apply`
- [ ] Pod Security Standards block privileged pods
- [ ] NetworkPolicies deny cross-namespace traffic by default
- [ ] Kyverno blocks: no limits, privileged, latest tag, no probes
- [ ] RBAC: developer cannot read secrets
- [ ] RBAC: auditor has read-only everywhere
- [ ] `terraform destroy` cleans up everything

## Files

```
lab-02-k8s-security-policies/
├── README.md
├── terraform/
│   ├── main.tf                 # Provider + minikube cluster config
│   ├── namespaces.tf           # Namespaces with PSS labels
│   ├── rbac.tf                 # ServiceAccounts, Roles, RoleBindings
│   ├── network-policies.tf     # Default-deny + allow rules
│   ├── resource-quotas.tf      # Quotas and LimitRanges
│   ├── variables.tf
│   └── outputs.tf
├── policies/
│   ├── kyverno/
│   │   ├── require-limits.yaml
│   │   ├── disallow-privileged.yaml
│   │   ├── disallow-latest-tag.yaml
│   │   ├── require-probes.yaml
│   │   └── require-labels.yaml
│   └── network/
│       ├── default-deny-all.yaml
│       └── allow-app-to-backend.yaml
├── test-manifests/
│   ├── violation-no-limits.yaml
│   ├── violation-privileged.yaml
│   ├── violation-latest-tag.yaml
│   └── compliant-deployment.yaml
└── k8s/
    └── kube-bench-job.yaml
```
