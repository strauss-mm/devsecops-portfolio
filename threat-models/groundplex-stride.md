# STRIDE Threat Model: SnapLogic Groundplex

**Author:** Marna Marie Strauss | **Date:** 2026-06-08 | **Version:** 1.0
**Scope:** Groundplex container runtime on customer-managed infrastructure (EKS/ECS/EC2)
**Classification:** Internal — SnapLogic Security Engineering

---

## 1. System Overview

The SnapLogic Groundplex is the customer-deployed execution engine for SnapLogic pipelines. It runs as a containerized Java application (JCC engine) connecting outbound to the SnapLogic Control Plane.

```
┌─────────────────────────────────────────────────────────────────────┐
│ Customer Infrastructure (AWS/Azure/GCP/On-Prem)                     │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Groundplex Container (Docker/K8s Pod)                        │   │
│  │                                                              │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │   │
│  │  │ JCC Engine  │  │ Snap Packs   │  │ Container OS       │  │   │
│  │  │ (Java WAR)  │  │ (176 ZIPs)   │  │ (Base Image)       │  │   │
│  │  └──────┬──────┘  └──────┬───────┘  └────────────────────┘  │   │
│  │         │                 │                                   │   │
│  │         ▼                 ▼                                   │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ /opt/snaplogic/run/ (application root)                  │ │   │
│  │  │   lib/jcc.war (engine)                                  │ │   │
│  │  │   jcc/classes/sidekick/ (snap packs)                    │ │   │
│  │  │   .slpropz (encrypted config)                           │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │              │                │                            │
│         │ TLS          │ TLS            │ Network                    │
│         ▼              ▼                ▼                            │
│  ┌──────────┐   ┌───────────┐   ┌──────────────┐                   │
│  │ Control  │   │ Customer  │   │ Internal     │                   │
│  │ Plane    │   │ Systems   │   │ K8s Network  │                   │
│  │ (SL CDN) │   │ (DBs/APIs)│   │              │                   │
│  └──────────┘   └───────────┘   └──────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ TLS 1.2+
         ▼
┌─────────────────────────────────────────┐
│ SnapLogic Control Plane (AWS, managed)  │
│                                         │
│  ┌──────────┐  ┌────────┐  ┌────────┐  │
│  │ Designer │  │ MongoDB│  │ API    │  │
│  │ (UI)     │  │ (meta) │  │ Server │  │
│  └──────────┘  └────────┘  └────────┘  │
└─────────────────────────────────────────┘
```

---

## 2. Trust Boundaries

| ID | Boundary | Description |
|----|----------|-------------|
| TB-1 | **Control Plane ↔ Groundplex** | TLS tunnel between SL-managed infra and customer-managed container |
| TB-2 | **Container ↔ Host OS** | Container isolation (namespaces, cgroups, seccomp) |
| TB-3 | **JCC Engine ↔ Snap Packs** | Code execution within same JVM — no isolation between snaps |
| TB-4 | **Groundplex ↔ Customer Systems** | Pipeline connections to customer databases, APIs, file systems |
| TB-5 | **User ↔ Pipeline Execution** | Pipeline author vs. runtime execution context (privilege boundary) |
| TB-6 | **Container ↔ K8s API** | Service account token → cluster API access |
| TB-7 | **Container ↔ Cloud Metadata** | IMDSv1/v2 access to instance credentials |

---

## 3. Data Flows

| ID | From | To | Data | Protocol | Trust Boundary |
|----|------|----|----|----------|----------------|
| DF-1 | Control Plane | Groundplex | Pipeline definitions, snap configs | TLS 1.2 | TB-1 |
| DF-2 | Groundplex | Control Plane | Execution status, logs, metrics | TLS 1.2 | TB-1 |
| DF-3 | Groundplex | Customer DBs | Customer data (read/write) | Various (JDBC, REST) | TB-4 |
| DF-4 | User (Designer) | Control Plane | Pipeline code (Script Snap, Mapper) | TLS 1.2 | TB-5 |
| DF-5 | Script Snap | OS | System commands, file I/O | Local process | TB-2, TB-3 |
| DF-6 | Container | K8s API | Service account auth, pod info | HTTPS | TB-6 |
| DF-7 | Container | Cloud Metadata | IAM role credentials | HTTP (169.254.169.254) | TB-7 |
| DF-8 | .slpropz | JCC Engine | Encrypted secrets (API keys, tokens) | Local file read | — |

---

## 4. STRIDE Analysis

### S — Spoofing

| ID | Threat | Attack Vector | Affected Boundary | Likelihood | Impact |
|----|--------|---------------|-------------------|------------|--------|
| S-1 | Attacker impersonates Control Plane | DNS poisoning or MITM on TLS connection | TB-1 | Low (TLS + certificate pinning) | Critical — could push malicious pipelines |
| S-2 | Pipeline author spoofs identity | Shared credentials or stolen bearer token | TB-5 | Medium | High — execute pipelines as legitimate user |
| S-3 | Container spoofs other pods | Service account token theft → impersonate other workloads | TB-6 | Medium (if RBAC overprivileged) | High |

**Existing Controls:**
- TLS 1.2+ on all Control Plane communication
- Bearer token auth for API calls
- Okta SSO + MFA for Designer access

**Gaps:**
- No mutual TLS (mTLS) between Groundplex and Control Plane
- Bearer tokens can be long-lived if not rotated
- K8s service account tokens are auto-mounted by default

**Recommendations:**
- Implement mTLS for Groundplex ↔ Control Plane (verify both ends)
- Enforce token rotation policy
- Set `automountServiceAccountToken: false` on Groundplex pods

---

### T — Tampering

| ID | Threat | Attack Vector | Affected Boundary | Likelihood | Impact |
|----|--------|---------------|-------------------|------------|--------|
| T-1 | Malicious snap pack injection | Modify JAR files on disk within container | TB-3 | Low (requires container access) | Critical — arbitrary code in JVM |
| T-2 | Pipeline modification in transit | MITM between Designer and Control Plane | TB-1 | Very Low (TLS) | Critical |
| T-3 | .slpropz tampering | Modify encrypted config to redirect pipelines | — | Low (requires container access) | High |
| T-4 | Container image supply chain | Compromised base image or dependency | TB-2 | Medium | Critical |

**Existing Controls:**
- Container image scanning (Trivy + WizCLI monthly)
- Snap packs delivered as signed ZIPs from Control Plane
- Read-only filesystem (when configured)

**Gaps:**
- No runtime file integrity monitoring (FIM) inside container
- No SLSA provenance attestation on snap pack builds
- Container image signed but not verified at deploy time (no cosign/notation)

**Recommendations:**
- Implement Falco or similar for runtime FIM on `/opt/snaplogic/`
- Add cosign signature verification in K8s admission controller
- SLSA Level 2+ for snap pack build pipeline

---

### R — Repudiation

| ID | Threat | Attack Vector | Affected Boundary | Likelihood | Impact |
|----|--------|---------------|-------------------|------------|--------|
| R-1 | Pipeline execution without audit trail | User executes pipeline via API, logs not retained | TB-5 | Medium | Medium |
| R-2 | Admin actions on Groundplex host | SSH to node, modify container, no audit | TB-2 | Medium | High |
| R-3 | Credential usage not attributed | Shared service accounts used by multiple pipelines | TB-4 | High | Medium |

**Existing Controls:**
- Control Plane audit logging (all pipeline executions)
- Datadog log aggregation
- CloudTrail for AWS API calls

**Gaps:**
- Groundplex-local actions (inside container) not centrally logged
- Shared Basic Auth accounts obscure which pipeline used which credential
- No forensic-grade timestamping

**Recommendations:**
- Forward Groundplex JCC logs to central SIEM (not just Control Plane logs)
- Deprecate shared Basic Auth → per-pipeline OAuth2 credentials
- Enable K8s audit logging for pod exec/attach events

---

### I — Information Disclosure

| ID | Threat | Attack Vector | Affected Boundary | Likelihood | Impact |
|----|--------|---------------|-------------------|------------|--------|
| I-1 | **Credential exfiltration via pipeline** | Script Snap sends creds to attacker endpoint (Boehringer 4.2.1) | TB-4 | **Demonstrated** | Critical |
| I-2 | **IAM role credential theft via metadata** | SSRF or Script Snap → 169.254.169.254 → IAM temp creds | TB-7 | **Demonstrated** (Boehringer 4.2.3) | Critical |
| I-3 | Secret exposure in .slpropz | Read encrypted config, decrypt with known key pattern | — | Medium | High |
| I-4 | Snap pack source/config leakage | Read JAR contents, extract hardcoded secrets | TB-3 | Medium | Medium |
| I-5 | K8s secrets from pod | Mount secrets or read from environment variables | TB-6 | Medium | High |

**Existing Controls:**
- .slpropz encryption
- `SECURE_PYTHON=True` (restricts Python imports)
- `ALLOW_GROUNDPLEX_PROCESS_CREATION=false` (blocks shell from Script Snap)

**Gaps:**
- **Basic Auth credentials transmitted in base64 to any endpoint** (platform design issue)
- IMDSv2 not enforced on all customer deployments
- No egress filtering (Groundplex can reach any external endpoint)
- Java native function access bypasses Python import restrictions

**Recommendations:**
- Enforce IMDSv2 (hop limit=1) on all Groundplex nodes
- Implement egress allowlisting (only approved endpoints)
- Migrate from Basic Auth to OAuth2 with token-bound endpoints
- JVM security manager or module system to restrict native access from Script Snap

---

### D — Denial of Service

| ID | Threat | Attack Vector | Affected Boundary | Likelihood | Impact |
|----|--------|---------------|-------------------|------------|--------|
| D-1 | Resource exhaustion via pipeline | Malicious pipeline consumes all CPU/memory | TB-3 | Medium | Medium (single plex) |
| D-2 | Connection pool exhaustion | Snap opens unlimited connections to customer DB | TB-4 | Medium | Medium |
| D-3 | Disk fill attack | Pipeline writes unlimited data to local filesystem | TB-2 | Medium | Medium |
| D-4 | Control Plane disconnect | Network disruption → Groundplex can't receive work | TB-1 | Low | High (operations stop) |

**Existing Controls:**
- K8s resource limits (CPU/memory per pod)
- JCC engine has configurable pipeline timeout
- Control Plane health monitoring

**Gaps:**
- No per-pipeline resource quotas within a single Groundplex
- No disk I/O limits or ephemeral storage caps
- No circuit breaker for failing connections

**Recommendations:**
- Set `ephemeralStorage` limits on pod spec
- Implement per-pipeline execution timeout enforcement
- Add connection pool limits in snap configurations

---

### E — Elevation of Privilege

| ID | Threat | Attack Vector | Affected Boundary | Likelihood | Impact |
|----|--------|---------------|-------------------|------------|--------|
| E-1 | **RCE via Script Snap → container escape** | Script Snap executes code → exploits container runtime vuln | TB-2, TB-5 | **Demonstrated** (Boehringer 4.1.1) | Critical |
| E-2 | **Pipeline user → OS-level access** | Non-admin user creates Script Snap → reverse shell → root | TB-5, TB-2 | **Demonstrated** | Critical |
| E-3 | Container → node via kernel exploit | CVE in container runtime or kernel | TB-2 | Low (patched kernels) | Critical |
| E-4 | Pod → cluster-admin via RBAC | Overprivileged service account → K8s API manipulation | TB-6 | Medium | Critical |
| E-5 | Pipeline user → Secrets Manager | Script Snap → metadata API → IAM role → secrets:GetSecretValue * | TB-5, TB-7 | **Demonstrated** (Boehringer 4.2.3) | Critical |

**Existing Controls:**
- Python import restrictions (`security_code.py`)
- `ALLOW_GROUNDPLEX_PROCESS_CREATION=false`
- PLAT-14611 (In Code Review) — further Script Snap restrictions
- Non-root container user (when configured)

**Gaps:**
- **Java native function access bypasses all Python restrictions** (fundamental architecture issue)
- Container often runs as root or with elevated capabilities
- No seccomp/AppArmor profiles specific to Groundplex
- Service account may have broad K8s permissions

**Recommendations:**
- Run container as non-root with `readOnlyRootFilesystem: true`
- Apply restrictive seccomp profile (block `ptrace`, `mount`, `unshare`)
- Drop all capabilities except `NET_BIND_SERVICE`
- Minimal K8s RBAC: service account with zero permissions
- Long-term: sandbox Script Snap execution in separate container/gVisor

---

## 5. Risk Summary

| Risk | STRIDE | Severity | Status | Mitigation Owner |
|------|--------|----------|--------|------------------|
| RCE via Script Snap bypass | E-1, E-2 | Critical | Active fix (PLAT-14611) | Platform Engineering |
| Credential exfiltration via pipelines | I-1 | Critical | Accepted risk (design limitation) | Product + Security |
| IAM credential theft via metadata | I-2, E-5 | Critical | Mitigation: IMDSv2 enforcement | Customer (with guidance) |
| No egress filtering | I-1 | High | No control in place | Security Engineering |
| Java native function bypass | E-1 | High | Architectural gap | Platform Engineering |
| Container privilege escalation | E-3, E-4 | High | Partially mitigated (varies by deployment) | Customer + Security |
| Weak audit trail inside container | R-1, R-2 | Medium | Partial (Control Plane logs only) | Security Engineering |
| DoS via resource exhaustion | D-1, D-3 | Medium | K8s limits exist but incomplete | Platform Engineering |

---

## 6. Recommended Controls (Priority Order)

### Immediate (Q3 2026)
1. Enforce IMDSv2 (hop limit=1) in all deployment guides and Terraform modules
2. Document + enforce non-root container, drop capabilities, seccomp profile
3. Validate PLAT-14611 fix actually blocks Java native function bypass

### Short-term (Q4 2026)
4. Egress allowlisting for Groundplex network (only Control Plane + customer-defined endpoints)
5. Runtime FIM (Falco) on `/opt/snaplogic/` directory
6. Forward JCC container logs to central SIEM

### Medium-term (2027)
7. Script Snap sandboxing (gVisor or separate sidecar container)
8. mTLS for Groundplex ↔ Control Plane
9. SLSA provenance for snap pack builds
10. Deprecate Basic Auth → OAuth2 only

---

## 7. References

- Boehringer Ingelheim Security Assessment (April 2026) — findings 4.1.1, 4.2.1, 4.2.3
- PLAT-14611 — Script Snap security hardening (In Code Review)
- PLAT-13522 — Python import restrictions (Closed/Done in 4.41.2.0)
- SnapLogic Platform Architecture & Security (2024) — internal reference
- NIST SP 800-154: Guide to Data-Centric System Threat Modeling
- OWASP Threat Modeling Cheat Sheet

---

## Appendix: STRIDE Cheat Sheet

| Category | Question |
|----------|----------|
| **S**poofing | Can an attacker pretend to be someone/something else? |
| **T**ampering | Can an attacker modify data in transit or at rest? |
| **R**epudiation | Can an attacker deny performing an action? |
| **I**nformation Disclosure | Can an attacker access data they shouldn't? |
| **D**enial of Service | Can an attacker disrupt availability? |
| **E**levation of Privilege | Can an attacker gain unauthorized access/permissions? |
