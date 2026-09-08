#!/usr/bin/env python3
"""Scan for raw 16-bit little-endian pointer-shaped words.
Candidate generator only; semantic reference validation is required later.
"""
import argparse,csv
from pathlib import Path
BANK=0x4000

def main():
    p=argparse.ArgumentParser(); p.add_argument('rom',type=Path); p.add_argument('-o','--out',type=Path,required=True); p.add_argument('--mode',choices=['home','switch','both'],default='both'); a=p.parse_args()
    d=a.rom.read_bytes(); a.out.parent.mkdir(parents=True,exist_ok=True)
    fields=['source_offset','source_offset_hex','source_bank_hex','source_cpu_address_hex','word_hex','target_window']
    with a.out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for off in range(len(d)-1):
            word=d[off]|(d[off+1]<<8); target=None
            if word<0x4000 and a.mode in ('home','both'): target='ROM0_0000_3FFF'
            elif 0x4000<=word<0x8000 and a.mode in ('switch','both'): target='ROMX_4000_7FFF'
            if target is None: continue
            bank=off//BANK; cpu=off if bank==0 else 0x4000+(off%BANK)
            w.writerow({'source_offset':off,'source_offset_hex':f'0x{off:06X}','source_bank_hex':f'0x{bank:02X}','source_cpu_address_hex':f'0x{cpu:04X}','word_hex':f'0x{word:04X}','target_window':target})
if __name__=='__main__': main()
