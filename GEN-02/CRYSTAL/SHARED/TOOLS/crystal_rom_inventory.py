#!/usr/bin/env python3
"""Inspect a user-supplied Pokemon Crystal ROM and emit non-ROM metadata.

This tool never writes ROM bytes to the repository.
"""
from pathlib import Path
import argparse, hashlib, json, zlib
BANK=0x4000

def inspect(path: Path):
    d=path.read_bytes()
    hc=0
    for b in d[0x134:0x14D]: hc=(hc-b-1)&0xff
    gc=(sum(d[:0x14E])+sum(d[0x150:]))&0xffff
    return {
      "filename":path.name,"size_bytes":len(d),
      "hashes":{"crc32":f"{zlib.crc32(d)&0xffffffff:08x}","md5":hashlib.md5(d).hexdigest(),"sha1":hashlib.sha1(d).hexdigest(),"sha256":hashlib.sha256(d).hexdigest()},
      "header":{"title":d[0x134:0x13F].split(b"\0")[0].decode("ascii","replace"),"game_code":d[0x13F:0x143].decode("ascii","replace"),"cgb_flag":f"0x{d[0x143]:02X}","sgb_flag":f"0x{d[0x146]:02X}","cartridge_type":f"0x{d[0x147]:02X}","rom_size_code":f"0x{d[0x148]:02X}","ram_size_code":f"0x{d[0x149]:02X}","destination_code":f"0x{d[0x14A]:02X}","mask_rom_version":d[0x14C],"header_checksum_valid":hc==d[0x14D],"global_checksum_valid":gc==int.from_bytes(d[0x14E:0x150],"big")},
      "bank_count":len(d)//BANK,
      "banks":[{"bank":i,"sha256":hashlib.sha256(d[i*BANK:(i+1)*BANK]).hexdigest()} for i in range(len(d)//BANK)]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("rom",type=Path); ap.add_argument("-o","--output",type=Path)
    a=ap.parse_args(); text=json.dumps(inspect(a.rom),indent=2)+"\n"
    if a.output:a.output.write_text(text,encoding="utf-8")
    else:print(text,end="")
if __name__=="__main__":main()
