#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from common import parse_lz77
ap=argparse.ArgumentParser();ap.add_argument('rom');ap.add_argument('output_csv');a=ap.parse_args();d=Path(a.rom).read_bytes();rows=[];p=0
while True:
    p=d.find(b'\x10',p)
    if p<0:break
    q=parse_lz77(d,p)
    if q:
        dec,span=q;rows.append((f'0x{p:08X}',dec,span,hashlib.sha256(d[p:p+span]).hexdigest()))
    p+=1
with Path(a.output_csv).open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['offset_hex','decompressed_size','compressed_span','compressed_sha256']);w.writerows(rows)
print('validated candidates',len(rows))
