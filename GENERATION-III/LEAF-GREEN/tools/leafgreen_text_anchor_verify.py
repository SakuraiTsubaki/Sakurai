#!/usr/bin/env python3
"""Verify confirmed LeafGreen fixed text/name table boundaries without exporting ROM text."""
from pathlib import Path
import argparse,csv

SPECIES = {
    'BPGJ': (0x0203C94, 6),
}
INTERNATIONAL_SPECIES = {
    ('BPGD',0):0x0245D8C, ('BPGS',0):0x0241628, ('BPGE',0):0x0245EBC,
    ('BPGE',1):0x0245F2C, ('BPGF',0):0x02402C8, ('BPGI',0):0x023EF60,
}
ITEMS = {
    ('BPGD',0):0x03DA354, ('BPGS',0):0x03D4D8C, ('BPGE',0):0x03DAE64,
    ('BPGE',1):0x03DAED4, ('BPGF',0):0x03D3160, ('BPGI',0):0x03D1D24,
}

def has_term(record: bytes) -> bool:
    return 0xFF in record

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom_dir',type=Path);ap.add_argument('out_csv',type=Path);a=ap.parse_args()
    rows=[]
    for p in sorted(a.rom_dir.glob('*.gba')):
        b=p.read_bytes(); code=b[0xAC:0xB0].decode('ascii','replace'); rev=b[0xBC]
        if code=='BPGJ': species,w=SPECIES[code]
        else: species,w=INTERNATIONAL_SPECIES[(code,rev)],11
        move=species+412*w; mw=8 if code=='BPGJ' else 13
        type_off=0x020C050 if code=='BPGJ' else species+0x92C0; tw=5 if code=='BPGJ' else 7
        checks={
            'species_412_all_terminated': all(has_term(b[species+i*w:species+(i+1)*w]) for i in range(412)),
            'moves_355_all_terminated': all(has_term(b[move+i*mw:move+(i+1)*mw]) for i in range(355)),
            'types_18_all_terminated': all(has_term(b[type_off+i*tw:type_off+(i+1)*tw]) for i in range(18)),
        }
        if code!='BPGJ':
            item=ITEMS[(code,rev)]
            checks['items_375_name_fields_terminated']=all(has_term(b[item+i*44:item+i*44+14]) for i in range(375))
        rows.append({'file':p.name,'game_code':code,'revision':rev,**checks})
    with a.out_csv.open('w',newline='',encoding='utf-8') as f:
        fields=[]
        for r in rows:
            for k in r:
                if k not in fields: fields.append(k)
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

if __name__=='__main__':main()
