#!/usr/bin/env python3
"""Generate GBA identity and 64 KiB bank fingerprints without modifying the ROM."""
import argparse, hashlib, json, pathlib, zlib

def gba_checksum(data):
    return (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF

def inspect(path):
    data=path.read_bytes()
    code=data[0xAC:0xB0].decode("ascii", "replace")
    ver=data[0xBC]
    return {"filename":path.name,"size":len(data),"game_code":code,"header_version":ver,"release_id":f"{code}-R{ver}","sha1":hashlib.sha1(data).hexdigest(),"sha256":hashlib.sha256(data).hexdigest(),"crc32":f"{zlib.crc32(data)&0xffffffff:08x}","header_checksum_valid":gba_checksum(data)==data[0xBD],"banks_64k":[hashlib.sha1(data[i:i+65536]).hexdigest() for i in range(0,len(data),65536)]}

if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("rom", nargs="+"); ns=ap.parse_args()
    print(json.dumps([inspect(pathlib.Path(x)) for x in ns.rom], indent=2))
