#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, deque
import hashlib, csv, struct, re, subprocess, tempfile, zipfile, json
import numpy as np
import pandas as pd

ROOT=Path('/mnt/data')
BANK=0x10000
ROM_BASE=0x08000000
MASTER=ROOT/'ruby_bank_master.csv'
SEM=ROOT/'ruby_bank_semantic_map.csv'
OBJCOPY='/usr/local/swift/usr/bin/llvm-objcopy'
OBJDUMP='/usr/local/swift/usr/bin/llvm-objdump'

REFS={
'f28b6ffc97847e94a6c21a63cacf633ee5c8df1e':('pret/pokeruby','pokeruby.gba','ruby','exact'),
'610b96a9c9a7d03d2bafb655e7560ccff1a6d894':('pret/pokeruby','pokeruby_rev1.gba','ruby_rev1','exact'),
'5b64eacf892920518db4ec664e62a086dd5f5bc8':('pret/pokeruby','pokeruby_rev2.gba','ruby_rev2','exact'),
'1c2a53332382e14dab8815e3a6dd81ad89534050':('pret/pokeruby','pokeruby_de.gba','ruby_de','exact'),
'424740be1fc67a5ddb954794443646e6aeee2c1b':('pret/pokeruby','pokeruby_de_rev1.gba','ruby_de_rev1','exact'),
'ca5e3d415c4b47353a73a616878ba833f3648b7a':('pret/pokeruby','pokeruby_de_debug.gba','ruby_de_debug','exact'),
}

def sx(x,bits):
    sign=1<<(bits-1)
    return x-(1<<bits) if x & sign else x

def arm_b_target(off,w):
    imm=sx(w & 0xFFFFFF,24)<<2
    return off+8+imm

def thumb_b_target(off,h):
    return off+4+sx((h&0x7FF)<<1,12)

def thumb_cond_target(off,h):
    return off+4+sx((h&0xFF)<<1,9)

def thumb_bl_target(off,h1,h2):
    hi=sx((h1&0x7FF)<<12,23)
    lo=(h2&0x7FF)<<1
    return off+4+hi+lo

def semantic_core_end(rows, rom_key, data_len):
    rr=rows[rows.rom_key==rom_key]
    for _,r in rr.iterrows():
        n=str(r['note'])
        m=re.search(r'last non-FF byte at 0x([0-9A-Fa-f]+)',n)
        if m and ('CORE' in str(r['semantic_region'])):
            return min(int(m.group(1),16)+1,data_len)
    core=rr[rr.semantic_region.astype(str).str.contains('CORE')]
    if len(core):
        return min((int(core.bank_dec.max())+1)*BANK,data_len)
    return data_len

def bootstrap_info(b):
    w0=int.from_bytes(b[0:4],'little')
    arm_entry=None
    if (w0 & 0x0E000000)==0x0A000000:
        arm_entry=arm_b_target(0,w0)
    bx_pat=(0xE12FFF11).to_bytes(4,'little')
    bx=b.find(bx_pat, 0, min(len(b),0x1000))
    ldr_off=None; lit_off=None; thumb_ptr=None; thumb_entry=None
    if bx>=8:
        w=int.from_bytes(b[bx-8:bx-4],'little')
        if (w & 0x0FFF0000)==0x059F0000 and ((w>>12)&0xF)==1:
            imm=w&0xFFF
            u=(w>>23)&1
            ldr_off=bx-8
            lit_off=ldr_off+8+(imm if u else -imm)
            if 0<=lit_off<=len(b)-4:
                thumb_ptr=int.from_bytes(b[lit_off:lit_off+4],'little')
                if ROM_BASE <= (thumb_ptr & ~1) < ROM_BASE+len(b) and (thumb_ptr&1):
                    thumb_entry=(thumb_ptr&~1)-ROM_BASE
    return dict(first_word=f'0x{w0:08X}',arm_entry=arm_entry,bx_r1_offset=bx if bx>=0 else None,
                ldr_r1_offset=ldr_off,literal_offset=lit_off,thumb_pointer=thumb_ptr,thumb_entry=thumb_entry)

def raw_bank_features(chunk, rom_len):
    h=np.frombuffer(chunk[:len(chunk)//2*2],dtype='<u2')
    w=np.frombuffer(chunk[:len(chunk)//4*4],dtype='<u4')
    out={}
    out['thumb_cond_b']=int(np.sum(((h&0xF000)==0xD000) & (((h>>8)&0xF)<0xE)))
    out['thumb_b']=int(np.sum((h&0xF800)==0xE000))
    out['thumb_bl_hi']=int(np.sum((h&0xF800)==0xF000))
    out['thumb_bl_lo']=int(np.sum((h&0xF800)==0xF800))
    if len(h)>1:
        out['thumb_bl_pairs']=int(np.sum(((h[:-1]&0xF800)==0xF000)&((h[1:]&0xF800)==0xF800)))
    else: out['thumb_bl_pairs']=0
    out['thumb_bx']=int(np.sum((h&0xFF87)==0x4700))
    out['thumb_push_lr']=int(np.sum((h&0xFF00)==0xB500))
    out['thumb_pop_pc']=int(np.sum((h&0xFF00)==0xBD00))
    out['thumb_bx_lr']=int(np.sum(h==0x4770))
    out['thumb_ldr_literal']=int(np.sum((h&0xF800)==0x4800))
    out['thumb_swi']=int(np.sum((h&0xFF00)==0xDF00))
    out['arm_b_or_bl']=int(np.sum((w&0x0E000000)==0x0A000000))
    out['arm_bl']=int(np.sum((w&0x0F000000)==0x0B000000))
    out['arm_bx']=int(np.sum((w&0x0FFFFFF0)==0x012FFF10))
    out['arm_push_like']=int(np.sum((w&0x0FFF0000)==0x092D0000))
    out['arm_pop_pc_like']=int(np.sum((w&0x0FFF8000)==0x08BD8000))
    out['arm_swi']=int(np.sum((w&0x0F000000)==0x0F000000))
    ptr=((w>=ROM_BASE)&(w<ROM_BASE+rom_len))
    odd=ptr & ((w&1)==1)
    out['aligned_rom_ptrs_raw']=int(np.sum(ptr))
    out['odd_thumb_ptrs_raw']=int(np.sum(odd))
    return out

def collect_thumb_ptr_targets(b, core_end):
    w=np.frombuffer(b[:len(b)//4*4],dtype='<u4')
    mask=(w>=ROM_BASE)&(w<ROM_BASE+len(b))&((w&1)==1)
    ctr=Counter(map(int,w[mask]))
    rows=[]; seeds=set()
    for v,c in ctr.items():
        off=(v&~1)-ROM_BASE
        if off<0 or off+2>len(b): continue
        h=int.from_bytes(b[off:off+2],'little')
        push_lr=((h&0xFF00)==0xB500)
        in_core=off<core_end
        if push_lr and in_core: seeds.add(off)
        rows.append((v,off,c,h,push_lr,in_core))
    return rows,seeds

def recursive_thumb_cfg(b, core_end, seeds):
    q=deque(sorted(seeds))
    visited=set(); edges=[]; calls=Counter(); returns=0; indirect=0
    while q:
        off=q.popleft()
        if off in visited or off<0 or off+2>core_end or (off&1): continue
        h=int.from_bytes(b[off:off+2],'little')
        visited.add(off)
        if (h&0xF800)==0xF000 and off+4<=core_end:
            h2=int.from_bytes(b[off+2:off+4],'little')
            if (h2&0xF800)==0xF800:
                visited.add(off+2)
                t=thumb_bl_target(off,h,h2)
                if 0<=t<core_end and not (t&1):
                    edges.append((off,t,'BL')); calls[t]+=1; q.append(t)
                q.append(off+4)
                continue
        if (h&0xF000)==0xD000 and ((h>>8)&0xF)<0xE:
            t=thumb_cond_target(off,h)
            if 0<=t<core_end and not (t&1): edges.append((off,t,'Bcc')); q.append(t)
            q.append(off+2); continue
        if (h&0xF800)==0xE000:
            t=thumb_b_target(off,h)
            if 0<=t<core_end and not (t&1): edges.append((off,t,'B')); q.append(t)
            continue
        if (h&0xFF00)==0xBD00:
            returns+=1; continue
        if (h&0xFF87)==0x4700:
            if h==0x4770: returns+=1
            else: indirect+=1
            continue
        if (h&0xFF87) in (0x4687,0x4487):
            indirect+=1; continue
        q.append(off+2)
    return visited,edges,calls,returns,indirect

def make_bank00_bundle(rom_rows):
    outzip=ROOT/'ruby_bank00_disassembly_bundle.zip'
    with zipfile.ZipFile(outzip,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for _,r in rom_rows.iterrows():
            p=ROOT/r['file']; key=r['rom_key']; b=p.read_bytes()[:BANK]
            with tempfile.TemporaryDirectory() as td:
                td=Path(td); raw=td/'bank00.bin'; obj=td/'bank00.o'; raw.write_bytes(b)
                subprocess.run([OBJCOPY,'-I','binary','-O','elf32-littlearm','-B','arm',
                                '--rename-section','.data=.text,alloc,load,readonly,code',str(raw),str(obj)],check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                for mode,triple in [('ARM','armv4t-none-eabi'),('THUMB','thumbv4t-none-eabi')]:
                    txt=subprocess.check_output([OBJDUMP,'-d',f'--triple={triple}',str(obj)],text=True,errors='replace')
                    z.writestr(f'{key}/bank_00_{mode.lower()}_raw.txt',txt)
            bi=bootstrap_info(p.read_bytes())
            z.writestr(f'{key}/bootstrap.json',json.dumps(bi,indent=2))
    return outzip

def main():
    master=pd.read_csv(MASTER)
    sem=pd.read_csv(SEM)
    rom_rows=master[['rom_key','file','language','region','kind','game_code','revision']].drop_duplicates()
    inv=[]; refs=[]; boot=[]; ptr_rows=[]; cfg_bank=[]; baseline_edges=[]; funcs=[]
    for _,rr in rom_rows.iterrows():
        key=rr.rom_key; p=ROOT/rr.file; b=p.read_bytes(); sha=hashlib.sha1(b).hexdigest(); core_end=semantic_core_end(sem,key,len(b))
        ref=REFS.get(sha)
        refs.append(dict(rom_key=key,file=rr.file,sha1=sha,reference_repo=ref[0] if ref else '',reference_build=ref[1] if ref else '',reference_variant=ref[2] if ref else '',match_status=ref[3] if ref else 'no_exact_pokeruby_reference'))
        bi=bootstrap_info(b); boot.append(dict(rom_key=key,file=rr.file,core_end=f'0x{core_end:08X}',**{k:(f'0x{v:08X}' if isinstance(v,int) else v) for k,v in bi.items()}))
        targets,seeds=collect_thumb_ptr_targets(b,core_end)
        if bi['thumb_entry'] is not None: seeds.add(bi['thumb_entry'])
        for v,off,c,h,push,in_core in targets:
            ptr_rows.append(dict(rom_key=key,target_pointer=f'0x{v:08X}',target_offset=f'0x{off:08X}',target_gba=f'0x{ROM_BASE+off:08X}',target_bank=f'{off//BANK:02X}',xref_count=c,first_halfword=f'0x{h:04X}',push_lr_prologue=push,in_core=in_core))
        visited,edges,calls,ret,ind=recursive_thumb_cfg(b,core_end,seeds)
        entry_types={s:'POINTER_PUSH_LR_SEED' for s in seeds}
        if bi['thumb_entry'] is not None: entry_types[bi['thumb_entry']]='BOOTSTRAP_THUMB_ENTRY'
        for t,c in calls.items(): entry_types.setdefault(t,'DISCOVERED_BL_TARGET')
        for e,t in sorted(entry_types.items()):
            funcs.append(dict(rom_key=key,entry_offset=f'0x{e:08X}',entry_gba=f'0x{ROM_BASE+e:08X}',bank=f'{e//BANK:02X}',provenance=t,bl_xrefs=int(calls.get(e,0))))
        if key=='AXVE_v0_USA':
            for s,t,typ in edges:
                baseline_edges.append(dict(source_offset=f'0x{s:08X}',source_gba=f'0x{ROM_BASE+s:08X}',source_bank=f'{s//BANK:02X}',edge_type=typ,target_offset=f'0x{t:08X}',target_gba=f'0x{ROM_BASE+t:08X}',target_bank=f'{t//BANK:02X}'))
        visited_bank=Counter(x//BANK for x in visited)
        seed_bank=Counter(x//BANK for x in seeds)
        call_bank=Counter(x//BANK for x in calls)
        rr_master=master[master.rom_key==key].sort_values('bank_index_dec')
        sem_key=sem[sem.rom_key==key].set_index('bank_dec')
        for _,br in rr_master.iterrows():
            bank=int(br.bank_index_dec); chunk=b[bank*BANK:min((bank+1)*BANK,len(b))]
            feat=raw_bank_features(chunk,len(b))
            semantic=str(sem_key.loc[bank,'semantic_region']) if bank in sem_key.index else ''
            inv.append(dict(rom_key=key,file=rr.file,bank_dec=bank,bank_hex=f'{bank:02X}',gba_start=f'0x{ROM_BASE+bank*BANK:08X}',semantic_region=semantic,
                            candidate_recursive_thumb_code_halfwords=visited_bank.get(bank,0),candidate_recursive_thumb_code_bytes=visited_bank.get(bank,0)*2,
                            strong_thumb_seed_count=seed_bank.get(bank,0),discovered_bl_target_count=call_bank.get(bank,0),**feat))
        cfg_bank.append(dict(rom_key=key,file=rr.file,core_end=f'0x{core_end:08X}',strong_seeds=len(seeds),candidate_recursive_code_halfwords=len(visited),candidate_recursive_code_bytes=len(visited)*2,cfg_edges=len(edges),distinct_bl_targets=len(calls),return_sites=ret,indirect_transfer_sites=ind))
    pd.DataFrame(inv).to_csv(ROOT/'ruby_bank_disasm_inventory.csv',index=False)
    pd.DataFrame(refs).to_csv(ROOT/'ruby_disasm_reference_matches.csv',index=False)
    pd.DataFrame(boot).to_csv(ROOT/'ruby_bootstrap_entries.csv',index=False)
    pd.DataFrame(ptr_rows).to_csv(ROOT/'ruby_thumb_pointer_targets.csv',index=False)
    pd.DataFrame(cfg_bank).to_csv(ROOT/'ruby_thumb_cfg_summary.csv',index=False)
    pd.DataFrame(funcs).to_csv(ROOT/'ruby_thumb_function_entries.csv',index=False)
    pd.DataFrame(baseline_edges).to_csv(ROOT/'ruby_usa_v0_thumb_cfg_edges.csv',index=False)
    make_bank00_bundle(rom_rows)
    print(pd.DataFrame(cfg_bank).to_string(index=False))

if __name__=='__main__': main()
