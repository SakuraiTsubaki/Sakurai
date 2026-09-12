#!/usr/bin/env python3
"""Convert the 650 x 60-byte BW personal base table into Gen II-friendly columns.

Each output table is smaller than one 16 KiB GBC ROMX bank. This lets the
Gen II adapter use banked far reads without truncating Generation V fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

RECORD_SIZE = 0x3C
RECORD_COUNT = 650

FIELDS = {
    "base_stats": (0x00, 6),
    "types": (0x06, 2),
    "catch_rate": (0x08, 1),
    "ev_yield": (0x0A, 2),
    "held_items": (0x0C, 6),
    "gender_ratio": (0x12, 1),
    "hatch_counter": (0x13, 1),
    "base_friendship": (0x14, 1),
    "growth_rate": (0x15, 1),
    "egg_groups": (0x16, 2),
    "abilities": (0x18, 3),
    "escape_rate": (0x1B, 1),
    "form_route": (0x1C, 5),
    "body_color": (0x21, 1),
    "base_exp_u16": (0x22, 2),
    "height": (0x24, 2),
    "weight": (0x26, 2),
    "tm_hm": (0x28, 16),
    "tutor": (0x38, 4),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("personal_bin", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("data/gen5/personal_columns"))
    args = ap.parse_args()

    data = args.personal_bin.read_bytes()
    expected = RECORD_COUNT * RECORD_SIZE
    if len(data) != expected:
        raise ValueError(f"expected {expected} bytes, got {len(data)}")

    records = [
        data[i * RECORD_SIZE : (i + 1) * RECORD_SIZE]
        for i in range(RECORD_COUNT)
    ]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": args.personal_bin.name,
        "source_sha1": hashlib.sha1(data).hexdigest(),
        "record_size": RECORD_SIZE,
        "record_count": RECORD_COUNT,
        "tables": {},
    }

    for name, (offset, size) in FIELDS.items():
        table = b"".join(record[offset : offset + size] for record in records)
        if len(table) > 0x4000:
            raise ValueError(f"{name} exceeds one GBC ROMX bank: {len(table)}")
        path = args.out_dir / f"{name}.bin"
        path.write_bytes(table)
        manifest["tables"][name] = {
            "source_offset": offset,
            "entry_size": size,
            "size": len(table),
            "sha1": hashlib.sha1(table).hexdigest(),
        }

    (args.out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
