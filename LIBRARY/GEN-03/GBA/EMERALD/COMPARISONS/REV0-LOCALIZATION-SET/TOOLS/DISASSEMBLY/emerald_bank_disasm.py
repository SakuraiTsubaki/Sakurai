#!/usr/bin/env python3
import argparse, csv, json, struct, subprocess, tempfile
from pathlib import Path
from collections import defaultdict, Counter

BANK=0x10000
ROM_BASE=0x08000000
ROMS={
 'JP':'/mnt/data/Pocket Monsters - Emerald (Japan).gba',
 'EN':'/mnt/data/Pokemon - Emerald Version (U).gba',
 'FR':'/mnt/data/Pokemon - Version Emeraude (France).gba',
 'DE':'/mnt/data/Pokemon - Smaragd-Edition (Germany).gba',
 'IT':'/mnt/data/Pokemon - Versione Smeraldo (Italy).gba',
 'ES':'/mnt/data/Pokemon - Edicion Esmeralda (Spain).gba',
}

EXEC_RANGES={
 'JP':[(0x000204,0x0003A4,'ARM_STARTUP'),(0x0003A4,0x1DABA4,'THUMB_MAIN'),(0x28D2F8,0x29BDA0,'LIBRARY_CODE')],
 'EN':[(0x000204,0x0003A4,'ARM_STARTUP'),(0x0003A4,0x1DB674,'THUMB_MAIN'),(0x2DED70,0x2E952E,'LIBRARY_CODE')],
 'FR':[(0x000204,0x0003A4,'ARM_STARTUP'),(0x0003A4,0x1DB2D0,'THUMB_MAIN'),(0x2E7D44,0x2F2502,'LIBRARY_CODE')],
 'DE':[(0x000204,0x0003A4,'ARM_STARTUP'),(0x0003A4,0x1DB1CC,'THUMB_MAIN'),(0x2F4AB0,0x2FF26E,'LIBRARY_CODE')],
 'IT':[(0x000204,0x0003A4,'ARM_STARTUP'),(0x0003A4,0x1DB1BC,'THUMB_MAIN'),(0x2DFCFC,0x2EA4BA,'LIBRARY_CODE')],
 'ES':[(0x000204,0x0003A4,'ARM_STARTUP'),(0x0003A4,0x1DB2D4,'THUMB_MAIN'),(0x2E64FC,0x2F0CBA,'LIBRARY_CODE')],
}

def exec_region_for_offset(lang,off):
    for a,z,name in EXEC_RANGES[lang]:
        if a<=off<z:return name
    return ''

def bank_class(lang,b):
    lo,hi=b*BANK,(b+1)*BANK
    overlaps=[]
    for a,z,name in EXEC_RANGES[lang]:
        if max(lo,a)<min(hi,z):overlaps.append((a,z,name))
    if b==0:return ('MIXED_CODE_HEADER','GBA header + ARM startup + Thumb main code')
    if overlaps:
        names='+'.join(x[2] for x in overlaps)
        covered=sum(max(0,min(hi,z)-max(lo,a)) for a,z,_ in overlaps)
        return ('CODE' if covered==BANK else 'MIXED_CODE_DATA',names)
    if 0x1E<=b<=0x2F:return ('SCRIPT_RODATA','event/script/rodata dominant outside language-specific library ranges')
    if 0x30<=b<=0xAF:return ('RODATA_DATA','rodata/text/maps/audio/tables; refine by object map')
    if 0xB0<=b<=0xB9:return ('MON_FRONT_GFX','animated Pokemon front-picture data')
    if 0xBA<=b<=0xBF:return ('PADDING_CANDIDATE','large low-information/padding region; pointer-safety pending')
    if 0xC0<=b<=0xDE:return ('GFX_DATA','main graphics payload')
    if 0xDF<=b<=0xE2:return ('PADDING_CANDIDATE','padding/empty candidate; pointer-safety pending')
    if b==0xE3:return ('EXTRA_SPARSE','sparse residual/extra data')
    if 0xE4<=b<=0xEF:return ('FREE_FF_CANDIDATE','all-region FF candidate; reference scan still required')
    if 0xF0<=b<=0xF3:return ('PADDING_VARIANT','region-dependent padding/residual differences')
    if 0xF4<=b<=0xFF:return ('FREE_FF_CANDIDATE','all-region FF candidate; reference scan still required')
    return ('UNKNOWN','')

def u16(data,o):return data[o]|(data[o+1]<<8)
def u32(data,o):return int.from_bytes(data[o:o+4],'little')

def thumb_bl_target(data,o,absolute):
    if o+4>len(data):return None
    h1,h2=u16(data,o),u16(data,o+2)
    if (h1&0xF800)!=0xF000 or (h2&0xF800)!=0xF800:return None
    hi=h1&0x7FF;lo=h2&0x7FF;off=(hi<<12)|(lo<<1)
    if hi&0x400:off-=1<<23
    return (absolute+o+4+off)&0xFFFFFFFF

def scan_rom(lang,path):
    data=Path(path).read_bytes();n=len(data);nb=n//BANK
    srcs=defaultdict(set);bl=[0]*nb;push=[0]*nb;bx=[0]*nb;pop=[0]*nb
    # Whole-ROM pointer pass: cross-bank references are credited to targets.
    for o in range(0,n-3,4):
        v=u32(data,o);tgt=v&~1
        if ROM_BASE<=tgt<ROM_BASE+n:
            if v&1:srcs[tgt].add('thumb_ptr')
            elif (v&3)==0:
                tb=(tgt-ROM_BASE)//BANK
                if tb<=0x1D or tb in (0x2D,0x2E):srcs[v].add('arm_ptr')
    # Thumb structural evidence.
    for o in range(0,n-1,2):
        h=u16(data,o);a=ROM_BASE+o;b=o//BANK
        if (h&0xFF00)==0xB500:srcs[a].add('push_lr');push[b]+=1
        if h==0x4770:bx[b]+=1
        if (h&0xFF00)==0xBD00:pop[b]+=1
        t=thumb_bl_target(data,o,ROM_BASE)
        if t is not None and ROM_BASE<=t<ROM_BASE+n:
            srcs[t].add('bl_target');bl[b]+=1
    candidates={b:[] for b in range(nb)}
    for addr,s in sorted(srcs.items()):
        b=(addr-ROM_BASE)//BANK
        if not 0<=b<nb:continue
        score=(3 if 'thumb_ptr' in s else 0)+(3 if 'bl_target' in s else 0)+(2 if 'push_lr' in s else 0)+(2 if 'arm_ptr' in s else 0)
        candidates[b].append({'address':f'0x{addr:08X}','offset':f'0x{addr-ROM_BASE:06X}','bank_offset':f'0x{addr-(ROM_BASE+b*BANK):04X}','score':score,'sources':'+'.join(sorted(s))})
    rows=[]
    for b in range(nb):
        local=candidates[b];strong=sum(x['score']>=5 for x in local)
        confirmed=[x for x in local if exec_region_for_offset(lang,int(x['offset'],16))]
        cls,note=bank_class(lang,b)
        rows.append({'language':lang,'bank':f'{b:02X}','rom_start':f'0x{b*BANK:06X}','gba_start':f'0x{ROM_BASE+b*BANK:08X}','class':cls,'class_note':note,'thumb_push_lr':push[b],'thumb_bl_encodings':bl[b],'bx_lr':bx[b],'pop_pc':pop[b],'function_candidates':len(local),'strong_function_candidates':strong,'confirmed_range_candidates':len(confirmed),'confirmed_range_strong_candidates':sum(x['score']>=5 for x in confirmed),'first_candidate':local[0]['address'] if local else '','last_candidate':local[-1]['address'] if local else ''})
    return rows,candidates

def make_obj(bank_bytes,tmpdir):
    binp=Path(tmpdir)/'bank.bin';objp=Path(tmpdir)/'bank.o';binp.write_bytes(bank_bytes)
    subprocess.run(['llvm-objcopy','-I','binary','-O','elf32-littlearm','-B','arm',str(binp),str(objp)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return objp

def disasm_region(bank_bytes,bank,mode,start,stop):
    with tempfile.TemporaryDirectory() as td:
        obj=make_obj(bank_bytes,td);triple='thumbv4t-none-eabi' if mode=='thumb' else 'armv4t-none-eabi'
        cp=subprocess.run(['llvm-objdump','-d','--section=.data',f'--triple={triple}',f'--adjust-vma=0x{ROM_BASE+bank*BANK:08X}',f'--start-address=0x{start:X}',f'--stop-address=0x{stop:X}',str(obj)],check=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return cp.stdout

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='/mnt/data/emerald_bank_audit/disassembly');ap.add_argument('--emit-bank00',action='store_true');args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);allrows=[];summary={}
    for lang,path in ROMS.items():
        rows,cands=scan_rom(lang,path);allrows.extend(rows);ldir=out/lang;ldir.mkdir(exist_ok=True)
        with (ldir/'function_candidates.csv').open('w',newline='',encoding='utf-8') as f:
            fields=['bank','address','offset','bank_offset','score','sources','exec_region'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
            for b,items in cands.items():
                for x in items:w.writerow({'bank':f'{b:02X}',**x,'exec_region':exec_region_for_offset(lang,int(x['offset'],16))})
        summary[lang]={'total_candidates':sum(map(len,cands.values())),'strong_candidates':sum(sum(y['score']>=5 for y in x) for x in cands.values()),'confirmed_exec_candidates':sum(1 for items in cands.values() for x in items if exec_region_for_offset(lang,int(x['offset'],16))),'confirmed_exec_strong_candidates':sum(1 for items in cands.values() for x in items if exec_region_for_offset(lang,int(x['offset'],16)) and x['score']>=5)}
        if args.emit_bank00:
            b0=Path(path).read_bytes()[:BANK]
            (ldir/'bank_00_ARM_startup.asm.txt').write_text(disasm_region(b0,0,'arm',0x204,0x3A4),encoding='utf-8')
            (ldir/'bank_00_Thumb_main.asm.txt').write_text(disasm_region(b0,0,'thumb',0x3A4,0x10000),encoding='utf-8')
    with (out/'bank_disassembly_inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0].keys()));w.writeheader();w.writerows(allrows)
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/'verified_exec_ranges.json').write_text(json.dumps({k:[{'start':f'0x{a:06X}','end_exclusive':f'0x{z:06X}','gba_start':f'0x{ROM_BASE+a:08X}','gba_end_exclusive':f'0x{ROM_BASE+z:08X}','kind':name} for a,z,name in v] for k,v in EXEC_RANGES.items()},indent=2),encoding='utf-8')
    en=[r for r in allrows if r['language']=='EN'];c=Counter(r['class'] for r in en)
    md=['# Pokemon Emerald 64 KiB bank + disassembly census','','This pass couples the 256-bank binary census with executable-code candidate discovery.','','## Method','','- 64 KiB analytical banks (not hardware banks).','- Thumb evidence: ROM pointers with bit0=1, Thumb BL targets, PUSH {...,LR} prologues.','- Candidate counts are a superset; arbitrary data is never promoted to code only because it decodes.','']
    for k,v in sorted(c.items()):md.append(f'- `{k}`: {v} banks')
    (out/'README.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

if __name__=='__main__':main()
