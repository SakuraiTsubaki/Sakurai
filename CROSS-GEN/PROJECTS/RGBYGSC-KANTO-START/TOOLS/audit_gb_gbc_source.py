#!/usr/bin/env python3
"""Metadata-only GB/GBC ROM audit. Reads a local image; never writes ROM bytes."""
from pathlib import Path
import argparse, hashlib, json

BANK=0x4000

def audit(path: Path):
    data=path.read_bytes()
    hc=0
    for i in range(0x134,0x14D): hc=(hc-data[i]-1)&0xff
    gc=(sum(data)-data[0x14E]-data[0x14F])&0xffff
    return {
        'filename':path.name,
        'size_bytes':len(data),
        'sha1':hashlib.sha1(data).hexdigest(),
        'sha256':hashlib.sha256(data).hexdigest(),
        'header_version':data[0x14C],
        'cgb_flag':data[0x143],
        'sgb_flag':data[0x146],
        'cartridge_type':data[0x147],
        'rom_size_code':data[0x148],
        'ram_size_code':data[0x149],
        'destination_code':data[0x14A],
        'header_checksum_valid':hc==data[0x14D],
        'global_checksum_valid':gc==((data[0x14E]<<8)|data[0x14F]),
        'banks_16k':[hashlib.sha256(data[i:i+BANK]).hexdigest() for i in range(0,len(data),BANK)]
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('roms',nargs='+',type=Path); ap.add_argument('-o','--out',type=Path,required=True); ns=ap.parse_args()
    ns.out.write_text(json.dumps([audit(p) for p in ns.roms],indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
