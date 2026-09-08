#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib
if len(sys.argv)<3: raise SystemExit('usage: split_banks.py ROM OUTDIR')
p=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True); b=p.read_bytes()
for i in range((len(b)+0x3fff)//0x4000):
    ch=b[i*0x4000:(i+1)*0x4000]; q=out/f'bank_{i:02X}.bin'; q.write_bytes(ch); print(q,hashlib.sha1(ch).hexdigest())
