#!/usr/bin/env python3
"""Inspect a GBA ROM header and compute verification hashes.

This tool is intended for local, read-only reference ROM verification. It does
not modify or copy the ROM and does not require reference ROMs to be committed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zlib


def inspect(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    if len(data) < 0xC0:
        raise ValueError("file is too small to contain a valid GBA header")

    return {
        "file": path.name,
        "size": len(data),
        "title": data[0xA0:0xAC].rstrip(b"\0").decode("ascii", "replace"),
        "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
        "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
        "software_version": data[0xBC],
        "header_complement": f"0x{data[0xBD]:02X}",
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path, help="local read-only reference ROM")
    parser.add_argument("--manifest", type=Path, default=None,
                        help="optional manifests/roms.json to match by SHA-256")
    args = parser.parse_args()

    info = inspect(args.rom)

    if args.manifest:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        matches = [r for r in manifest.get("references", [])
                   if r.get("sha256") == info["sha256"]]
        info["manifest_matches"] = [r.get("id") for r in matches]

    print(json.dumps(info, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
