# Module 05: Platform Security

Container hardening, Kubernetes security policies, supply chain integrity (SBOM/SLSA), and runtime threat detection for cloud-native platforms.

## Labs

| Lab | Focus | Difficulty | Status |
|-----|-------|-----------|--------|
| [lab-01](labs/lab-01-container-hardening/) | Container hardening (distroless, multi-stage, benchmarks) | Senior | Planned |
| [lab-02](labs/lab-02-k8s-security-policies/) | K8s security policies (OPA/Kyverno, NetworkPolicy, RBAC) | Senior+ | Planned |
| [lab-03](labs/lab-03-supply-chain/) | Supply chain security (SBOM, SLSA provenance, cosign) | Principal | Planned |
| [lab-04](labs/lab-04-runtime-security/) | Runtime security (Falco/Tetragon rules + alert pipeline) | Principal | Planned |

## Writeups

- Groundplex security deep dive (why runtime scanning matters)
- EKS hardening for multi-tenant SaaS
- Snap pack supply chain risks (transitive JAR vulnerabilities)
- Fargate vs EKS: security trade-offs for containerized workloads

## Configs

- [network-policies/](configs/network-policies/) — Production K8s NetworkPolicies
- [pod-security-standards/](configs/pod-security-standards/) — PSS enforcement configs

## Key Concepts

- **Defense in depth**: Image hardening + admission control + runtime detection
- **Supply chain integrity**: From source to deployed artifact
- **Runtime vs build-time**: Detecting threats that survive the build pipeline
- **Least privilege**: Pod security, RBAC, network segmentation

## Prerequisites

- Docker and container fundamentals
- Kubernetes basics (pods, deployments, services, RBAC)
- Understanding of Linux security (capabilities, namespaces, seccomp)
