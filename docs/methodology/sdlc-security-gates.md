# SDLC Security Gates

## Gate Definitions

Security gates integrated at each phase of the software development lifecycle. Each gate has clear pass/fail criteria and automated enforcement where possible.

## Pre-Commit (Developer Workstation)

| Check | Tool | Blocking |
|-------|------|----------|
| Secret detection | Gitleaks pre-commit hook | Yes |
| Dependency check | pip-audit / npm audit | Warning |
| Code formatting | ruff / prettier | Yes |

## Pull Request (CI)

| Check | Tool | Blocking |
|-------|------|----------|
| SAST | Semgrep | Yes (Critical/High) |
| Dependency review | GitHub dependency-review-action | Yes (High+) |
| Secret scan | Gitleaks | Yes |
| License compliance | dependency-review (deny GPL-3.0, AGPL) | Yes |
| IaC scan | Checkov + tfsec | Yes (Critical) |
| Container scan | Trivy image | Yes (Critical) |

## Pre-Merge (Approval)

| Check | Requirement |
|-------|-------------|
| Security review | Required for: auth changes, crypto, input handling, infra |
| CODEOWNERS approval | Required for security-sensitive paths |
| All CI checks green | Mandatory |
| No unresolved security comments | Mandatory |

## Post-Merge (Release Pipeline)

| Check | Tool | Action |
|-------|------|--------|
| SBOM generation | CycloneDX | Attach to release |
| Full vulnerability scan | Trivy (all severities) | Report, don't block |
| Container signing | cosign | Sign all published images |
| SLSA provenance | slsa-verifier | Generate provenance attestation |

## Production (Runtime)

| Check | Tool | Action |
|-------|------|--------|
| Runtime behavior | Falco / Tetragon | Alert on anomalies |
| Drift detection | Config auditor | Alert on unexpected changes |
| Vulnerability monitoring | Wiz / Trivy scheduled | SLA-based remediation |

## Gate Override Process

Emergency overrides require:
1. Written justification in PR description
2. Compensating control documented
3. Follow-up ticket created with SLA
4. Security team notification
