#!/usr/bin/env python3
"""Inventory Pokémon BW battle-sprite archive /a/0/0/4.

This script intentionally does not require committing a ROM. Give it a local,
read-only Pokémon Black/White NDS image and it emits reproducible provenance
and per-member inventory data suitable for Sakurai BATTLE_MASTER_V1 analysis.

It parses the Nintendo DS FNT/FAT directly, extracts the NARC in memory, hashes
all members, decodes valid LZ10/LZ11 members, classifies Nitro resources, and
records NCGR canvas dimensions. It never modifies the input ROM.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path


def u16(buf: bytes, off: int) -> int:
    return struct.unpack_from("<H", buf, off)[0]


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_nds_filesystem(rom: bytes) -> dict[str, tuple[int, int, int]]:
    fnt_off, fnt_size = u32(rom, 0x40), u32(rom, 0x44)
    fat_off, fat_size = u32(rom, 0x48), u32(rom, 0x4C)
    fnt = rom[fnt_off : fnt_off + fnt_size]
    fat = rom[fat_off : fat_off + fat_size]

    dir_count = u16(fnt, 6)
    dirs = []
    for i in range(dir_count):
        off = i * 8
        dirs.append((u32(fnt, off), u16(fnt, off + 4), u16(fnt, off + 6)))

    files: dict[str, tuple[int, int, int]] = {}

    def walk(dir_id: int, prefix: str) -> None:
        sub_off, first_file_id, _parent = dirs[dir_id - 0xF000]
        pos = sub_off
        file_id = first_file_id
        while True:
            tag = fnt[pos]
            pos += 1
            if tag == 0:
                return
            is_dir = bool(tag & 0x80)
            name_len = tag & 0x7F
            name = fnt[pos : pos + name_len].decode("ascii", "replace")
            pos += name_len
            if is_dir:
                child = u16(fnt, pos)
                pos += 2
                walk(child, prefix + name + "/")
            else:
                start = u32(fat, file_id * 8)
                end = u32(fat, file_id * 8 + 4)
                files[prefix + name] = (file_id, start, end)
                file_id += 1

    walk(0xF000, "")
    return files


def parse_narc_members(narc: bytes) -> list[bytes]:
    if narc[:4] != b"NARC":
        raise ValueError("target is not a NARC")

    fat_block = None
    image_block = None
    pos = 0x10
    while pos + 8 <= len(narc):
        sig = narc[pos : pos + 4]
        size = u32(narc, pos + 4)
        if size < 8:
            raise ValueError(f"invalid NARC section size {size} at 0x{pos:X}")
        if sig in (b"BTAF", b"FATB"):
            fat_block = pos
        elif sig in (b"GMIF", b"FIMG"):
            image_block = pos
        pos += size

    if fat_block is None or image_block is None:
        raise ValueError("NARC FAT/image section not found")

    count = u16(narc, fat_block + 8)
    base = image_block + 8
    members = []
    for i in range(count):
        start = u32(narc, fat_block + 12 + i * 8)
        end = u32(narc, fat_block + 16 + i * 8)
        members.append(narc[base + start : base + end])
    return members


def decompress_lz10(src: bytes) -> bytes:
    if not src or src[0] != 0x10:
        return src
    out_size = src[1] | (src[2] << 8) | (src[3] << 16)
    pos = 4
    out = bytearray()
    while len(out) < out_size:
        flags = src[pos]
        pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= out_size:
                break
            if not ((flags >> bit) & 1):
                out.append(src[pos])
                pos += 1
            else:
                b1, b2 = src[pos], src[pos + 1]
                pos += 2
                length = (b1 >> 4) + 3
                disp = (((b1 & 0x0F) << 8) | b2) + 1
                if disp > len(out):
                    raise ValueError("invalid LZ10 back-reference")
                for _ in range(length):
                    out.append(out[-disp])
                    if len(out) >= out_size:
                        break
    return bytes(out)


def decompress_lz11(src: bytes) -> bytes:
    if not src or src[0] != 0x11:
        return src

    out_size = src[1] | (src[2] << 8) | (src[3] << 16)
    pos = 4
    if out_size == 0:
        out_size = int.from_bytes(src[4:8], "little")
        pos = 8

    out = bytearray()
    while len(out) < out_size:
        flags = src[pos]
        pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= out_size:
                break
            if not ((flags >> bit) & 1):
                out.append(src[pos])
                pos += 1
                continue

            b1, b2 = src[pos], src[pos + 1]
            pos += 2
            hi = b1 >> 4
            if hi == 0:
                b3 = src[pos]
                pos += 1
                length = (((b1 & 0x0F) << 4) | (b2 >> 4)) + 0x11
                disp = (((b2 & 0x0F) << 8) | b3) + 1
            elif hi == 1:
                b3, b4 = src[pos], src[pos + 1]
                pos += 2
                length = (((b1 & 0x0F) << 12) | (b2 << 4) | (b3 >> 4)) + 0x111
                disp = (((b3 & 0x0F) << 8) | b4) + 1
            else:
                length = hi + 1
                disp = (((b1 & 0x0F) << 8) | b2) + 1

            if disp > len(out):
                raise ValueError("invalid LZ11 back-reference")
            for _ in range(length):
                out.append(out[-disp])
                if len(out) >= out_size:
                    break

    return bytes(out)


def maybe_decompress(member: bytes) -> tuple[bytes, str]:
    if not member:
        return member, ""
    try:
        if member[0] == 0x10:
            return decompress_lz10(member), ""
        if member[0] == 0x11:
            return decompress_lz11(member), ""
    except Exception as exc:  # record, do not discard the original member
        return member, str(exc)
    return member, ""


def classify(data: bytes) -> str:
    if not data:
        return "EMPTY"
    table = {
        b"RGCN": "NCGR",
        b"NCGR": "NCGR",
        b"RLCN": "NCLR",
        b"NCLR": "NCLR",
        b"RECN": "NCER",
        b"NCER": "NCER",
        b"RNAN": "NANR",
        b"NANR": "NANR",
        b"RCMN": "NMCR",
        b"NMCR": "NMCR",
        b"RAMN": "NMAR",
        b"NMAR": "NMAR",
    }
    if data[:4] in table:
        return table[data[:4]]
    if data[0] == 0x10:
        return "LZ10"
    if data[0] == 0x11:
        return "LZ11"
    return "AUX:" + data[:4].hex()


def ncgr_dimensions(data: bytes) -> tuple[int | None, int | None]:
    if data[:4] not in (b"RGCN", b"NCGR"):
        return None, None
    p = data.find(b"RAHC")
    if p < 0 or p + 12 > len(data):
        return None, None
    height_tiles = u16(data, p + 8)
    width_tiles = u16(data, p + 10)
    return width_tiles * 8, height_tiles * 8


def build_inventory(rom_path: Path, archive_path: str, out_dir: Path) -> None:
    rom = rom_path.read_bytes()
    files = parse_nds_filesystem(rom)
    file_id, start, end = files[archive_path]
    archive = rom[start:end]
    members = parse_narc_members(archive)

    provenance = {
        "file_name": rom_path.name,
        "title_header": rom[:12].rstrip(b"\0").decode("ascii", "replace"),
        "game_code": rom[12:16].decode("ascii", "replace"),
        "maker_code": rom[16:18].decode("ascii", "replace"),
        "unit_code": rom[18],
        "rom_version": rom[30],
        "rom_size": len(rom),
        "rom_sha256": sha256(rom),
        "archive_path": archive_path,
        "archive_file_id": file_id,
        "archive_rom_offset": start,
        "archive_size": len(archive),
        "archive_sha256": sha256(archive),
        "member_count": len(members),
    }

    rows = []
    for member_id, stored in enumerate(members):
        decoded, error = maybe_decompress(stored)
        width, height = ncgr_dimensions(decoded)
        rows.append(
            {
                "member": member_id,
                "complete_20_block": member_id // 20 if member_id < (len(members) // 20) * 20 else "",
                "slot_in_20_block": member_id % 20 if member_id < (len(members) // 20) * 20 else "",
                "stored_size": len(stored),
                "stored_sha256": sha256(stored),
                "stored_type": classify(stored),
                "decoded_size": len(decoded),
                "decoded_sha256": sha256(decoded),
                "decoded_type": classify(decoded),
                "decode_error": error,
                "ncgr_width_px": width if width is not None else "",
                "ncgr_height_px": height if height is not None else "",
            }
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = rom_path.stem
    (out_dir / f"{stem}.provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (out_dir / f"{stem}.members.csv").open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "provenance": provenance,
        "decoded_types": dict(Counter(row["decoded_type"] for row in rows)),
        "ncgr_dimensions": {
            f"{w}x{h}": n
            for (w, h), n in Counter(
                (row["ncgr_width_px"], row["ncgr_height_px"])
                for row in rows
                if row["ncgr_width_px"] != ""
            ).items()
        },
        "complete_20_member_blocks": len(members) // 20,
        "trailing_members": len(members) % 20,
    }
    (out_dir / f"{stem}.summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--archive", default="a/0/0/4")
    ap.add_argument("--out", type=Path, default=Path("inventory_out"))
    args = ap.parse_args()
    build_inventory(args.rom, args.archive, args.out)


if __name__ == "__main__":
    main()
