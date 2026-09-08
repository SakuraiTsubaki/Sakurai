#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,pathlib
BANK_SIZE=0x4000;PAGE_SIZE=0x100

def resolve_rom(cp,item):
    p=pathlib.Path(item['path']); return p if p.is_absolute() else (cp.resolve().parent/p).resolve()
def cpu_addr(bank,off): return off if bank==0 else 0x4000+off
def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();cp=pathlib.Path(a.catalog);cat=json.loads(cp.read_text());root=pathlib.Path(a.output);summary={}
    for item in cat['roms']:
        size=resolve_rom(cp,item).stat().st_size;od=root/item['output_subdir'];banks=[];pages=[]
        for bank,start in enumerate(range(0,size,BANK_SIZE)):
            n=min(BANK_SIZE,size-start);banks.append({'bank_hex':f'{bank:02X}','bank_dec':bank,'file_start_hex':f'{start:06X}','file_end_exclusive_hex':f'{start+n:06X}','offset_in_bank_start_hex':'0000','offset_in_bank_end_exclusive_hex':f'{n:04X}','cpu_start_hex':f'{cpu_addr(bank,0):04X}','cpu_end_inclusive_hex':f'{cpu_addr(bank,n-1):04X}','window':'ROM0' if bank==0 else 'ROMX'})
            for p in range(0,n,PAGE_SIZE):
                ps=min(PAGE_SIZE,n-p);pages.append({'bank_hex':f'{bank:02X}','page_in_bank_hex':f'{p//PAGE_SIZE:02X}','file_start_hex':f'{start+p:06X}','file_end_exclusive_hex':f'{start+p+ps:06X}','cpu_start_hex':f'{cpu_addr(bank,p):04X}','cpu_end_inclusive_hex':f'{cpu_addr(bank,p+ps-1):04X}','window':'ROM0' if bank==0 else 'ROMX'})
        write_csv(od/'address_map_banks.csv',banks);write_csv(od/'address_map_pages.csv',pages);summary[item['label']]={'banks':len(banks),'pages':len(pages),'bytes':size}
    out=root/'MULTI-REGION'/'REV-MIXED'/'ROM-REPRODUCIBILITY'/'address_map_summary.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
