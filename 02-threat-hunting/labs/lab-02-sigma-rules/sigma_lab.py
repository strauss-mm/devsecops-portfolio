"""Sigma Rule Lab — validate, test, and convert detection rules."""

from __future__ import annotations

import re
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

REQUIRED_FIELDS = ["title", "id", "status", "description", "author", "date", "tags", "logsource", "detection", "level"]
VALID_LEVELS = ["informational", "low", "medium", "high", "critical"]
VALID_STATUSES = ["stable", "test", "experimental", "deprecated", "unsupported"]


def validate_rule(path: Path) -> tuple[bool, list[str]]:
    """Validate a Sigma rule file for required fields and structure."""
    errors = []

    try:
        with open(path) as f:
            rule = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parse error: {e}"]

    if not isinstance(rule, dict):
        return False, ["File does not contain a valid YAML mapping"]

    for field in REQUIRED_FIELDS:
        if field not in rule:
            errors.append(f"Missing required field: {field}")

    if "id" in rule:
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        if not re.match(uuid_pattern, str(rule["id"])):
            errors.append(f"Invalid UUID format for id: {rule['id']}")

    if "level" in rule and rule["level"] not in VALID_LEVELS:
        errors.append(f"Invalid level '{rule['level']}' — must be one of {VALID_LEVELS}")

    if "status" in rule and rule["status"] not in VALID_STATUSES:
        errors.append(f"Invalid status '{rule['status']}' — must be one of {VALID_STATUSES}")

    if "detection" in rule:
        detection = rule["detection"]
        if "condition" not in detection:
            errors.append("Detection block missing 'condition' field")
        selections = [k for k in detection if k != "condition" and not k.startswith("filter")]
        if not selections:
            errors.append("Detection block has no selection criteria")

    if "logsource" in rule:
        logsource = rule["logsource"]
        if not any(k in logsource for k in ["category", "product", "service"]):
            errors.append("Logsource must specify at least one of: category, product, service")

    if "tags" in rule:
        for tag in rule["tags"]:
            if not tag.startswith("attack."):
                errors.append(f"Tag '{tag}' should start with 'attack.' for ATT&CK mapping")

    return len(errors) == 0, errors


def extract_mitre_techniques(rule: dict) -> list[str]:
    """Extract MITRE ATT&CK technique IDs from tags."""
    techniques = []
    for tag in rule.get("tags", []):
        if re.match(r"attack\.t\d{4}", tag):
            techniques.append(tag.replace("attack.", "").upper())
    return techniques


@click.group()
def cli():
    """Sigma Rule Development Lab."""
    pass


@cli.command()
@click.option("--rules-dir", required=True, type=click.Path(exists=True))
def validate(rules_dir):
    """Validate all Sigma rules in a directory."""
    rules_path = Path(rules_dir)
    rule_files = list(rules_path.glob("*.yml")) + list(rules_path.glob("*.yaml"))

    if not rule_files:
        console.print(f"[yellow]No YAML files found in {rules_dir}[/yellow]")
        return

    table = Table(title="Rule Validation Results")
    table.add_column("Rule")
    table.add_column("Status")
    table.add_column("Issues")

    passed = 0
    failed = 0

    for rule_file in sorted(rule_files):
        valid, errors = validate_rule(rule_file)
        if valid:
            passed += 1
            table.add_row(rule_file.name, "[green]PASS[/green]", "")
        else:
            failed += 1
            table.add_row(
                rule_file.name,
                "[red]FAIL[/red]",
                "; ".join(errors[:3]),
            )

    console.print(table)
    console.print(f"\n  Passed: [green]{passed}[/green] | Failed: [red]{failed}[/red] | Total: {passed + failed}")


@cli.command()
@click.option("--rules-dir", required=True, type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default=None)
def docs(rules_dir, output):
    """Generate documentation catalog for all rules."""
    rules_path = Path(rules_dir)
    rule_files = list(rules_path.glob("*.yml")) + list(rules_path.glob("*.yaml"))

    lines = ["# Detection Rule Catalog\n"]
    lines.append(f"**Rules**: {len(rule_files)}\n")
    lines.append("| Rule | Level | MITRE | Status |")
    lines.append("|------|-------|-------|--------|")

    for rule_file in sorted(rule_files):
        with open(rule_file) as f:
            rule = yaml.safe_load(f)

        techniques = extract_mitre_techniques(rule)
        mitre_str = ", ".join(techniques) if techniques else "—"

        lines.append(
            f"| {rule.get('title', rule_file.stem)} | "
            f"{rule.get('level', '?')} | "
            f"{mitre_str} | "
            f"{rule.get('status', '?')} |"
        )

    lines.append("\n---\n")

    for rule_file in sorted(rule_files):
        with open(rule_file) as f:
            rule = yaml.safe_load(f)

        lines.append(f"\n## {rule.get('title', rule_file.stem)}\n")
        lines.append(f"**File**: `{rule_file.name}`  ")
        lines.append(f"**ID**: `{rule.get('id', 'N/A')}`  ")
        lines.append(f"**Level**: {rule.get('level', 'N/A')}  ")
        lines.append(f"**Author**: {rule.get('author', 'N/A')}  ")
        lines.append(f"**Status**: {rule.get('status', 'N/A')}\n")

        desc = rule.get("description", "").strip()
        if desc:
            lines.append(f"{desc}\n")

        techniques = extract_mitre_techniques(rule)
        if techniques:
            lines.append(f"**MITRE ATT&CK**: {', '.join(techniques)}\n")

        fps = rule.get("falsepositives", [])
        if fps:
            lines.append("**False Positives**:")
            for fp in fps:
                lines.append(f"- {fp}")
            lines.append("")

    content = "\n".join(lines)

    if output:
        Path(output).write_text(content)
        console.print(f"Catalog written to {output}")
    else:
        console.print(content)


if __name__ == "__main__":
    cli()
