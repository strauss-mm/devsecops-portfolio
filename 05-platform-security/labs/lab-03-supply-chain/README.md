# Lab 03: Supply Chain Security

Build a complete supply chain integrity pipeline: SBOM generation, image signing with cosign, SLSA provenance, and admission control that only allows verified images.

## Objectives

- Generate CycloneDX and SPDX SBOMs with Syft
- Sign container images with cosign (keyless via Sigstore)
- Create SLSA provenance attestations
- Deploy Kyverno policy that verifies image signatures before admission
- Diff SBOMs across versions to detect dependency changes
- Terraform provisions the verification infrastructure

## Prerequisites

```bash
minikube start --driver=docker --memory=4096 --cpus=2
# Install tools
brew install sigstore/tap/cosign syft
```

## Exercises

### Exercise 1: SBOM Generation

Generate SBOMs for a container image in multiple formats:

```bash
cd app/

# Build the image
docker build -t lab03-app:v1.0 .

# CycloneDX (JSON)
syft lab03-app:v1.0 -o cyclonedx-json > sbom/app-v1.0-cyclonedx.json

# SPDX
syft lab03-app:v1.0 -o spdx-json > sbom/app-v1.0-spdx.json

# Analyze: count packages, find critical deps
cat sbom/app-v1.0-cyclonedx.json | jq '.components | length'
cat sbom/app-v1.0-cyclonedx.json | jq '.components[] | select(.type=="library") | .name'
```

### Exercise 2: Image Signing with Cosign

Sign and verify images using keyless signing (Sigstore Fulcio/Rekor):

```bash
# Generate a key pair (for local lab — production uses keyless)
cosign generate-key-pair

# Sign the image
cosign sign --key cosign.key lab03-app:v1.0

# Verify
cosign verify --key cosign.pub lab03-app:v1.0

# Attach SBOM as attestation
cosign attest --key cosign.key --predicate sbom/app-v1.0-cyclonedx.json \
  --type cyclonedx lab03-app:v1.0
```

### Exercise 3: SLSA Provenance

Create a provenance attestation documenting the build:

```bash
# Generate provenance (in-toto format)
cosign attest --key cosign.key \
  --predicate provenance/slsa-provenance.json \
  --type slsaprovenance lab03-app:v1.0

# Verify provenance
cosign verify-attestation --key cosign.pub \
  --type slsaprovenance lab03-app:v1.0
```

### Exercise 4: Admission Control (Terraform + Kyverno)

Deploy Kyverno policy that only admits signed images:

```bash
cd terraform/
terraform init && terraform apply

# Test: unsigned image should be BLOCKED
kubectl run unsigned --image=nginx:1.25 -n supply-chain

# Test: signed image should PASS
kubectl run signed --image=lab03-app:v1.0 -n supply-chain
```

### Exercise 5: SBOM Diff Across Versions

Detect dependency changes between releases:

```bash
# Build v2 with a dependency bump
docker build -f Dockerfile.v2 -t lab03-app:v2.0 .
syft lab03-app:v2.0 -o cyclonedx-json > sbom/app-v2.0-cyclonedx.json

# Diff: what packages were added/removed/changed?
python3 scripts/sbom-diff.py sbom/app-v1.0-cyclonedx.json sbom/app-v2.0-cyclonedx.json
```

## Success Criteria

- [ ] CycloneDX + SPDX SBOMs generated and readable
- [ ] Image signed and verification passes with cosign
- [ ] SBOM attached as in-toto attestation
- [ ] SLSA provenance attestation created and verifiable
- [ ] Kyverno blocks unsigned images from deploying
- [ ] SBOM diff correctly identifies added/removed/changed packages
- [ ] Full pipeline reproducible via `make all`

## Files

```
lab-03-supply-chain/
├── README.md
├── Makefile
├── app/
│   ├── Dockerfile             # v1: Python app with pinned deps
│   ├── Dockerfile.v2          # v2: bumped dependency (introduces change)
│   ├── app.py
│   └── requirements.txt
├── sbom/
│   └── .gitkeep
├── provenance/
│   └── slsa-provenance.json   # Template provenance document
├── terraform/
│   ├── main.tf
│   ├── kyverno-verify-images.tf
│   └── variables.tf
├── scripts/
│   └── sbom-diff.py           # Diff two CycloneDX SBOMs
└── k8s/
    └── test-unsigned.yaml
```
