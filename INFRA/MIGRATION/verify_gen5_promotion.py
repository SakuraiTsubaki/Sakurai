#!/usr/bin/env python3
"""Fail when Generation V work is stranded only in migration quarantine.

This checks path promotion, not byte identity. A canonical file may legitimately be a
newer revision than its quarantined predecessor, but every quarantined active-work
path must have a canonical owner path.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

MAPPINGS = [
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/ROOT/LIBRARY/GEN-05/WHITE/SOURCE",
        ROOT / "GEN-05/WHITE/RELEASES",
    ),
    (
        ROOT / "INFRA/MIGRATION/PRE-V12/CROSS-GEN/TARGET/GEN5-TO-POCKET-MONSTERS",
        ROOT / "CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS",
    ),
]

missing = []
checked = 0
for legacy_root, canonical_root in MAPPINGS:
    if not legacy_root.exists():
        continue
    for legacy in legacy_root.rglob("*"):
        if not legacy.is_file():
            continue
        checked += 1
        relative = legacy.relative_to(legacy_root)
        canonical = canonical_root / relative
        if not canonical.exists():
            missing.append((legacy.relative_to(ROOT), canonical.relative_to(ROOT)))

if missing:
    print("Generation V promotion verification FAILED")
    for legacy, canonical in missing:
        print(f" - stranded: {legacy} -> expected {canonical}")
    sys.exit(1)

print(f"Generation V promotion verification passed: {checked} quarantined files have canonical owner paths.")
