#!/usr/bin/env python3
from pathlib import Path
import re,csv,sys
if len(sys.argv)<3: raise SystemExit('usage: parse_pret_symbols.py pokeyellow.map pokeyellow.sym [outdir]')
mapf=Path(sys.argv[1]); symf=Path(sys.argv[2]); out=Path(sys.argv[3]) if len(sys.argv)>3 else Path('parsed_symbols'); out.mkdir(parents=True,exist_ok=True)
section_re=re.compile(r'^\s*SECTION: \$([0-9a-fA-F]{4})(?:-\$([0-9a-fA-F]{4}))? \(\$([0-9a-fA-F]{4}) bytes?\) \["(.*)"\]')
bank_re=re.compile(r'^(ROM0|ROMX) bank #(\d+):')
rows=[]; bank=None; kind=None
for line in mapf.read_text(encoding='utf-8').splitlines():
    m=bank_re.match(line)
    if m: kind=m.group(1); bank=int(m.group(2)); continue
    m=section_re.match(line)
    if m and bank is not None:
        start=int(m.group(1),16); end=int(m.group(2) or m.group(1),16); size=int(m.group(3),16); name=m.group(4)
        file_start=start if bank==0 else bank*0x4000+(start-0x4000)
        rows.append({'bank_hex':f'{bank:02X}','kind':kind,'section':name,'cpu_start':f'0x{start:04X}','cpu_end':f'0x{end:04X}','file_start':f'0x{file_start:06X}','file_end':f'0x{file_start+size-1:06X}','size':size})
with open(out/'sections.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
srows=[]
for line in symf.read_text(encoding='utf-8').splitlines():
    if not line or line.startswith(';'): continue
    m=re.match(r'^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(.+)$',line)
    if not m: continue
    bank=int(m.group(1),16); addr=int(m.group(2),16); name=m.group(3)
    fileoff=addr if bank==0 else bank*0x4000+(addr-0x4000)
    srows.append({'bank_hex':f'{bank:02X}','cpu_address':f'0x{addr:04X}','file_offset':f'0x{fileoff:06X}','symbol':name})
with open(out/'symbols.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(srows[0])); w.writeheader(); w.writerows(srows)
print('sections',len(rows),'symbols',len(srows))
