# Lab 01: Container Hardening

Harden a vulnerable container image through multi-stage builds, distroless base images, and CIS Docker Benchmark compliance.

## Objectives

- Reduce a bloated container from 800MB+ to <50MB using multi-stage builds
- Eliminate unnecessary packages, shells, and debug tools
- Run as non-root with read-only filesystem
- Pass CIS Docker Benchmark Level 2 checks
- Scan before/after with Trivy to measure CVE reduction

## Prerequisites

```bash
minikube start --driver=docker --memory=4096 --cpus=2
# Verify
docker info && kubectl get nodes
```

## Exercises

### Exercise 1: Analyze the Vulnerable Image

Build the intentionally vulnerable image and scan it:

```bash
cd vulnerable-app/
docker build -t lab01-vulnerable:latest .
trivy image --severity HIGH,CRITICAL lab01-vulnerable:latest
```

Record the findings: image size, CVE count, running as root, writable filesystem.

### Exercise 2: Multi-Stage Hardening

Create `Dockerfile.hardened` using:
1. Build stage: compile the app with full toolchain
2. Runtime stage: `gcr.io/distroless/static-debian12` (no shell, no package manager)

```bash
docker build -f Dockerfile.hardened -t lab01-hardened:latest .
trivy image --severity HIGH,CRITICAL lab01-hardened:latest
```

Compare: image size, CVE count, attack surface.

### Exercise 3: Runtime Security Controls

Deploy both images to minikube and verify security posture:

```bash
kubectl apply -f k8s/deployment-vulnerable.yaml
kubectl apply -f k8s/deployment-hardened.yaml

# Try to exec into each
kubectl exec -it deploy/vulnerable-app -- /bin/sh   # Should work (bad)
kubectl exec -it deploy/hardened-app -- /bin/sh     # Should fail (good)
```

### Exercise 4: CIS Benchmark Validation

Run Docker Bench against your hardened image:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

Fix any remaining Level 2 findings.

## Success Criteria

- [ ] Hardened image <50MB (vs >800MB vulnerable)
- [ ] Zero CRITICAL CVEs in hardened image
- [ ] Non-root user (UID > 10000)
- [ ] Read-only root filesystem
- [ ] No shell available in container
- [ ] CIS Docker Benchmark Level 2 pass
- [ ] Trivy scan report saved to `results/`

## Files

```
lab-01-container-hardening/
├── README.md
├── vulnerable-app/
│   ├── Dockerfile              # Intentionally bad: FROM ubuntu, root, bloated
│   ├── Dockerfile.hardened     # Your solution: multi-stage, distroless
│   └── main.go                 # Simple HTTP server
├── k8s/
│   ├── deployment-vulnerable.yaml
│   └── deployment-hardened.yaml
└── results/
    └── .gitkeep
```
