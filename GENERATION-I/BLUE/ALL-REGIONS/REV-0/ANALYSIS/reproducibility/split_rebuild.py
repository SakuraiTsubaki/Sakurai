#!/usr/bin/env python3
"""Split a ROM into 16 KiB banks, rebuild it, and prove byte-for-byte identity."""
import argparse,hashlib
from pathlib import Path
BANK=0x4000

def sha256(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom',type=Path); ap.add_argument('workdir',type=Path); a=ap.parse_args()
    d=a.rom.read_bytes()
    if len(d)%BANK: raise SystemExit('ROM size is not a multiple of 16 KiB')
    bankdir=a.workdir/'banks'; bankdir.mkdir(parents=True,exist_ok=True); parts=[]
    for i in range(len(d)//BANK):
        p=bankdir/f'bank_{i:02X}.bin'; p.write_bytes(d[i*BANK:(i+1)*BANK]); parts.append(p)
    rebuilt=a.workdir/'rebuilt.gb'; rebuilt.write_bytes(b''.join(p.read_bytes() for p in parts))
    ok=sha256(a.rom)==sha256(rebuilt)
    print(f'original_sha256={sha256(a.rom)}'); print(f'rebuilt_sha256={sha256(rebuilt)}'); print(f'roundtrip_ok={ok}')
    if not ok: raise SystemExit(1)
if __name__=='__main__': main()
