# DevSecOps Portfolio

**Marna Marie Strauss** | Global Lead Security Engineer | Advancing to Principal DevSecOps Engineer

Production security engineering, vulnerability management, threat hunting, and AI-augmented security operations for enterprise SaaS platforms.

---

## Capabilities

| Domain | Evidence | Level |
|--------|----------|-------|
| Vulnerability Management | CVE intake pipeline (serverless AWS), regression detection, SLA automation | Principal |
| Threat Hunting | CTI dashboard (15+ feeds), Sigma/YARA rules, detection engineering | Senior+ |
| Penetration Testing | 44-tool MCP server, K8s exploitation, automated reporting, playbook orchestration | Principal |
| SDLC Security | PR review automation, shift-left gates, sprint regression tracking | Principal |
| Platform Security | EKS hardening, container scanning, SBOM/SLSA, supply chain security | Principal |
| Security Engineering | Multi-cloud IaC, policy-as-code, secrets management, zero-trust | Senior+ |
| Agentic AI Security | MCP servers, autonomous triage, multi-agent incident response | Principal |

---

## Modules

| # | Module | Focus | Status |
|---|--------|-------|--------|
| 01 | [Vulnerability Management](01-vulnerability-management/) | Triage, SLA tracking, regression detection, vendor response | In Progress |
| 02 | [Threat Hunting](02-threat-hunting/) | Sigma/YARA rules, log analysis, CTI enrichment | Planned |
| 03 | [Pentesting](03-pentesting/) | Methodology, tool development, automated reporting | Planned |
| 04 | [SDLC Security](04-sdlc-security/) | PR review automation, sprint tracking, security gates | Planned |
| 05 | [Platform Security](05-platform-security/) | Container hardening, K8s policies, SBOM/SLSA, runtime | Planned |
| 06 | [Security Engineering](06-security-engineering/) | IaC security, policy-as-code, secrets, zero-trust | Planned |
| 07 | [Agentic Security](07-agentic-security/) | MCP servers, detection agents, autonomous triage | Planned |

---

## Assessments & Threat Models

| Artifact | Type | Status |
|----------|------|--------|
| [Groundplex STRIDE Threat Model](threat-models/groundplex-stride.md) | Threat Model | Complete |
| [Defense-in-Depth Scorecard](assessments/defense-in-depth-scorecard.md) | Posture Assessment | Complete |
| [Skills Tracker](SKILLS-TRACKER.md) | Living CV / Career Development | Active |

---

## Skills & Career Progression

See **[SKILLS-TRACKER.md](SKILLS-TRACKER.md)** for the full skills matrix across 8 security domains, quarterly goals, metrics tracking, certification roadmap, and zero trust learning path with Wiz integration points.

---

## Shipped Tools

| Tool | Purpose |
|------|---------|
| [regression-detector](tools/regression-detector/) | Detect reintroduced CVEs across software releases |
| [pr-security-reviewer](tools/pr-security-reviewer/) | AI-assisted GitHub PR security review |
| [sbom-diff](tools/sbom-diff/) | Diff SBOMs across versions to track dependency changes |
| [sigma-validator](tools/sigma-validator/) | Validate and test Sigma detection rules |

---

## Production Systems (External)

These are production systems I've built and operate — architecture referenced in writeups throughout this repo:

| System | Stack | Scale |
|--------|-------|-------|
| CVE Intake MCP Server | Python, AWS Lambda/Fargate, DynamoDB, Jira, Wiz, Slack | 500+ CVEs/month |
| Pentest Red Team MCP | Python, 44 security tools, K8s, 7 playbooks | Full red team engagements |
| CTI Grafana Dashboard | Terraform, EKS, PostgreSQL, 10+ data sources | 15+ dashboards |
| AppSec RAG Agent | FastAPI, ChromaDB, multi-cloud (AWS + GCP) | Real-time inventory queries |
| Groundplex Scan Pipeline | Trivy + WizCLI + Maven, ECS Fargate | Automated monthly scans |

---

## Security Pipeline

Every PR in this repository passes through:

[![Security Scan](https://github.com/strauss-mm/devsecops-portfolio/actions/workflows/security-scan.yml/badge.svg)](https://github.com/strauss-mm/devsecops-portfolio/actions/workflows/security-scan.yml)
[![Secret Scan](https://github.com/strauss-mm/devsecops-portfolio/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/strauss-mm/devsecops-portfolio/actions/workflows/secret-scan.yml)
[![IaC Scan](https://github.com/strauss-mm/devsecops-portfolio/actions/workflows/iac-scan.yml/badge.svg)](https://github.com/strauss-mm/devsecops-portfolio/actions/workflows/iac-scan.yml)

- Trivy + Semgrep static analysis
- Gitleaks secret detection
- Checkov + tfsec for infrastructure-as-code
- Dependency review for vulnerable packages
- Container image scanning for Dockerfiles
- CycloneDX SBOM generation on release

---

## Progression Path

```
Associate                    Senior                       Principal
    |                           |                            |
    v                           v                            v
[Scan & Report]         [Triage & Prioritize]      [Architect & Automate]
[Follow playbooks]      [Write detections]         [Build platforms]
[Use tools]             [Develop tools]            [Design frameworks]
[Single domain]         [Cross-domain]             [Organization-wide]
```

Each module progresses from Senior-level labs (01-02) to Principal-level capstones (03-04).

---

## Tech Stack

- **Languages**: Python 3.11+, HCL (Terraform), Rego (OPA), YAML (K8s/Sigma)
- **Cloud**: AWS (Lambda, Fargate, EKS, S3, DynamoDB, Secrets Manager)
- **Security Tools**: Trivy, Semgrep, Nuclei, Nmap, Falco, Gitleaks, Checkov
- **AI/ML**: Claude API (Bedrock), MCP (Model Context Protocol), ChromaDB
- **Platforms**: Kubernetes (EKS), Docker, GitHub Actions
- **Integrations**: Jira, Slack, Wiz, Grafana, NVD, CISA KEV, EPSS

---

## License

MIT License - see [LICENSE](LICENSE)
