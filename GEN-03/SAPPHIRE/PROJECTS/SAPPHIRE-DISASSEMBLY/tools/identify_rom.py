#!/usr/bin/env python3
"""Identify a local GBA ROM against config/versions.yml reference metadata.

This tool is for local analysis/verification only. ROM files are never committed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import zlib


def gba_header(data: bytes) -> dict[str, object]:
    if len(data) < 0xC0:
        raise ValueError("file is too small to contain a valid GBA header")

    def text(start: int, end: int) -> str:
        return data[start:end].rstrip(b"\0").decode("ascii", errors="replace")

    return {
        "title": text(0xA0, 0xAC),
        "game_code": text(0xAC, 0xB0),
        "maker_code": text(0xB0, 0xB2),
        "fixed_value": data[0xB2],
        "unit_code": data[0xB3],
        "device_type": data[0xB4],
        "software_version": data[0xBC],
        "header_checksum": data[0xBD],
    }


def identify(path: pathlib.Path) -> dict[str, object]:
    data = path.read_bytes()
    result = {
        "file": path.name,
        "size": len(data),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    result.update(gba_header(data))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Print GBA header and hash identity metadata")
    parser.add_argument("rom", type=pathlib.Path)
    args = parser.parse_args()
    print(json.dumps(identify(args.rom), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
