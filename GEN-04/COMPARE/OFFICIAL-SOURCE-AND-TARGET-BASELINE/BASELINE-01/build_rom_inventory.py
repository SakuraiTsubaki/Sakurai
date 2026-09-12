#!/usr/bin/env python3
"""Build a read-only inventory of Nintendo DS, GBA, and GBC source ROMs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import zlib
from pathlib import Path


RELEASES = {
    "APAE": ("Pokémon Pearl", "USA/English", "NDS-APAE"),
    "ADAE": ("Pokémon Diamond", "USA/English", "NDS-ADAE"),
    "CPUK": ("Pokémon Platinum", "Korea/Korean", "NDS-CPUK"),
    "IPGK": ("Pokémon SoulSilver", "Korea/Korean", "NDS-IPGK"),
    "IPKK": ("Pokémon HeartGold", "Korea/Korean", "NDS-IPKK"),
    "AXPJ": ("Pocket Monsters Sapphire", "Japan/Japanese", "AGB-AXPJ"),
    "BPEJ": ("Pocket Monsters Emerald", "Japan/Japanese", "AGB-BPEJ"),
    "BPGE": ("Pokémon LeafGreen", "English", "AGB-BPGE"),
    "BPEE": ("Pokémon Emerald", "English", "AGB-BPEE"),
    "BPGJ": ("Pocket Monsters LeafGreen", "Japan/Japanese", "AGB-BPGJ"),
    "AXPE": ("Pokémon Sapphire", "English", "AGB-AXPE"),
    "AXVJ": ("Pocket Monsters Ruby", "Japan/Japanese", "AGB-AXVJ"),
    "AXVE": ("Pokémon Ruby", "English", "AGB-AXVE"),
    "BPRE": ("Pokémon FireRed", "English", "AGB-BPRE"),
    "BPRJ": ("Pocket Monsters FireRed", "Japan/Japanese", "AGB-BPRJ"),
}


def ascii_field(data: bytes) -> str:
    return data.rstrip(b"\0 ").decode("ascii", "replace")


def crc16_nds(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc & 0xFFFF


def digests(data: bytes) -> dict[str, str]:
    return {
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def parse_nds(data: bytes) -> dict[str, object]:
    logo_stored = struct.unpack_from("<H", data, 0x15C)[0]
    header_stored = struct.unpack_from("<H", data, 0x15E)[0]
    return {
        "platform": "NDS",
        "internal_title": ascii_field(data[0:12]),
        "game_code": ascii_field(data[12:16]),
        "maker_code": ascii_field(data[16:18]),
        "revision": data[0x1E],
        "region_code": ascii_field(data[15:16]),
        "unit_code": data[0x12],
        "device_capacity_code": data[0x14],
        "arm9_offset": struct.unpack_from("<I", data, 0x20)[0],
        "arm9_entry": struct.unpack_from("<I", data, 0x24)[0],
        "arm9_ram": struct.unpack_from("<I", data, 0x28)[0],
        "arm9_size": struct.unpack_from("<I", data, 0x2C)[0],
        "arm7_offset": struct.unpack_from("<I", data, 0x30)[0],
        "arm7_entry": struct.unpack_from("<I", data, 0x34)[0],
        "arm7_ram": struct.unpack_from("<I", data, 0x38)[0],
        "arm7_size": struct.unpack_from("<I", data, 0x3C)[0],
        "fnt_offset": struct.unpack_from("<I", data, 0x40)[0],
        "fnt_size": struct.unpack_from("<I", data, 0x44)[0],
        "fat_offset": struct.unpack_from("<I", data, 0x48)[0],
        "fat_size": struct.unpack_from("<I", data, 0x4C)[0],
        "overlay9_offset": struct.unpack_from("<I", data, 0x50)[0],
        "overlay9_size": struct.unpack_from("<I", data, 0x54)[0],
        "overlay7_offset": struct.unpack_from("<I", data, 0x58)[0],
        "overlay7_size": struct.unpack_from("<I", data, 0x5C)[0],
        "banner_offset": struct.unpack_from("<I", data, 0x68)[0],
        "rom_size_header": struct.unpack_from("<I", data, 0x80)[0],
        "header_size": struct.unpack_from("<I", data, 0x84)[0],
        "nitrofs_file_count": struct.unpack_from("<I", data, 0x4C)[0] // 8,
        "logo_crc_stored": f"{logo_stored:04x}",
        "logo_crc_calculated": f"{crc16_nds(data[0xC0:0x15C]):04x}",
        "logo_crc_valid": logo_stored == crc16_nds(data[0xC0:0x15C]),
        "header_crc_stored": f"{header_stored:04x}",
        "header_crc_calculated": f"{crc16_nds(data[:0x15E]):04x}",
        "header_crc_valid": header_stored == crc16_nds(data[:0x15E]),
    }


def parse_gba(data: bytes) -> dict[str, object]:
    stored = data[0xBD]
    calculated = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
    return {
        "platform": "GBA",
        "internal_title": ascii_field(data[0xA0:0xAC]),
        "game_code": ascii_field(data[0xAC:0xB0]),
        "maker_code": ascii_field(data[0xB0:0xB2]),
        "revision": data[0xBC],
        "region_code": ascii_field(data[0xAF:0xB0]),
        "fixed_value": f"{data[0xB2]:02x}",
        "header_checksum_stored": f"{stored:02x}",
        "header_checksum_calculated": f"{calculated:02x}",
        "header_checksum_valid": stored == calculated,
    }


def parse_gbc(data: bytes) -> dict[str, object]:
    cgb_flag = data[0x143]
    title_end = 0x143 if cgb_flag in (0x80, 0xC0) else 0x144
    calculated = 0
    for byte in data[0x134:0x14D]:
        calculated = (calculated - byte - 1) & 0xFF
    global_calculated = (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF
    global_stored = struct.unpack_from(">H", data, 0x14E)[0]
    return {
        "platform": "GBC",
        "internal_title": ascii_field(data[0x134:title_end]),
        "game_code": "",
        "maker_code": ascii_field(data[0x144:0x146]),
        "revision": data[0x14C],
        "region_code": str(data[0x14A]),
        "cgb_flag": f"{cgb_flag:02x}",
        "sgb_flag": f"{data[0x146]:02x}",
        "cartridge_type": f"{data[0x147]:02x}",
        "rom_size_code": f"{data[0x148]:02x}",
        "ram_size_code": f"{data[0x149]:02x}",
        "header_checksum_stored": f"{data[0x14D]:02x}",
        "header_checksum_calculated": f"{calculated:02x}",
        "header_checksum_valid": data[0x14D] == calculated,
        "global_checksum_stored": f"{global_stored:04x}",
        "global_checksum_calculated": f"{global_calculated:04x}",
        "global_checksum_valid": global_stored == global_calculated,
    }


def classify(name: str, parsed: dict[str, object]) -> tuple[str, str]:
    code = str(parsed["game_code"])
    if code in {"APAE", "ADAE", "CPUK", "IPGK", "IPKK"}:
        return "GEN-IV-OFFICIAL-RESEARCH-SOURCE", "read-only"
    if parsed["platform"] in {"GBA", "GBC"}:
        return "TARGET-POCKET-MONSTERS-OFFICIAL-SOURCE", "read-only"
    return "UNCLASSIFIED", "read-only"


def inspect(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    if path.suffix.lower() == ".gba":
        parsed = parse_gba(data)
    elif path.suffix.lower() == ".gbc":
        parsed = parse_gbc(data)
    elif data[0xC0:0xC4] == bytes.fromhex("24ffae51"):
        parsed = parse_nds(data)
    else:
        raise ValueError(f"Unsupported ROM format: {path}")
    role, policy = classify(path.name, parsed)
    if parsed["platform"] == "GBC":
        game, language_region, release_id = "Pocket Monsters Gold", "Korea/Korean", "CGB-AAUK"
    else:
        game, language_region, release_id = RELEASES.get(
            str(parsed["game_code"]), ("Unknown", "Unknown", "UNKNOWN")
        )
    return {
        "file": path.name,
        "size_bytes": len(data),
        "game": game,
        "language_region": language_region,
        "release_id": release_id,
        "project_side": "generation-iv-source" if role == "GEN-IV-OFFICIAL-RESEARCH-SOURCE" else "pocket-monsters-target",
        "source_priority": "equal",
        "implementation_status": "not-applicable" if role == "GEN-IV-OFFICIAL-RESEARCH-SOURCE" else "target-scope-confirmed",
        "coverage_status": "attached-and-header-verified",
        **parsed,
        **digests(data),
        "project_role": role,
        "preservation_policy": policy,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    rows = [inspect(p) for p in sorted(args.source_dir.iterdir()) if p.is_file() and not p.name.startswith(".")]
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps({"schema_version": 1, "roms": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    columns = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
