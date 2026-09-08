#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,pathlib
from collections import Counter
BANK_SIZE=0x4000

def resolve(cp,item):
    p=pathlib.Path(item['path']);return p if p.is_absolute() else (cp.resolve().parent/p).resolve()
def classify(v):
    if v<0x4000:return 'ROM0'
    if v<0x8000:return 'ROMX'
    if v<0xA000:return 'VRAM'
    if v<0xC000:return 'SRAM'
    if v<0xE000:return 'WRAM'
    if v<0xFE00:return 'ECHO'
    if v<0xFEA0:return 'OAM'
    if v<0xFF00:return 'UNUSABLE'
    if v<0xFF80:return 'IO'
    if v<0xFFFF:return 'HRAM'
    return 'IE'
def write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();cp=pathlib.Path(a.catalog);cat=json.loads(cp.read_text());root=pathlib.Path(a.output);classes=['ROM0','ROMX','VRAM','SRAM','WRAM','ECHO','OAM','UNUSABLE','IO','HRAM','IE'];summary={}
    for item in cat['roms']:
        d=resolve(cp,item).read_bytes();rows=[];tot=Counter()
        for bank,start in enumerate(range(0,len(d),BANK_SIZE)):
            end=min(start+BANK_SIZE,len(d));c=Counter(classify(d[o]|(d[o+1]<<8)) for o in range(start,end-1));r={'bank_hex':f'{bank:02X}','candidate_words':sum(c.values())};r.update({k:c[k] for k in classes});rows.append(r);tot.update(c)
        write(root/item['output_subdir']/'pointer_word_target_class_counts_by_bank.csv',rows);summary[item['label']]={'candidate_words':sum(tot.values()),**{k:tot[k] for k in classes}}
    out=root/'MULTI-REGION'/'REV-MIXED'/'ROM-REPRODUCIBILITY'/'pointer_sweep_summary.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
