#!/usr/bin/env python3
"""Produce reproducible metadata-only audits for GB/GBC source images."""
from pathlib import Path
import argparse, hashlib, json

BANK = 0x4000


def audit(path: Path):
    b = path.read_bytes()
    hc = 0
    for i in range(0x134, 0x14D):
        hc = (hc - b[i] - 1) & 0xFF
    gc = (sum(b) - b[0x14E] - b[0x14F]) & 0xFFFF
    return {
        "filename": path.name,
        "size_bytes": len(b),
        "sha1": hashlib.sha1(b).hexdigest(),
        "sha256": hashlib.sha256(b).hexdigest(),
        "header_version": b[0x14C],
        "cgb_flag": b[0x143],
        "sgb_flag": b[0x146],
        "cartridge_type": b[0x147],
        "rom_size_code": b[0x148],
        "ram_size_code": b[0x149],
        "destination_code": b[0x14A],
        "header_checksum_valid": hc == b[0x14D],
        "global_checksum_valid": gc == ((b[0x14E] << 8) | b[0x14F]),
        "banks_16k": [
            hashlib.sha256(b[i:i + BANK]).hexdigest()
            for i in range(0, len(b), BANK)
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roms", nargs="+", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ns = ap.parse_args()
    ns.out.write_text(
        json.dumps([audit(p) for p in ns.roms], indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
