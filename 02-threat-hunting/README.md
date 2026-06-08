# Module 02: Threat Hunting

Detection engineering, indicator development, and proactive threat hunting using Sigma, YARA, and multi-source CTI enrichment.

## Labs

| Lab | Focus | Difficulty | Status |
|-----|-------|-----------|--------|
| [lab-01](labs/lab-01-log-analysis/) | CloudTrail + K8s audit log hunting | Senior | Planned |
| [lab-02](labs/lab-02-sigma-rules/) | Sigma rule development and testing | Senior | Planned |
| [lab-03](labs/lab-03-yara-rules/) | YARA rules for artifact/malware detection | Senior+ | Planned |
| [lab-04](labs/lab-04-threat-intel-enrichment/) | Multi-source CTI enrichment pipeline | Principal | Planned |

## Published Detections

- [sigma/](detections/sigma/) — Production Sigma detection rules
- [yara/](detections/yara/) — YARA rules for artifact detection
- [kql/](detections/kql/) — KQL queries for cloud SIEM

## Writeups

- Building a CTI dashboard from 10+ threat intel feeds
- EPSS vs CVSS: data-driven hunting prioritization
- Multi-source collector architecture for real-time threat landscape

## Key Concepts

- **Detection-as-code**: Version-controlled, tested detection rules
- **Indicator lifecycle**: Creation, validation, deployment, retirement
- **Enrichment pipeline**: IOC correlation across multiple CTI sources
- **Hunting hypotheses**: Structured approach to proactive threat discovery

## Prerequisites

- Familiarity with log formats (CloudTrail, K8s audit, syslog)
- Basic understanding of MITRE ATT&CK framework
- Python 3.11+
