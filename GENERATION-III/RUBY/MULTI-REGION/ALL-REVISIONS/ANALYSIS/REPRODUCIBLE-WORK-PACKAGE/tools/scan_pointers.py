#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,struct
ap=argparse.ArgumentParser();ap.add_argument('rom');ap.add_argument('output_csv');ap.add_argument('--unaligned',action='store_true');a=ap.parse_args()
d=Path(a.rom).read_bytes();step=1 if a.unaligned else 4;lo=0x08000000;hi=lo+len(d)
with Path(a.output_csv).open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['source_offset_hex','pointer_hex','target_offset_hex'])
    n=0
    for off in range(0,len(d)-3,step):
        v=struct.unpack_from('<I',d,off)[0]
        if lo<=v<hi:
            w.writerow([f'0x{off:08X}',f'0x{v:08X}',f'0x{v-lo:08X}']);n+=1
print('pointer candidates',n)
