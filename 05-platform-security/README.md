# Module 05: Platform Security

Container hardening, Kubernetes security policies, supply chain integrity (SBOM/SLSA), and runtime threat detection for cloud-native platforms.

## Local Lab Setup

All labs run on **minikube** (already installed). No cloud resources needed.

```bash
# Start cluster
minikube start --driver=docker --memory=4096 --cpus=2

# Verify
kubectl get nodes
kubectl config current-context  # should say "minikube"

# Required tools
brew install terraform kubectl minikube
brew install sigstore/tap/cosign syft  # Lab 03
```

**Safety**: Everything runs locally inside Docker. `terraform destroy` cleans up each lab. Never touches AWS/cloud accounts.

## Labs

| Lab | Focus | Tools | Difficulty | Status |
|-----|-------|-------|-----------|--------|
| [lab-01](labs/lab-01-container-hardening/) | Container hardening (distroless, multi-stage, CIS benchmarks) | Docker, Trivy | Senior | Ready |
| [lab-02](labs/lab-02-k8s-security-policies/) | K8s security policies (Kyverno, NetworkPolicy, RBAC, PSS) | Terraform, Kyverno, kubectl | Senior+ | Ready |
| [lab-03](labs/lab-03-supply-chain/) | Supply chain security (SBOM, cosign, SLSA, admission control) | Syft, Cosign, Terraform, Kyverno | Principal | Ready |
| [lab-04](labs/lab-04-runtime-security/) | Runtime security (Falco rules, attack simulation, alert pipeline) | Terraform, Falco, Tetragon | Principal | Ready |

## Progression

```
Lab 01 (Container Hardening)
  └── Lab 02 (K8s Policies)        ← builds on hardened images from Lab 01
        └── Lab 03 (Supply Chain)   ← signs and attests images, enforces via Kyverno
              └── Lab 04 (Runtime)  ← detects attacks that bypass build-time controls
```

Each lab is self-contained — start from any lab if you have the prerequisites.

## Configs (Production Reference)

- [network-policies/](configs/network-policies/) — Zero-trust NetworkPolicy templates
- [pod-security-standards/](configs/pod-security-standards/) — PSS namespace enforcement

## Key Concepts

- **Defense in depth**: Image hardening → admission control → runtime detection
- **Supply chain integrity**: From source to deployed artifact (SBOM + signatures)
- **Runtime vs build-time**: Detecting threats that survive the build pipeline
- **Least privilege**: Pod security, RBAC, network segmentation
- **Policy as code**: Terraform + Kyverno for reproducible, auditable security

## Writeups

- Groundplex security deep dive (why runtime scanning matters)
- EKS hardening for multi-tenant SaaS
- Snap pack supply chain risks (transitive JAR vulnerabilities)
- Fargate vs EKS: security trade-offs for containerized workloads

## Prerequisites

- Docker Desktop (running)
- minikube (`brew install minikube`)
- Terraform >= 1.5 (`brew install terraform`)
- kubectl (`brew install kubectl`)
- Trivy (`brew install trivy`)
- Basic understanding of containers, K8s pods/deployments/services, Linux security
