#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib
if len(sys.argv)<3: raise SystemExit('usage: rebuild_from_banks.py BANKDIR OUTROM')
d=Path(sys.argv[1]); files=sorted(d.glob('bank_*.bin')); b=b''.join(p.read_bytes() for p in files); Path(sys.argv[2]).write_bytes(b); print('banks',len(files),'size',len(b),'sha1',hashlib.sha1(b).hexdigest())
