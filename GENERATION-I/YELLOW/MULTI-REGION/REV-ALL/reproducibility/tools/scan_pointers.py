#!/usr/bin/env python3
from pathlib import Path
import sys,csv
if len(sys.argv)<2:raise SystemExit('usage: scan_pointers.py ROM [OUT.csv]')
b=Path(sys.argv[1]).read_bytes();out=open(sys.argv[2],'w',newline='') if len(sys.argv)>2 else sys.stdout;w=csv.writer(out);w.writerow(['source_offset','source_bank','kind','value','target_offset'])
for bank in range((len(b)+0x3fff)//0x4000):
    ch=b[bank*0x4000:(bank+1)*0x4000]
    for j in range(len(ch)-1):
        v=ch[j]|(ch[j+1]<<8)
        if bank==0 and v<0x4000:w.writerow([f'0x{bank*0x4000+j:06X}',f'{bank:02X}','bank0',f'0x{v:04X}',f'0x{v:06X}'])
        elif bank>0 and 0x4000<=v<0x8000:w.writerow([f'0x{bank*0x4000+j:06X}',f'{bank:02X}','same-bank',f'0x{v:04X}',f'0x{bank*0x4000+v-0x4000:06X}'])
