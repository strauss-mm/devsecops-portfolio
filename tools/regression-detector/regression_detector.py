"""Regression Detector — identify reintroduced vulnerabilities across releases."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class Finding:
    cve_id: str
    package: str
    installed_version: str
    fixed_version: str
    severity: str
    path: str = ""


@dataclass
class ScanResult:
    scan_date: date
    source_file: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def cve_ids(self) -> set[str]:
        return {f.cve_id for f in self.findings}


@dataclass
class Regression:
    cve_id: str
    package: str
    severity: str
    first_seen: date
    resolved_date: date
    reintroduced_date: date
    original_version: str
    current_version: str


def parse_trivy_json(path: Path) -> ScanResult:
    """Parse Trivy JSON output into a ScanResult."""
    data = json.loads(path.read_text())

    findings = []
    results = data.get("Results", data.get("results", []))
    for result in results:
        vulns = result.get("Vulnerabilities", result.get("vulnerabilities", []))
        for vuln in vulns:
            findings.append(
                Finding(
                    cve_id=vuln.get("VulnerabilityID", vuln.get("id", "")),
                    package=vuln.get("PkgName", vuln.get("package", "")),
                    installed_version=vuln.get(
                        "InstalledVersion", vuln.get("installed_version", "")
                    ),
                    fixed_version=vuln.get(
                        "FixedVersion", vuln.get("fixed_version", "")
                    ),
                    severity=vuln.get("Severity", vuln.get("severity", "UNKNOWN")),
                    path=vuln.get("PkgPath", vuln.get("path", "")),
                )
            )

    scan_date_str = data.get("CreatedAt", data.get("scan_date", ""))
    scan_date = (
        date.fromisoformat(scan_date_str[:10]) if scan_date_str else date.today()
    )

    return ScanResult(scan_date=scan_date, source_file=str(path), findings=findings)


def detect_regressions(
    current: ScanResult, history: list[ScanResult]
) -> list[Regression]:
    """Compare current scan against history to find regressions."""
    sorted_history = sorted(history, key=lambda s: s.scan_date)

    ever_resolved: dict[str, tuple[date, date, Finding]] = {}

    for i, scan in enumerate(sorted_history[:-1]):
        next_scan = sorted_history[i + 1]
        resolved_cves = scan.cve_ids - next_scan.cve_ids
        for cve_id in resolved_cves:
            finding = next(f for f in scan.findings if f.cve_id == cve_id)
            ever_resolved[cve_id] = (scan.scan_date, next_scan.scan_date, finding)

    regressions = []
    for finding in current.findings:
        if finding.cve_id in ever_resolved:
            first_seen, resolved_date, original = ever_resolved[finding.cve_id]
            regressions.append(
                Regression(
                    cve_id=finding.cve_id,
                    package=finding.package,
                    severity=finding.severity,
                    first_seen=first_seen,
                    resolved_date=resolved_date,
                    reintroduced_date=current.scan_date,
                    original_version=original.installed_version,
                    current_version=finding.installed_version,
                )
            )

    return sorted(
        regressions,
        key=lambda r: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(
            r.severity, 4
        ),
    )


def render_table(regressions: list[Regression]) -> None:
    """Display regressions in a rich table."""
    table = Table(title="Vulnerability Regressions Detected")
    table.add_column("CVE", style="red bold")
    table.add_column("Package")
    table.add_column("Severity")
    table.add_column("Resolved")
    table.add_column("Reintroduced")
    table.add_column("Version Change")

    for r in regressions:
        severity_style = {
            "CRITICAL": "red bold",
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "green",
        }.get(r.severity, "white")

        table.add_row(
            r.cve_id,
            r.package,
            f"[{severity_style}]{r.severity}[/]",
            str(r.resolved_date),
            str(r.reintroduced_date),
            f"{r.original_version} -> {r.current_version}",
        )

    console.print(table)


def generate_markdown_report(regressions: list[Regression]) -> str:
    """Generate a markdown report of regressions."""
    lines = ["# Regression Report\n"]
    lines.append(f"**Date**: {date.today()}\n")
    lines.append(f"**Regressions Found**: {len(regressions)}\n")

    if not regressions:
        lines.append("No regressions detected.\n")
        return "\n".join(lines)

    lines.append("| CVE | Package | Severity | Resolved | Reintroduced | Version |")
    lines.append("|-----|---------|----------|----------|--------------|---------|")

    for r in regressions:
        lines.append(
            f"| {r.cve_id} | {r.package} | {r.severity} | "
            f"{r.resolved_date} | {r.reintroduced_date} | "
            f"{r.original_version} -> {r.current_version} |"
        )

    lines.append("\n## Action Required\n")
    lines.append(
        "Each regression requires root cause analysis before closure. "
        "Priority is bumped by one severity level.\n"
    )

    return "\n".join(lines)


@click.group()
def cli():
    """Regression Detector — find reintroduced vulnerabilities."""
    pass


@cli.command()
@click.option("--current", required=True, type=click.Path(exists=True))
@click.option("--baseline", required=True, type=click.Path(exists=True))
def compare(current: str, baseline: str):
    """Compare two scan results for regressions."""
    current_scan = parse_trivy_json(Path(current))
    baseline_scan = parse_trivy_json(Path(baseline))

    new_cves = current_scan.cve_ids - baseline_scan.cve_ids
    resolved_cves = baseline_scan.cve_ids - current_scan.cve_ids

    console.print(f"\n[bold]Scan Comparison[/bold]")
    console.print(f"  Current:  {len(current_scan.findings)} findings")
    console.print(f"  Baseline: {len(baseline_scan.findings)} findings")
    console.print(f"  New:      [red]{len(new_cves)}[/red]")
    console.print(f"  Resolved: [green]{len(resolved_cves)}[/green]")


@cli.command()
@click.option("--current", required=True, type=click.Path(exists=True))
@click.option("--history", required=True, type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default=None)
def analyze(current: str, history: str, output: str | None):
    """Full regression analysis with historical scan data."""
    current_scan = parse_trivy_json(Path(current))

    history_path = Path(history)
    historical_scans = []
    for scan_file in sorted(history_path.glob("*.json")):
        if scan_file.name != Path(current).name:
            historical_scans.append(parse_trivy_json(scan_file))

    historical_scans.append(current_scan)

    regressions = detect_regressions(current_scan, historical_scans)

    if regressions:
        render_table(regressions)
        console.print(
            f"\n[red bold]{len(regressions)} regression(s) detected![/red bold]"
        )
    else:
        console.print("\n[green]No regressions detected.[/green]")

    if output:
        report = generate_markdown_report(regressions)
        Path(output).write_text(report)
        console.print(f"\nReport written to {output}")


if __name__ == "__main__":
    cli()
