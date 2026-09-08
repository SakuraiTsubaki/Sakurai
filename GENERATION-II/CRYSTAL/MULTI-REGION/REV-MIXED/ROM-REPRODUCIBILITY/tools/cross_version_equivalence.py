#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,pathlib
from collections import defaultdict
BANK_SIZE=0x4000;PAGE_SIZE=0x100

def sha256(b):return hashlib.sha256(b).hexdigest()
def resolve(cp,item):
    p=pathlib.Path(item['path']);return p if p.is_absolute() else (cp.resolve().parent/p).resolve()
def groups(chunks):
    g=defaultdict(list)
    for label,data in chunks:g[sha256(data)].append(label)
    x=sorted((sorted(v) for v in g.values()),key=lambda y:(y[0],len(y)));return len(x),' | '.join(','.join(v) for v in x)
def write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();cp=pathlib.Path(a.catalog);cat=json.loads(cp.read_text());roms=[(i['label'],resolve(cp,i).read_bytes()) for i in cat['roms']];sizes={len(d) for _,d in roms}
    if len(sizes)!=1:raise SystemExit('all ROMs must have equal size')
    size=next(iter(sizes));br=[];pr=[]
    for bank,start in enumerate(range(0,size,BANK_SIZE)):
        n,g=groups([(l,d[start:start+BANK_SIZE]) for l,d in roms]);br.append({'bank_hex':f'{bank:02X}','file_start_hex':f'{start:06X}','unique_payload_count':n,'all_identical':int(n==1),'equivalence_groups':g})
    for start in range(0,size,PAGE_SIZE):
        bank=start//BANK_SIZE;page=(start%BANK_SIZE)//PAGE_SIZE;n,g=groups([(l,d[start:start+PAGE_SIZE]) for l,d in roms]);pr.append({'bank_hex':f'{bank:02X}','page_in_bank_hex':f'{page:02X}','file_start_hex':f'{start:06X}','unique_payload_count':n,'all_identical':int(n==1),'equivalence_groups':g})
    out=pathlib.Path(a.output)/'MULTI-REGION'/'REV-MIXED'/'ROM-REPRODUCIBILITY';write(out/'same_offset_bank_equivalence.csv',br);write(out/'same_offset_page_equivalence.csv',pr);s={'rom_count':len(roms),'bank_count':len(br),'page_count':len(pr),'all_identical_banks':sum(r['all_identical'] for r in br),'all_identical_pages':sum(r['all_identical'] for r in pr),'nonidentical_banks':sum(not r['all_identical'] for r in br),'nonidentical_pages':sum(not r['all_identical'] for r in pr)};(out/'same_offset_equivalence_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
if __name__=='__main__':main()
