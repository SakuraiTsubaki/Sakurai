#!/usr/bin/env python3
"""Extract Generation V BW personal data for the Gen III adapter layer.

This tool does not contain ROM offsets. It walks the NDS NitroFS, locates
/a/0/1/6, parses the NARC, and writes locally generated build inputs.

Generated binaries are intentionally not committed to the repository.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
from pathlib import Path

PERSONAL_PATH = "a/0/1/6"
RECORD_SIZE = 0x3C
BASE_LAST_SPECIES = 649


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def walk_nitrofs(nds: bytes) -> dict[str, int]:
    fnt_offset = u32(nds, 0x40)
    fnt_size = u32(nds, 0x44)
    fnt = nds[fnt_offset : fnt_offset + fnt_size]
    files: dict[str, int] = {}

    def walk_dir(directory_id: int, prefix: str = "") -> None:
        index = directory_id - 0xF000
        table_offset = index * 8
        subtable_offset = u32(fnt, table_offset)
        file_id = u16(fnt, table_offset + 4)
        pos = subtable_offset

        while True:
            descriptor = fnt[pos]
            pos += 1
            if descriptor == 0:
                break

            is_directory = bool(descriptor & 0x80)
            name_length = descriptor & 0x7F
            name = fnt[pos : pos + name_length].decode("ascii")
            pos += name_length

            if is_directory:
                child_id = u16(fnt, pos)
                pos += 2
                walk_dir(child_id, prefix + name + "/")
            else:
                files[prefix + name] = file_id
                file_id += 1

    walk_dir(0xF000)
    return files


def read_nitrofs_file(nds: bytes, path: str) -> bytes:
    files = walk_nitrofs(nds)
    if path not in files:
        raise KeyError(f"NitroFS path not found: {path}")

    fat_offset = u32(nds, 0x48)
    file_id = files[path]
    start = u32(nds, fat_offset + file_id * 8)
    end = u32(nds, fat_offset + file_id * 8 + 4)
    return nds[start:end]


def parse_narc(narc: bytes) -> list[bytes]:
    if narc[:4] != b"NARC":
        raise ValueError("source file is not a NARC")

    chunks: dict[bytes, int] = {}
    pos = 0x10
    while pos + 8 <= len(narc):
        magic = narc[pos : pos + 4]
        size = u32(narc, pos + 4)
        if size < 8 or pos + size > len(narc):
            raise ValueError(f"invalid NARC chunk at 0x{pos:X}")
        chunks[magic] = pos
        pos += size

    if b"BTAF" not in chunks or b"GMIF" not in chunks:
        raise ValueError("NARC is missing BTAF or GMIF")

    btaf = chunks[b"BTAF"]
    gmif = chunks[b"GMIF"]
    count = u16(narc, btaf + 8)
    data_base = gmif + 8
    members: list[bytes] = []

    for index in range(count):
        rel_start = u32(narc, btaf + 0x0C + index * 8)
        rel_end = u32(narc, btaf + 0x10 + index * 8)
        members.append(narc[data_base + rel_start : data_base + rel_end])

    return members


def decode_record(species: int, record: bytes) -> dict[str, object]:
    if len(record) != RECORD_SIZE:
        raise ValueError(
            f"member {species} has size {len(record)}, expected {RECORD_SIZE}"
        )

    ev = u16(record, 0x0A)
    return {
        "species": species,
        "hp": record[0x00],
        "attack": record[0x01],
        "defense": record[0x02],
        "speed": record[0x03],
        "sp_attack": record[0x04],
        "sp_defense": record[0x05],
        "type1": record[0x06],
        "type2": record[0x07],
        "catch_rate": record[0x08],
        "ev_hp": (ev >> 0) & 3,
        "ev_attack": (ev >> 2) & 3,
        "ev_defense": (ev >> 4) & 3,
        "ev_speed": (ev >> 6) & 3,
        "ev_sp_attack": (ev >> 8) & 3,
        "ev_sp_defense": (ev >> 10) & 3,
        "held_item_1": u16(record, 0x0C),
        "held_item_2": u16(record, 0x0E),
        "held_item_3": u16(record, 0x10),
        "gender_ratio": record[0x12],
        "hatch_counter": record[0x13],
        "base_friendship": record[0x14],
        "growth_rate": record[0x15],
        "egg_group_1": record[0x16],
        "egg_group_2": record[0x17],
        "ability_1": record[0x18],
        "ability_2": record[0x19],
        "ability_hidden": record[0x1A],
        "escape_rate": record[0x1B],
        "form_stats_start": u16(record, 0x1C),
        "form_sprites_start": u16(record, 0x1E),
        "form_count": record[0x20],
        "body_color": record[0x21],
        "base_exp": u16(record, 0x22),
        "height": u16(record, 0x24),
        "weight": u16(record, 0x26),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path, help="Pokémon Black/White .nds")
    parser.add_argument("--out-dir", type=Path, default=Path("data/gen5"))
    parser.add_argument("--personal-path", default=PERSONAL_PATH)
    args = parser.parse_args()

    nds = args.rom.read_bytes()
    narc = read_nitrofs_file(nds, args.personal_path)
    members = parse_narc(narc)

    if len(members) <= BASE_LAST_SPECIES:
        raise ValueError(
            f"personal NARC has {len(members)} members; need at least {BASE_LAST_SPECIES + 1}"
        )

    for index, member in enumerate(members):
        if len(member) != RECORD_SIZE:
            raise ValueError(
                f"personal member {index} has size {len(member)}, expected {RECORD_SIZE}"
            )

    args.out_dir.mkdir(parents=True, exist_ok=True)

    base_bin = args.out_dir / "personal_bw_base_000_649.bin"
    all_bin = args.out_dir / "personal_bw_all_members.bin"
    csv_path = args.out_dir / "personal_bw_base_000_649.csv"
    manifest_path = args.out_dir / "personal_bw_manifest.json"

    base_data = b"".join(members[: BASE_LAST_SPECIES + 1])
    all_data = b"".join(members)
    base_bin.write_bytes(base_data)
    all_bin.write_bytes(all_data)

    rows = [decode_record(i, members[i]) for i in range(BASE_LAST_SPECIES + 1)]
    with csv_path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    manifest = {
        "rom_file": args.rom.name,
        "rom_sha1": hashlib.sha1(nds).hexdigest(),
        "personal_path": args.personal_path,
        "member_count": len(members),
        "record_size": RECORD_SIZE,
        "base_species_first": 0,
        "base_species_last": BASE_LAST_SPECIES,
        "base_binary_size": len(base_data),
        "all_binary_size": len(all_data),
        "base_binary_sha1": hashlib.sha1(base_data).hexdigest(),
        "all_binary_sha1": hashlib.sha1(all_data).hexdigest(),
        "note": "Members above 649 are preserved in all_members for separate form routing; do not discard them.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
