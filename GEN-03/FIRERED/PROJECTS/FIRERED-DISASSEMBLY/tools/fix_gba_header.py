#!/usr/bin/env python3
"""Populate the standard GBA header without requiring a base ROM.

The fixed Nintendo logo bytes are part of the GBA cartridge header format.
Version-specific title/game-code/maker/version values come from config/versions.json.
The complement checksum at 0xBD is regenerated according to the GBA header rule.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

NINTENDO_LOGO = bytes.fromhex(
    "24ffae51699aa2213d84820a84e409ad11248b98c0817f21a352be199309ce20"
    "10464a4af82731ec58c7e83382e3cebf85f4df94ce4b09c194568ac01372a7fc"
    "9f844d73a3ca9a615897a327fc039876231dc7610304ae56bf38840040a70efd"
    "ff52fe036f9530f197fbc08560d68025a963be03014e38e2f9a234ffbb3e0344"
    "780090cb88113a9465c07c6387f03cafd625e48b380aac7221d4f807"
)


def fix_header(data: bytearray, title: str, game_code: str, maker: str, version: int) -> None:
    if len(data) < 0xC0:
        raise ValueError("file too small for a GBA header")

    title_bytes = title.encode("ascii")
    game_code_bytes = game_code.encode("ascii")
    maker_bytes = maker.encode("ascii")

    if len(title_bytes) != 12:
        raise ValueError("title must be exactly 12 ASCII bytes")
    if len(game_code_bytes) != 4:
        raise ValueError("game code must be exactly 4 ASCII bytes")
    if len(maker_bytes) != 2:
        raise ValueError("maker code must be exactly 2 ASCII bytes")

    data[0x04:0xA0] = NINTENDO_LOGO
    data[0xA0:0xAC] = title_bytes
    data[0xAC:0xB0] = game_code_bytes
    data[0xB0:0xB2] = maker_bytes
    data[0xB2] = 0x96
    data[0xB3] = 0
    data[0xB4] = 0
    data[0xB5:0xBC] = b"\0" * 7
    data[0xBC] = version & 0xFF
    data[0xBD] = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
    data[0xBE:0xC0] = b"\0\0"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path, help="linked ROM image to fix")
    ap.add_argument("--config", type=Path, default=Path("config/versions.json"))
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))[args.baseline]
    data = bytearray(args.rom.read_bytes())
    fix_header(
        data,
        config["title"],
        config["game_code"],
        config["maker_code"],
        config["software_version"],
    )

    output = args.output or args.rom
    output.write_bytes(data)


if __name__ == "__main__":
    main()
