# Defense-in-Depth Scorecard

**Author:** Marna Marie Strauss | **Date:** 2026-06-08 | **Version:** 1.0
**Scope:** SnapLogic Platform — Control Plane + Groundplex + Supporting Infrastructure
**Classification:** Internal — SnapLogic Security Engineering

---

## Scoring Legend

| Score | Meaning | Criteria |
|-------|---------|----------|
| 5 | Optimized | Automated, measured, continuously improved |
| 4 | Managed | Consistent process, metrics tracked, exceptions documented |
| 3 | Defined | Documented policy, partially implemented, some gaps |
| 2 | Developing | Ad-hoc controls exist, no consistent process |
| 1 | Initial | Minimal or no controls in place |

---

## Layer 1: Network Security

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Network segmentation (VPC/subnets) | 4 | 3-tier architecture, private subnets, NAT gateway | UAT + Prod in same AWS account (accepted risk) | Document compensating controls |
| Firewall / Security Groups | 4 | Control Plane unreachable from internet, SG rules | Groundplex egress unrestricted | Egress allowlisting |
| TLS enforcement | 4 | TLS 1.2 minimum, Qualys SSL Labs validated | No mTLS for service-to-service | Implement mTLS roadmap |
| DDoS protection | 3 | Cloudflare CDN fronts customer-facing endpoints | No explicit DDoS plan for Control Plane APIs | AWS Shield Advanced evaluation |
| Network monitoring | 3 | Datadog integration, VPC Flow Logs (assumed) | No IDS/IPS for east-west traffic | Evaluate Wiz network sensors |
| DNS security | 3 | Cloudflare DNS management | No DNSSEC, DKIM/DMARC partially deployed | Full DMARC enforcement |
| **Layer Average** | **3.5** | | | |

---

## Layer 2: Identity & Access

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Authentication (SSO/MFA) | 4 | Okta SSO + MFA for all users, SAML/OIDC | Service accounts lack MFA equivalent | Workload identity (SPIFFE) |
| Authorization (RBAC) | 3 | K8s RBAC, IAM policies, SnapLogic ACLs per org | Overprivileged service accounts (Boehringer IAM finding) | Wiz Effective Permissions audit |
| Privileged access management | 3 | VPN + MFA for admin access, role-based | No PAM solution (CyberArk/BeyondTrust) | Evaluate PAM for DB/infra access |
| Identity governance | 2 | Okta lifecycle management | No automated access reviews/certification | Implement quarterly access reviews |
| Service-to-service auth | 2 | Bearer tokens, some API keys | Long-lived tokens, no mTLS | mTLS + short-lived token rotation |
| Zero trust posture | 2 | Perimeter-based with MFA | No device posture checks, no continuous auth | Conditional access pilot |
| **Layer Average** | **2.7** | | | |

---

## Layer 3: Application Security

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Vulnerability scanning (SCA) | 5 | Trivy + WizCLI monthly, CVE intake pipeline, 500+ CVEs/month, SLA enforcement | — | Maintain cadence |
| SAST / code review | 3 | risk3sixty quarterly pentest, Semgrep in CI (portfolio) | No SAST in SnapLogic's main product CI | Advocate for SAST adoption |
| DAST / runtime testing | 3 | Pentest playbook (ZAP, Nuclei, Nikto) | Manual/periodic, not continuous | ZAP in staging CI pipeline |
| Secure SDLC | 3 | SLA-driven remediation, regression detection | No formal security gates in dev workflow | Shift-left: PR security checks |
| Input validation | 2 | Platform-level (Script Snap restrictions) | Bypass via Java native functions (PLAT-14611) | Sandbox execution |
| API security | 3 | Bearer token auth, rate limiting (assumed) | No API schema validation, no WAF | API gateway with schema validation |
| Dependency management | 4 | Maven dependency explorer, SBOM generation, transitive tree analysis | No automated dependency update (Dependabot) | Enable automated PRs for dep updates |
| **Layer Average** | **3.3** | | | |

---

## Layer 4: Data Security

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Encryption at rest | 4 | AES-256-GCM (S3), EBS encryption, MongoDB on encrypted volumes | Non-AWS assets use SL-managed keys (rotation unclear) | Key rotation audit |
| Encryption in transit | 4 | TLS 1.2+ all connections | Basic Auth sends creds base64 in headers (design issue) | OAuth2 migration |
| Data classification | 2 | "SnapLogic does not persist customer data" (pass-through) | No formal classification schema | Define classification levels |
| Data loss prevention | 2 | No DLP tooling in place | Pipeline can exfiltrate data to any endpoint | Egress filtering + DLP monitoring |
| Backup & recovery | 3 | Multi-AZ, RTO 48h/RPO 2h | No tested recovery runbook (publicly documented) | DR drill |
| Secrets management | 4 | AWS Secrets Manager, .slpropz encryption | No automated rotation, IAM scope too broad (Boehringer) | Rotation automation + scoped policies |
| **Layer Average** | **3.2** | | | |

---

## Layer 5: Endpoint Security

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Device management (MDM) | 4 | JAMF (macOS) + Intune (Windows), monitored in Grafana | Compliance enforcement actions unclear | Automate non-compliant device blocking |
| Disk encryption | 4 | FileVault + BitLocker tracked in PCI dashboard | Enforcement of encryption on enroll | Verify 100% coverage |
| EDR / antivirus | 3 | Assumed (not directly managed by security eng) | No visibility into EDR alert triage | Dashboard integration |
| Patch management | 3 | OS distribution tracked in endpoint dashboard | No SLA for endpoint patching | Define patch SLA |
| Browser security | 2 | No browser isolation or extension control | — | Evaluate browser security platform |
| **Layer Average** | **3.2** | | | |

---

## Layer 6: Container & Workload Security

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Image scanning | 5 | Trivy + WizCLI, full filesystem + snap pack scanning, monthly cadence | — | Maintain |
| Runtime security | 2 | Container escape checks in pentest playbook | No runtime monitoring (Falco/Sysdig) in production | Deploy Falco |
| Pod security | 2 | Varies by customer deployment | No enforced pod security standards, root common | Enforce restricted PSS |
| Image signing | 1 | No cosign/notation in pipeline | Images not verified at deploy time | Implement sigstore |
| Supply chain (SLSA) | 2 | SBOM generation, dependency tracking | No provenance attestation, no hermetic builds | SLSA Level 2 target |
| Network policies | 2 | K8s namespace isolation | No fine-grained network policies (Calico/Cilium) | Pod-level egress rules |
| **Layer Average** | **2.3** | | | |

---

## Layer 7: Monitoring & Response

| Control | Score | Evidence | Gap | Action |
|---------|-------|----------|-----|--------|
| Log aggregation | 4 | Datadog (platform), Grafana CTI (security-specific) | Groundplex container logs not centrally collected | Forward JCC logs |
| Threat detection | 3 | CTI dashboards (10), Wiz findings, BitSight | No real-time detection rules (Sigma) on SnapLogic-specific TTPs | Write production Sigma rules |
| Incident response | 3 | Pentest playbook, CVE triage process | No formal IR playbook for security incidents | Write IR runbook |
| Vulnerability response | 5 | Automated intake, Jira ticket creation, SLA tracking, customer reporting | — | Maintain |
| Security metrics | 4 | CTI Grafana (44x ROI), SLA compliance, scan cadence | No executive dashboard (CISO-level) | Build exec summary view |
| Threat intelligence | 4 | 15+ CTI feeds, CISA KEV, EPSS, NVD, GreyNoise, Wiz | Feeds not yet actionable (alert on new Groundplex-relevant CVEs) | Auto-alert on relevant KEV additions |
| **Layer Average** | **3.8** | | | |

---

## Overall Posture

```
Layer                          Score    Visual
─────────────────────────────────────────────────────────
Network Security               3.5     ████████████████░░░░  
Identity & Access              2.7     █████████████░░░░░░░  
Application Security           3.3     ████████████████░░░░  
Data Security                  3.2     ████████████████░░░░  
Endpoint Security              3.2     ████████████████░░░░  
Container & Workload           2.3     ███████████░░░░░░░░░  
Monitoring & Response          3.8     ███████████████████░  
─────────────────────────────────────────────────────────
OVERALL AVERAGE                3.1 / 5.0
```

---

## Priority Improvements (by impact)

### Critical Gaps (Score 1-2, High Impact)

| # | Gap | Layer | Current | Target | Owner | Timeline |
|---|-----|-------|---------|--------|-------|----------|
| 1 | No runtime security monitoring | Container | 2 | 4 | Security Eng | Q3 2026 |
| 2 | No egress filtering for Groundplex | Network + Data | 2 | 4 | Platform + Security | Q3 2026 |
| 3 | No image signing/verification | Container | 1 | 3 | Security Eng | Q4 2026 |
| 4 | No continuous authorization (zero trust) | Identity | 2 | 3 | Security Eng + IT | Q4 2026 |
| 5 | No DLP tooling | Data | 2 | 3 | Security Eng | Q1 2027 |

### Quick Wins (Low Effort, Score Improvement)

| # | Action | Layer | Effort | Score Impact |
|---|--------|-------|--------|--------------|
| 1 | Enforce pod security standards in deployment docs | Container | Low | 2 → 3 |
| 2 | Forward JCC logs to Datadog | Monitoring | Low | 4 → 5 (completeness) |
| 3 | Write 3 Sigma rules for Groundplex TTPs | Monitoring | Medium | 3 → 4 |
| 4 | Wiz Effective Permissions audit | Identity | Low | 3 → 4 (RBAC) |
| 5 | DR drill (test RTO/RPO) | Data | Medium | 3 → 4 |

---

## Wiz Integration Points

| Wiz Feature | DiD Layer | How to Use |
|-------------|-----------|------------|
| CSPM | Network, Identity, Data | Continuous posture assessment across all AWS accounts |
| Attack Path Analysis | All layers | Map internet → sensitive data paths, prioritize by blast radius |
| Effective Permissions | Identity | Audit overprivileged identities, enforce least privilege |
| DSPM | Data | Discover and classify sensitive data flows |
| Runtime Sensor | Container | Detect anomalous behavior, lateral movement, container escapes |
| Vulnerability Scanning | Application, Container | Correlate with Trivy findings, add exploitability context |
| Network Exposure | Network | Identify unintended internet-facing resources |
| Kubernetes Security | Container | Audit RBAC, pod security, network policies |

---

## How to Use This Scorecard

1. **Quarterly review:** Re-score each control, update evidence
2. **Project justification:** Reference gaps when proposing security projects
3. **Risk register:** Map gaps to business risk for executive communication
4. **Interview prep:** Walk through layers, cite specific evidence
5. **Team planning:** Use priority improvements as team OKR candidates
