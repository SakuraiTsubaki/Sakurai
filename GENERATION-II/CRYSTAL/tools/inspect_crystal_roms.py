#!/usr/bin/env python3
"""Inventory Pokemon Crystal GBC ROMs without emitting ROM contents."""
from pathlib import Path
import hashlib, json, sys

def inspect(path: Path):
    b=path.read_bytes()
    hdr=0
    for x in b[0x134:0x14D]: hdr=(hdr-x-1)&0xff
    glob=(sum(b[:0x14E])+sum(b[0x150:]))&0xffff
    return {
        "filename": path.name,
        "size_bytes": len(b),
        "banks_16k": len(b)//0x4000,
        "md5": hashlib.md5(b).hexdigest(),
        "sha1": hashlib.sha1(b).hexdigest(),
        "sha256": hashlib.sha256(b).hexdigest(),
        "title_ascii": bytes(x for x in b[0x134:0x144] if x).decode("ascii", "replace"),
        "cgb_flag": f"0x{b[0x143]:02X}",
        "cartridge_type": f"0x{b[0x147]:02X}",
        "rom_size_code": f"0x{b[0x148]:02X}",
        "ram_size_code": f"0x{b[0x149]:02X}",
        "destination_code": f"0x{b[0x14A]:02X}",
        "version": b[0x14C],
        "header_checksum_ok": hdr == b[0x14D],
        "global_checksum_ok": glob == int.from_bytes(b[0x14E:0x150], "big"),
    }

if __name__ == "__main__":
    paths=[Path(x) for x in sys.argv[1:]]
    print(json.dumps([inspect(p) for p in paths], indent=2, ensure_ascii=False))
