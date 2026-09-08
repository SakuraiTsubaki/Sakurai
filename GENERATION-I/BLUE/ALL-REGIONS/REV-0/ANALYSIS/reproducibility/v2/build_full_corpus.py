#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math, zlib
from collections import Counter, defaultdict
from pathlib import Path

BANK=0x4000
CHUNK=0x100

def sha256(b): return hashlib.sha256(b).hexdigest()
def entropy(data: bytes) -> float:
    if not data: return 0.0
    c=Counter(data); n=len(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
def cpu_addr(bank:int, inbank:int)->int:
    return inbank if bank==0 else 0x4000+inbank

def load_cfg(root:Path):
    return json.loads((root/'config/roms.json').read_text(encoding='utf-8'))

def resolve_roms(root:Path, rom_dir:Path):
    cfg=load_cfg(root); out=[]
    manifest=json.loads((root/'manifest/rom_manifest.json').read_text(encoding='utf-8'))
    by_code={r['code']:r for r in manifest}
    for r in cfg['roms']:
        p=rom_dir/r['filename']
        if not p.exists(): raise SystemExit(f'missing ROM: {p}')
        data=p.read_bytes(); exp=by_code[r['code']]['sha256']; got=sha256(data)
        if got!=exp: raise SystemExit(f"SHA-256 mismatch {r['code']}: {got} != {exp}")
        out.append((r,p,data))
    return out

def build_chunk_ledger(root, roms):
    out=root/'reports/chunk_ledger_256.csv'
    fields=['code','locale','bank_hex','chunk_hex','file_start','file_end','cpu_start','cpu_end','sha256','crc32','entropy','zero_bytes','ff_bytes','unique_bytes','class']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for meta,p,data in roms:
            for off in range(0,len(data),CHUNK):
                b=data[off:off+CHUNK]; bank=off//BANK; ib=off%BANK; c=Counter(b)
                if all(x==0 for x in b): cls='ALL_00'
                elif all(x==0xff for x in b): cls='ALL_FF'
                elif c[0]>=len(b)*0.9: cls='MOSTLY_00'
                elif c[0xff]>=len(b)*0.9: cls='MOSTLY_FF'
                else: cls='MIXED'
                w.writerow({'code':meta['code'],'locale':meta['locale'],'bank_hex':f'{bank:02X}','chunk_hex':f'{ib//CHUNK:02X}','file_start':f'0x{off:06X}','file_end':f'0x{off+len(b)-1:06X}','cpu_start':f'0x{cpu_addr(bank,ib):04X}','cpu_end':f'0x{cpu_addr(bank,ib+len(b)-1):04X}','sha256':sha256(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','entropy':f'{entropy(b):.6f}','zero_bytes':c[0],'ff_bytes':c[0xff],'unique_bytes':len(c),'class':cls})

def build_scaffold(root, roms):
    sroot=root/'scaffold'; index=[]
    for meta,p,data in roms:
        code=meta['code']; d=sroot/code; (d/'banks').mkdir(parents=True,exist_ok=True); includes=[]
        for bank in range(len(data)//BANK):
            fn=f'banks/bank_{bank:02X}.asm'; includes.append(f'INCLUDE "{fn}"')
            lines=[f'; {code} bank ${bank:02X} byte-exact editable scaffold','; Replace individual INCBIN chunks with decoded source only after exact equivalence is proven.',f'SECTION "{code} Bank {bank:02X}", {"ROM0[$0000]" if bank==0 else f"ROMX[$4000], BANK[${bank:02X}]"}','']
            for ci in range(BANK//CHUNK):
                off=bank*BANK+ci*CHUNK; label=f'{code}_B{bank:02X}_C{ci:02X}'
                lines += [f'{label}::',f'    INCBIN "baserom.gb", ${off:06X}, ${CHUNK:04X}','']
                index.append((code,bank,ci,off,off+CHUNK-1,label,fn))
            (d/fn).write_text('\n'.join(lines),encoding='utf-8')
        (d/'rom.asm').write_text('; Auto-generated full-ROM scaffold\n'+'\n'.join(includes)+'\n',encoding='utf-8')
    with (sroot/'scaffold_index.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['code','bank_hex','chunk_hex','file_start','file_end','label','asm_file'])
        for code,b,c,s,e,l,fn in index: w.writerow([code,f'{b:02X}',f'{c:02X}',f'0x{s:06X}',f'0x{e:06X}',l,fn])

def unique_anchor_map(a:bytes,b:bytes,step=16,block=32):
    ia=defaultdict(list); ib=defaultdict(list)
    def fillish(x): return len(set(x))<=2 and (x.count(0)>=len(x)*0.9 or x.count(255)>=len(x)*0.9)
    for i in range(0,len(a)-block+1,step):
        x=a[i:i+block]
        if not fillish(x): ia[hashlib.blake2s(x,digest_size=12).digest()].append(i)
    for i in range(0,len(b)-block+1,step):
        x=b[i:i+block]
        if not fillish(x): ib[hashlib.blake2s(x,digest_size=12).digest()].append(i)
    pairs=[]
    for h,pa in ia.items():
        pb=ib.get(h)
        if len(pa)==1 and pb and len(pb)==1 and a[pa[0]:pa[0]+block]==b[pb[0]:pb[0]+block]: pairs.append((pa[0],pb[0]))
    pairs.sort(); runs=[]
    if not pairs: return runs
    sa,sb=pairs[0]; la,lb=sa,sb
    for xa,xb in pairs[1:]:
        if xa-la==step and xb-lb==step and (xa-xb)==(la-lb): la,lb=xa,xb; continue
        runs.append((sa,sb,(la-sa)+block)); sa,sb=xa,xb; la,lb=xa,xb
    runs.append((sa,sb,(la-sa)+block)); return runs

def build_alignments(root,roms):
    by={m['code']:d for m,p,d in roms}; pairs=[('EN','JP'),('EN','DE'),('EN','FR'),('EN','IT'),('EN','ES')]; rows=[]
    for a,b in pairs:
        for sa,sb,n in unique_anchor_map(by[a],by[b]): rows.append((a,b,sa,sb,n,sb-sa,sha256(by[a][sa:sa+n])))
    with (root/'reports/exact_alignment_runs.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['source','target','source_start','target_start','length','target_minus_source','sha256'])
        for r in rows: w.writerow([r[0],r[1],f'0x{r[2]:06X}',f'0x{r[3]:06X}',r[4],r[5],r[6]])
    sums=defaultdict(lambda:[0,0])
    for a,b,sa,sb,n,delta,h in rows: sums[(a,b)][0]+=1; sums[(a,b)][1]+=n
    with (root/'reports/exact_alignment_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['source','target','run_count','exact_bytes_in_runs'])
        for k,v in sorted(sums.items()): w.writerow([*k,*v])

def build_pointer_summary(root,roms):
    rows=[]; farrows=[]
    for meta,p,data in roms:
        code=meta['code']; nbank=len(data)//BANK; target_counts=Counter(); far_counts=Counter()
        for off in range(len(data)-1):
            v=data[off] | (data[off+1]<<8); bank=off//BANK; to=None; kind=None
            if v<0x4000: to=v; kind='ROM0_16'
            elif 0x4000<=v<0x8000 and bank>0: to=bank*BANK+(v-0x4000); kind='SAME_BANK_16'
            if to is not None and to<len(data): target_counts[(kind,to)]+=1
        for off in range(len(data)-2):
            bank=data[off]; addr=data[off+1] | (data[off+2]<<8)
            if 1<=bank<nbank and 0x4000<=addr<0x8000: far_counts[bank*BANK+(addr-0x4000)]+=1
        for (kind,to),cnt in target_counts.most_common(1000): rows.append((code,kind,to,cnt))
        for to,cnt in far_counts.most_common(1000): farrows.append((code,'BANK_ADDR_24',to,cnt))
    for name,rr in [('pointer_target_hotspots.csv',rows),('far_pointer_target_hotspots.csv',farrows)]:
        with (root/'reports'/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['code','hypothesis','target_file_offset','candidate_reference_count'])
            for code,kind,to,cnt in rr: w.writerow([code,kind,f'0x{to:06X}',cnt])

def build_coverage(root,roms):
    rows=[]; ok=True
    for meta,p,data in roms:
        banks=len(data)//BANK; chunks=len(data)//CHUNK; covered=chunks*CHUNK; passed=covered==len(data) and len(data)%BANK==0; ok &= passed
        rows.append((meta['code'],len(data),banks,chunks,covered,passed))
    with (root/'reports/coverage_proof.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['code','rom_bytes','banks','chunks_0x100','covered_bytes','exact_cover']); w.writerows(rows)
    if not ok: raise SystemExit('coverage proof failed')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--rom-dir',type=Path,required=True)
    a=ap.parse_args(); roms=resolve_roms(a.root,a.rom_dir); build_chunk_ledger(a.root,roms); build_scaffold(a.root,roms); build_alignments(a.root,roms); build_pointer_summary(a.root,roms); build_coverage(a.root,roms)
    print('full corpus generated for',','.join(m['code'] for m,p,d in roms))
if __name__=='__main__': main()
