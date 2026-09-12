#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

EXTS = {".gb", ".gbc"}

def row(path: Path):
    data = path.read_bytes()
    return {
        "file": path.name,
        "size_bytes": len(data),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "header": {
            "title_hex": data[0x134:0x144].hex(),
            "cgb_flag": f"0x{data[0x143]:02X}",
            "cartridge_type": f"0x{data[0x147]:02X}",
            "rom_size_code": f"0x{data[0x148]:02X}",
            "ram_size_code": f"0x{data[0x149]:02X}",
            "destination_code": f"0x{data[0x14A]:02X}",
        },
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom_dir", type=Path)
    args = ap.parse_args()
    rows = [row(p) for p in sorted(args.rom_dir.iterdir()) if p.suffix.lower() in EXTS]
    print(json.dumps({"roms": rows}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
