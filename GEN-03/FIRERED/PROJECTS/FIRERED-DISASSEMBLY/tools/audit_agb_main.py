#!/usr/bin/env python3
"""Audit the first Thumb function (AgbMain) across FireRed baselines.

Input manifest format: JSON object mapping baseline id to local ROM path.
The tool is read-only. It records the function end, Thumb BL count, the
observed print-init call slot, and the flash-memory guard sequence.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

AGB_MAIN_START = 0x3A4
NEXT_FUNC_SEARCH_START = 0x480
NEXT_FUNC_SEARCH_END = 0x500
FLASH_GUARD_PATTERN = bytes.fromhex("0068012802d00020")


def find_next_function(data: bytes) -> int:
    for offset in range(NEXT_FUNC_SEARCH_START, NEXT_FUNC_SEARCH_END, 2):
        if data[offset:offset + 2] == b"\x00\xB5":  # push {lr}
            return offset
    raise ValueError("could not locate the function following AgbMain")


def is_thumb_bl(data: bytes, offset: int) -> bool:
    first = int.from_bytes(data[offset:offset + 2], "little")
    second = int.from_bytes(data[offset + 2:offset + 4], "little")
    return (first & 0xF800) == 0xF000 and (second & 0xF800) == 0xF800


def count_thumb_bl(data: bytes, start: int, end: int) -> int:
    count = 0
    offset = start
    while offset + 3 < end:
        if is_thumb_bl(data, offset):
            count += 1
            offset += 4
        else:
            offset += 2
    return count


def audit(path: Path) -> dict:
    data = path.read_bytes()
    end = find_next_function(data)
    flash_offset = data.find(FLASH_GUARD_PATTERN, AGB_MAIN_START, end)
    return {
        "start": AGB_MAIN_START,
        "end_exclusive": end,
        "size": end - AGB_MAIN_START,
        "thumb_bl_calls": count_thumb_bl(data, AGB_MAIN_START, end),
        # In every audited FireRed baseline the optional print-init slot is
        # precisely the instruction at 0x40A. When absent, that location is
        # the following LDR/guard sequence instead.
        "print_init_call": is_thumb_bl(data, 0x40A),
        "flash_memory_guard": flash_offset >= 0,
        "flash_guard_offset": flash_offset if flash_offset >= 0 else None,
        "next_function": end,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path, help="JSON mapping baseline id -> ROM path")
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = {name: audit(Path(path)) for name, path in manifest.items()}

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "baseline", "start", "end_exclusive", "size", "thumb_bl_calls",
                "print_init_call", "flash_memory_guard", "flash_guard_offset",
                "next_function",
            ])
            for name, row in result.items():
                w.writerow([
                    name,
                    f"0x{row['start']:06X}",
                    f"0x{row['end_exclusive']:06X}",
                    f"0x{row['size']:X}",
                    row["thumb_bl_calls"],
                    str(row["print_init_call"]).lower(),
                    str(row["flash_memory_guard"]).lower(),
                    "" if row["flash_guard_offset"] is None else f"0x{row['flash_guard_offset']:06X}",
                    f"0x{row['next_function']:06X}",
                ])

    if not args.csv and not args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
