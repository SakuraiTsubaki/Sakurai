#!/usr/bin/env python3
from __future__ import annotations
import csv, json, hashlib, math, re
from collections import Counter, defaultdict
from pathlib import Path

BANK=0x4000
ROOT=Path(__file__).resolve().parents[2]
V3=ROOT/'v3'
ROM_DIR=Path('/mnt/data')
CFG=json.loads((ROOT/'config/roms.json').read_text())
ROM_FILES={r['code']: ROM_DIR/r['filename'] for r in CFG['roms']}

SEM_REF={}
with (ROOT/'reports/en_semantic_bank_reference.csv').open(newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f): SEM_REF[int(row['en_bank_hex'],16)]=row

CROSS={}
cp=ROOT/'reports/semantic_bank_crosswalk_best.csv'
if cp.exists():
    with cp.open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            CROSS[(row['target'],int(row['target_bank_hex'],16))]=row

BANK_META={}
with (ROOT/'manifest/bank_manifest.csv').open(newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f): BANK_META[(row['rom_code'],int(row['bank']))]=row

PRINTABLE_WEST=set(range(0x60,0xC0))|set(range(0xE0,0x100))|{0x7F}
PRINTABLE_JP=(set(range(0x05,0x14))|set(range(0x19,0x1D))|set(range(0x26,0x35))|set(range(0x3A,0x3F))|
              set(range(0x40,0x49))|set(range(0x70,0x76))|{0x7F}|set(range(0x80,0xE9))|{0xF0}|set(range(0xF2,0xF5))|set(range(0xF6,0x100)))

def cpu_addr(off:int)->int:
    bank=off//BANK; within=off%BANK
    return within if bank==0 else 0x4000+within

def addrstr(off:int)->str:
    return f"{off//BANK:02X}:{cpu_addr(off):04X}"

def cats(sem:str)->list[str]:
    s=sem.lower(); out=[]
    rules=[
      ('AUDIO',['audio','music','sound']),('GRAPHICS',['pic','sprite','font','diploma']),
      ('BATTLE',['battle']),('MAPS',['map','doors','ledges']),('EVENTS',['event','guards','trainer sight','fossil','vending','itemfinder']),
      ('TEXT',['text']),('POKEDEX',['pokedex','pokédex','starter dex']),('NAMES',['names']),
      ('TILESETS',['tileset']),('SYSTEM',['rom0','header','home','predef','play time','screen effects','slot machines','bills pc',"bill's pc"])]
    for cat,keys in rules:
        if any(k in s for k in keys): out.append(cat)
    if not out or re.fullmatch(r'bank[0-9a-f]+',s.strip()): out.append('UNKNOWN')
    return sorted(set(out))

def extractor_for(tags:list[str], blank:bool)->str:
    if blank: return 'free_space_reference_audit'
    order=[('TEXT','text_pointer_extractor'),('POKEDEX','pokedex_extractor'),('NAMES','name_table_extractor'),
           ('GRAPHICS','gfx_2bpp_extractor'),('TILESETS','tileset_extractor'),('MAPS','map_event_extractor'),
           ('EVENTS','map_event_extractor'),('AUDIO','audio_extractor'),('BATTLE','gbz80_code_disassembly'),('SYSTEM','gbz80_code_disassembly')]
    for k,v in order:
        if k in tags:return v
    return 'manual_structural_survey'

def semantic_for(code:str,b:int):
    blank=BANK_META[(code,b)]['all_zero']=='True'
    if blank:
        return 'PHYSICAL BLANK BANK','EXACT','bank is 100% 0x00 in supplied ROM'
    if code=='EN' and b in SEM_REF:
        r=SEM_REF[b]; return r['semantic_sections'],'EXACT',r['reference']
    r=CROSS.get((code,b))
    if r and r['confidence'] in ('HIGH','MEDIUM'):
        return r['en_semantic_sections'],r['confidence'],f"exact-byte alignment to EN bank {r['best_en_bank_hex']} ({r['target_bank_fraction']})"
    if r:
        return 'UNRESOLVED',r['confidence'],f"low-confidence alignment to EN bank {r['best_en_bank_hex']}"
    return 'UNRESOLVED','NONE','no semantic mapping yet'

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def scan_pointer_tables(data:bytes, code:str):
    rows=[]
    bank_count=len(data)//BANK
    for b in range(bank_count):
        chunk=data[b*BANK:(b+1)*BANK]
        i=0
        while i+8<=BANK:
            vals=[]; j=i
            while j+1<BANK:
                v=chunk[j]|(chunk[j+1]<<8)
                if not (0x4000<=v<=0x7fff): break
                vals.append(v); j+=2
            if len(vals)>=4:
                uniq=len(set(vals)); monotonic=sum(vals[k]<=vals[k+1] for k in range(len(vals)-1))/max(1,len(vals)-1)
                rows.append({'rom_code':code,'source_bank_hex':f'{b:02X}','start_offset_hex':f'0x{b*BANK+i:06X}',
                    'start_bank_cpu':addrstr(b*BANK+i),'entry_count':len(vals),'unique_targets':uniq,
                    'target_min_hex':f'0x{min(vals):04X}','target_max_hex':f'0x{max(vals):04X}','monotonic_fraction':f'{monotonic:.3f}',
                    'classification':'16-bit pointer-table candidate','confidence':'HEURISTIC'})
                i=j
            else:i+=2
    return rows

def scan_text(data:bytes,code:str):
    printable=PRINTABLE_JP if code=='JP' else PRINTABLE_WEST
    perbank=defaultdict(lambda:{'candidates':0,'bytes':0,'max':0,'terminated':0})
    tops=[]
    for b in range(len(data)//BANK):
        chunk=data[b*BANK:(b+1)*BANK]
        starts=[-1]+[i for i,x in enumerate(chunk) if x==0x50]
        for s0,s1 in zip(starts,starts[1:]):
            s=s0+1; e=s1
            n=e-s
            if n<4 or n>512: continue
            seg=chunk[s:e]
            score=sum(x in printable for x in seg)/n
            if score>=0.78:
                d=perbank[b]; d['candidates']+=1;d['bytes']+=n;d['max']=max(d['max'],n);d['terminated']+=1
                tops.append((n,{'rom_code':code,'bank_hex':f'{b:02X}','start_offset_hex':f'0x{b*BANK+s:06X}',
                   'start_bank_cpu':addrstr(b*BANK+s),'length':n,'printable_ratio':f'{score:.3f}',
                   'terminator':'0x50','classification':'text-like candidate','confidence':'HEURISTIC'}))
    rows=[]
    for b in range(len(data)//BANK):
        d=perbank[b]; rows.append({'rom_code':code,'bank_hex':f'{b:02X}','candidate_count':d['candidates'],
          'candidate_payload_bytes':d['bytes'],'longest_candidate':d['max'],'terminated_candidates':d['terminated'],'method':'0x50-delimited glyph-byte heuristic'})
    by=defaultdict(list)
    for n,r in tops:by[(r['rom_code'],r['bank_hex'])].append((n,r))
    detail=[]
    for arr in by.values(): detail.extend([r for _,r in sorted(arr,key=lambda x:x[0],reverse=True)[:20]])
    return rows,detail

def scan_tiles(data:bytes,code:str):
    rows=[]
    for b in range(len(data)//BANK):
        chunk=data[b*BANK:(b+1)*BANK]; ent=[]; blank=0; low=0; high=0
        for i in range(0,BANK,16):
            t=chunk[i:i+16]; c=Counter(t); n=len(t); e=-sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0
            ent.append(e)
            if len(c)==1:blank+=1
            if e<=2:low+=1
            if e>=3.5:high+=1
        rows.append({'rom_code':code,'bank_hex':f'{b:02X}','tile_units':len(ent),'uniform_tiles':blank,'low_entropy_tiles_le2':low,
          'high_entropy_tiles_ge3_5':high,'mean_tile_entropy':f'{sum(ent)/len(ent):.4f}','classification':'2bpp-aligned structural statistic; not proof of graphics'})
    return rows

def scan_xrefs(data:bytes,code:str):
    rows=[]; bank_count=len(data)//BANK
    op16={0xC3:'JP',0xC2:'JP_NZ',0xCA:'JP_Z',0xD2:'JP_NC',0xDA:'JP_C',0xCD:'CALL',0xC4:'CALL_NZ',0xCC:'CALL_Z',0xD4:'CALL_NC',0xDC:'CALL_C'}
    for b in range(bank_count):
        chunk=data[b*BANK:(b+1)*BANK]; shaped=far=raw=0
        for i in range(BANK-2):
            op=chunk[i]
            if op in op16 and (chunk[i+1]|(chunk[i+2]<<8))<0x8000: shaped+=1
            bk=chunk[i]; v=chunk[i+1]|(chunk[i+2]<<8)
            if bk<bank_count and 0x4000<=v<0x8000: far+=1
        for i in range(BANK-1):
            v=chunk[i]|(chunk[i+1]<<8)
            if 0x4000<=v<0x8000:raw+=1
        rows.append({'rom_code':code,'bank_hex':f'{b:02X}','jp_call_opcode_shaped':shaped,'far_pointer_triplet_shaped':far,'raw_16bit_pointer_shaped':raw,
          'note':'candidate counts only; data bytes can resemble opcodes/pointers'})
    return rows

def main():
    wr=[]; xrefs=[]; ptrtabs=[]; textsum=[]; textdetail=[]; tiles=[]
    for code,path in ROM_FILES.items():
        data=path.read_bytes(); bank_count=len(data)//BANK
        for b in range(bank_count):
            sem,conf,evidence=semantic_for(code,b); blank=BANK_META[(code,b)]['all_zero']=='True'; tags=['FREE_SPACE'] if blank else cats(sem)
            wr.append({'rom_code':code,'bank_hex':f'{b:02X}','rom_offset_start_hex':f'0x{b*BANK:06X}','rom_offset_end_hex':f'0x{(b+1)*BANK-1:06X}',
             'semantic_sections':sem,'category_tags':'|'.join(tags),'semantic_confidence':conf,'evidence':evidence,
             'physical_state':'BLANK_00' if blank else 'POPULATED','reproducibility_state':'BYTE_EXACT_SCAFFOLD_VERIFIED',
             'next_extractor':extractor_for(tags,blank),'completion_gate':'extract -> reinsert -> original SHA-256 exact match'})
        xrefs+=scan_xrefs(data,code); ptrtabs+=scan_pointer_tables(data,code)
        a,b=scan_text(data,code);textsum+=a;textdetail+=b;tiles+=scan_tiles(data,code)
    write_csv(V3/'reports/work_unit_registry.csv',wr,list(wr[0]))
    write_csv(V3/'reports/structural_xref_summary.csv',xrefs,list(xrefs[0]))
    write_csv(V3/'reports/pointer_table_candidates.csv',ptrtabs,list(ptrtabs[0]))
    write_csv(V3/'reports/text_candidate_summary.csv',textsum,list(textsum[0]))
    write_csv(V3/'reports/text_candidate_top20_per_bank.csv',textdetail,list(textdetail[0]))
    write_csv(V3/'reports/tile_unit_statistics.csv',tiles,list(tiles[0]))
    cov=[]
    for code in ROM_FILES:
        rr=[r for r in wr if r['rom_code']==code]; c=Counter(r['semantic_confidence'] for r in rr); catsc=Counter()
        for r in rr:
            for t in r['category_tags'].split('|'):catsc[t]+=1
        cov.append({'rom_code':code,'banks':len(rr),'bytes':len(ROM_FILES[code].read_bytes()),'exact_semantic_banks':c['EXACT'],'high_semantic_banks':c['HIGH'],
         'medium_semantic_banks':c['MEDIUM'],'low_or_unresolved_banks':c['LOW']+c['NONE'],'category_bank_counts':' '.join(f'{k}:{v}' for k,v in sorted(catsc.items()))})
    write_csv(V3/'reports/semantic_work_coverage.csv',cov,list(cov[0]))
    man={'schema_version':3,'purpose':'ROM-free reproducible whole-ROM analysis/work-unit pipeline','bank_size':BANK,
         'roms':[], 'reports':[p.name for p in sorted((V3/'reports').glob('*.csv'))],
         'policy':{'source_roms':'local read-only','committed_raw_rom_bytes':False,'candidate_scans':'heuristic unless explicitly marked EXACT/HIGH/MEDIUM','semantic_completion_gate':'extract/reinsert must reproduce original SHA-256 exactly'}}
    for code,path in ROM_FILES.items():
        d=path.read_bytes();man['roms'].append({'code':code,'filename_reference':path.name,'size':len(d),'sha256':hashlib.sha256(d).hexdigest(),'banks':len(d)//BANK})
    (V3/'reports/v3_manifest.json').write_text(json.dumps(man,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"generated v3: {len(wr)} bank work units; {len(ptrtabs)} pointer-table candidates; {len(textdetail)} text candidate detail rows")

if __name__=='__main__':main()
