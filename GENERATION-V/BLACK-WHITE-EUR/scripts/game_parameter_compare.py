#!/usr/bin/env python3
"""Compare core Pokémon Black/White (BW1) parameter NARCs member-by-member.

Usage:
    python game_parameter_compare.py BLACK.nds WHITE.nds > game_parameter_bw_compare.json

This script is read-only. It parses NitroFS FNT/FAT directly, then extracts selected
NARC members without external packages.
"""
from __future__ import annotations
import argparse, json, struct
from pathlib import Path

PARAMETERS = [
    ("personal", "a/0/1/6"),
    ("growth", "a/0/1/7"),
    ("level_up_moves", "a/0/1/8"),
    ("evolutions", "a/0/1/9"),
    ("baby_base", "a/0/2/0"),
    ("move_data", "a/0/2/1"),
    ("item_data", "a/0/2/4"),
    ("trainer_meta", "a/0/9/2"),
    ("trainer_party", "a/0/9/3"),
    ("egg_moves", "a/1/2/3"),
    ("encounters", "a/1/2/6"),
    ("zone_data", "a/0/1/2"),
    ("field_scripts", "a/0/5/7"),
    ("overworlds", "a/1/2/5"),
    ("main_text", "a/0/0/2"),
    ("story_text", "a/0/0/3"),
]

def u16(b: bytes, o: int) -> int:
    return struct.unpack_from("<H", b, o)[0]

def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]

def nitrofs_index(rom: Path) -> dict[str, tuple[int, int]]:
    with rom.open("rb") as f:
        header = f.read(0x200)
        fnt_off, fnt_size = u32(header, 0x40), u32(header, 0x44)
        fat_off, fat_size = u32(header, 0x48), u32(header, 0x4C)
        f.seek(fnt_off); fnt = f.read(fnt_size)
        f.seek(fat_off); fat = f.read(fat_size)

    fat_entries = [struct.unpack_from("<II", fat, i) for i in range(0, len(fat), 8)]
    dir_count = u16(fnt, 6)
    dirs = {
        0xF000 + i: (u32(fnt, i * 8), u16(fnt, i * 8 + 4), u16(fnt, i * 8 + 6))
        for i in range(dir_count)
    }
    id_to_path: dict[int, str] = {}

    def walk(dir_id: int, prefix: str) -> None:
        sub_off, first_file_id, _parent = dirs[dir_id]
        pos, file_id = sub_off, first_file_id
        while True:
            token = fnt[pos]; pos += 1
            if token == 0:
                return
            is_dir, name_len = bool(token & 0x80), token & 0x7F
            name = fnt[pos:pos + name_len].decode("ascii")
            pos += name_len
            if is_dir:
                child = u16(fnt, pos); pos += 2
                walk(child, prefix + name + "/")
            else:
                id_to_path[file_id] = prefix + name
                file_id += 1

    walk(0xF000, "")
    return {id_to_path[i]: fat_entries[i] for i in id_to_path}

def read_nitro_file(rom: Path, index: dict[str, tuple[int, int]], path: str) -> bytes:
    start, end = index[path]
    with rom.open("rb") as f:
        f.seek(start)
        return f.read(end - start)

def narc_members(blob: bytes) -> list[bytes]:
    if blob[:4] != b"NARC":
        raise ValueError("not a NARC archive")
    pos = u16(blob, 0x0C)
    chunks: dict[bytes, bytes] = {}
    for _ in range(u16(blob, 0x0E)):
        tag = blob[pos:pos + 4]
        size = u32(blob, pos + 4)
        chunks[tag] = blob[pos:pos + size]
        pos += size
    fat, img = chunks[b"BTAF"], chunks[b"GMIF"]
    count = u16(fat, 8)
    data = img[8:]
    bounds = [struct.unpack_from("<II", fat, 12 + i * 8) for i in range(count)]
    return [data[start:end] for start, end in bounds]

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("black", type=Path)
    ap.add_argument("white", type=Path)
    args = ap.parse_args()

    b_index, w_index = nitrofs_index(args.black), nitrofs_index(args.white)
    result = []
    for role, path in PARAMETERS:
        b_blob = read_nitro_file(args.black, b_index, path)
        w_blob = read_nitro_file(args.white, w_index, path)
        b_mem, w_mem = narc_members(b_blob), narc_members(w_blob)
        diffs = [i for i, (b, w) in enumerate(zip(b_mem, w_mem)) if b != w]
        result.append({
            "role": role,
            "path": path,
            "black_archive_bytes": len(b_blob),
            "white_archive_bytes": len(w_blob),
            "black_members": len(b_mem),
            "white_members": len(w_mem),
            "archive_identical": b_blob == w_blob,
            "differing_member_count": len(diffs),
            "differing_members": diffs,
            "black_member_size_min": min(map(len, b_mem)) if b_mem else 0,
            "black_member_size_max": max(map(len, b_mem)) if b_mem else 0,
            "black_member_payload_bytes": sum(map(len, b_mem)),
        })
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
