#!/usr/bin/env python3
"""Pokémon Emerald multi-region 64 KiB bank audit.

This script does not distribute ROM data. Supply local ROM paths explicitly.
It emits CSV/JSON metadata for banks 00-FF.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import zlib
from collections import Counter, defaultdict
from pathlib import Path

BANK_SIZE = 0x10000
EXPECTED_SIZE = 0x1000000


def shannon_entropy(data: bytes) -> float:
    counts = Counter(data)
    n = len(data)
    return -sum((count / n) * math.log2(count / n) for count in counts.values())


def longest_run(data: bytes, value: int) -> int:
    best = current = 0
    for byte in data:
        if byte == value:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def aligned_rom_pointer_count(data: bytes) -> int:
    count = 0
    for offset in range(0, len(data) - 3, 4):
        value = int.from_bytes(data[offset : offset + 4], "little")
        if 0x08000000 <= value < 0x0A000000:
            count += 1
    return count


def plausible_lz77_10_headers(data: bytes) -> int:
    count = 0
    for offset in range(0, len(data) - 4):
        if data[offset] != 0x10:
            continue
        size = data[offset + 1] | (data[offset + 2] << 8) | (data[offset + 3] << 16)
        if 1 <= size <= 0x100000:
            count += 1
    return count


def diff_count(a: bytes, b: bytes) -> int:
    return sum(x != y for x, y in zip(a, b))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jp", required=True, type=Path)
    parser.add_argument("--en", required=True, type=Path)
    parser.add_argument("--fr", required=True, type=Path)
    parser.add_argument("--de", required=True, type=Path)
    parser.add_argument("--it", required=True, type=Path)
    parser.add_argument("--es", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rom_paths = {
        "JP": args.jp,
        "EN": args.en,
        "FR": args.fr,
        "DE": args.de,
        "IT": args.it,
        "ES": args.es,
    }
    roms = {name: path.read_bytes() for name, path in rom_paths.items()}

    for name, data in roms.items():
        if len(data) != EXPECTED_SIZE:
            raise SystemExit(f"{name}: expected {EXPECTED_SIZE:#x} bytes, got {len(data):#x}")

    args.out.mkdir(parents=True, exist_ok=True)
    rows = []

    for bank in range(256):
        start = bank * BANK_SIZE
        blocks = {name: data[start : start + BANK_SIZE] for name, data in roms.items()}
        hashes = {name: hashlib.sha256(block).hexdigest() for name, block in blocks.items()}

        groups = defaultdict(list)
        for name, digest in hashes.items():
            groups[digest].append(name)
        identity_groups = " | ".join(
            "+".join(names)
            for _, names in sorted(groups.items(), key=lambda item: (-len(item[1]), item[1]))
        )

        en = blocks["EN"]
        row = {
            "bank_hex": f"{bank:02X}",
            "bank_index": bank,
            "start": f"0x{start:06X}",
            "end": f"0x{start + BANK_SIZE - 1:06X}",
            "all_identical": len(groups) == 1,
            "variant_count": len(groups),
            "identity_groups": identity_groups,
            "EN_entropy": round(shannon_entropy(en), 5),
            "EN_ff_pct": round(en.count(0xFF) / BANK_SIZE * 100, 3),
            "EN_00_pct": round(en.count(0x00) / BANK_SIZE * 100, 3),
            "EN_longest_ff": longest_run(en, 0xFF),
            "EN_longest_00": longest_run(en, 0x00),
            "EN_ptr32_count": aligned_rom_pointer_count(en),
            "EN_lz10_candidates": plausible_lz77_10_headers(en),
            "EN_crc32": f"{zlib.crc32(en) & 0xFFFFFFFF:08x}",
        }

        for other in ("JP", "FR", "DE", "IT", "ES"):
            changed = diff_count(en, blocks[other])
            row[f"diff_EN_{other}_bytes"] = changed
            row[f"diff_EN_{other}_pct"] = round(changed / BANK_SIZE * 100, 3)

        for name, digest in hashes.items():
            row[f"{name}_sha256"] = digest

        rows.append(row)

    csv_path = args.out / "emerald_64k_bank_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path = args.out / "emerald_64k_bank_audit.json"
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    print(csv_path)
    print(json_path)


if __name__ == "__main__":
    main()
