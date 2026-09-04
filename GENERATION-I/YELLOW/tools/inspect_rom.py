#!/usr/bin/env python3
"""Inventory Game Boy/GBC ROM metadata without distributing ROM content."""
from pathlib import Path
import hashlib, sys

def inspect(path: Path):
    b = path.read_bytes()
    hc = 0
    for i in range(0x134, 0x14D):
        hc = (hc - b[i] - 1) & 0xFF
    gc = (sum(b[:0x14E]) + sum(b[0x150:])) & 0xFFFF
    return {
        "file": path.name,
        "size": len(b),
        "banks_16k": len(b) // 0x4000,
        "md5": hashlib.md5(b).hexdigest(),
        "sha1": hashlib.sha1(b).hexdigest(),
        "sha256": hashlib.sha256(b).hexdigest(),
        "cgb_flag": f"0x{b[0x143]:02X}",
        "sgb_flag": f"0x{b[0x146]:02X}",
        "cartridge_type": f"0x{b[0x147]:02X}",
        "rom_size_code": f"0x{b[0x148]:02X}",
        "ram_size_code": f"0x{b[0x149]:02X}",
        "destination_code": f"0x{b[0x14A]:02X}",
        "header_version": b[0x14C],
        "header_checksum_valid": hc == b[0x14D],
        "global_checksum_valid": gc == int.from_bytes(b[0x14E:0x150], "big"),
    }

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(inspect(Path(arg)))
