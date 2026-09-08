#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('generated_dir',type=Path); ap.add_argument('baseline',type=Path); x=ap.parse_args()
    m=json.loads(x.baseline.read_text()); failures=0
    for r in m['datasets']:
        p=x.generated_dir/r['file']
        if not p.exists(): print('MISSING',r['file']); failures+=1; continue
        rows=sum(1 for _ in p.open('rb'))-1
        got=sha256(p); ok=p.stat().st_size==r['bytes'] and rows==r['rows'] and got==r['sha256']
        print(('OK' if ok else 'FAIL'),r['file'])
        failures += 0 if ok else 1
    raise SystemExit(1 if failures else 0)
if __name__=='__main__': main()
