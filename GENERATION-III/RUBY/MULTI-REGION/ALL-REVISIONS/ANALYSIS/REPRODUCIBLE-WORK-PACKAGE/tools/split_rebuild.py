#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib
ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True)
s=sub.add_parser('split');s.add_argument('rom');s.add_argument('out_dir');s.add_argument('--chunk-size',type=lambda x:int(x,0),default=0x100000)
r=sub.add_parser('rebuild');r.add_argument('manifest');r.add_argument('out_rom')
a=ap.parse_args()
if a.cmd=='split':
    p=Path(a.rom);data=p.read_bytes();out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True); rows=[]
    for off in range(0,len(data),a.chunk_size):
        b=data[off:off+a.chunk_size];name=f'{off:08X}.bin';(out/name).write_bytes(b)
        rows.append({'file':name,'offset':off,'length':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    m={'source_filename':p.name,'source_size':len(data),'source_sha256':hashlib.sha256(data).hexdigest(),'chunk_size':a.chunk_size,'chunks':rows}
    (out/'split_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
else:
    mp=Path(a.manifest);m=json.loads(mp.read_text());buf=bytearray()
    for c in m['chunks']:
        b=(mp.parent/c['file']).read_bytes()
        if hashlib.sha256(b).hexdigest()!=c['sha256']: raise SystemExit(f"chunk hash mismatch: {c['file']}")
        buf.extend(b)
    if len(buf)!=m['source_size'] or hashlib.sha256(buf).hexdigest()!=m['source_sha256']: raise SystemExit('rebuild mismatch')
    Path(a.out_rom).write_bytes(buf);print('rebuild OK',m['source_sha256'])
