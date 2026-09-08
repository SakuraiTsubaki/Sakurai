#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib
BANK=0x4000
if len(sys.argv)!=3: raise SystemExit("usage: split_banks.py ROM.gb OUTPUT_DIR")
rom=Path(sys.argv[1]).read_bytes(); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
for i in range((len(rom)+BANK-1)//BANK): (out/f"bank_{i:02X}.bin").write_bytes(rom[i*BANK:(i+1)*BANK])
print(hashlib.sha256(rom).hexdigest())
