#!/usr/bin/env python3
from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
checks=[('external/pokered/pokered.gbc','ea9bcae617fdf159b045185467ae58b2e4a48b9a'),('external/pokegreen/pokered.gbc','0623ad12f48c259447980d68bd85ddbf8204b2cd'),('external/pokegreen/pokered11.gbc','ef74c79cded14204ac79e77f4964d9cb25003120')]
out=[]
for rel,exp in checks:
 p=root/rel
 if not p.exists(): out.append({'file':rel,'status':'missing','expected_sha1':exp}); continue
 h=hashlib.sha1(p.read_bytes()).hexdigest(); out.append({'file':rel,'status':'ok' if h==exp else 'mismatch','sha1':h,'expected_sha1':exp})
print(json.dumps(out,indent=2))
raise SystemExit(0 if all(x['status']=='ok' for x in out) else 1)
