#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import gba_header
ap=argparse.ArgumentParser();ap.add_argument('rom_dir');ap.add_argument('--manifest',default=str(Path(__file__).resolve().parents[1]/'manifests'/'roms.json'));a=ap.parse_args()
rows=json.loads(Path(a.manifest).read_text(encoding='utf-8')); root=Path(a.rom_dir); failures=[]
for r in rows:
    p=root/r['filename']
    if not p.exists(): failures.append((r['id'],'missing')); continue
    d=p.read_bytes(); sha=hashlib.sha256(d).hexdigest(); h=gba_header(d)
    if sha!=r['sha256']: failures.append((r['id'],'sha256 mismatch'))
    if not h['header_checksum_ok']: failures.append((r['id'],'header checksum invalid'))
    if len(d)!=r['size_bytes']: failures.append((r['id'],'size mismatch'))
print(f'checked={len(rows)} failures={len(failures)}')
for x in failures: print(*x,sep=': ')
raise SystemExit(1 if failures else 0)
