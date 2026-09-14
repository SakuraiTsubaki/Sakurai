#!/usr/bin/env python3
"""Audit user-supplied Game Boy Advance ROM files without modifying them.

No ROMs are bundled with this repository. Point this tool at ROM files you
legally possess; it prints header metadata and cryptographic hashes as JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zlib


def audit(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 0xC0:
        raise ValueError(f"{path}: file is too small to contain a GBA header")

    expected_header_checksum = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
    return {
        "file": path.name,
        "size_bytes": len(data),
        "title": data[0xA0:0xAC].rstrip(b"\0").decode("ascii", "replace"),
        "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
        "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
        "fixed_value_0xb2": data[0xB2],
        "unit_code": data[0xB3],
        "device_type": data[0xB4],
        "revision": data[0xBC],
        "header_checksum": f"{data[0xBD]:02x}",
        "header_checksum_expected": f"{expected_header_checksum:02x}",
        "header_checksum_valid": data[0xBD] == expected_header_checksum,
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps([audit(path) for path in args.rom], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
