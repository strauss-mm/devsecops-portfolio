# Regression Detection Methodology

## Problem Statement

Vulnerabilities that were previously fixed can be reintroduced through:
- Dependency downgrades (version pinning conflicts)
- Reverted commits
- Parallel development branches merging stale code
- Container base image changes
- Transitive dependency resolution changes

## Detection Approach

### 1. Scan-to-Scan Comparison

Compare consecutive vulnerability scans to identify:
- **New findings**: CVEs appearing for the first time
- **Resolved findings**: CVEs no longer present
- **Regressions**: CVEs that were resolved but reappeared

```python
def detect_regressions(current_scan, previous_scan, historical_scans):
    current_cves = set(current_scan.cve_ids)
    previous_cves = set(previous_scan.cve_ids)
    
    # CVEs present now but not in previous scan
    new_findings = current_cves - previous_cves
    
    # Check if any "new" findings were actually resolved before
    ever_resolved = set()
    for scan in historical_scans:
        resolved_in_scan = set(scan.cve_ids) - set(scan.next_scan.cve_ids)
        ever_resolved |= resolved_in_scan
    
    regressions = new_findings & ever_resolved
    truly_new = new_findings - ever_resolved
    
    return regressions, truly_new
```

### 2. SBOM Diff

Compare Software Bill of Materials across releases:
- Package version downgrades (regression signal)
- Removed-then-readded packages
- Changed dependency resolution paths

### 3. Jira State Tracking

Cross-reference scan results with ticket history:
- CVE had a "Resolved" ticket → now appears in scan again
- Ticket was closed with "fixed in version X" → version X no longer deployed

## Automation

The `tools/regression-detector/` implements this as a standalone tool:

```bash
regression-detector compare \
  --current scan-2026-06.json \
  --baseline scan-2026-05.json \
  --history scans/ \
  --output report.md
```

## Escalation Policy

Regressions receive automatic escalation:
- Priority bumped by one severity level
- Root cause analysis required before re-closure
- Notification to both security and engineering leads
- Added to sprint retrospective agenda
