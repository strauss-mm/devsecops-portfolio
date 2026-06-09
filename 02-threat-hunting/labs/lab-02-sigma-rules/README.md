# Lab 02: Sigma Rule Development

## Objective

Write, test, and validate Sigma detection rules targeting SaaS platform threats — from pipeline injection to credential abuse patterns.

## Why This Matters

Sigma is the lingua franca of detection engineering. Rules written in Sigma can be converted to any SIEM (Splunk, Elastic, Sentinel, Chronicle). Building a library of tested detection rules demonstrates both threat knowledge and engineering discipline.

## What You'll Build

1. Sigma rules for common SaaS platform attack patterns
2. A rule validation framework (syntax + logic testing)
3. Test cases (true positive, true negative, edge cases)
4. A conversion pipeline to multiple SIEM backends

## Running the Lab

```bash
pip install -r requirements.txt

# Validate all rules
python sigma_lab.py validate --rules-dir rules/

# Test a rule against sample logs
python sigma_lab.py test --rule rules/pipeline-injection.yml --logs test-data/

# Convert rules to Splunk/Elastic/KQL
python sigma_lab.py convert --rule rules/pipeline-injection.yml --backend splunk

# Generate rule documentation
python sigma_lab.py docs --rules-dir rules/ --output rule-catalog.md
```

## Exercises

1. **Write a detection**: Create a Sigma rule that detects unauthorized API key usage from an unexpected IP range. Test against the sample logs.

2. **Reduce false positives**: The `suspicious-api-activity.yml` rule fires too often. Tune the detection logic to reduce noise while maintaining coverage.

3. **Coverage mapping**: Map each rule to MITRE ATT&CK techniques. Which techniques have no detection? Write rules to close the gaps.

4. **Backend conversion**: Convert all rules to Splunk SPL and Elastic KQL. Do any rules lose fidelity in translation? Why?

## Key Takeaways

- Good detection rules balance precision (few false positives) with recall (catch real attacks)
- Every rule needs test cases — untested detections are liabilities
- MITRE ATT&CK mapping shows coverage gaps systematically
- Cross-backend compatibility forces you to write portable, well-structured rules
