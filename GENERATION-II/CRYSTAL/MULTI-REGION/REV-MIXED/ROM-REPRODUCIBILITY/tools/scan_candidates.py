#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,pathlib
from collections import Counter
BANK=0x4000

# Immediate 16-bit absolute branch/call opcodes on LR35902.
OPS={0xC3:'JP',0xC2:'JP_NZ',0xCA:'JP_Z',0xD2:'JP_NC',0xDA:'JP_C',
     0xCD:'CALL',0xC4:'CALL_NZ',0xCC:'CALL_Z',0xD4:'CALL_NC',0xDC:'CALL_C'}

def write_csv(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def scan(path: pathlib.Path,out: pathlib.Path):
    d=path.read_bytes(); rows=[]; counts=Counter()
    for off in range(len(d)-2):
        op=d[off]
        if op not in OPS: continue
        target=d[off+1]|(d[off+2]<<8)
        # Filter to ROM address space only. This is pattern-level, not proof of code.
        if target>=0x8000: continue
        bank=off//BANK; cpu=(off if bank==0 else 0x4000+(off%BANK))
        rows.append({'file_offset_hex':f'{off:06X}','source_bank_hex':f'{bank:02X}',
                     'source_cpu_hex':f'{cpu:04X}','opcode_hex':f'{op:02X}','mnemonic':OPS[op],
                     'target_cpu_hex':f'{target:04X}','target_class':'ROM0' if target<0x4000 else 'ROMX'})
        counts[(bank,OPS[op])]+=1
    write_csv(out/'branch_call_immediate_candidates.csv',rows,list(rows[0]) if rows else ['file_offset_hex','source_bank_hex','source_cpu_hex','opcode_hex','mnemonic','target_cpu_hex','target_class'])
    summ=[]
    for bank in range((len(d)+BANK-1)//BANK):
        r={'bank_hex':f'{bank:02X}','total_candidates':sum(v for (b,_),v in counts.items() if b==bank)}
        for m in sorted(set(OPS.values())): r[m]=counts[(bank,m)]
        summ.append(r)
    write_csv(out/'branch_call_candidate_counts_by_bank.csv',summ,list(summ[0]))
    return len(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    cat=json.loads(pathlib.Path(a.catalog).read_text()); root=pathlib.Path(a.output); result={}
    for item in cat['roms']:
        rom=pathlib.Path(item['path']); rom=rom if rom.is_absolute() else (pathlib.Path(a.catalog).resolve().parent/rom).resolve()
        result[item['label']]=scan(rom,root/item['output_subdir'])
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
