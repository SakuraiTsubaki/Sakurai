#!/usr/bin/env python3
"""Scan a GBA ROM for structurally valid BIOS-LZ77 (type 0x10) streams.

This is a structural census tool. A hit is not automatically a sprite or other
semantic asset. Output is TSV and contains no ROM bytes.
"""
import argparse, csv, hashlib
from pathlib import Path

def parse_stream(data, off, max_output=0x400000):
    if off + 4 > len(data) or data[off] != 0x10:
        return None
    out_len = data[off+1] | data[off+2] << 8 | data[off+3] << 16
    if not (0 < out_len <= max_output):
        return None
    p, made = off + 4, 0
    while made < out_len:
        if p >= len(data): return None
        flags = data[p]; p += 1
        for bit in range(8):
            if made >= out_len: break
            if flags & (0x80 >> bit):
                if p + 1 >= len(data): return None
                a, b = data[p], data[p+1]; p += 2
                length = (a >> 4) + 3
                disp = ((a & 0x0F) << 8 | b) + 1
                if disp > made: return None
                made += min(length, out_len - made)
            else:
                if p >= len(data): return None
                p += 1; made += 1
    return out_len, p - off

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom')
    ap.add_argument('output_tsv')
    ap.add_argument('--alignment', type=int, default=4)
    a=ap.parse_args()
    data=Path(a.rom).read_bytes()
    rows=[]
    for off in range(0, len(data)-4, a.alignment):
        hit=parse_stream(data, off)
        if hit:
            out_len, comp_len=hit
            rows.append((f'0x{off:08X}', off, off//0x10000, out_len, comp_len))
    with open(a.output_tsv,'w',newline='') as f:
        w=csv.writer(f,delimiter='\t')
        w.writerow(['offset_hex','offset_dec','bank64k','decompressed_size','compressed_size'])
        w.writerows(rows)
    print('sha256', hashlib.sha256(data).hexdigest())
    print('candidates', len(rows))
if __name__=='__main__': main()
