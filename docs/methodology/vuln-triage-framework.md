# Vulnerability Triage Framework

## Context-Aware Prioritization

Traditional CVSS-only prioritization leads to alert fatigue. This framework combines multiple signals for actionable prioritization.

## Scoring Model

```
Priority Score = (CVSS_base * 0.3) + (EPSS * 0.25) + (Context * 0.25) + (Exploitability * 0.2)
```

### CVSS Base (30%)
- Raw NVD CVSS 3.1 score (0-10)
- Normalized to 0-1 for formula

### EPSS Score (25%)
- Exploit Prediction Scoring System probability (0-1)
- Updated daily from FIRST.org
- Reflects real-world exploitation likelihood

### Context Score (25%)
| Factor | Weight |
|--------|--------|
| Internet-facing asset | +0.3 |
| Contains sensitive data | +0.25 |
| Business-critical service | +0.25 |
| Customer-impacting | +0.2 |
| Internal-only / isolated | -0.2 |

### Exploitability (20%)
| Factor | Score |
|--------|-------|
| Active exploitation (CISA KEV) | 1.0 |
| Public exploit available | 0.8 |
| PoC exists | 0.5 |
| Theoretical only | 0.2 |

## SLA Assignment

| Priority Score | SLA | Severity Label |
|---------------|-----|----------------|
| >= 0.8 | 5 calendar days | Critical |
| >= 0.6 | 15 calendar days | Critical |
| >= 0.4 | 30 calendar days | High |
| >= 0.2 | 90 calendar days | Medium |
| < 0.2 | Best effort | Low |

## Triage Decision Tree

```
1. Is CVE in CISA KEV?
   YES → Critical SLA (5 days), escalate immediately
   NO  → Continue

2. Is EPSS > 0.5?
   YES → Likely Critical, check context
   NO  → Continue

3. Is the vulnerable component internet-facing?
   YES → Increase priority by one level
   NO  → Continue

4. Does a patch/upgrade exist?
   YES → Standard remediation path
   NO  → Evaluate mitigating controls, consider compensating controls

5. Is it a transitive dependency?
   YES → Identify upgrade path for direct dependency
   NO  → Direct remediation
```

## Regression Detection

A reintroduced vulnerability is automatically escalated:
- Previous SLA resets
- Priority Score gets +0.2 bonus (regression penalty)
- Requires root cause analysis before closure
