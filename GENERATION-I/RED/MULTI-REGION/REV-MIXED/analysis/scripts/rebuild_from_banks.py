#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib
if len(sys.argv)!=3: raise SystemExit("usage: rebuild_from_banks.py BANK_DIR OUT.gb")
files=sorted(Path(sys.argv[1]).glob("bank_*.bin"))
if not files: raise SystemExit("no bank_*.bin files")
data=b"".join(p.read_bytes() for p in files); Path(sys.argv[2]).write_bytes(data); print(hashlib.sha256(data).hexdigest())
