#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json
ap=argparse.ArgumentParser();ap.add_argument('rom_dir');ap.add_argument('--manifest',default=str(Path(__file__).resolve().parents[1]/'manifests'/'roms.json'));a=ap.parse_args();root=Path(a.rom_dir);rows=json.loads(Path(a.manifest).read_text());fail=[]
for r in rows:
    d=(root/r['filename']).read_bytes();chunk=0x100000;parts=[d[i:i+chunk] for i in range(0,len(d),chunk)];rebuilt=b''.join(parts)
    ok=(rebuilt==d and hashlib.sha256(rebuilt).hexdigest()==r['sha256']);print(r['id'], 'PASS' if ok else 'FAIL')
    if not ok:fail.append(r['id'])
print(f'{len(rows)-len(fail)}/{len(rows)} round-trip tests passed')
raise SystemExit(1 if fail else 0)
