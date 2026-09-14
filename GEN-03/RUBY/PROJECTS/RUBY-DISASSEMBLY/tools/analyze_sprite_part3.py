#!/usr/bin/env python3
"""Verify/fingerprint Pokémon Ruby sprite.c Part 3.

Scope: SetOamMatrixRotationScaling through FreeSpritePaletteByTag.
Japanese Rev 0 and international/debug ROMs use different linked layouts.
ROMs are read-only inputs and are never emitted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROM_BASE = 0x08000000


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def load_sources(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row["id"]: row for row in data["roms"]}


def load_layouts(path: Path):
    result = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as fp:
        for row in csv.DictReader(fp):
            result[row["layout"]].append(
                (row["symbol"], int(row["relative_offset"], 16), int(row["size"]))
            )
    return dict(result)


def load_targets(path: Path):
    with path.open(encoding="utf-8", newline="") as fp:
        return list(csv.DictReader(fp))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rom-dir", required=True, type=Path)
    p.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("manifests/source_roms.json"),
    )
    p.add_argument(
        "--layouts",
        type=Path,
        default=Path("symbols/sprite_part3_layouts.csv"),
    )
    p.add_argument(
        "--targets",
        type=Path,
        default=Path("symbols/sprite_part3_targets.csv"),
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("symbols/sprite_part3_fingerprints.csv"),
    )
    p.add_argument("--verify-only", action="store_true")
    args = p.parse_args()

    sources = load_sources(args.source_manifest)
    layouts = load_layouts(args.layouts)
    targets = load_targets(args.targets)
    records = []

    for target in targets:
        target_id = target["target"]
        source = sources[target_id]
        rom_path = args.rom_dir / source["file"]
        data = rom_path.read_bytes()

        if sha1(data) != source["sha1"]:
            raise SystemExit(f"{target_id}: whole-ROM SHA-1 mismatch")

        base = int(target["part3_base_offset"], 16)
        end = int(target["mapped_end_offset"], 16)
        expected_size = int(target["mapped_size"])
        expected_sha1 = target["mapped_sha1"]
        region = data[base:end]

        if len(region) != expected_size or sha1(region) != expected_sha1:
            raise SystemExit(f"{target_id}: Part-3 region verification failed")

        layout_name = target["layout"]
        if layout_name not in layouts:
            raise SystemExit(f"{target_id}: unknown layout {layout_name}")

        for symbol, rel, size in layouts[layout_name]:
            start = base + rel
            chunk = data[start:start + size]
            if len(chunk) != size:
                raise SystemExit(f"{target_id}:{symbol}: truncated ROM region")
            records.append(
                {
                    "target": target_id,
                    "symbol": symbol,
                    "file_offset": f"0x{start:X}",
                    "address": f"0x{ROM_BASE + start:08X}",
                    "thumb_address": f"0x{ROM_BASE + start + 1:08X}",
                    "size": size,
                    "sha1": sha1(chunk),
                }
            )

        # The next mapped byte sequence is SetSubspriteTables in both layouts.
        next_bytes = data[end:end + 10]
        if next_bytes != bytes.fromhex("81614230402101707047"):
            raise SystemExit(f"{target_id}: unexpected next-boundary bytes")

    if args.verify_only:
        print(f"verified {len(targets)} targets / {len(records)} function records")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fp:
        fieldnames = [
            "target",
            "symbol",
            "file_offset",
            "address",
            "thumb_address",
            "size",
            "sha1",
        ]
        writer = csv.DictWriter(fp, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    print(f"verified {len(targets)} targets / {len(records)} function records")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
