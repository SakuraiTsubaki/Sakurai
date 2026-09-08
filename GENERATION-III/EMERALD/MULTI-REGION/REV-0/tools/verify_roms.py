#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
manifest=Path(__file__).resolve().parents[1]/'manifest'/'rom_manifest.json'
m=json.loads(manifest.read_text(encoding='utf-8'))
fail=0
for rec in m['files']:
    p=root/rec['filename']
    if not p.exists():
        print('MISSING', p); fail+=1; continue
    data=p.read_bytes(); got=hashlib.sha256(data).hexdigest()
    ok=(got==rec['sha256'] and len(data)==rec['size'])
    print(('OK' if ok else 'FAIL'), rec['tag'], p.name, len(data), got)
    fail += 0 if ok else 1
sys.exit(1 if fail else 0)
