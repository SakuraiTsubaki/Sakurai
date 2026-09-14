#!/usr/bin/env python3
"""Verify/fingerprint Pokémon Ruby text.c Phase 2 Part 1.

Scope: the first linked text/font/window-engine block through EmptyFunc.
Japanese Rev 0 uses a distinct early WindowTemplate lookup API and function order;
international/debug targets use the later common layout.
ROMs are read-only inputs and are never emitted.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import defaultdict
from pathlib import Path

ROM_BASE = 0x08000000

def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--rom-dir',required=True,type=Path)
    p.add_argument('--source-manifest',type=Path,default=Path('manifests/source_roms.json'))
    p.add_argument('--layouts',type=Path,default=Path('symbols/text_part1_layouts.csv'))
    p.add_argument('--targets',type=Path,default=Path('symbols/text_part1_targets.csv'))
    p.add_argument('--out',type=Path,default=Path('symbols/text_part1_fingerprints.csv'))
    p.add_argument('--verify-only',action='store_true')
    args=p.parse_args()
    sources={r['id']:r for r in json.loads(args.source_manifest.read_text(encoding='utf-8'))['roms']}
    layouts=defaultdict(list)
    with args.layouts.open(encoding='utf-8',newline='') as fp:
        for r in csv.DictReader(fp):
            layouts[r['layout']].append((r['symbol'],int(r['relative_offset'],16),int(r['size']),r['status']))
    with args.targets.open(encoding='utf-8',newline='') as fp:
        targets=list(csv.DictReader(fp))
    records=[]
    for t in targets:
        tid=t['target']; src=sources[tid]
        data=(args.rom_dir/src['file']).read_bytes()
        if sha1(data)!=src['sha1']:
            raise SystemExit(f'{tid}: whole-ROM SHA-1 mismatch')
        base=int(t['part1_base_offset'],16); end=int(t['mapped_end_offset'],16)
        region=data[base:end]
        if len(region)!=int(t['mapped_size']) or sha1(region)!=t['mapped_sha1']:
            raise SystemExit(f'{tid}: text Part-1 region verification failed')
        layout=t['layout']
        for sym,rel,size,status in layouts[layout]:
            start=base+rel; chunk=data[start:start+size]
            if len(chunk)!=size:
                raise SystemExit(f'{tid}:{sym}: truncated region')
            records.append({'target':tid,'symbol':sym,'status':status,'file_offset':f'0x{start:X}','address':f'0x{ROM_BASE+start:08X}','thumb_address':f'0x{ROM_BASE+start+1:08X}','size':size,'sha1':sha1(chunk)})
        # The next function is Text_InitWindowWithTemplate in both layout families.
        if data[end:end+2] != bytes.fromhex('70b5'):
            raise SystemExit(f'{tid}: unexpected Part-1 next boundary')
    if args.verify_only:
        print(f'verified {len(targets)} targets / {len(records)} function records')
        return 0
    args.out.parent.mkdir(parents=True,exist_ok=True)
    fields=['target','symbol','status','file_offset','address','thumb_address','size','sha1']
    with args.out.open('w',encoding='utf-8',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(records)
    print(f'verified {len(targets)} targets / {len(records)} function records')
    print(f'wrote {args.out}')
    return 0
if __name__=='__main__':
    raise SystemExit(main())
