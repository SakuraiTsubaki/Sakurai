#!/usr/bin/env python3
"""Analyze verified Pokémon Ruby GBA ROMs without committing ROM binaries.

Reads the repository's source ROM manifest, verifies local files, parses GBA
headers, identifies entry branches and large filler ranges, and summarizes
revision-to-revision byte differences. Standard library only.
"""
from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import struct
from pathlib import Path

PAIR_IDS = [
    ("english_rev0", "english_rev1"),
    ("english_rev1", "english_rev2"),
    ("germany_rev0", "germany_rev1"),
    ("france_rev0", "france_rev1"),
    ("italy_rev0", "italy_rev1"),
    ("spain_rev0", "spain_rev1"),
    ("germany_rev0", "germany_debug_rev0"),
]

THUMB_CONDS = {
    0x0: "EQ", 0x1: "NE", 0x2: "CS/HS", 0x3: "CC/LO",
    0x4: "MI", 0x5: "PL", 0x6: "VS", 0x7: "VC",
    0x8: "HI", 0x9: "LS", 0xA: "GE", 0xB: "LT",
    0xC: "GT", 0xD: "LE",
}


def digest(data: bytes) -> dict[str, str]:
    return {
        "crc32": f"{binascii.crc32(data) & 0xFFFFFFFF:08x}",
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def parse_header(data: bytes) -> dict:
    if len(data) < 0xC0:
        raise ValueError("file is too small to contain a GBA header")
    entry_word = struct.unpack_from("<I", data, 0)[0]
    entry_target = None
    if ((entry_word >> 24) & 0xF) == 0xA:  # ARM B
        imm = entry_word & 0x00FFFFFF
        if imm & 0x00800000:
            imm -= 1 << 24
        entry_target = (8 + (imm << 2)) & 0xFFFFFFFF

    calc = (-(0x19 + sum(data[0xA0:0xBD]))) & 0xFF
    return {
        "title": data[0xA0:0xAC].rstrip(b"\0").decode("ascii", "replace"),
        "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
        "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
        "unit_code": data[0xB3],
        "device_type": data[0xB4],
        "software_version": data[0xBC],
        "header_checksum": data[0xBD],
        "header_checksum_calculated": calc,
        "header_checksum_valid": data[0xBD] == calc,
        "entry_word": f"0x{entry_word:08X}",
        "entry_target_file_offset": None if entry_target is None else f"0x{entry_target:08X}",
        "entry_target_rom_address": None if entry_target is None else f"0x{0x08000000 + entry_target:08X}",
    }


def filler_runs(data: bytes, minimum: int = 0x1000) -> list[dict]:
    runs = []
    i = 0
    while i < len(data):
        value = data[i]
        if value not in (0x00, 0xFF):
            i += 1
            continue
        j = i + 1
        while j < len(data) and data[j] == value:
            j += 1
        if j - i >= minimum:
            runs.append({"start": f"0x{i:X}", "end": f"0x{j:X}", "size": j - i, "byte": f"0x{value:02X}"})
        i = j
    runs.sort(key=lambda x: x["size"], reverse=True)
    return runs


def diff_runs(a: bytes, b: bytes) -> tuple[int, list[tuple[int, int]]]:
    n = min(len(a), len(b))
    runs = []
    diff_bytes = 0
    i = 0
    while i < n:
        if a[i] == b[i]:
            i += 1
            continue
        start = i
        while i < n and a[i] != b[i]:
            i += 1
        runs.append((start, i))
        diff_bytes += i - start
    if len(a) != len(b):
        runs.append((n, max(len(a), len(b))))
        diff_bytes += abs(len(a) - len(b))
    return diff_bytes, runs


def thumb_conditional_at(data: bytes, offset: int) -> dict | None:
    if offset + 2 > len(data) or offset & 1:
        return None
    insn = int.from_bytes(data[offset:offset + 2], "little")
    if (insn & 0xF000) != 0xD000:
        return None
    cond = (insn >> 8) & 0xF
    if cond >= 0xE:
        return None
    imm = insn & 0xFF
    if imm & 0x80:
        imm -= 0x100
    target = offset + 4 + imm * 2
    return {
        "offset": f"0x{offset:X}",
        "halfword": f"0x{insn:04X}",
        "condition": THUMB_CONDS[cond],
        "target_offset": f"0x{target:X}",
    }


def compare(a: bytes, b: bytes, exact_limit: int = 1024) -> dict:
    diff_bytes, runs = diff_runs(a, b)
    result = {
        "different_bytes": diff_bytes,
        "different_runs": len(runs),
        "first_difference": None if not runs else f"0x{runs[0][0]:X}",
        "last_difference_end": None if not runs else f"0x{runs[-1][1]:X}",
    }
    if diff_bytes <= exact_limit:
        changes = []
        for start, end in runs:
            for off in range(start, end):
                old = a[off] if off < len(a) else None
                new = b[off] if off < len(b) else None
                changes.append({
                    "offset": f"0x{off:X}",
                    "old": None if old is None else f"0x{old:02X}",
                    "new": None if new is None else f"0x{new:02X}",
                })
        result["changes"] = changes

        # Also decode aligned Thumb conditional branches whose high byte changed.
        thumb = []
        touched_halfwords = sorted({off & ~1 for start, end in runs for off in range(start, end)})
        for off in touched_halfwords:
            old = thumb_conditional_at(a, off)
            new = thumb_conditional_at(b, off)
            if old and new and old != new:
                thumb.append({"old": old, "new": new})
        if thumb:
            result["thumb_conditional_changes"] = thumb
    else:
        # Compact 64 KiB difference map for large regional/revision changes.
        block = 0x10000
        changed_blocks = []
        for off in range(0, max(len(a), len(b)), block):
            if a[off:off + block] != b[off:off + block]:
                changed_blocks.append(f"0x{off:X}")
        result["changed_64k_blocks"] = changed_blocks
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True, help="directory containing local read-only ROM files")
    ap.add_argument("--manifest", type=Path, default=Path("manifests/source_roms.json"))
    ap.add_argument("--output", type=Path, default=Path("build/rom_structure.json"))
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in manifest["roms"]}
    loaded: dict[str, bytes] = {}
    rom_reports = {}

    for rom_id, row in by_id.items():
        path = args.rom_dir / row["file"]
        data = path.read_bytes()
        got = digest(data)
        for key in ("crc32", "sha1", "sha256"):
            if got[key].lower() != row[key].lower():
                raise SystemExit(f"{rom_id}: {key} mismatch for {path}")
        loaded[rom_id] = data
        rom_reports[rom_id] = {
            "file": row["file"],
            "size": len(data),
            "hashes": got,
            "header": parse_header(data),
            "largest_filler_runs": filler_runs(data)[:10],
        }

    comparisons = {}
    for left, right in PAIR_IDS:
        if left in loaded and right in loaded:
            comparisons[f"{left}__to__{right}"] = compare(loaded[left], loaded[right])

    output = {
        "schema_version": 1,
        "policy": "Generated metadata only; ROM binaries are never written to the repository.",
        "roms": rom_reports,
        "comparisons": comparisons,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
