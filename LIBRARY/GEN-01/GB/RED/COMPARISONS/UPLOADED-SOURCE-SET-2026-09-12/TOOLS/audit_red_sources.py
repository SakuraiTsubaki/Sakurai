#!/usr/bin/env python3
"""Audit supplied Pokémon Red GB images without committing ROM bytes.

Outputs release identity, header/checksum observations, duplicate SHA-1 groups,
and zero-filled 16 KiB bank ranges. The script is deliberately filename-light:
release identity is resolved from known hashes after the file is read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

BANK = 0x4000
KNOWN = {
    "0623ad12f48c259447980d68bd85ddbf8204b2cd": "JP-JA-HV0",
    "ef74c79cded14204ac79e77f4964d9cb25003120": "JP-JA-HV1",
    "ea9bcae617fdf159b045185467ae58b2e4a48b9a": "US-EU-EN-HV0",
    "87d523fe1a0c548db7c5477b451ddec1eb083c06": "EU-DE-HV0",
    "47a7622fa30e6402a3891fe65b3a930bf9bd7aec": "EU-FR-HV0",
    "65b97cf8f2f1cff711a6d08c6c894c8ce65ce522": "EU-IT-HV0",
    "fc17c5b904d551b1b908054ccd1c493f755f832a": "EU-ES-HV0",
}


def audit(path: Path) -> dict:
    data = path.read_bytes()
    sha1 = hashlib.sha1(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    title = data[0x134:0x144].rstrip(b"\0").decode("ascii", "replace")
    header_calc = (0xE7 - sum(data[0x134:0x14D])) & 0xFF
    global_calc = (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF
    global_stored = (data[0x14E] << 8) | data[0x14F]
    zero_banks = [
        f"{i:02X}"
        for i in range(len(data) // BANK)
        if not any(data[i * BANK:(i + 1) * BANK])
    ]
    return {
        "filename": path.name,
        "release_id": KNOWN.get(sha1),
        "size_bytes": len(data),
        "banks_16k": len(data) // BANK,
        "title": title,
        "header_version": data[0x14C],
        "cartridge_type": f"0x{data[0x147]:02X}",
        "header_checksum_ok": header_calc == data[0x14D],
        "global_checksum_ok": global_calc == global_stored,
        "zero_banks": zero_banks,
        "sha1": sha1,
        "sha256": sha256,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    args = ap.parse_args()
    rows = [audit(p) for p in args.paths]
    dup = {}
    for row in rows:
        dup.setdefault(row["sha1"], []).append(row["filename"])
    print(json.dumps({
        "files": rows,
        "duplicate_groups": {k: v for k, v in dup.items() if len(v) > 1},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
