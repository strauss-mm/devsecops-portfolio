"""Tests for regression detector."""

from datetime import date
from pathlib import Path
import json
import tempfile

from regression_detector import (
    Finding,
    ScanResult,
    detect_regressions,
    generate_markdown_report,
    parse_trivy_json,
)


def make_scan(scan_date: str, cves: list[dict]) -> ScanResult:
    findings = [
        Finding(
            cve_id=c["id"],
            package=c.get("package", "test-pkg"),
            installed_version=c.get("version", "1.0.0"),
            fixed_version=c.get("fix", "2.0.0"),
            severity=c.get("severity", "HIGH"),
        )
        for c in cves
    ]
    return ScanResult(
        scan_date=date.fromisoformat(scan_date),
        source_file="test.json",
        findings=findings,
    )


def test_no_regressions():
    scan1 = make_scan("2026-01-01", [{"id": "CVE-2026-001"}])
    scan2 = make_scan("2026-02-01", [{"id": "CVE-2026-001"}])
    current = make_scan("2026-03-01", [{"id": "CVE-2026-001"}])

    regressions = detect_regressions(current, [scan1, scan2, current])
    assert len(regressions) == 0


def test_detects_regression():
    scan1 = make_scan("2026-01-01", [{"id": "CVE-2026-001"}])
    scan2 = make_scan("2026-02-01", [])  # CVE resolved
    current = make_scan("2026-03-01", [{"id": "CVE-2026-001"}])  # CVE reintroduced

    regressions = detect_regressions(current, [scan1, scan2, current])
    assert len(regressions) == 1
    assert regressions[0].cve_id == "CVE-2026-001"
    assert regressions[0].resolved_date == date(2026, 2, 1)
    assert regressions[0].reintroduced_date == date(2026, 3, 1)


def test_new_cve_not_regression():
    scan1 = make_scan("2026-01-01", [{"id": "CVE-2026-001"}])
    scan2 = make_scan("2026-02-01", [{"id": "CVE-2026-001"}])
    current = make_scan(
        "2026-03-01", [{"id": "CVE-2026-001"}, {"id": "CVE-2026-999"}]
    )

    regressions = detect_regressions(current, [scan1, scan2, current])
    assert len(regressions) == 0


def test_severity_sorting():
    scan1 = make_scan(
        "2026-01-01",
        [
            {"id": "CVE-2026-001", "severity": "LOW"},
            {"id": "CVE-2026-002", "severity": "CRITICAL"},
        ],
    )
    scan2 = make_scan("2026-02-01", [])
    current = make_scan(
        "2026-03-01",
        [
            {"id": "CVE-2026-001", "severity": "LOW"},
            {"id": "CVE-2026-002", "severity": "CRITICAL"},
        ],
    )

    regressions = detect_regressions(current, [scan1, scan2, current])
    assert len(regressions) == 2
    assert regressions[0].severity == "CRITICAL"
    assert regressions[1].severity == "LOW"


def test_markdown_report():
    scan1 = make_scan("2026-01-01", [{"id": "CVE-2026-001", "severity": "HIGH"}])
    scan2 = make_scan("2026-02-01", [])
    current = make_scan("2026-03-01", [{"id": "CVE-2026-001", "severity": "HIGH"}])

    regressions = detect_regressions(current, [scan1, scan2, current])
    report = generate_markdown_report(regressions)

    assert "CVE-2026-001" in report
    assert "HIGH" in report
    assert "Regressions Found**: 1" in report


def test_parse_trivy_json():
    trivy_output = {
        "CreatedAt": "2026-03-01T00:00:00Z",
        "Results": [
            {
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-2026-12345",
                        "PkgName": "netty-codec-http",
                        "InstalledVersion": "4.1.94",
                        "FixedVersion": "4.1.108",
                        "Severity": "HIGH",
                    }
                ]
            }
        ],
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(trivy_output, f)
        f.flush()
        result = parse_trivy_json(Path(f.name))

    assert len(result.findings) == 1
    assert result.findings[0].cve_id == "CVE-2026-12345"
    assert result.findings[0].package == "netty-codec-http"
    assert result.scan_date == date(2026, 3, 1)
