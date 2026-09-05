#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math, collections, struct
from pathlib import Path
import numpy as np

ROM_NAMES = [
    'Pocket Monsters - Fire Red (Japan) (Rev 1).gba',
    'Pocket Monsters - Fire Red (Japan).gba',
    'Pokemon - Edicion Rojo Fuego (Spain).gba',
    'Pokemon - Feuerrote Edition (Germany).gba',
    'Pokemon - Fire Red Version (USA).gba',
    'Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba',
    'Pokemon - Version Rouge Feu (France).gba',
    'Pokemon - Versione Rosso Fuoco (Italy).gba',
]
BANK=0x10000
ROM_BASE=0x08000000

def sha256(b: bytes)->str: return hashlib.sha256(b).hexdigest()
def entropy(b: bytes)->float:
    if not b: return 0.0
    a=np.frombuffer(b,dtype=np.uint8); c=np.bincount(a,minlength=256); p=c[c>0]/len(a)
    return float(-(p*np.log2(p)).sum())

def western_map():
    m={0x00:' '}
    for i,ch in enumerate('0123456789',0xA1): m[i]=ch
    for i,ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ',0xBB): m[i]=ch
    for i,ch in enumerate('abcdefghijklmnopqrstuvwxyz',0xD5): m[i]=ch
    m.update({0x01:'À',0x02:'Á',0x03:'Â',0x04:'Ç',0x05:'È',0x06:'É',0x07:'Ê',0x08:'Ë',0x09:'Ì',0x0B:'Î',0x0C:'Ï',0x0D:'Ò',0x0E:'Ó',0x0F:'Ô',0x10:'Œ',0x11:'Ù',0x12:'Ú',0x13:'Û',0x14:'Ñ',0x15:'ß',0x16:'à',0x17:'á',0x19:'ç',0x1A:'è',0x1B:'é',0x1C:'ê',0x1D:'ë',0x1E:'ì',0x20:'î',0x21:'ï',0x22:'ò',0x23:'ó',0x24:'ô',0x25:'œ',0x26:'ù',0x27:'ú',0x28:'û',0x29:'ñ',0x2A:'º',0x2B:'ª',0x2D:'&',0x2E:'+',0x35:'=',0x36:';',0x51:'¿',0x52:'¡',0x5A:'Í',0x5B:'%',0x5C:'(',0x5D:')',0x68:'â',0x6F:'í',0x79:'↑',0x7A:'↓',0x7B:'←',0x7C:'→',0x85:'<',0x86:'>',0xAB:'!',0xAC:'?',0xAD:'.',0xAE:'-',0xAF:'·',0xB0:'…',0xB1:'“',0xB2:'”',0xB3:'‘',0xB4:'’',0xB5:'♂',0xB6:'♀',0xB7:'¥',0xB8:',',0xB9:'×',0xBA:'/',0xEF:'▶',0xF0:':',0xF1:'Ä',0xF2:'Ö',0xF3:'Ü',0xF4:'ä',0xF5:'ö',0xF6:'ü'})
    return m

def japanese_map():
    m={0x00:'　'}
    hira='あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっ'
    kata='アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ'
    for i,ch in enumerate(hira,1): m[i]=ch
    for i,ch in enumerate(kata,0x51): m[i]=ch
    for i,ch in enumerate('0123456789',0xA1): m[i]=ch
    for i,ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ',0xBB): m[i]=ch
    for i,ch in enumerate('abcdefghijklmnopqrstuvwxyz',0xD5): m[i]=ch
    m.update({0xAB:'！',0xAC:'？',0xAD:'。',0xAE:'ー',0xB0:'‥'})
    return m

# Extended control parameter counts after FC opcode, from FireRed text engine behavior.
EXT_ARGS={0x01:1,0x02:1,0x03:1,0x04:3,0x05:1,0x06:1,0x07:0,0x08:1,0x09:0,0x0A:0,0x0B:2,0x0C:1,0x0D:1,0x0E:1,0x0F:0,0x10:2,0x11:1,0x12:1,0x13:1,0x14:1,0x15:0,0x16:0,0x17:0,0x18:0}

def parse_candidate(data: bytes, off:int, jp:bool, maxlen=2048):
    cmap=japanese_map() if jp else western_map()
    i=off; end=min(len(data),off+maxlen); text=[]; glyphs=0; controls=0
    while i<end:
        b=data[i]
        if b==0xFF:
            if glyphs < 4: return None
            return i-off+1, ''.join(text), glyphs, controls
        if b==0xFE: text.append('\\n'); controls+=1; i+=1; continue
        if b in (0xFA,0xFB): text.append('<PROMPT>'); controls+=1; i+=1; continue
        if b==0xFC:
            if i+1>=end: return None
            op=data[i+1]
            if op not in EXT_ARGS: return None
            n=EXT_ARGS[op]
            if i+2+n>end: return None
            text.append(f'<FC{op:02X}>'); controls+=1; i+=2+n; continue
        if b==0xFD:
            if i+1>=end: return None
            text.append(f'<VAR{data[i+1]:02X}>'); controls+=1; i+=2; continue
        if b in (0xF7,0xF8,0xF9):
            if i+1>=end: return None
            text.append(f'<C{b:02X}:{data[i+1]:02X}>'); controls+=1; i+=2; continue
        ch=cmap.get(b)
        if ch is None: return None
        text.append(ch); glyphs+=1; i+=1
    return None

def all_pointer_targets(data:bytes):
    vals=[]; poss=[]; n=len(data)
    for shift in range(4):
        usable=((n-shift)//4)*4
        a=np.frombuffer(memoryview(data)[shift:shift+usable],dtype='<u4')
        mask=(a>=ROM_BASE)&(a<ROM_BASE+n); idx=np.flatnonzero(mask)
        vals.append((a[mask]-ROM_BASE).astype(np.uint32)); poss.append((idx*4+shift).astype(np.uint32))
    return np.concatenate(vals),np.concatenate(poss)

def write_csv(path:Path, rows):
    rows=list(rows)
    if not rows: path.write_text('',encoding='utf-8'); return
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def save_sector_rows():
    return [
        {'logical_id':'0','role':'SaveBlock2','chunk_capacity':3968,'used_west':3876,'used_jp':3876,'free_west':92,'free_jp':92,'physical_sector_size':4096,'notes':'player/options/pokedex header block'},
        {'logical_id':'1-4','role':'SaveBlock1','chunk_capacity':15872,'used_west':15720,'used_jp':15680,'free_west':152,'free_jp':192,'physical_sector_size':4096,'notes':'4 logical sectors'},
        {'logical_id':'5-13','role':'PokemonStorage','chunk_capacity':35712,'used_west':33744,'used_jp':33744,'free_west':1968,'free_jp':1968,'physical_sector_size':4096,'notes':'9 logical sectors; 14 boxes x 30 BoxPokemon'},
        {'logical_id':'slot-total','role':'Main save slot','chunk_capacity':55552,'used_west':53340,'used_jp':53300,'free_west':2212,'free_jp':2252,'physical_sector_size':57344,'notes':'14 x 4096 physical sectors; payload capacity is 14 x 3968'},
        {'logical_id':'0-13 / 14-27','role':'Two alternating save slots','chunk_capacity':111104,'used_west':106680,'used_jp':106600,'free_west':4424,'free_jp':4504,'physical_sector_size':114688,'notes':'28 physical sectors total'},
        {'logical_id':'28-29','role':'Hall of Fame / save index special area','chunk_capacity':'','used_west':'','used_jp':'','free_west':'','free_jp':'','physical_sector_size':8192,'notes':'special sectors; sector 28 also used by save-index logic'},
        {'logical_id':'30-31','role':'Trainer Tower special area','chunk_capacity':'','used_west':'','used_jp':'','free_west':'','free_jp':'','physical_sector_size':8192,'notes':'special sectors'},
        {'logical_id':'all','role':'Flash','chunk_capacity':'','used_west':'','used_jp':'','free_west':'','free_jp':'','physical_sector_size':131072,'notes':'32 x 4096 = 128 KiB FLASH1M'},
    ]

def save_sector_layout_exact_rows():
    rows=[]
    for region,sb1_size in [('JP',0x3D40),('WEST',0x3D68)]:
        specs=[(0,'SaveBlock2',0,0xF24)]
        for i in range(4):
            off=i*3968; size=max(0,min(3968,sb1_size-off)); specs.append((1+i,'SaveBlock1',off,size))
        storage_size=0x83D0
        for i in range(9):
            off=i*3968; size=max(0,min(3968,storage_size-off)); specs.append((5+i,'PokemonStorage',off,size))
        for sid,role,off,size in specs:
            rows.append({'region_class':region,'logical_sector_id':sid,'role':role,'logical_offset':f'0x{off:04X}','payload_size':size,'payload_capacity':3968,'payload_free':3968-size,'footer_start':'0x0F80','id_offset':'0x0FF4','checksum_offset':'0x0FF6','signature_offset':'0x0FF8','counter_offset':'0x0FFC','physical_sector_size':4096})
    return rows

def find_all(data:bytes, pat:bytes):
    out=[]; pos=0
    while True:
        x=data.find(pat,pos)
        if x<0: return out
        out.append(x); pos=x+1

def save_binary_constant_rows(roms):
    sig=struct.pack('<I',0x08012025); sentinel=struct.pack('<H',0xB39D); rows=[]
    for name,data in roms.items():
        sh=find_all(data,sig); th=find_all(data,sentinel)
        rows.append({'rom':name,'sector_signature_08012025_hits':len(sh),'sector_signature_offsets':';'.join(f'0x{x:08X}' for x in sh),'special_sentinel_B39D_hits':len(th),'special_sentinel_offsets_first20':';'.join(f'0x{x:08X}' for x in th[:20])})
    return rows

def compact_bank_summary(rom_name,candidates):
    bct=collections.Counter(r['source_bank'] for r in candidates); bref=collections.Counter()
    for r in candidates: bref[r['source_bank']]+=r['pointer_occurrences']
    def topstr(c): return ';'.join(f'{b:02X}:{v}' for b,v in sorted(c.items(),key=lambda kv:(-kv[1],kv[0]))[:12])
    return {'rom':rom_name,'banks_with_candidates':len(bct),'candidate_total':len(candidates),'pointer_occurrence_total':sum(r['pointer_occurrences'] for r in candidates),'top_candidate_banks':topstr(bct),'top_reference_banks':topstr(bref)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom_dir',nargs='?',default='/mnt/data'); ap.add_argument('-o','--out',default='/mnt/data/fire_red_stage5_systems'); args=ap.parse_args()
    rd=Path(args.rom_dir); out=Path(args.out); out.mkdir(parents=True,exist_ok=True); per=out/'per_rom'; per.mkdir(exist_ok=True)
    roms={n:(rd/n).read_bytes() for n in ROM_NAMES}; summaries=[]; bankrows=[]; compact_bankrows=[]; manifest=[]; all_candidates={}
    for name,data in roms.items():
        jp='Japan' in name; targets,srcpos=all_pointer_targets(data); cnt=collections.Counter(int(x) for x in targets)
        aligned_mask=(srcpos % 4)==0; aligned_count=int(aligned_mask.sum()); shift_counts={sh:int(((srcpos % 4)==sh).sum()) for sh in range(4)}; candidates=[]
        for t,refs in cnt.items():
            q=parse_candidate(data,t,jp)
            if q:
                ln,txt,glyphs,controls=q; poss_for_target=srcpos[targets==t]; aligned_refs=int(((poss_for_target % 4)==0).sum()); unaligned_refs=int(len(poss_for_target)-aligned_refs)
                candidates.append({'target_offset':f'0x{t:08X}','rom_address':f'0x{ROM_BASE+t:08X}','length_bytes':ln,'glyph_count':glyphs,'control_count':controls,'pointer_occurrences':refs,'aligned_pointer_occurrences':aligned_refs,'unaligned_pointer_occurrences':unaligned_refs,'target_parity':'odd' if t&1 else 'even','target_in_gba_header':t<0xC0,'source_bank':t//BANK,'text_preview':txt[:240]})
        candidates.sort(key=lambda r:int(r['target_offset'],16)); all_candidates[name]=candidates
        safe=''.join(c if c.isalnum() else '_' for c in Path(name).stem); pth=per/f'{safe}_referenced_strings.csv'; write_csv(pth,candidates); manifest.append({'file':pth.name,'size':pth.stat().st_size,'sha256':sha256(pth.read_bytes())})
        summaries.append({'rom':name,'pointer_occurrences_all_byte':len(targets),'pointer_occurrences_aligned':aligned_count,'pointer_occurrences_shift1':shift_counts[1],'pointer_occurrences_shift2':shift_counts[2],'pointer_occurrences_shift3':shift_counts[3],'unique_pointer_targets':len(cnt),'referenced_string_candidates':len(candidates),'candidates_with_aligned_refs':sum(1 for r in candidates if r['aligned_pointer_occurrences']>0),'candidates_unaligned_only':sum(1 for r in candidates if r['aligned_pointer_occurrences']==0),'candidate_bytes_total':sum(r['length_bytes'] for r in candidates),'candidate_pointer_occurrences':sum(r['pointer_occurrences'] for r in candidates)})
        bct=collections.Counter(r['source_bank'] for r in candidates); bref=collections.Counter()
        for r in candidates: bref[r['source_bank']]+=r['pointer_occurrences']
        for b in range(256): bankrows.append({'rom':name,'bank':b,'start':f'0x{b*BANK:08X}','string_candidates':bct.get(b,0),'candidate_pointer_occurrences':bref.get(b,0)})
        compact_bankrows.append(compact_bank_summary(name,candidates))
    write_csv(out/'referenced_text_summary.csv',summaries); write_csv(out/'referenced_text_bank_matrix.csv',bankrows); write_csv(out/'referenced_text_bank_summary.csv',compact_bankrows); write_csv(out/'referenced_text_manifest.csv',manifest)

    en0=roms['Pokemon - Fire Red Version (USA).gba']; anchor=0x1EEF00; sig=en0[anchor:anchor+64]; fontrows=[]
    for name,data in roms.items():
        hits=[]; s=0
        while True:
            x=data.find(sig,s)
            if x<0: break
            hits.append(x); s=x+1
        fontrows.append({'rom':name,'small_latin_width_signature_hits':len(hits),'offsets':';'.join(f'0x{x:08X}' for x in hits),'signature_sha256':sha256(sig),'signature_length':len(sig),'classification':'shared Western small-Latin width prefix' if len(hits)==1 and 'Japan' not in name else ('JP layout differs / no shared Latin prefix' if not hits and 'Japan' in name else 'unexpected')})
    write_csv(out/'font_anchor_summary.csv',fontrows); write_csv(out/'save_sector_schema.csv',save_sector_rows()); write_csv(out/'save_sector_layout_exact.csv',save_sector_layout_exact_rows()); write_csv(out/'save_binary_constant_audit.csv',save_binary_constant_rows(roms))

    revrows=[]
    for name in ['Pokemon - Fire Red Version (USA).gba','Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba']:
        hits=[r for r in all_candidates[name] if ('NEXT DATA' in r['text_preview'] or 'AREAS' in r['text_preview']) and ('TOWN MAP' in r['text_preview'] or 'habitat' in r['text_preview'])]
        revrows.append({'rom':name,'matching_candidate_count':len(hits),'targets':';'.join(r['target_offset'] for r in hits[:10]),'previews':' || '.join(r['text_preview'].replace('\n',' ')[:180] for r in hits[:5])})
    write_csv(out/'english_revision_help_probe.csv',revrows)

    jp0=roms['Pocket Monsters - Fire Red (Japan).gba']; jp1=roms['Pocket Monsters - Fire Red (Japan) (Rev 1).gba']; arr0=np.frombuffer(jp0,dtype=np.uint8); arr1=np.frombuffer(jp1,dtype=np.uint8); dif=np.flatnonzero(arr0!=arr1); high=dif[dif>=0xF00000]; first=int(high[0]); last=int(high[-1]); region_end=0xFE0000
    def ptr_counts(data,st,en):
        sub=data[st:en]; outc={}; ranges={'EWRAM':(0x02000000,0x02040000),'IWRAM':(0x03000000,0x03008000),'IO':(0x04000000,0x04000400),'PAL':(0x05000000,0x05000400),'VRAM':(0x06000000,0x06018000),'OAM':(0x07000000,0x07000400),'ROM':(0x08000000,0x09000000)}
        for k,(lo,hi) in ranges.items():
            total=0
            for shift in range(4):
                usable=((len(sub)-shift)//4)*4; a=np.frombuffer(memoryview(sub)[shift:shift+usable],dtype='<u4'); total+=int(((a>=lo)&(a<hi)).sum())
            outc[k]=total
        return outc
    pc0=ptr_counts(jp0,first,region_end); pc1=ptr_counts(jp1,first,region_end); resrows=[]
    for label,data,pc in [('JP Rev0',jp0,pc0),('JP Rev1',jp1,pc1)]:
        reg=data[first:region_end]; a=np.frombuffer(reg,dtype=np.uint8); resrows.append({'build':label,'start':f'0x{first:08X}','end_exclusive':f'0x{region_end:08X}','last_difference':f'0x{last:08X}','region_size':len(reg),'sha256':sha256(reg),'entropy':round(entropy(reg),6),'zero_pct':round(float((a==0).sum())/len(a)*100,6),'ff_pct':round(float((a==0xFF).sum())/len(a)*100,6),**{f'allbyte_ptr_{k}':v for k,v in pc.items()}})
    write_csv(out/'jp_rev0_highrom_residual_summary.csv',resrows); br=[]
    for bank in range(0xF3,0xFE):
        st=bank*BANK; en=st+BANK
        for label,data in [('JP Rev0',jp0),('JP Rev1',jp1)]:
            b=data[st:en]; a=np.frombuffer(b,dtype=np.uint8); pc=ptr_counts(data,st,en); br.append({'build':label,'bank':f'{bank:02X}','start':f'0x{st:08X}','entropy':round(entropy(b),6),'zero_pct':round(float((a==0).sum())/len(a)*100,6),'ff_pct':round(float((a==0xFF).sum())/len(a)*100,6),'sha256':sha256(b),**{f'ptr_{k}':v for k,v in pc.items()}})
    write_csv(out/'jp_rev0_highrom_residual_banks.csv',br)

    expect_aligned={'Pocket Monsters - Fire Red (Japan) (Rev 1).gba':63953,'Pocket Monsters - Fire Red (Japan).gba':64495,'Pokemon - Edicion Rojo Fuego (Spain).gba':63563,'Pokemon - Feuerrote Edition (Germany).gba':63463,'Pokemon - Fire Red Version (USA).gba':63771,'Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba':63766,'Pokemon - Version Rouge Feu (France).gba':63524,'Pokemon - Versione Rosso Fuoco (Italy).gba':63511}; validation=[]
    for r in summaries:
        validation.append({'rom':r['rom'],'stage2_aligned_expected':expect_aligned[r['rom']],'stage5_aligned_actual':r['pointer_occurrences_aligned'],'aligned_regression_match':r['pointer_occurrences_aligned']==expect_aligned[r['rom']],'allbyte_occurrences':r['pointer_occurrences_all_byte'],'allbyte_ge_aligned':r['pointer_occurrences_all_byte']>=r['pointer_occurrences_aligned'],'shift_sum_match':r['pointer_occurrences_all_byte']==r['pointer_occurrences_aligned']+r['pointer_occurrences_shift1']+r['pointer_occurrences_shift2']+r['pointer_occurrences_shift3'],'string_candidates_positive':r['referenced_string_candidates']>0})
    write_csv(out/'stage5_validation.csv',validation)
    summary={'rom_count':8,'pointer_scan_all_byte':True,'aligned_pointer_regression_validation':all(x['aligned_regression_match'] for x in validation),'shift_partition_validation':all(x['shift_sum_match'] for x in validation),'font_signature_sha256':sha256(sig),'save_flash_bytes':131072,'save_slot_physical_bytes':57344,'jp_highrom_first_difference':f'0x{first:08X}','jp_highrom_last_difference':f'0x{last:08X}','referenced_string_candidates':{r['rom']:r['referenced_string_candidates'] for r in summaries}}
    (out/'stage5_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    generated_names=['stage5_validation.csv','referenced_text_summary.csv','referenced_text_bank_summary.csv','english_revision_help_probe.csv','font_anchor_summary.csv','save_sector_schema.csv','save_sector_layout_exact.csv','save_binary_constant_audit.csv','jp_rev0_highrom_residual_summary.csv','jp_rev0_highrom_residual_banks.csv','stage5_summary.json']; genmanifest=[]
    for fn in generated_names:
        fp=out/fn; genmanifest.append({'file':fn,'bytes':fp.stat().st_size,'sha256':sha256(fp.read_bytes())})
    write_csv(out/'artifact_manifest_generated.csv',genmanifest); print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
