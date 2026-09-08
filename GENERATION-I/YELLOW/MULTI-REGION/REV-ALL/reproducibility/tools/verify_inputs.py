#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
EXPECTED = {
    '42f3714eec6eca25200d42461ff08d57c98f6d1d': 'DE-DE_REV-0',
    'cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1': 'EN-US-EU_REV-0',
    '1dc242039218fba50928d1afb66b70565b6b9daf': 'ES-ES_REV-0',
    '0aceec0ef7aa2ca5aa831554598d91f61a925591': 'FR-FR_REV-0',
    '05bb8e99f24d498613930949730afa8024e77d08': 'IT-IT_REV-0',
    '1fb6c264e950d97ce3fd99b347e485b2150df4ff': 'JA-JP_REV-0A',
    '28e4b8531ea4ea1de5a396fccb0cfba51b06b149': 'JA-JP_REV-B',
    '91864ecdf26d1c593bde4d9ed615520eb57d5e41': 'JA-JP_REV-C',
    'a40298a8123613ee60cd7aab204d788b8425976e': 'JA-JP_REV-D',
}
def sha1(p):
    h=hashlib.sha1()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
found=[]
for arg in sys.argv[1:] or ['.']:
    p=Path(arg)
    files=[p] if p.is_file() else list(p.glob('*.gb'))+list(p.glob('*.gbc'))
    for f in files:
        s=sha1(f); found.append({'path':str(f),'sha1':s,'rom_id':EXPECTED.get(s),'recognized':s in EXPECTED})
print(json.dumps(found,indent=2))
raise SystemExit(0 if all(x['recognized'] for x in found) else 2)
