#!/usr/bin/env python3
"""Diff two CycloneDX SBOMs and report added/removed/changed packages."""

import json
import sys
from pathlib import Path


def load_sbom(path: str) -> dict[str, dict]:
    with open(path) as f:
        data = json.load(f)

    packages = {}
    for comp in data.get("components", []):
        key = f"{comp.get('group', '')}/{comp['name']}"
        packages[key] = {
            "name": comp["name"],
            "version": comp.get("version", "unknown"),
            "type": comp.get("type", "unknown"),
            "purl": comp.get("purl", ""),
        }
    return packages


def diff_sboms(old_path: str, new_path: str) -> None:
    old = load_sbom(old_path)
    new = load_sbom(new_path)

    old_keys = set(old.keys())
    new_keys = set(new.keys())

    added = new_keys - old_keys
    removed = old_keys - new_keys
    common = old_keys & new_keys

    changed = []
    for key in sorted(common):
        if old[key]["version"] != new[key]["version"]:
            changed.append((key, old[key]["version"], new[key]["version"]))

    print(f"SBOM Diff: {Path(old_path).name} → {Path(new_path).name}")
    print(f"{'=' * 60}")
    print(f"Old: {len(old)} packages | New: {len(new)} packages")
    print()

    if added:
        print(f"ADDED ({len(added)}):")
        for key in sorted(added):
            print(f"  + {key} @ {new[key]['version']}")
        print()

    if removed:
        print(f"REMOVED ({len(removed)}):")
        for key in sorted(removed):
            print(f"  - {key} @ {old[key]['version']}")
        print()

    if changed:
        print(f"VERSION CHANGED ({len(changed)}):")
        for key, old_ver, new_ver in changed:
            print(f"  ~ {key}: {old_ver} → {new_ver}")
        print()

    if not added and not removed and not changed:
        print("No differences found.")

    total_changes = len(added) + len(removed) + len(changed)
    print(f"Total changes: {total_changes}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old-sbom.json> <new-sbom.json>")
        sys.exit(1)
    diff_sboms(sys.argv[1], sys.argv[2])
