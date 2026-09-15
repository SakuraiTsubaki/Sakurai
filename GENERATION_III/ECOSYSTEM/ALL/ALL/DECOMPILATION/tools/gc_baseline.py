#!/usr/bin/env python3
"""Generate a reproducible first-pass baseline for a local GameCube disc image.

Commercial disc images remain outside GitHub. This tool emits derived identity,
hashes, disc-header metadata, DOL layout, and FST summary for Generation III
GameCube research targets such as Colosseum, XD, Box, Channel, and distribution
discs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

GC_MAGIC = 0xC2339F3D
MAX_FST_READ = 64 * 1024 * 1024


def hash_file(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ascii_field(raw: bytes) -> str:
    return raw.split(b"\0", 1)[0].decode("ascii", errors="replace")


def be32(raw: bytes, offset: int) -> int:
    return struct.unpack_from(">I", raw, offset)[0]


def read_at(path: Path, offset: int, size: int) -> bytes:
    with path.open("rb") as f:
        f.seek(offset)
        return f.read(size)


def disc_header(path: Path) -> dict[str, object]:
    raw = read_at(path, 0, 0x440)
    if len(raw) < 0x440:
        raise ValueError("file is too small to contain a complete GameCube disc header")
    return {
        "game_code": ascii_field(raw[0:4]),
        "maker_code": ascii_field(raw[4:6]),
        "disc_number": raw[6],
        "disc_version": raw[7],
        "audio_streaming": raw[8],
        "stream_buffer_size": raw[9],
        "magic": f"0x{be32(raw, 0x1C):08X}",
        "magic_valid": be32(raw, 0x1C) == GC_MAGIC,
        "game_name": ascii_field(raw[0x20:0x400]),
        "dol_offset": be32(raw, 0x420),
        "fst_offset": be32(raw, 0x424),
        "fst_size": be32(raw, 0x428),
        "fst_max_size": be32(raw, 0x42C),
    }


def dol_summary(path: Path, offset: int, file_size: int) -> dict[str, object]:
    if offset <= 0 or offset + 0xE4 > file_size:
        return {"present": False, "reason": "DOL header outside image"}
    raw = read_at(path, offset, 0xE4)
    if len(raw) != 0xE4:
        return {"present": False, "reason": "truncated DOL header"}

    text_offsets = [be32(raw, i * 4) for i in range(7)]
    data_offsets = [be32(raw, 0x1C + i * 4) for i in range(11)]
    text_addresses = [be32(raw, 0x48 + i * 4) for i in range(7)]
    data_addresses = [be32(raw, 0x64 + i * 4) for i in range(11)]
    text_sizes = [be32(raw, 0x90 + i * 4) for i in range(7)]
    data_sizes = [be32(raw, 0xAC + i * 4) for i in range(11)]

    segments = []
    for kind, offsets, addresses, sizes in (
        ("text", text_offsets, text_addresses, text_sizes),
        ("data", data_offsets, data_addresses, data_sizes),
    ):
        for index, (seg_off, addr, size) in enumerate(zip(offsets, addresses, sizes)):
            if size:
                segments.append({
                    "kind": kind,
                    "index": index,
                    "file_offset": seg_off,
                    "address": f"0x{addr:08X}",
                    "size": size,
                    "in_image": seg_off + size <= file_size,
                })
    return {
        "present": True,
        "entry_point": f"0x{be32(raw, 0xE0):08X}",
        "bss_address": f"0x{be32(raw, 0xD8):08X}",
        "bss_size": be32(raw, 0xDC),
        "segments": segments,
    }


def fst_summary(path: Path, offset: int, size: int, file_size: int) -> dict[str, object]:
    if offset <= 0 or size <= 0 or offset + size > file_size:
        return {"present": False, "reason": "FST outside image or empty"}
    if size > MAX_FST_READ:
        return {"present": True, "size": size, "parsed": False, "reason": "FST exceeds safety read cap"}
    raw = read_at(path, offset, size)
    if len(raw) < 12:
        return {"present": False, "reason": "truncated FST root entry"}
    root_type_name = be32(raw, 0)
    entry_count = be32(raw, 8)
    table_bytes = entry_count * 12
    plausible = bool(root_type_name & 0x01000000) and 1 <= entry_count and table_bytes <= len(raw)
    return {
        "present": True,
        "size": size,
        "root_is_directory": bool(root_type_name & 0x01000000),
        "entry_count": entry_count,
        "entry_table_bytes": table_bytes,
        "structure_plausible": plausible,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Inventory a local GameCube disc image")
    p.add_argument("image", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    if not args.image.is_file():
        p.error(f"image not found: {args.image}")

    file_size = args.image.stat().st_size
    try:
        header = disc_header(args.image)
    except ValueError as exc:
        p.error(str(exc))

    report = {
        "schema_version": 1,
        "source": {
            "filename": args.image.name,
            "size": file_size,
            "sha1": hash_file(args.image, "sha1"),
            "sha256": hash_file(args.image, "sha256"),
        },
        "disc_header": header,
        "dol": dol_summary(args.image, int(header["dol_offset"]), file_size),
        "fst": fst_summary(args.image, int(header["fst_offset"]), int(header["fst_size"]), file_size),
    }
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
