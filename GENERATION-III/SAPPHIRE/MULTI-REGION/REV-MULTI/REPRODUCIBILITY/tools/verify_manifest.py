#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def hash_file(p, algo):
    h=hashlib.new(algo)
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom_dir',type=Path); ap.add_argument('manifest',type=Path); x=ap.parse_args()
    m=json.loads(x.manifest.read_text()); failures=0
    for r in m['roms']:
        p=x.rom_dir/r['filename']
        if not p.exists(): print('MISSING',p.name); failures+=1; continue
        got={a:hash_file(p,a) for a in ('md5','sha1','sha256')}
        ok=p.stat().st_size==r['size_bytes'] and all(got[a]==r[a] for a in got)
        print(('OK' if ok else 'FAIL'),p.name)
        failures += 0 if ok else 1
    raise SystemExit(1 if failures else 0)
if __name__=='__main__': main()
