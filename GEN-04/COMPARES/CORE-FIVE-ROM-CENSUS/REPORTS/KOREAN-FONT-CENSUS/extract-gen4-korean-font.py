#!/usr/bin/env python3
"""Extract mapped Korean Generation IV font glyphs from a retail NDS ROM.

The output source pack contains only mapped glyph resources, metadata and
hashes. The ROM itself is never copied into the repository.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import struct
from pathlib import Path

WANSUNG_START_SLOT = 1024
WANSUNG_COUNT = 2350
JAMO_START_SLOT = 3376
JAMO_COUNT = 51
PRINCIPAL_MEMBERS = (0, 1, 2, 4, 10)


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def parse_fnt_paths(rom: bytes):
    fnt_off = u32(rom, 0x40)
    fnt_size = u32(rom, 0x44)
    fat_off = u32(rom, 0x48)
    fat_size = u32(rom, 0x4C)
    fnt = rom[fnt_off:fnt_off + fnt_size]

    # In the root directory-table entry, parentId stores the directory count.
    dir_count = u16(fnt, 6)
    dirs = []
    for i in range(dir_count):
        off = i * 8
        dirs.append((u32(fnt, off), u16(fnt, off + 4), u16(fnt, off + 6)))

    paths = {}

    def walk(dir_id: int, prefix: str):
        sub_off, first_id, _ = dirs[dir_id - 0xF000]
        pos = sub_off
        file_id = first_id
        while True:
            n = fnt[pos]
            pos += 1
            if n == 0:
                break
            is_dir = bool(n & 0x80)
            name_len = n & 0x7F
            name = fnt[pos:pos + name_len].decode("ascii")
            pos += name_len
            if is_dir:
                child = u16(fnt, pos)
                pos += 2
                walk(child, prefix + name + "/")
            else:
                paths[prefix + name] = file_id
                file_id += 1

    walk(0xF000, "")

    fat = []
    for i in range(fat_size // 8):
        fat.append((u32(rom, fat_off + i * 8), u32(rom, fat_off + i * 8 + 4)))
    return paths, fat


def parse_narc(data: bytes):
    if data[:4] != b"NARC":
        raise ValueError("not a NARC archive")

    header_size = u16(data, 0x0C)
    block_count = u16(data, 0x0E)
    pos = header_size
    btaf = None
    gmif = None
    for _ in range(block_count):
        magic = data[pos:pos + 4]
        size = u32(data, pos + 4)
        if magic in (b"BTAF", b"FATB"):
            btaf = (pos, size)
        elif magic in (b"GMIF", b"FIMG"):
            gmif = (pos, size)
        pos += size

    if btaf is None or gmif is None:
        raise ValueError("NARC FAT or image block missing")

    fat_pos, _ = btaf
    count = u16(data, fat_pos + 8)
    entries = []
    for i in range(count):
        entries.append((
            u32(data, fat_pos + 12 + i * 8),
            u32(data, fat_pos + 16 + i * 8),
        ))

    image_pos, _ = gmif
    base = image_pos + 8
    return [data[base + start:base + end] for start, end in entries]


def wansung_chars():
    chars = []
    for lead in range(0xB0, 0xC9):
        for trail in range(0xA1, 0xFF):
            try:
                ch = bytes((lead, trail)).decode("euc_kr")
            except UnicodeDecodeError:
                continue
            if len(ch) == 1 and 0xAC00 <= ord(ch) <= 0xD7A3:
                chars.append(ch)
    if len(chars) != WANSUNG_COUNT:
        raise AssertionError(len(chars))
    return chars


def compat_jamo_chars():
    chars = []
    for trail in range(0xA1, 0xD4):
        chars.append(bytes((0xA4, trail)).decode("euc_kr"))
    if len(chars) != JAMO_COUNT:
        raise AssertionError(len(chars))
    return chars


def decode_tile_2bpp(tile: bytes):
    if len(tile) != 16:
        raise ValueError("tile must be 16 bytes")
    pixels = [[0] * 8 for _ in range(8)]
    for y in range(8):
        x = 0
        for value in (tile[2 * y + 1], tile[2 * y]):
            for shift in (6, 4, 2, 0):
                pixels[y][x] = (value >> shift) & 3
                x += 1
    return pixels


def decode_glyph(raw: bytes):
    if len(raw) != 64:
        raise ValueError("16x16 glyph must be 64 bytes")
    pixels = [[0] * 16 for _ in range(16)]
    for tile_index, (ox, oy) in enumerate(((0, 0), (8, 0), (0, 8), (8, 8))):
        tile = decode_tile_2bpp(raw[tile_index * 16:(tile_index + 1) * 16])
        for y in range(8):
            for x in range(8):
                pixels[oy + y][ox + x] = tile[y][x]
    return pixels


def ink_bbox(pixels):
    # 1=foreground and 2=shadow are visible glyph ink. 0 is zero/transparent
    # and 3 is explicit background in the Generation IV renderer.
    xs = []
    ys = []
    for y, row in enumerate(pixels):
        for x, value in enumerate(row):
            if value in (1, 2):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return [min(xs), min(ys), max(xs) + 1, max(ys) + 1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("nds")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--archive", default="a/0/1/6")
    ap.add_argument("--members", type=int, nargs="+", default=list(PRINCIPAL_MEMBERS))
    args = ap.parse_args()

    rom = Path(args.nds).read_bytes()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    paths, fat = parse_fnt_paths(rom)
    if args.archive not in paths:
        raise SystemExit(f"archive not found: {args.archive}")

    file_id = paths[args.archive]
    start, end = fat[file_id]
    narc = rom[start:end]
    members = parse_narc(narc)

    mapping = []
    for i, ch in enumerate(wansung_chars()):
        mapping.append({
            "char": ch,
            "codepoint": f"U+{ord(ch):04X}",
            "slot": WANSUNG_START_SLOT + i,
            "message_code": WANSUNG_START_SLOT + i + 1,
            "class": "ks_x_1001_wansung",
        })
    for i, ch in enumerate(compat_jamo_chars()):
        mapping.append({
            "char": ch,
            "codepoint": f"U+{ord(ch):04X}",
            "slot": JAMO_START_SLOT + i,
            "message_code": JAMO_START_SLOT + i + 1,
            "class": "ks_x_1001_compatibility_jamo",
        })

    mapping_json = json.dumps(mapping, ensure_ascii=False, indent=2).encode("utf-8")
    mapping_name = "mapping.json.gz"
    (out / mapping_name).write_bytes(gzip.compress(mapping_json, compresslevel=9, mtime=0))
    with (out / "mapping.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["char", "codepoint", "slot", "message_code", "class"]
        )
        writer.writeheader()
        writer.writerows(mapping)

    manifest = {
        "schema": "gen4-korean-font-source-pack.v1",
        "source_rom": {
            "game_code": rom[0x0C:0x10].decode("ascii"),
            "revision": rom[0x1E],
            "sha256": hashlib.sha256(rom).hexdigest(),
        },
        "archive": args.archive,
        "archive_file_id": file_id,
        "archive_sha256": hashlib.sha256(narc).hexdigest(),
        "glyph_format": "nds_font_16x16_2bpp_4tiles_64bytes",
        "mapping_file": mapping_name,
        "mapping_file_encoding": "gzip",
        "mapped_glyph_count": len(mapping),
        "unresolved_slots_excluded": [3427, 3428],
        "members": [],
    }

    slots = (
        list(range(WANSUNG_START_SLOT, WANSUNG_START_SLOT + WANSUNG_COUNT))
        + list(range(JAMO_START_SLOT, JAMO_START_SLOT + JAMO_COUNT))
    )

    for member_id in args.members:
        member = members[member_id]
        header_size = u32(member, 0)
        width_start = u32(member, 4)
        num_glyphs = u32(member, 8)
        fixed_width, fixed_height, glyph_width, glyph_height = member[12:16]

        expected = (16, 0x35C10, 3440, 2, 2)
        actual = (header_size, width_start, num_glyphs, glyph_width, glyph_height)
        if actual != expected:
            raise AssertionError((member_id, actual, expected))

        raw = bytearray()
        bboxes = []
        for slot in slots:
            offset = header_size + slot * 64
            glyph = member[offset:offset + 64]
            if len(glyph) != 64:
                raise AssertionError((member_id, slot, len(glyph)))
            raw += glyph
            bboxes.append(ink_bbox(decode_glyph(glyph)))

        raw_bytes = bytes(raw)
        file_name = f"member_{member_id:02d}_official_2bpp.bin.gz"
        compressed = gzip.compress(raw_bytes, compresslevel=9, mtime=0)
        (out / file_name).write_bytes(compressed)
        wansung_boxes = [b for b in bboxes[:WANSUNG_COUNT] if b]
        manifest["members"].append({
            "member": member_id,
            "member_size": len(member),
            "member_sha256": hashlib.sha256(member).hexdigest(),
            "source_file": file_name,
            "source_file_encoding": "gzip",
            "source_file_sha256": hashlib.sha256(compressed).hexdigest(),
            "source_raw_sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "source_raw_size": len(raw_bytes),
            "glyph_count": len(mapping),
            "bytes_per_glyph": 64,
            "header": {
                "header_size": header_size,
                "width_data_start": width_start,
                "num_glyphs": num_glyphs,
                "fixed_width": fixed_width,
                "fixed_height": fixed_height,
                "glyph_width_tiles": glyph_width,
                "glyph_height_tiles": glyph_height,
            },
            "wansung_ink_bbox_union": [
                min(b[0] for b in wansung_boxes),
                min(b[1] for b in wansung_boxes),
                max(b[2] for b in wansung_boxes),
                max(b[3] for b in wansung_boxes),
            ],
        })

    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
