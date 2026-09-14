#!/usr/bin/env python3
from pathlib import Path
import hashlib

BANK = 0x4000


def h1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def audit(path: Path):
    data = path.read_bytes()
    return {
        "filename": path.name,
        "size": len(data),
        "banks": len(data) // BANK,
        "sha1": h1(data),
        "title": data[0x134:0x144].split(b"\0", 1)[0].decode("ascii", "replace").rstrip(),
        "cgb_flag": f"0x{data[0x143]:02X}",
        "sgb_flag": f"0x{data[0x146]:02X}",
        "header_version": data[0x14C],
    }


def bank_hashes(path: Path):
    data = path.read_bytes()
    for offset in range(0, len(data), BANK):
        block = data[offset:offset + BANK]
        yield offset // BANK, offset, h1(block)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path)
    args = parser.parse_args()

    print(json.dumps(audit(args.rom), indent=2))
    for bank, offset, digest in bank_hashes(args.rom):
        print(f"{bank:02X},{offset:06X},{digest}")
