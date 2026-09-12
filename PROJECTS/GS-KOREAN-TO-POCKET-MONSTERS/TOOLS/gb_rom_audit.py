#!/usr/bin/env python3
from pathlib import Path
import hashlib

BANK = 0x4000


def h1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def hardware_profile(cgb_flag: int) -> str:
    if cgb_flag == 0x00:
        return "DMG_ONLY"
    if cgb_flag == 0x80:
        return "DMG_CGB_DUAL"
    if cgb_flag == 0xC0:
        return "CGB_ONLY"
    return f"UNKNOWN_CGB_FLAG_0x{cgb_flag:02X}"


def audit(path: Path):
    data = path.read_bytes()
    cgb = data[0x143]
    sgb = data[0x146]
    return {
        "filename": path.name,
        "file_extension": path.suffix.lower(),
        "size": len(data),
        "banks": len(data) // BANK,
        "sha1": h1(data),
        "title": data[0x134:0x144].split(b"\0", 1)[0].decode("ascii", "replace").rstrip(),
        "cgb_flag": f"0x{cgb:02X}",
        "hardware_profile": hardware_profile(cgb),
        "sgb_flag": f"0x{sgb:02X}",
        "sgb_supported": sgb == 0x03,
        "header_version": data[0x14C],
        "path_policy_note": "title platform is canonical metadata; do not infer LIBRARY platform from extension/CGB/SGB flags",
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
