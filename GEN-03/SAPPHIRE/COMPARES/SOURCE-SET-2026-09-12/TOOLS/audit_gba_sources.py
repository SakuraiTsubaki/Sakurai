#!/usr/bin/env python3
"""Audit local GBA source images without committing ROM bytes."""
from pathlib import Path
import hashlib, json, zlib, sys

def audit(p: Path):
    d=p.read_bytes()
    calc=(-sum(d[0xA0:0xBD])-0x19)&0xff
    return {
      "filename": p.name, "size_bytes": len(d),
      "title": d[0xA0:0xAC].rstrip(b"\0").decode("ascii","replace"),
      "game_code": d[0xAC:0xB0].decode("ascii","replace"),
      "maker_code": d[0xB0:0xB2].decode("ascii","replace"),
      "header_version": d[0xBC], "header_checksum": d[0xBD],
      "header_checksum_calculated": calc, "header_checksum_valid": d[0xBD]==calc,
      "crc32": f"{zlib.crc32(d)&0xffffffff:08x}",
      "md5": hashlib.md5(d).hexdigest(), "sha1": hashlib.sha1(d).hexdigest(),
      "sha256": hashlib.sha256(d).hexdigest()
    }
if __name__ == "__main__":
    print(json.dumps([audit(Path(x)) for x in sys.argv[1:]], indent=2, ensure_ascii=False))
