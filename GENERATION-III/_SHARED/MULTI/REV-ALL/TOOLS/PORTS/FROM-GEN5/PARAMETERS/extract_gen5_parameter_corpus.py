#!/usr/bin/env python3
"""Extract the Generation V parameter corpus used by the Gen II/III adapters.

The tool walks NitroFS and extracts source NARCs by role instead of using ROM
file offsets. Generated data stays local and is not committed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

SOURCES = {
    "personal": "a/0/1/6",
    "growth": "a/0/1/7",
    "level_up": "a/0/1/8",
    "evolution": "a/0/1/9",
    "breeding_child": "a/0/2/0",
    "moves": "a/0/2/1",
    "items": "a/0/2/4",
}

FIXED_RECORD_SIZES = {
    "personal": 0x3C,
    "moves": 0x24,
    "evolution": 0x2A,
}


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def nitrofs_index(nds: bytes) -> dict[str, int]:
    fnt_offset = u32(nds, 0x40)
    fnt_size = u32(nds, 0x44)
    fnt = nds[fnt_offset : fnt_offset + fnt_size]
    result: dict[str, int] = {}

    def walk(directory_id: int, prefix: str = "") -> None:
        table_offset = (directory_id - 0xF000) * 8
        pos = u32(fnt, table_offset)
        file_id = u16(fnt, table_offset + 4)

        while True:
            desc = fnt[pos]
            pos += 1
            if desc == 0:
                return
            is_dir = bool(desc & 0x80)
            length = desc & 0x7F
            name = fnt[pos : pos + length].decode("ascii")
            pos += length
            if is_dir:
                child = u16(fnt, pos)
                pos += 2
                walk(child, prefix + name + "/")
            else:
                result[prefix + name] = file_id
                file_id += 1

    walk(0xF000)
    return result


def read_file(nds: bytes, index: dict[str, int], path: str) -> bytes:
    if path not in index:
        raise KeyError(path)
    fat_offset = u32(nds, 0x48)
    file_id = index[path]
    start = u32(nds, fat_offset + file_id * 8)
    end = u32(nds, fat_offset + file_id * 8 + 4)
    return nds[start:end]


def parse_narc(narc: bytes) -> list[bytes]:
    if narc[:4] != b"NARC":
        raise ValueError("not a NARC")
    chunks: dict[bytes, int] = {}
    pos = 0x10
    while pos + 8 <= len(narc):
        magic = narc[pos : pos + 4]
        size = u32(narc, pos + 4)
        if size < 8 or pos + size > len(narc):
            raise ValueError(f"bad NARC chunk at 0x{pos:X}")
        chunks[magic] = pos
        pos += size
    btaf = chunks[b"BTAF"]
    gmif = chunks[b"GMIF"]
    data_base = gmif + 8
    count = u16(narc, btaf + 8)
    out: list[bytes] = []
    for i in range(count):
        start = u32(narc, btaf + 0x0C + i * 8)
        end = u32(narc, btaf + 0x10 + i * 8)
        out.append(narc[data_base + start : data_base + end])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("data/gen5/corpus"))
    args = ap.parse_args()

    nds = args.rom.read_bytes()
    fs = nitrofs_index(nds)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "rom_file": args.rom.name,
        "rom_sha1": hashlib.sha1(nds).hexdigest(),
        "sources": {},
    }

    for role, path in SOURCES.items():
        narc = read_file(nds, fs, path)
        members = parse_narc(narc)
        role_dir = args.out_dir / role
        role_dir.mkdir(parents=True, exist_ok=True)
        (role_dir / "source.narc").write_bytes(narc)

        for i, member in enumerate(members):
            (role_dir / f"{i:04d}.bin").write_bytes(member)

        fixed = FIXED_RECORD_SIZES.get(role)
        bad_sizes = []
        flat_sha1 = None
        flat_size = None
        if fixed is not None:
            bad_sizes = [i for i, member in enumerate(members) if len(member) != fixed]
            if not bad_sizes:
                flat = b"".join(members)
                flat_path = role_dir / "flat.bin"
                flat_path.write_bytes(flat)
                flat_sha1 = hashlib.sha1(flat).hexdigest()
                flat_size = len(flat)

        manifest["sources"][role] = {
            "nitrofs_path": path,
            "narc_sha1": hashlib.sha1(narc).hexdigest(),
            "member_count": len(members),
            "member_sizes": sorted({len(m) for m in members}),
            "fixed_record_size_expected": fixed,
            "fixed_record_size_mismatches": bad_sizes,
            "flat_binary": "flat.bin" if flat_sha1 else None,
            "flat_binary_size": flat_size,
            "flat_binary_sha1": flat_sha1,
        }

    (args.out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
