# Living Skills Tracker

**Marna Marie Strauss** | Global Lead Security Engineer → Security Engineering Team Lead

Last updated: 2026-06-08

---

## Skills Matrix

### Legend
- **Practicing** — doing this daily/weekly in production
- **Demonstrated** — have shipped artifacts, can speak to results
- **Learning** — actively building, no production artifact yet
- **Planned** — identified gap, have a plan to close it

---

### 1. Defense in Depth

| Layer | Skill | Level | Evidence | Next Step |
|-------|-------|-------|----------|-----------|
| Network | VPC architecture, subnet isolation, NAT filtering | Demonstrated | SnapLogic platform architecture knowledge, EKS networking | Document segmentation improvements proposed |
| Network | TLS enforcement & certificate management | Demonstrated | TLS 1.2 minimum enforcement, Qualys SSL Labs validation, Cloudflare CDN | mTLS implementation for service-to-service |
| Application | Vulnerability scanning (Trivy, WizCLI) | Practicing | Automated monthly Groundplex scans, 500+ CVEs/month intake | Expand to DAST (ZAP in CI/CD) |
| Application | Secure SDLC / SLA enforcement | Practicing | SLA policy (15/30/90 day), Jira automation, regression detection | Shift-left: pre-merge scanning gates |
| Application | OWASP Top 10 assessment | Demonstrated | Pentest playbook, Boehringer RCE analysis, Script Snap bypass | Threat model all snap execution paths |
| Data | Encryption at rest (AES-256-GCM, KMS) | Demonstrated | Platform architecture review, S3/EBS encryption audit | DSPM implementation via Wiz |
| Data | Encryption in motion (TLS) | Demonstrated | TLS enforcement, identified Basic Auth gap in pipelines | Push OAuth2 adoption, kill Basic Auth |
| Data | Secrets management | Practicing | AWS Secrets Manager, .slpropz handling, secret scanning | Vault rotation automation |
| Identity | SSO/MFA (Okta, SAML, OIDC) | Demonstrated | CVE intake portal (Cognito + Okta SAML), GRC portal (NextAuth + Azure AD + Okta) | Conditional access policies |
| Identity | RBAC / least privilege | Demonstrated | K8s RBAC auditing, IAM policy review (Boehringer finding) | Continuous permission monitoring via Wiz |
| Identity | Service identity (mTLS, workload identity) | Learning | Awareness from architecture review | SPIFFE/SPIRE POC or Wiz workload identity |
| Endpoint | Device compliance (JAMF, Intune) | Demonstrated | Grafana endpoint compliance dashboard, PCI DSS scorecard | Drive remediation workflows from dashboard |
| Monitoring | SIEM / log analysis | Demonstrated | Grafana CTI (10 dashboards, 14 datasources), Datadog awareness | Correlation rules, automated alert triage |
| Monitoring | Detection engineering | Learning | Sigma/YARA rules (planned in portfolio) | Write 5 production Sigma rules for SnapLogic |

---

### 2. Zero Trust

| Principle | Skill | Level | Evidence | Next Step |
|-----------|-------|-------|----------|-----------|
| Verify explicitly | JWT-based API auth, Okta SSO | Demonstrated | CVE intake portal, GRC portal | Device posture checks before access |
| Least privilege | IAM review, RBAC audit | Demonstrated | Boehringer IAM finding, K8s RBAC tools | Wiz Effective Permissions audit across all accounts |
| Assume breach | Network scanning, lateral movement detection | Demonstrated | Pentest playbook (container escape, network pivot, metadata check) | Wiz Attack Path analysis → remediation plan |
| Microsegmentation | K8s namespace isolation, VPC subnets | Learning | EKS cluster design, namespace separation | Network policies (Calico/Cilium) for Groundplex pods |
| Continuous authorization | Token-based auth | Learning | JWT expiry, session management | Step-up auth for sensitive operations |
| Identity-based access | Service accounts, workload identity | Learning | K8s service account awareness | Replace IP-based trust with identity (SPIFFE) |

**Wiz-Specific Zero Trust Actions:**
1. Run Attack Path Analysis → document all internet-to-data paths
2. Audit Effective Permissions → identify overprivileged identities
3. Review Network Exposure graph → propose segmentation improvements
4. Deploy Runtime Sensor (if available) → detect lateral movement

---

### 3. Threat Modeling

| Skill | Level | Evidence | Next Step |
|-------|-------|----------|-----------|
| Attack surface decomposition | Practicing | Groundplex attack surface table (7 surfaces), pentest playbook | Formalize as STRIDE DFD |
| Kill chain analysis | Demonstrated | Boehringer RCE chain (Mapper→Script→shell→IAM), MITRE mapping | Document for all known attack paths |
| STRIDE methodology | Learning | Informal practice, haven't produced formal artifact | Complete Groundplex STRIDE (see threat-models/) |
| Trust boundary identification | Demonstrated | Platform architecture (Cloudplex vs Groundplex, control plane vs data plane) | Diagram in threat model |
| Risk scoring / prioritization | Practicing | CVSS + EPSS + Wiz enrichment, SLA calculation | Add business impact scoring |
| Threat model facilitation | Planned | — | Run workshop with Platform Engineering team |

---

### 4. Multi-Cloud Security

| Cloud | Skill | Level | Evidence | Next Step |
|-------|-------|-------|----------|-----------|
| AWS | IAM, VPC, EKS, Lambda, Fargate, S3, KMS, SES, Cognito, ECR, Secrets Manager | Practicing | All production systems run on AWS (account 179029418357) | AWS Security Specialty cert |
| AWS | CloudTrail / GuardDuty / Security Hub | Learning | Awareness, Datadog integration | Enable + dashboard in Grafana |
| Azure | Entra ID monitoring, Conditional Access awareness | Demonstrated | Grafana PCI dashboard (Azure datasource) | Azure security posture via Wiz |
| GCP | Service accounts, basic IAM | Learning | AppSec RAG agent (ChromaDB on GCP) | GCP Wiz integration review |
| Multi-cloud | Wiz CSPM across providers | Learning | Wiz CVE lookups, tenant access (us52) | Own CSPM findings → drive remediation |

---

### 5. Leadership & Influence

| Skill | Level | Evidence | Next Step |
|-------|-------|----------|-----------|
| Technical authority | Practicing | "Global Lead" title, sole owner of vuln management program | Document team impact metrics |
| Process design | Demonstrated | SLA policy, CVE classification rules, intake workflow, scan cadence | Publish as team runbooks |
| Tooling that scales teams | Demonstrated | CVE intake portal (support team uses it), Slack bot, Grafana dashboards | Track adoption metrics |
| Cross-functional influence | Demonstrated | PLAT/SNAP/SECENG ticket creation, Engineering remediation tracking | Joint threat model workshops |
| Mentoring | Planned | — | Mentor 1-2 junior engineers, document it |
| Hiring / team building | Planned | — | Write JDs for security engineer roles, participate in interviews |
| Roadmap / OKRs | Planned | — | Propose Q3 security engineering OKRs |
| Stakeholder communication | Demonstrated | Customer-facing CVE reports, Boehringer response, Confluence dashboard | Executive security briefings |
| Knowledge sharing | Practicing | Claude Tips & Tricks Lunch & Learn, portfolio repo | Internal security training program |

---

### 6. Offensive Security

| Skill | Level | Evidence | Next Step |
|-------|-------|----------|-----------|
| Network penetration testing | Demonstrated | 44-tool MCP server, nmap/nuclei/nikto, Kali + AWX workflow | OSCP certification |
| Web application testing | Demonstrated | OWASP analysis tool, ZAP/Gobuster/ffuf, Groundplex pentest | Expand to API fuzzing |
| Container/K8s exploitation | Demonstrated | Container escape checks, runtime escape, RBAC audit, secret scan | CKS certification |
| Red team operations | Demonstrated | Full red team playbook (7 playbooks), credential testing, lateral movement | Purple team exercises |
| Pentest report assessment | Practicing | Boehringer report analysis, ownership classification, remediation tracking | Standardize assessment framework |

---

### 7. GRC & Compliance

| Skill | Level | Evidence | Next Step |
|-------|-------|----------|-----------|
| SOC 2 | Demonstrated | Platform architecture review, risk3sixty audit awareness | Participate in audit prep |
| PCI DSS v4.0 | Demonstrated | Grafana PCI compliance dashboard (8 requirements tracked) | Gap analysis against v4.0 changes |
| Compliance portal design | Demonstrated | GRC Trust Hub (Next.js, SSO, audit logging, document access control) | Deploy to production |
| Vulnerability disclosure | Practicing | CVE intake, customer scan responses, Anthropic Mythos CVD monitoring | Formalize VDP |
| Policy writing | Demonstrated | SLA policy, BitSight policy, classification rules | Expand to full security policy suite |

---

### 8. Security Automation & AI

| Skill | Level | Evidence | Next Step |
|-------|-------|----------|-----------|
| MCP server development | Practicing | 2 production MCP servers (CVE intake + pentest), 44+ tools | Open-source the scaffold |
| AI-assisted triage | Practicing | Claude Code for CVE classification, Wiz enrichment, Jira automation | Fully autonomous low-severity triage |
| Infrastructure as Code | Demonstrated | Terraform (Lambda, Fargate, EKS, RDS, S3), Helm charts | Policy-as-code (OPA/Rego) |
| CI/CD security | Demonstrated | GitHub Actions (Trivy, Semgrep, Gitleaks, Checkov, tfsec) | SLSA provenance, signed builds |
| RAG for security | Demonstrated | AppSec RAG agent (cloud inventory queries) | Expand to policy Q&A |

---

## Quarterly Goals

### Q3 2026 (July - September)

| Goal | Domain | Target Artifact | Status |
|------|--------|-----------------|--------|
| Complete Groundplex STRIDE threat model | Threat Modeling | `threat-models/groundplex-stride.md` | In Progress |
| Wiz Attack Path analysis + zero trust gap doc | Zero Trust | `assessments/zero-trust-gap-analysis.md` | Planned |
| Defense-in-depth scorecard with metrics | Defense in Depth | `assessments/defense-in-depth-scorecard.md` | In Progress |
| Run 1 threat model workshop with Engineering | Leadership | Meeting notes + resulting Jira tickets | Planned |
| Publish SLA compliance metrics (6-month trend) | Vuln Mgmt | Dashboard or report | Planned |
| Mentor 1 team member on CVE intake process | Leadership | Document mentoring sessions | Planned |
| AWS Security Specialty study plan | Multi-Cloud | Study schedule + practice exams | Planned |

### Q4 2026 (October - December)

| Goal | Domain | Target Artifact | Status |
|------|--------|-----------------|--------|
| OSCP or CKS certification | Offensive | Cert | Planned |
| Full Wiz CSPM ownership + MTTR metrics | Multi-Cloud | Monthly report | Planned |
| Security team OKR proposal for 2027 | Leadership | Doc | Planned |
| Deploy GRC Trust Hub to production | GRC | Live system | Planned |
| 3 production Sigma detection rules | Monitoring | Rules in repo | Planned |

---

## Metrics to Track

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| CVEs processed/month | ~500 | Maintain | Jira ticket count |
| SLA compliance rate | TBD (pull from Jira) | >90% | Tickets closed within SLA window |
| Mean time to triage | Minutes (automated) | <1 hour | Intake timestamp → ticket created |
| Critical vuln MTTR | TBD | <15 days | Jira created → resolved |
| Wiz critical findings | TBD (baseline) | -50% in 6 months | Wiz dashboard |
| Team members mentored | 0 | 2 | Direct mentoring relationships |
| Threat models completed | 0 formal | 3 | Documented STRIDE artifacts |
| Attack paths remediated | TBD | 10/quarter | Wiz Attack Path → resolved |

---

## Certifications Roadmap

| Cert | Relevance | Timeline | Status |
|------|-----------|----------|--------|
| AWS Security Specialty | Multi-cloud depth | Q4 2026 | Planned |
| CKS (Certified Kubernetes Security) | Container/K8s | Q1 2027 | Planned |
| OSCP | Offensive validation | Q1 2027 | Planned |
| CISSP | Leadership credibility | Q2 2027 | Planned (if pursuing management track) |

---

## How to Use This Tracker

1. **Weekly:** Update "Level" column as you ship artifacts
2. **Monthly:** Review quarterly goals, adjust priorities
3. **Before interviews:** Pull evidence column for STAR stories
4. **After learning:** Add new skills rows, move from Planned → Learning → Demonstrated
