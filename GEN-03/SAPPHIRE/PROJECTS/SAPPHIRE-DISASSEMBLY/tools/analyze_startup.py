#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import struct
from pathlib import Path

ROM_BASE = 0x08000000
EXPECTED_INIT_WORD = 0xE3A00012
STARTUP_SIZE = 0x17C
EXTENDED_METADATA_START = 0xD0
EXTENDED_METADATA_END = 0x204

LANGUAGE_IDS = {
    1: "Japanese",
    2: "English",
    3: "French",
    4: "Italian",
    5: "German",
    7: "Spanish",
}

POINTER_NAMES = (
    "mon_front_pic_table",
    "mon_back_pic_table",
    "mon_palette_table",
    "mon_shiny_palette_table",
    "mon_icon_table",
    "mon_icon_palette_indices",
    "mon_icon_palette_table",
    "species_names",
    "move_names",
    "decorations",
)


def u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


def decode_arm_branch_target(word: int, address: int = 0) -> int:
    if word >> 24 != 0xEA:
        raise ValueError(f"expected unconditional ARM B at 0x{address:X}, got 0x{word:08X}")
    imm24 = word & 0x00FFFFFF
    if imm24 & 0x00800000:
        imm24 -= 1 << 24
    return address + 8 + (imm24 << 2)


def parse_extended_metadata(data: bytes) -> dict | None:
    if len(data) < EXTENDED_METADATA_END:
        return None
    block = data[EXTENDED_METADATA_START:EXTENDED_METADATA_END]
    if block[:0x30] != b"\xFF" * 0x30:
        return None

    game_version = u32(block, 0x30)
    language_id = u32(block, 0x34)
    raw_name = block[0x38:0x50]
    name = raw_name.rstrip(b"\x00").decode("ascii", errors="replace")
    pointers = {
        name_: u32(block, 0x58 + i * 4)
        for i, name_ in enumerate(POINTER_NAMES)
    }
    constants = [u32(block, off) for off in range(0x80, 0x130, 4)]

    return {
        "game_version": game_version,
        "language_id": language_id,
        "language": LANGUAGE_IDS.get(language_id, "unknown"),
        "name": name,
        "pointers": pointers,
        "constants": constants,
        "final_sentinel": u32(block, 0x130),
        "sha256": hashlib.sha256(block).hexdigest(),
    }


def analyze(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 0x400:
        raise ValueError("file is too small to be a GBA ROM")

    start_word = u32(data, 0)
    init_off = decode_arm_branch_target(start_word, 0)
    if u32(data, init_off) != EXPECTED_INIT_WORD:
        raise ValueError(
            f"entry target 0x{init_off:X} does not begin with expected Init word "
            f"0x{EXPECTED_INIT_WORD:08X}"
        )

    startup = data[init_off:init_off + STARTUP_SIZE]
    if len(startup) != STARTUP_SIZE:
        raise ValueError("truncated startup block")

    return {
        "path": path,
        "game_code": data[0xAC:0xB0].decode("ascii", errors="replace"),
        "software_version": data[0xBC],
        "init_offset": init_off,
        "init_address": ROM_BASE + init_off,
        "intr_vector_literal": u32(startup, 0x170),
        "agb_main_ptr": u32(startup, 0x174),
        "g_intr_table_ptr": u32(startup, 0x178),
        "startup_sha256": hashlib.sha256(startup).hexdigest(),
        "instruction_prefix_sha256": hashlib.sha256(startup[:0x170]).hexdigest(),
        "extended_metadata": parse_extended_metadata(data),
    }


def format_report(result: dict) -> str:
    lines = [
        f"file: {result['path'].name}",
        f"game_code: {result['game_code']}",
        f"software_version: {result['software_version']}",
        f"Init: file+0x{result['init_offset']:X} / 0x{result['init_address']:08X}",
        f"INTR_VECTOR literal: 0x{result['intr_vector_literal']:08X}",
        f"AgbMain pointer: 0x{result['agb_main_ptr']:08X}",
        f"gIntrTable pointer: 0x{result['g_intr_table_ptr']:08X}",
        f"startup[0x17C] sha256: {result['startup_sha256']}",
        f"startup instructions[0x170] sha256: {result['instruction_prefix_sha256']}",
    ]

    meta = result["extended_metadata"]
    if meta is None:
        lines.append("extended localization metadata @ 0xD0: absent")
    else:
        lines.extend([
            "extended localization metadata @ 0xD0: present",
            f"  game_version: {meta['game_version']}",
            f"  language_id: {meta['language_id']} ({meta['language']})",
            f"  identifier: {meta['name']!r}",
            f"  sha256: {meta['sha256']}",
        ])
        for key, value in meta["pointers"].items():
            lines.append(f"  {key}: 0x{value:08X}")
        lines.append(f"  final_sentinel: 0x{meta['final_sentinel']:08X}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze Pokémon Sapphire GBA startup/header-localization data."
    )
    parser.add_argument("rom", type=Path, nargs="+", help="one or more local ROM paths")
    args = parser.parse_args()

    for i, path in enumerate(args.rom):
        if i:
            print()
        print(format_report(analyze(path)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
