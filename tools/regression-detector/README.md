# Regression Detector

Detect reintroduced vulnerabilities across software releases by comparing scan results over time.

## Usage

```bash
pip install -r requirements.txt

# Compare two scans
python regression_detector.py compare \
  --current scan-2026-06.json \
  --baseline scan-2026-05.json

# Full regression analysis with history
python regression_detector.py analyze \
  --current scan-2026-06.json \
  --history scans/ \
  --output report.md

# Watch mode: monitor a directory for new scans
python regression_detector.py watch \
  --directory scans/ \
  --alert-webhook https://hooks.slack.com/...
```

## Input Format

Accepts Trivy JSON output, CycloneDX SBOM, or a simple CSV:

```json
{
  "results": [
    {
      "vulnerabilities": [
        {
          "id": "CVE-2026-12345",
          "package": "netty-codec-http",
          "installed_version": "4.1.94",
          "fixed_version": "4.1.108",
          "severity": "HIGH"
        }
      ]
    }
  ]
}
```

## Output

- Markdown report with regression table
- JSON output for pipeline integration
- Slack webhook notification (optional)

## How It Works

1. Parse current and historical scan results
2. Build a CVE timeline: when each CVE first appeared, was resolved, reappeared
3. Flag any CVE that was previously resolved but now present again
4. Calculate regression severity (original severity + regression penalty)
5. Generate report with root cause hints (version downgrade, dep change, etc.)
