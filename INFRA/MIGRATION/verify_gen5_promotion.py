#!/usr/bin/env python3
"""Fail when Generation V work is stranded only in migration quarantine.

Sakurai's active Generation V corpus is consolidated under the project-facing
CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS tree. This checks path promotion,
not byte identity: canonical files may be newer than their quarantined ancestors.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS"

MAPPINGS = [
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/ROOT/LIBRARY/GEN-05/WHITE/SOURCE",
        PROJECT / "WHITE/RELEASES",
    ),
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/GEN-05/BLACK/SOURCE",
        PROJECT / "BLACK/RELEASES",
    ),
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/GEN-05/WHITE/SOURCE",
        PROJECT / "WHITE/RELEASES",
    ),
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/GEN-05/COMPARE",
        PROJECT / "COMPARES",
    ),
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/CROSS-GEN/TARGET/GEN5-TO-POCKET-MONSTERS",
        PROJECT,
    ),
]


def canonical_relative(relative: Path) -> Path:
    return Path(*("CATALOGS" if part == "CATALOG" else part for part in relative.parts))


missing = []
checked = 0
for legacy_root, canonical_root in MAPPINGS:
    if not legacy_root.exists():
        continue
    for legacy in legacy_root.rglob("*"):
        if not legacy.is_file():
            continue
        checked += 1
        relative = canonical_relative(legacy.relative_to(legacy_root))
        canonical = canonical_root / relative
        if not canonical.exists():
            missing.append((legacy.relative_to(ROOT), canonical.relative_to(ROOT)))

if missing:
    print("Generation V promotion verification FAILED")
    for legacy, canonical in missing:
        print(f" - stranded: {legacy} -> expected {canonical}")
    sys.exit(1)

print(f"Generation V promotion verification passed: {checked} quarantined files have canonical owner paths.")
