#!/usr/bin/env python3
from pathlib import Path
import hashlib, csv, json, sys

ROM_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
OUT_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('out')
OUT_DIR.mkdir(parents=True, exist_ok=True)


def sha(data, name):
    h = hashlib.new(name); h.update(data); return h.hexdigest()

def header_checksum(data):
    calc = (-(sum(data[0xA0:0xBD]) + 0x19)) & 0xFF
    return calc, data[0xBD], calc == data[0xBD]

def trailing_ff(data):
    i = len(data)
    while i and data[i-1] == 0xFF:
        i -= 1
    return len(data)-i, i

def diff_summary(a, b):
    pos=[]
    for i in range(max(len(a),len(b))):
        av=a[i] if i < len(a) else None
        bv=b[i] if i < len(b) else None
        if av != bv: pos.append(i)
    ranges=[]
    if pos:
        s=p=pos[0]
        for x in pos[1:]:
            if x == p+1: p=x
            else: ranges.append((s,p)); s=p=x
        ranges.append((s,p))
    return pos, ranges

files=sorted(ROM_DIR.glob('*.gba'))
records=[]
blob={}
for p in files:
    b=p.read_bytes(); blob[p.name]=b
    calc,stored,ok=header_checksum(b)
    ff,ff_start=trailing_ff(b)
    records.append({
        'file':p.name,'size_bytes':len(b),'size_mib':len(b)/(1024*1024),
        'md5':sha(b,'md5'),'sha1':sha(b,'sha1'),'sha256':sha(b,'sha256'),
        'title':b[0xA0:0xAC].decode('ascii','replace').rstrip('\0'),
        'game_code':b[0xAC:0xB0].decode('ascii','replace'),
        'maker_code':b[0xB0:0xB2].decode('ascii','replace'),
        'revision':b[0xBC], 'header_checksum_stored':stored,
        'header_checksum_calculated':calc,'header_checksum_valid':ok,
        'trailing_ff_bytes':ff,'trailing_ff_start':f'0x{ff_start:08X}',
    })

with (OUT_DIR/'rom_inventory.json').open('w',encoding='utf-8') as f:
    json.dump(records,f,ensure_ascii=False,indent=2)
with (OUT_DIR/'rom_inventory.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=records[0].keys()); w.writeheader(); w.writerows(records)

pairs=[
('EN US Rev0 vs EU Rev1','Pokemon - Ruby Version (USA).gba','Pokemon - Ruby Version (Europe) (Rev 1).gba','cross-region/build comparison'),
('EN EU Rev1 to USA/EU Rev2','Pokemon - Ruby Version (Europe) (Rev 1).gba','Pokemon - Ruby Version (USA, Europe) (Rev 2).gba','clean revision delta'),
('DE Rev0 to Rev1','Pokemon - Rubin-Edition (Germany).gba','Pokemon - Rubin-Edition (Germany) (Rev 1).gba','clean revision delta'),
('DE Rev0 vs Debug','Pokemon - Rubin-Edition (Germany).gba','Pokemon - Rubin-Edition (Germany) (Debug Version).gba','debug build comparison'),
('FR Rev0 to Rev1','Pokemon - Version Rubis (France).gba','Pokemon - Version Rubis (France) (Rev 1).gba','clean revision delta'),
('IT Rev0 to Rev1','Pokemon - Versione Rubino (Italy).gba','Pokemon - Versione Rubino (Italy) (Rev 1).gba','clean revision delta'),
('ES Rev0 to Rev1','Pokemon - Edicion Rubi (Spain).gba','Pokemon - Edicion Rubi (Spain) (Rev 1).gba','clean revision delta'),
]
rows=[]
for label,a,b,kind in pairs:
    if a not in blob or b not in blob: continue
    pos,ranges=diff_summary(blob[a],blob[b])
    rows.append({'pair':label,'kind':kind,'old_file':a,'new_file':b,
                 'different_bytes':len(pos),'contiguous_ranges':len(ranges),
                 'first_difference':f'0x{pos[0]:08X}' if pos else '',
                 'last_difference':f'0x{pos[-1]:08X}' if pos else '',
                 'first_ranges':';'.join(f'0x{s:08X}-0x{e:08X}' for s,e in ranges[:20])})
with (OUT_DIR/'revision_diff_summary.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
