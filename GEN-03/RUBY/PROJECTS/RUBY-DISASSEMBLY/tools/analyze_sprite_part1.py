#!/usr/bin/env python3
"""Verify and fingerprint the first mapped portion of Pokémon Ruby sprite.c.

Scope: ResetSpriteData through ContinueAnim.  The checked-in layout and target
CSVs define the three compiler/layout families discovered in the verified ROM
set. ROM binaries are read-only inputs and are never written or emitted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROM_BASE = 0x08000000


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def load_source_manifest(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row["id"]: row for row in data["roms"]}


def load_layouts(path: Path):
    families = {}
    with path.open(encoding="utf-8", newline="") as fp:
        for row in csv.DictReader(fp):
            families.setdefault(row["family"], []).append(
                (row["symbol"], int(row["relative_offset"], 16), int(row["size"]))
            )
    return families


def load_targets(path: Path):
    with path.open(encoding="utf-8", newline="") as fp:
        return list(csv.DictReader(fp))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rom-dir", required=True, type=Path)
    p.add_argument("--source-manifest", type=Path, default=Path("manifests/source_roms.json"))
    p.add_argument("--layouts", type=Path, default=Path("symbols/sprite_part1_layouts.csv"))
    p.add_argument("--targets", type=Path, default=Path("symbols/sprite_part1_targets.csv"))
    p.add_argument("--out-manifest", type=Path, default=Path("manifests/sprite_phase2_part1.json"))
    p.add_argument("--out-fingerprints", type=Path, default=Path("symbols/sprite_part1_fingerprints.csv"))
    p.add_argument("--verify-only", action="store_true")
    args = p.parse_args()

    source = load_source_manifest(args.source_manifest)
    layouts = load_layouts(args.layouts)
    targets = load_targets(args.targets)

    out = {
        "schema_version": 1,
        "scope": "sprite.c part 1: ResetSpriteData through ContinueAnim",
        "address_base": f"0x{ROM_BASE:08X}",
        "layouts": {
            family: [[name, f"0x{rel:X}", size] for name, rel, size in rows]
            for family, rows in layouts.items()
        },
        "targets": {},
    }
    fingerprints = []

    for target in targets:
        target_id = target["target"]
        src = source[target_id]
        data = (args.rom_dir / src["file"]).read_bytes()
        actual_rom_sha1 = sha1(data)
        if actual_rom_sha1 != src["sha1"]:
            raise SystemExit(
                f"{target_id}: whole-ROM SHA-1 mismatch: expected {src['sha1']}, got {actual_rom_sha1}"
            )

        family = target["family"]
        base = int(target["sprite_base_offset"], 16)
        expected_end = int(target["mapped_end_offset"], 16)
        expected_size = int(target["mapped_size"])
        expected_region_sha1 = target["mapped_sha1"]
        region = data[base:expected_end]

        if len(region) != expected_size:
            raise SystemExit(f"{target_id}: mapped-region size mismatch")
        if sha1(region) != expected_region_sha1:
            raise SystemExit(f"{target_id}: mapped-region SHA-1 mismatch")

        function_hashes = []
        for symbol, rel, size in layouts[family]:
            start = base + rel
            chunk = data[start:start + size]
            digest = sha1(chunk)
            function_hashes.append(digest)
            fingerprints.append(
                {
                    "target": target_id,
                    "family": family,
                    "symbol": symbol,
                    "file_offset": f"0x{start:X}",
                    "address": f"0x{ROM_BASE + start:08X}",
                    "thumb_address": f"0x{ROM_BASE + start + 1:08X}",
                    "size": size,
                    "sha1": digest,
                }
            )

        out["targets"][target_id] = [
            family,
            f"0x{base:X}",
            f"0x{expected_end:X}",
            expected_size,
            expected_region_sha1,
            function_hashes,
        ]

    if args.verify_only:
        print(f"verified {len(targets)} targets / {len(fingerprints)} function records")
        return 0

    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_fingerprints.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8")

    with args.out_fingerprints.open("w", encoding="utf-8", newline="") as fp:
        fieldnames = ["target", "family", "symbol", "file_offset", "address", "thumb_address", "size", "sha1"]
        writer = csv.DictWriter(fp, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(fingerprints)

    print(f"verified {len(targets)} targets / {len(fingerprints)} function records")
    print(f"wrote {args.out_manifest}")
    print(f"wrote {args.out_fingerprints}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
