#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

def header_checksum(b):
    x=0
    for i in range(0x134,0x14D): x=(x-b[i]-1)&0xff
    return x

def global_checksum(b): return (sum(b[:0x14E])+sum(b[0x150:]))&0xffff

def inspect(path):
    b=Path(path).read_bytes()
    return {
      "filename":Path(path).name,"size":len(b),
      "md5":hashlib.md5(b).hexdigest(),"sha1":hashlib.sha1(b).hexdigest(),"sha256":hashlib.sha256(b).hexdigest(),
      "cgb_flag":f"0x{b[0x143]:02X}","sgb_flag":f"0x{b[0x146]:02X}","cartridge_type":f"0x{b[0x147]:02X}",
      "rom_size_code":f"0x{b[0x148]:02X}","ram_size_code":f"0x{b[0x149]:02X}","destination_code":f"0x{b[0x14A]:02X}",
      "header_version":b[0x14C],"header_checksum_valid":header_checksum(b)==b[0x14D],
      "global_checksum_valid":global_checksum(b)==int.from_bytes(b[0x14E:0x150],"big")
    }

if __name__=="__main__":
    import sys
    print(json.dumps([inspect(p) for p in sys.argv[1:]],indent=2))
