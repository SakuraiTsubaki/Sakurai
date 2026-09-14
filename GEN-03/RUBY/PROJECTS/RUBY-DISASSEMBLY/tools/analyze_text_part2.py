#!/usr/bin/env python3
"""Verify/fingerprint Pokémon Ruby text.c Phase 2 Part 2.

Scope: window/text initialization and synchronous printer entry helpers, ending
at the verified PrintNextChar boundary. ROMs are read-only inputs.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import defaultdict
from pathlib import Path
ROM_BASE=0x08000000
def sha1(b:bytes)->str:return hashlib.sha1(b).hexdigest()
def main()->int:
 p=argparse.ArgumentParser();p.add_argument('--rom-dir',required=True,type=Path)
 p.add_argument('--source-manifest',type=Path,default=Path('manifests/source_roms.json'))
 p.add_argument('--layouts',type=Path,default=Path('symbols/text_part2_layouts.csv'))
 p.add_argument('--targets',type=Path,default=Path('symbols/text_part2_targets.csv'))
 p.add_argument('--out',type=Path,default=Path('symbols/text_part2_fingerprints.csv'));p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 srcs={r['id']:r for r in json.loads(a.source_manifest.read_text(encoding='utf-8'))['roms']}
 layouts=defaultdict(list)
 with a.layouts.open(encoding='utf-8',newline='') as f:
  for r in csv.DictReader(f):layouts[r['layout']].append((r['symbol'],int(r['relative_offset'],16),int(r['size']),r['status']))
 with a.targets.open(encoding='utf-8',newline='') as f:targets=list(csv.DictReader(f))
 records=[]
 for t in targets:
  tid=t['target'];src=srcs[tid];data=(a.rom_dir/src['file']).read_bytes()
  if sha1(data)!=src['sha1']:raise SystemExit(f'{tid}: whole-ROM SHA-1 mismatch')
  base=int(t['part2_base_offset'],16);end=int(t['mapped_end_offset'],16);region=data[base:end]
  if len(region)!=int(t['mapped_size']) or sha1(region)!=t['mapped_sha1']:raise SystemExit(f'{tid}: text Part-2 region verification failed')
  for sym,rel,size,status in layouts[t['layout']]:
   start=base+rel;chunk=data[start:start+size]
   if len(chunk)!=size:raise SystemExit(f'{tid}:{sym}: truncated region')
   records.append({'target':tid,'symbol':sym,'status':status,'file_offset':f'0x{start:X}','address':f'0x{ROM_BASE+start:08X}','thumb_address':f'0x{ROM_BASE+start+1:08X}','size':size,'sha1':sha1(chunk)})
  if data[end:end+2]!=bytes.fromhex('10b5'):raise SystemExit(f'{tid}: PrintNextChar boundary mismatch')
 if a.verify_only:print(f'verified {len(targets)} targets / {len(records)} function records');return 0
 a.out.parent.mkdir(parents=True,exist_ok=True);fields=['target','symbol','status','file_offset','address','thumb_address','size','sha1']
 with a.out.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(records)
 print(f'verified {len(targets)} targets / {len(records)} function records');print(f'wrote {a.out}');return 0
if __name__=='__main__':raise SystemExit(main())
