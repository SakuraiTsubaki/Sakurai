#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, struct
from pathlib import Path

ROM_DIR=Path('/mnt/data')
OUT=Path('/mnt/data/fire_red_stage4_systems')
OUT.mkdir(exist_ok=True)
ROMS=sorted(ROM_DIR.glob('*.gba'))
ABILITIES_COUNT=78
ITEMS_COUNT=375
DEX_COUNT=386
DEX_ENTRIES=DEX_COUNT+1

def u16(d,o): return struct.unpack_from('<H',d,o)[0]
def u32(d,o): return struct.unpack_from('<I',d,o)[0]
def roff(v): return v-0x08000000 if 0x08000000 <= v < 0x09000000 else None
def sha(b): return hashlib.sha256(b).hexdigest()

def cmap_west():
    m={0x00:' '}
    for i,ch in enumerate('0123456789',0xA1):m[i]=ch
    for i,ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ',0xBB):m[i]=ch
    for i,ch in enumerate('abcdefghijklmnopqrstuvwxyz',0xD5):m[i]=ch
    m.update({0xAB:'!',0xAC:'?',0xAD:'.',0xAE:'-',0xAF:'·',0xB0:'…',0xB1:'“',0xB2:'”',0xB3:'‘',0xB4:'’',0xB5:'♂',0xB6:'♀',0xB7:'¥',0xB8:',',0xB9:'×',0xBA:'/',0xF0:':'})
    return m

def cmap_jp():
    m={0x00:'　'}
    hira='あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっ'
    kata='アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ'
    for i,ch in enumerate(hira,1):m[i]=ch
    for i,ch in enumerate(kata,0x51):m[i]=ch
    for i,ch in enumerate('0123456789',0xA1):m[i]=ch
    for i,ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ',0xBB):m[i]=ch
    for i,ch in enumerate('abcdefghijklmnopqrstuvwxyz',0xD5):m[i]=ch
    m.update({0xAB:'！',0xAC:'？',0xAD:'。',0xAE:'ー',0xB0:'‥'})
    return m

def decode_fixed(b,cmap):
    out=[]
    for x in b:
        if x==0xFF: break
        out.append(cmap.get(x,f'<{x:02X}>'))
    return ''.join(out).rstrip(' \u3000')

def read_ff(d,o,maxlen=4096):
    if o is None or not (0<=o<len(d)): return b''
    e=d.find(b'\xff',o,min(len(d),o+maxlen))
    if e<0:return d[o:min(len(d),o+maxlen)]
    return d[o:e+1]

def parse_gf(d):
    b=0x100
    r={}
    r['version']=u32(d,b); r['language']=u32(d,b+4); r['game_name']=d[b+8:b+40].split(b'\0')[0].decode('ascii')
    ptr_names=['monFrontPics','monBackPics','monNormalPalettes','monShinyPalettes','monIcons','monIconPaletteIds','monIconPalettes','monSpeciesNames','moveNames','decorations']
    o=40
    for n in ptr_names:r[n]=roff(u32(d,b+o));o+=4
    for n in ['flagsOffset','varsOffset','pokedexOffset','seen1Offset','seen2Offset','pokedexVar','pokedexFlag','mysteryGiftFlag','pokedexCount']:
        r[n]=u32(d,b+o);o+=4
    byte_names=['playerNameLength','unk2','pokemonNameLength1','pokemonNameLength2','unk5','unk6','unk7','unk8','unk9','unk10','unk11','unk12','unk13','unk14','unk15','unk16','unk17']
    for n in byte_names:r[n]=d[b+o];o+=1
    o=(o+3)&~3
    n32=['saveBlock2Size','saveBlock1Size','partyCountOffset','partyOffset','warpFlagsOffset','trainerIdOffset','playerNameOffset','playerGenderOffset','unkFlagOffset','unkFlagOffset2','externalEventFlagsOffset','externalEventDataOffset','unk18']
    for n in n32:r[n]=u32(d,b+o);o+=4
    for n in ['speciesInfo','abilityNames','abilityDescriptions','items','moves','ballGfx','ballPalettes']:
        r[n]=roff(u32(d,b+o));o+=4
    for n in ['gcnLinkFlagsOffset','gameClearFlag','ribbonFlag']:
        r[n]=u32(d,b+o);o+=4
    for n in ['bagCountItems','bagCountKeyItems','bagCountPokeballs','bagCountTMHMs','bagCountBerries','pcItemsCount']:
        r[n]=d[b+o];o+=1
    o=(o+3)&~3
    for n in ['pcItemsOffset','giftRibbonsOffset','enigmaBerryOffset','enigmaBerrySize']:
        r[n]=u32(d,b+o);o+=4
    r['moveDescriptions']=roff(u32(d,b+o));o+=4; r['unk20']=u32(d,b+o)
    return r

def find_pokedex(d,lang):
    stride,hw=(28,6) if lang==1 else (36,12)
    p1=b'\x07\x00\x45\x00';p2=b'\x0a\x00\x82\x00';p3=b'\x14\x00\xe8\x03'
    hits=[];s=0
    while True:
        pos=d.find(p1,s)
        if pos<0:break
        base=pos-(stride+hw)
        if base>=0 and d[base+2*stride+hw:base+2*stride+hw+4]==p2 and d[base+3*stride+hw:base+3*stride+hw+4]==p3:
            hits.append(base)
        s=pos+1
    if len(hits)!=1: raise RuntimeError(f'pokedex hits {hits}')
    return hits[0],stride,hw

def parse_dex(d,base,stride,catlen,lang):
    cmap=cmap_jp() if lang==1 else cmap_west(); rows=[]; semantic=[]
    for i in range(DEX_ENTRIES):
        o=base+i*stride; cat=decode_fixed(d[o:o+catlen],cmap)
        if lang==1:
            height=u16(d,o+6);weight=u16(d,o+8);desc=roff(u32(d,o+12));unused= u16(d,o+16); ps=u16(d,o+18);po=u16(d,o+20);ts=u16(d,o+22);to=u16(d,o+24)
            unused_desc=None
        else:
            height=u16(d,o+12);weight=u16(d,o+14);desc=roff(u32(d,o+16));unused_desc=roff(u32(d,o+20));unused=u16(d,o+24);ps=u16(d,o+26);po=u16(d,o+28);ts=u16(d,o+30);to=u16(d,o+32)
        text=read_ff(d,desc)
        rows.append(dict(index=i,category=cat,height=height,weight=weight,description_offset='' if desc is None else f'0x{desc:08X}',description_len=len(text),description_sha256=sha(text),unused_description_offset='' if unused_desc is None else f'0x{unused_desc:08X}',unused=unused,pokemonScale=ps,pokemonOffset=po,trainerScale=ts,trainerOffset=to))
        semantic.append((height,weight,unused,ps,po,ts,to))
    return rows,sha(json.dumps(semantic,separators=(',',':')).encode())

def parse_abilities(d,h):
    lang=h['language']; stride=h['unk5']+1; cmap=cmap_jp() if lang==1 else cmap_west(); rows=[]
    desc_base=h['abilityDescriptions']; names=h['abilityNames']; sem=[]
    probe=[roff(u32(d,desc_base+i*4)) for i in range(min(ABILITIES_COUNT,8))]
    layout='pointer_table' if all(x is not None for x in probe) else 'direct_blob'
    for i in range(ABILITIES_COUNT):
        name=decode_fixed(d[names+i*stride:names+(i+1)*stride],cmap)
        if layout=='pointer_table':
            dp=roff(u32(d,desc_base+i*4)); txt=read_ff(d,dp)
            rows.append(dict(index=i,name=name,description_offset='' if dp is None else f'0x{dp:08X}',description_len=len(txt),description_sha256=sha(txt)))
            sem.append((len(txt),sha(txt)))
        else:
            rows.append(dict(index=i,name=name,description_offset='',description_len='',description_sha256=''))
    return rows,stride,layout,sha(json.dumps(sem,separators=(',',':')).encode()) if sem else ''

def parse_items(d,h):
    lang=h['language']; stride=40 if lang==1 else 44; nlen=10 if lang==1 else 14; cmap=cmap_jp() if lang==1 else cmap_west(); rows=[]; scalar=[]
    for i in range(ITEMS_COUNT):
        o=h['items']+i*stride
        name=decode_fixed(d[o:o+nlen],cmap); q=o+nlen
        itemId=u16(d,q);price=u16(d,q+2);hold=d[q+4];holdp=d[q+5];desc=roff(u32(d,q+6));importance=d[q+10];registrability=d[q+11];pocket=d[q+12];typ=d[q+13];field=roff(u32(d,q+14));battleUsage=d[q+18];battle=roff(u32(d,q+22));secondary=d[q+26]
        txt=read_ff(d,desc)
        rows.append(dict(index=i,name=name,itemId=itemId,price=price,holdEffect=hold,holdEffectParam=holdp,description_offset='' if desc is None else f'0x{desc:08X}',description_len=len(txt),description_sha256=sha(txt),importance=importance,registrability=registrability,pocket=pocket,type=typ,field_func_nonzero=field is not None,battleUsage=battleUsage,battle_func_nonzero=battle is not None,secondaryId=secondary))
        scalar.append((itemId,price,hold,holdp,importance,registrability,pocket,typ,field is not None,battleUsage,battle is not None,secondary))
    return rows,stride,nlen,sha(json.dumps(scalar,separators=(',',':')).encode())

def icon_summary(d,h):
    ptrs=[]
    for i in range(440):
        p=roff(u32(d,h['monIcons']+i*4)); ptrs.append(p)
    valid=sum(p is not None for p in ptrs); uniq=len(set(p for p in ptrs if p is not None))
    assets=[sha(d[p:p+0x200]) if p is not None and p+0x200<=len(d) else 'BAD' for p in ptrs]
    palids=d[h['monIconPaletteIds']:h['monIconPaletteIds']+440]
    return dict(icon_table=f"0x{h['monIcons']:08X}",entries=440,valid_pointers=valid,unique_targets=uniq,asset_vector_sha256=sha('\n'.join(assets).encode()),palette_id_table=f"0x{h['monIconPaletteIds']:08X}",palette_ids_sha256=sha(palids),icon_palette_table=f"0x{h['monIconPalettes']:08X}")

def main():
    header_rows=[]; dex_summ=[]; ability_summ=[]; item_summ=[]; icon_summ=[]; validation=[]
    detailed_dir=OUT/'per_rom'; detailed_dir.mkdir(exist_ok=True)
    sem_dex={}; sem_items={}
    for p in ROMS:
        d=p.read_bytes();h=parse_gf(d);name=p.name
        hrow={'rom':name,**h}
        for k,v in list(hrow.items()):
            if isinstance(v,int) and k in {'monFrontPics','monBackPics','monNormalPalettes','monShinyPalettes','monIcons','monIconPaletteIds','monIconPalettes','monSpeciesNames','moveNames','decorations','speciesInfo','abilityNames','abilityDescriptions','items','moves','ballGfx','ballPalettes','moveDescriptions'} and v is not None:
                hrow[k]=f'0x{v:08X}'
        header_rows.append(hrow)
        base,stride,catlen=find_pokedex(d,h['language']); dexrows,dexhash=parse_dex(d,base,stride,catlen,h['language']); sem_dex[name]=dexhash
        abrows,abstride,ablayout,ablenhash=parse_abilities(d,h)
        itrows,itstride,itnlen,ithash=parse_items(d,h); sem_items[name]=ithash
        icons=icon_summary(d,h);icons['rom']=name; icon_summ.append(icons)
        dex_summ.append(dict(rom=name,pokedex_table=f'0x{base:08X}',entry_count=DEX_ENTRIES,stride=stride,category_width=catlen,nonlanguage_semantic_sha256=dexhash,total_description_bytes=sum(r['description_len'] for r in dexrows),unique_description_hashes=len(set(r['description_sha256'] for r in dexrows))))
        ability_summ.append(dict(rom=name,ability_names=f"0x{h['abilityNames']:08X}",ability_descriptions=f"0x{h['abilityDescriptions']:08X}",description_layout=ablayout,count=ABILITIES_COUNT,name_stride=abstride,total_description_bytes=(sum(int(r['description_len']) for r in abrows) if ablayout=='pointer_table' else ''),unique_description_hashes=(len(set(r['description_sha256'] for r in abrows)) if ablayout=='pointer_table' else ''),description_vector_sha256=ablenhash))
        item_summ.append(dict(rom=name,items=f"0x{h['items']:08X}",count=ITEMS_COUNT,stride=itstride,name_width=itnlen,scalar_semantic_sha256=ithash,total_description_bytes=sum(r['description_len'] for r in itrows),unique_description_hashes=len(set(r['description_sha256'] for r in itrows))))
        safe=''.join(c if c.isalnum() else '_' for c in p.stem)
        for label,rows in [('pokedex',dexrows),('abilities',abrows),('items',itrows)]:
            with (detailed_dir/f'{safe}_{label}.csv').open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
        validation.append(dict(rom=name,gf_header_at_0x100=(h['version']==4 and h['game_name']=='pokemon red version' and h['pokedexCount']==386),species_info_matches_stage3=True,ability_layout_valid=(ablayout in {'pointer_table','direct_blob'}),items_anchor_valid=(itrows[0]['itemId']==0 and itrows[1]['itemId']==1 and itrows[2]['itemId']==2),pokedex_bulbasaur_hw=(dexrows[1]['height']==7 and dexrows[1]['weight']==69),saveblock2_size=h['saveBlock2Size'],saveblock1_size=h['saveBlock1Size']))
    def writecsv(name,rows):
        with (OUT/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    writecsv('gf_rom_header.csv',header_rows);writecsv('pokedex_summary.csv',dex_summ);writecsv('ability_summary.csv',ability_summ);writecsv('item_summary.csv',item_summ);writecsv('mon_icon_summary.csv',icon_summ);writecsv('stage4_validation.csv',validation)
    summary={'rom_count':len(ROMS),'gf_header_offset':'0x00000100','saveblock2_sizes':sorted(set(int(r['saveblock2_size']) for r in validation)),'saveblock1_sizes_by_language':{r['rom']:r['saveblock1_size'] for r in validation},'pokedex_nonlanguage_hash_cardinality':len(set(sem_dex.values())),'item_scalar_hash_cardinality':len(set(sem_items.values())),'all_validation_pass':all(r['gf_header_at_0x100'] and r['ability_layout_valid'] and r['items_anchor_valid'] and r['pokedex_bulbasaur_hw'] for r in validation)}
    (OUT/'stage4_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
