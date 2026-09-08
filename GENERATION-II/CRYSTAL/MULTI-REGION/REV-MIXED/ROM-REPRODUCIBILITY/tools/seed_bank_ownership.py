#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,pathlib
BANK_SIZE=0x4000

def sha256(b):return hashlib.sha256(b).hexdigest()
def resolve(cp,item):
    p=pathlib.Path(item['path']);return p if p.is_absolute() else (cp.resolve().parent/p).resolve()
def read_roles(path):
    with pathlib.Path(path).open(encoding='utf-8') as f:return {int(r['bank_hex'],16):r for r in csv.DictReader(f)}
def write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',required=True);ap.add_argument('--roles',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();cp=pathlib.Path(a.catalog);cat=json.loads(cp.read_text());roles=read_roles(a.roles);root=pathlib.Path(a.output);roms={i['label']:resolve(cp,i).read_bytes() for i in cat['roms']};items={i['label']:i for i in cat['roms']};en0=roms.get('USA-EUROPE_REV0');en1=roms.get('USA-EUROPE_REV1');summary={}
    for label,d in roms.items():
        rows=[];high=tent=0
        for bank,start in enumerate(range(0,len(d),BANK_SIZE)):
            chunk=d[start:start+BANK_SIZE];same0=en0 is not None and chunk==en0[start:start+BANK_SIZE];same1=en1 is not None and chunk==en1[start:start+BANK_SIZE]
            if label in ('USA-EUROPE_REV0','USA-EUROPE_REV1'):conf='authoritative-layout';basis='exact English source target'
            elif same0 or same1:conf='high';basis='byte-identical same-offset bank to '+('EN Rev0+Rev1' if same0 and same1 else ('EN Rev0' if same0 else 'EN Rev1'));high+=1
            else:conf='tentative';basis='same bank-number role inferred from English layout; requires regional structural proof';tent+=1
            rows.append({'bank_hex':f'{bank:02X}','file_start_hex':f'{start:06X}','file_end_exclusive_hex':f'{start+len(chunk):06X}','sha256':sha256(chunk),'semantic_role_summary':roles.get(bank,{'semantic_role_summary':'unknown'})['semantic_role_summary'],'role_confidence':conf,'role_basis':basis,'same_as_en_rev0':int(bool(same0)),'same_as_en_rev1':int(bool(same1)),'ownership_granularity':'whole-bank seed','semantic_complete':0})
        write(root/items[label]['output_subdir']/'bank_ownership_seed.csv',rows);summary[label]={'banks':len(rows),'high_confidence_inherited_regional_banks':high,'tentative_regional_banks':tent}
    out=root/'MULTI-REGION'/'REV-MIXED'/'ROM-REPRODUCIBILITY'/'bank_ownership_seed_summary.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
