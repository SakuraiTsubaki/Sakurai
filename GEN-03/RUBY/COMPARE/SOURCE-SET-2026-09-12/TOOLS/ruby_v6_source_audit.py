#!/usr/bin/env python3
"""Mechanical Pokémon Ruby GBA source identity audit for the v6 repository model.
Reads local .gba files, emits no ROM bytes, and never modifies inputs.
"""
from pathlib import Path
import argparse, hashlib, json, zlib

def release_id(data: bytes, name: str) -> str:
    code = data[0xAC:0xB0].decode("ascii")
    hv = data[0xBC]
    suffix = "-DEBUG" if "Debug Version" in name else ""
    return f"{code}-HV{hv}{suffix}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("directory", type=Path)
    ns=ap.parse_args()
    rows=[]
    for p in sorted(ns.directory.glob("*.gba")):
        b=p.read_bytes()
        calc = (-(sum(b[0xA0:0xBD]) + 0x19)) & 0xFF
        sha1=hashlib.sha1(b).hexdigest()
        rows.append({
            "release_id": release_id(b,p.name),
            "dump_id": f"UPLOAD-{sha1[:8]}",
            "filename": p.name,
            "size_bytes": len(b),
            "title": b[0xA0:0xAC].rstrip(b"\0").decode("ascii","replace"),
            "game_code": b[0xAC:0xB0].decode("ascii","replace"),
            "maker_code": b[0xB0:0xB2].decode("ascii","replace"),
            "header_version": b[0xBC],
            "header_checksum_valid": calc == b[0xBD],
            "crc32": f"{zlib.crc32(b)&0xffffffff:08x}",
            "md5": hashlib.md5(b).hexdigest(),
            "sha1": sha1,
            "sha256": hashlib.sha256(b).hexdigest(),
            "rom_binary_committed": False,
        })
    print(json.dumps(rows, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
