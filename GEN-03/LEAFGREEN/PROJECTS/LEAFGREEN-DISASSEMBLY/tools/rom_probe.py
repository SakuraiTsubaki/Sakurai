#!/usr/bin/env python3
"""Small read-only probe for Pokémon LeafGreen GBA images.

The tool does not modify ROMs. It reports the standard GBA header and the
Game Freak compatibility header found at ROM offset 0x100.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

GF_HEADER_OFFSET = 0x100
GF_HEADER_SIZE = 0x104
LANGUAGES = {
    1: "Japanese",
    2: "English",
    3: "French",
    4: "Italian",
    5: "German",
    6: "Korean (unused in these ROMs)",
    7: "Spanish",
}
VERSIONS = {5: "LeafGreen"}

GF_U32_FIELDS = {
    "version": 0x00,
    "language": 0x04,
    "mon_front_pics": 0x28,
    "mon_back_pics": 0x2C,
    "mon_normal_palettes": 0x30,
    "mon_shiny_palettes": 0x34,
    "mon_icons": 0x38,
    "mon_icon_palette_ids": 0x3C,
    "mon_icon_palettes": 0x40,
    "mon_species_names": 0x44,
    "move_names": 0x48,
    "decorations": 0x4C,
}


def u32le(data: bytes, off: int) -> int:
    return int.from_bytes(data[off:off + 4], "little")


def arm_branch_target(word: int, pc_offset: int = 0) -> int | None:
    # ARM B/BL immediate: bits 27..25 == 101. PC observed by instruction is +8.
    if ((word >> 25) & 0x7) != 0b101:
        return None
    imm24 = word & 0x00FFFFFF
    if imm24 & 0x00800000:
        imm24 -= 1 << 24
    return pc_offset + 8 + (imm24 << 2)


def gba_header_checksum(data: bytes) -> int:
    # Complement check over 0xA0..0xBC inclusive.
    return (-(sum(data[0xA0:0xBD]) + 0x19)) & 0xFF


def probe(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < GF_HEADER_OFFSET + GF_HEADER_SIZE:
        raise ValueError(f"{path}: file too small")

    entry_word = u32le(data, 0)
    branch_target = arm_branch_target(entry_word, 0)
    gf = GF_HEADER_OFFSET
    version = u32le(data, gf + 0x00)
    language = u32le(data, gf + 0x04)
    game_name = data[gf + 0x08:gf + 0x28].split(b"\0", 1)[0].decode("ascii", "replace")

    pointers = {
        name: u32le(data, gf + rel)
        for name, rel in GF_U32_FIELDS.items()
        if rel >= 0x28
    }

    expected_checksum = gba_header_checksum(data)
    stored_checksum = data[0xBD]

    return {
        "file": path.name,
        "size": len(data),
        "sha1": hashlib.sha1(data).hexdigest(),
        "entry_word": f"0x{entry_word:08X}",
        "entry_target_offset": None if branch_target is None else f"0x{branch_target:06X}",
        "entry_target_address": None if branch_target is None else f"0x{0x08000000 + branch_target:08X}",
        "gba": {
            "title": data[0xA0:0xAC].decode("ascii", "replace").rstrip("\0"),
            "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
            "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
            "fixed_value": f"0x{data[0xB2]:02X}",
            "main_unit_code": data[0xB3],
            "device_type": data[0xB4],
            "software_version": data[0xBC],
            "header_checksum": f"0x{stored_checksum:02X}",
            "calculated_checksum": f"0x{expected_checksum:02X}",
            "checksum_ok": stored_checksum == expected_checksum,
        },
        "gf": {
            "offset": f"0x{GF_HEADER_OFFSET:06X}",
            "size": f"0x{GF_HEADER_SIZE:X}",
            "version": version,
            "version_name": VERSIONS.get(version, "unknown"),
            "language": language,
            "language_name": LANGUAGES.get(language, "unknown"),
            "game_name": game_name,
            "pointers": {k: f"0x{v:08X}" for k, v in pointers.items()},
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", nargs="+", type=Path)
    ap.add_argument("--compact", action="store_true")
    args = ap.parse_args()
    reports = [probe(p) for p in args.rom]
    print(json.dumps(reports, indent=None if args.compact else 2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
