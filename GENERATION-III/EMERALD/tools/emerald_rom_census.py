#!/usr/bin/env python3
"""Safe Pokémon Emerald / GBA ROM metadata census.

Reads local .gba files and emits only derived metadata, hashes, and byte-difference
statistics. It never copies ROM bytes into output artifacts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path
import zlib

LANG_BY_CODE = {
    "J": "Japanese",
    "E": "English",
    "D": "German",
    "F": "French",
    "I": "Italian",
    "S": "Spanish",
}
BLOCK_SIZE = 0x10000  # 64 KiB fingerprint block


def digests(data: bytes) -> dict[str, str]:
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
    }


def header_checksum(data: bytes) -> int:
    # GBA header complement check: -(sum(A0..BC) + 0x19) mod 256.
    return (-(sum(data[0xA0:0xBD]) + 0x19)) & 0xFF


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    code = data[0xAC:0xB0].decode("ascii", "replace")
    calculated = header_checksum(data)
    return {
        "file": path.name,
        "size": len(data),
        "title": data[0xA0:0xAC].decode("ascii", "replace").rstrip("\x00"),
        "game_code": code,
        "language": LANG_BY_CODE.get(code[-1:], "Unknown"),
        "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
        "fixed_value": f"{data[0xB2]:02X}",
        "software_version": data[0xBC],
        "header_checksum_stored": f"{data[0xBD]:02X}",
        "header_checksum_calculated": f"{calculated:02X}",
        "header_checksum_ok": calculated == data[0xBD],
        **digests(data),
    }


def pairwise(rows: list[dict], data_by_file: dict[str, bytes]) -> list[dict]:
    out = []
    for a, b in itertools.combinations(rows, 2):
        ba = data_by_file[a["file"]]
        bb = data_by_file[b["file"]]
        if len(ba) != len(bb):
            limit = min(len(ba), len(bb))
        else:
            limit = len(ba)

        different = 0
        first = None
        last = None
        # Chunking avoids building a giant per-byte index list.
        chunk = 1 << 20
        for start in range(0, limit, chunk):
            xa = ba[start:start + chunk]
            xb = bb[start:start + chunk]
            for rel, (x, y) in enumerate(zip(xa, xb)):
                if x != y:
                    pos = start + rel
                    different += 1
                    if first is None:
                        first = pos
                    last = pos
        different += abs(len(ba) - len(bb))
        if len(ba) != len(bb):
            first = first if first is not None else limit
            last = max(len(ba), len(bb)) - 1

        blocks = min(len(ba), len(bb)) // BLOCK_SIZE
        same_blocks = sum(
            ba[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
            == bb[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
            for i in range(blocks)
        )
        denom = max(len(ba), len(bb)) or 1
        out.append({
            "a": a["game_code"],
            "b": b["game_code"],
            "file_a": a["file"],
            "file_b": b["file"],
            "identical": different == 0 and len(ba) == len(bb),
            "differing_bytes": different,
            "difference_percent": round(100 * different / denom, 6),
            "first_diff_offset": None if first is None else f"0x{first:08X}",
            "last_diff_offset": None if last is None else f"0x{last:08X}",
            "identical_64k_blocks": same_blocks,
            "total_64k_blocks": blocks,
        })
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom_dir", type=Path, help="directory containing .gba inputs")
    ap.add_argument("out_dir", type=Path, help="directory for non-ROM reports")
    args = ap.parse_args()

    roms = sorted(args.rom_dir.glob("*.gba"))
    if not roms:
        raise SystemExit("no .gba files found")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    data_by_file = {p.name: p.read_bytes() for p in roms}
    rows = [inspect(p) for p in roms]
    pairs = pairwise(rows, data_by_file)

    groups: dict[str, list[str]] = {}
    for row in rows:
        groups.setdefault(row["sha256"], []).append(row["file"])
    duplicates = [files for files in groups.values() if len(files) > 1]

    report = {
        "rom_count": len(rows),
        "unique_binary_count": len(groups),
        "duplicate_groups": duplicates,
        "roms": rows,
        "pairwise": pairs,
    }
    (args.out_dir / "rom-census.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(args.out_dir / "rom-inventory.csv", rows)
    write_csv(args.out_dir / "pairwise-diff.csv", pairs)


if __name__ == "__main__":
    main()
