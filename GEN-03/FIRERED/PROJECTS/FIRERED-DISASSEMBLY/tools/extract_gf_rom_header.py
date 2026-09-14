#!/usr/bin/env python3
"""Decode the 0x104-byte Game Freak compatibility header at ROM offset 0x100.

The field layout is validated against the eight FireRed baselines in this
project. This tool is read-only and never modifies the ROM.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

GF_HEADER_OFFSET = 0x100
GF_HEADER_SIZE = 0x104

FIELDS = [
    ("version", 0x000, "u32"),
    ("language", 0x004, "u32"),
    ("game_name", 0x008, "str32"),
    ("mon_front_pics", 0x028, "ptr"),
    ("mon_back_pics", 0x02C, "ptr"),
    ("mon_normal_palettes", 0x030, "ptr"),
    ("mon_shiny_palettes", 0x034, "ptr"),
    ("mon_icons", 0x038, "ptr"),
    ("mon_icon_palette_ids", 0x03C, "ptr"),
    ("mon_icon_palettes", 0x040, "ptr"),
    ("mon_species_names", 0x044, "ptr"),
    ("move_names", 0x048, "ptr"),
    ("decorations", 0x04C, "ptr"),
    ("flags_offset", 0x050, "u32"),
    ("vars_offset", 0x054, "u32"),
    ("pokedex_offset", 0x058, "u32"),
    ("seen1_offset", 0x05C, "u32"),
    ("seen2_offset", 0x060, "u32"),
    ("pokedex_var", 0x064, "u32"),
    ("pokedex_flag", 0x068, "u32"),
    ("mystery_gift_flag", 0x06C, "u32"),
    ("pokedex_count", 0x070, "u32"),
    ("player_name_length", 0x074, "u8"),
    ("field_075", 0x075, "u8"),
    ("pokemon_name_length_1", 0x076, "u8"),
    ("pokemon_name_length_2", 0x077, "u8"),
    ("field_078", 0x078, "u8"),
    ("field_079", 0x079, "u8"),
    ("field_07A", 0x07A, "u8"),
    ("field_07B", 0x07B, "u8"),
    ("field_07C", 0x07C, "u8"),
    ("field_07D", 0x07D, "u8"),
    ("field_07E", 0x07E, "u8"),
    ("field_07F", 0x07F, "u8"),
    ("field_080", 0x080, "u8"),
    ("field_081", 0x081, "u8"),
    ("field_082", 0x082, "u8"),
    ("field_083", 0x083, "u8"),
    ("field_084", 0x084, "u8"),
    ("save_block_2_size", 0x088, "u32"),
    ("save_block_1_size", 0x08C, "u32"),
    ("party_count_offset", 0x090, "u32"),
    ("party_offset", 0x094, "u32"),
    ("warp_flags_offset", 0x098, "u32"),
    ("trainer_id_offset", 0x09C, "u32"),
    ("player_name_offset", 0x0A0, "u32"),
    ("player_gender_offset", 0x0A4, "u32"),
    ("field_0A8", 0x0A8, "u32"),
    ("field_0AC", 0x0AC, "u32"),
    ("external_event_flags_offset", 0x0B0, "u32"),
    ("external_event_data_offset", 0x0B4, "u32"),
    ("field_0B8", 0x0B8, "u32"),
    ("species_info", 0x0BC, "ptr"),
    ("ability_names", 0x0C0, "ptr"),
    ("ability_descriptions", 0x0C4, "ptr"),
    ("items", 0x0C8, "ptr"),
    ("moves", 0x0CC, "ptr"),
    ("ball_gfx", 0x0D0, "ptr"),
    ("ball_palettes", 0x0D4, "ptr"),
    ("gcn_link_flags_offset", 0x0D8, "u32"),
    ("game_clear_flag", 0x0DC, "u32"),
    ("ribbon_flag", 0x0E0, "u32"),
    ("bag_count_items", 0x0E4, "u8"),
    ("bag_count_key_items", 0x0E5, "u8"),
    ("bag_count_pokeballs", 0x0E6, "u8"),
    ("bag_count_tmhms", 0x0E7, "u8"),
    ("bag_count_berries", 0x0E8, "u8"),
    ("pc_items_count", 0x0E9, "u8"),
    ("pc_items_offset", 0x0EC, "u32"),
    ("gift_ribbons_offset", 0x0F0, "u32"),
    ("enigma_berry_offset", 0x0F4, "u32"),
    ("enigma_berry_size", 0x0F8, "u32"),
    ("move_descriptions", 0x0FC, "ptr"),
    ("field_100", 0x100, "u32"),
]


def read_value(blob: bytes, off: int, kind: str):
    p = GF_HEADER_OFFSET + off
    if kind == "u8":
        return blob[p]
    if kind in ("u32", "ptr"):
        return int.from_bytes(blob[p:p + 4], "little")
    if kind == "str32":
        raw = blob[p:p + 32]
        return raw.split(b"\0", 1)[0].decode("ascii", "replace")
    raise ValueError(kind)


def decode(path: Path) -> dict:
    blob = path.read_bytes()
    if len(blob) < GF_HEADER_OFFSET + GF_HEADER_SIZE:
        raise ValueError(f"{path}: too small")
    return {name: read_value(blob, off, kind) for name, off, kind in FIELDS}


def fmt(name: str, value):
    kind = next(kind for field, _, kind in FIELDS if field == name)
    if kind in ("ptr", "u32"):
        return f"0x{value:08X}"
    return value


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path, help="JSON mapping baseline id -> ROM path")
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    decoded = {name: decode(Path(path)) for name, path in manifest.items()}

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(decoded, indent=2) + "\n", encoding="utf-8")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            names = list(manifest)
            w.writerow(["field", "offset", *names])
            for field, off, _ in FIELDS:
                w.writerow([field, f"0x{off:03X}", *[fmt(field, decoded[name][field]) for name in names]])

    if not args.csv and not args.json:
        print(json.dumps(decoded, indent=2))


if __name__ == "__main__":
    main()
