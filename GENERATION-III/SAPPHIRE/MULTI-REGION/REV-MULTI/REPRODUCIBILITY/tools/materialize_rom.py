#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(p: Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def split(rom: Path, out: Path, chunk_size: int):
    out.mkdir(parents=True,exist_ok=True); rows=[]
    with rom.open('rb') as f:
        i=0
        while True:
            b=f.read(chunk_size)
            if not b: break
            q=out/f'{i:04d}.bin'; q.write_bytes(b)
            rows.append({'index':i,'file':q.name,'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}); i+=1
    m={'source_name':rom.name,'source_size':rom.stat().st_size,'source_sha256':sha256(rom),'chunk_size':chunk_size,'chunks':rows}
    (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    return m

def rebuild(chunks: Path, out: Path):
    m=json.loads((chunks/'manifest.json').read_text())
    with out.open('wb') as w:
        for r in m['chunks']:
            p=chunks/r['file']; b=p.read_bytes()
            if len(b)!=r['size'] or hashlib.sha256(b).hexdigest()!=r['sha256']: raise SystemExit(f'chunk verification failed: {p}')
            w.write(b)
    got=sha256(out)
    if got!=m['source_sha256']: raise SystemExit(f'rebuild mismatch: {got} != {m["source_sha256"]}')
    print(f'OK {out} {got}')

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('split'); a.add_argument('rom',type=Path); a.add_argument('out',type=Path); a.add_argument('--chunk-size',type=int,default=1024*1024)
    b=sub.add_parser('rebuild'); b.add_argument('chunks',type=Path); b.add_argument('out',type=Path)
    x=ap.parse_args()
    if x.cmd=='split': split(x.rom,x.out,x.chunk_size)
    else: rebuild(x.chunks,x.out)
if __name__=='__main__': main()
