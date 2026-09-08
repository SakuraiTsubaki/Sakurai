#!/usr/bin/env python3
import argparse,hashlib,math
from pathlib import Path
BANK=0x4000
ap=argparse.ArgumentParser(); ap.add_argument("rom",type=Path); ap.add_argument("out",type=Path); a=ap.parse_args()
data=a.rom.read_bytes(); a.out.mkdir(parents=True,exist_ok=True)
for i in range(math.ceil(len(data)/BANK)):
 b=data[i*BANK:(i+1)*BANK]; p=a.out/f"bank_{i:03d}_{i:02X}.bin"; p.write_bytes(b); print(i,hashlib.sha256(b).hexdigest(),p)
