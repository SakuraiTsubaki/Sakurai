from pathlib import Path
import csv, math, hashlib, re
from collections import Counter, defaultdict

ROOT=Path('/mnt/data')
OUT=ROOT/'silver_analysis'/'stage2-semantic-census'
OUT.mkdir(parents=True, exist_ok=True)
ROM_FILES=[
'Pocket Monsters Gin (Japan).gbc',
'Pocket Monsters Gin (Japan) (Rev A).gbc',
'Pokemon - Silver Version (USA, Europe).gbc',
'Pokemon - Silberne Edition (Germany).gbc',
'Pokemon - Version Argent (France).gbc',
'Pokemon - Versione Argento (Italy).gbc',
'Pokemon - Edicion Plata (Spain).gbc',
'Pocket Monsters Eun (Korea).gbc',
]
LANG={
'Pocket Monsters Gin (Japan).gbc':'JP-Rev0',
'Pocket Monsters Gin (Japan) (Rev A).gbc':'JP-RevA',
'Pokemon - Silver Version (USA, Europe).gbc':'EN',
'Pokemon - Silberne Edition (Germany).gbc':'DE',
'Pokemon - Version Argent (France).gbc':'FR',
'Pokemon - Versione Argento (Italy).gbc':'IT',
'Pokemon - Edicion Plata (Spain).gbc':'ES',
'Pocket Monsters Eun (Korea).gbc':'KR',
}
FAMILY={k:('JP' if LANG[k].startswith('JP') else 'KR' if LANG[k]=='KR' else 'INTL') for k in LANG}

BASE={0x50:'@',0x7f:' ',0x54:'#',0x4a:'<PKMN>',0xe0:"'",0xe3:'-',0xe6:'?',0xe7:'!',0xe8:'.',0xe9:'&',0xea:'é',0xeb:'→',0xec:'▷',0xed:'▶',0xee:'▼',0xef:'♂',0xf0:'¥',0xf1:'×',0xf2:'.',0xf3:'/',0xf4:',',0xf5:'♀'}
for i in range(26):
    BASE[0x80+i]=chr(65+i)
    BASE[0xa0+i]=chr(97+i)
for i,c in enumerate('ÄÖÜäöü'): BASE[0xc0+i]=c
for i in range(10): BASE[0xf6+i]=str(i)
EXTRA={'EN':{},'DE':{},'FR':{0xE4:'+'},'IT':{0xBE:'À',0xC6:'È',0xCD:'Ù'},'ES':{0xBF:'Á',0xC7:'É',0xC9:'Í',0xCA:'Ñ',0xCC:'Ó',0xCE:'Ú'}}

def decode_western(bs, lang):
    m=dict(BASE); m.update(EXTRA.get(lang,{}))
    return ''.join(m.get(b, f'<{b:02X}>') for b in bs)

def entropy(data):
    if not data: return 0.0
    c=Counter(data); n=len(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def nonzero_span(bank):
    nz=[i for i,b in enumerate(bank) if b!=0]
    return (nz[0],nz[-1]+1) if nz else (None,None)

def semantic_class(label, zero=False):
    if zero: return 'free-zero'
    s=label.lower()
    if any(x in s for x in ['song','audio','sound','cries']): return 'audio'
    if any(x in s for x in ['pics','pic ','sprites','gfx','font','title screen','copyright','diploma','end']): return 'graphics-ui'
    if 'map blocks' in s or s=='maps / events': return 'map-data'
    if 'map script' in s or 'standard scripts' in s or 'phone scripts' in s: return 'scripts-dialogue'
    if any(x in s for x in ['pokedex entries','names','move descriptions','item descriptions','text 1','text 2','text 3','credits strings']): return 'localization-text'
    if any(x in s for x in ['hangul','dmg error']): return 'localization-system'
    if any(x in s for x in ['tileset']): return 'tileset-data'
    if any(x in s for x in ['battle','effect commands','evolutions and attacks','enemy trainers','egg moves']): return 'battle-pokemon-data'
    if label.startswith('bank') or label in ['ROM0: vectors/header/home','Home','Clock Reset','Catch Tutorial','Credits','Move Animations / Extra Songs 2','Pokégear GFX / mixed late data']:
        return 'engine-mixed'
    return 'other-mixed'

first=ROOT/'silver_analysis'/'full-census'/'bank_census.csv'
labels={}
if first.exists():
    with first.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f): labels[(r['file'],int(r['bank_dec']))]=r['layout_label']

atlas=[]
for fn in ROM_FILES:
    data=(ROOT/fn).read_bytes(); banks=len(data)//0x4000
    for b in range(banks):
        chunk=data[b*0x4000:(b+1)*0x4000]
        label=labels.get((fn,b),'unlabeled')
        if LANG[fn] in {'DE','FR','IT','ES'} and b==0x27: label='Localized landmark/location names overflow'
        if LANG[fn] in {'DE','FR','IT','ES'} and b==0x58: label='Localized map-script/dialogue overflow'
        z=all(x==0 for x in chunk); a,e=nonzero_span(chunk)
        atlas.append({'file':fn,'language':LANG[fn],'family':FAMILY[fn],'bank_hex':f'{b:02X}','bank_dec':b,'rom_start':f'0x{b*0x4000:06X}','rom_end':f'0x{(b+1)*0x4000:06X}','reference_label':label,'semantic_class':semantic_class(label,z),'all_zero':int(z),'entropy':round(entropy(chunk),6),'unique_bytes':len(set(chunk)),'nonzero_start_in_bank':'' if a is None else f'0x{a:04X}','nonzero_end_in_bank_exclusive':'' if e is None else f'0x{e:04X}','sha1':hashlib.sha1(chunk).hexdigest(),'provenance':'direct ROM + public linker-layout label'})
with (OUT/'semantic_bank_atlas.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=atlas[0].keys()); w.writeheader(); w.writerows(atlas)

western=[fn for fn in ROM_FILES if LANG[fn] in {'EN','DE','FR','IT','ES'}]
name_rows=[]; table_rows=[]; matrix=defaultdict(dict)
CATEGORY_COUNTS=[('item',256),('trainer_class',66),('pokemon_slot',256),('move',251)]
for fn in western:
    lang=LANG[fn]; data=(ROOT/fn).read_bytes(); bank_base=0x6c*0x4000; b=data[bank_base:bank_base+0x4000]; pos=0; cat_entries=[]
    for idx in range(1,257):
        end=b.index(0x50,pos); raw=b[pos:end]; cat_entries.append(('item',idx,pos,end+1,raw)); pos=end+1
    item_end=pos
    for idx in range(1,67):
        end=b.index(0x50,pos); raw=b[pos:end]; cat_entries.append(('trainer_class',idx,pos,end+1,raw)); pos=end+1
    trainer_end=pos; pokemon_start=pos
    for idx in range(1,257):
        start=pos+(idx-1)*10; end=start+10; rec=b[start:end]; raw=rec.rstrip(b'\x50'); cat_entries.append(('pokemon_slot',idx,start,end,raw))
    pos += 2560; move_start=pos
    for idx in range(1,252):
        end=b.index(0x50,pos); raw=b[pos:end]; cat_entries.append(('move',idx,pos,end+1,raw)); pos=end+1
    move_end=pos; assert len(cat_entries)==829
    table_rows += [
        {'file':fn,'language':lang,'table':'ItemNames','bank':'6C','start':f'0x{bank_base:06X}','end_exclusive':f'0x{bank_base+item_end:06X}','bytes':item_end,'records':256,'format':'@-terminated variable length'},
        {'file':fn,'language':lang,'table':'TrainerClassNames','bank':'6C','start':f'0x{bank_base+item_end:06X}','end_exclusive':f'0x{bank_base+trainer_end:06X}','bytes':trainer_end-item_end,'records':66,'format':'@-terminated variable length'},
        {'file':fn,'language':lang,'table':'PokemonNames','bank':'6C','start':f'0x{bank_base+pokemon_start:06X}','end_exclusive':f'0x{bank_base+move_start:06X}','bytes':2560,'records':256,'format':'fixed 10 bytes, @ padded'},
        {'file':fn,'language':lang,'table':'MoveNames','bank':'6C','start':f'0x{bank_base+move_start:06X}','end_exclusive':f'0x{bank_base+move_end:06X}','bytes':move_end-move_start,'records':251,'format':'@-terminated variable length'},]
    for cat,idx,s,e,raw in cat_entries:
        dec=decode_western(raw,lang); row={'file':fn,'language':lang,'category':cat,'index':idx,'bank':'6C','rom_offset':f'0x{bank_base+s:06X}','record_end_exclusive':f'0x{bank_base+e:06X}','record_bytes':e-s,'decoded':dec,'raw_hex':raw.hex().upper()}; name_rows.append(row); matrix[(cat,idx)][lang]=dec; matrix[(cat,idx)][lang+'_offset']=row['rom_offset']
with (OUT/'western_name_table_locations.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=table_rows[0].keys()); w.writeheader(); w.writerows(table_rows)
with (OUT/'western_name_inventory_829x5.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=name_rows[0].keys()); w.writeheader(); w.writerows(name_rows)
matrix_rows=[]
for cat,count in CATEGORY_COUNTS:
    for idx in range(1,count+1):
        d=matrix[(cat,idx)]; row={'category':cat,'index':idx}
        for lang in ['EN','DE','FR','IT','ES']: row[lang]=d.get(lang,''); row[lang+'_offset']=d.get(lang+'_offset','')
        matrix_rows.append(row)
with (OUT/'western_name_matrix_829.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=matrix_rows[0].keys()); w.writeheader(); w.writerows(matrix_rows)
unknown=[]
for r in name_rows:
    for v in re.findall(r'<([0-9A-F]{2})>',r['decoded']): unknown.append((r['language'],v,r['category'],r['index'],r['decoded']))
with (OUT/'western_name_decode_unknowns.csv').open('w',encoding='utf-8-sig',newline='') as f:
    fields=['language','byte_hex','category','index','decoded']; w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); [w.writerow(dict(zip(fields,x))) for x in unknown]

def find_fixed_name_table(bank, width, records=256):
    best=None
    for off in range(0,len(bank)-width*records+1):
        good=0; pads=0
        for i in range(records):
            rec=bank[off+i*width:off+(i+1)*width]
            if 0x50 in rec:
                j=rec.index(0x50)
                if j>0 and all(x==0x50 for x in rec[j:]): good+=1; pads+=width-j
            elif any(rec) and len(set(rec))>1: good+=1
        score=(good,pads)
        if best is None or score>best[0]: best=(score,off)
    return best
fixed_rows=[]; fixed_summary=[]
for fn,bankno,width in [('Pocket Monsters Gin (Japan).gbc',0x14,5),('Pocket Monsters Gin (Japan) (Rev A).gbc',0x14,5),('Pocket Monsters Eun (Korea).gbc',0x6c,10)]:
    data=(ROOT/fn).read_bytes(); bank=data[bankno*0x4000:(bankno+1)*0x4000]; (good,pads),off=find_fixed_name_table(bank,width); base=bankno*0x4000+off
    fixed_summary.append({'file':fn,'language':LANG[fn],'table':'PokemonNames','bank':f'{bankno:02X}','start':f'0x{base:06X}','end_exclusive':f'0x{base+256*width:06X}','record_width':width,'records':256,'structural_good_records':good,'padding_bytes':pads,'detection':'fixed-width @-padding structural scan'})
    for idx in range(1,257):
        rec=data[base+(idx-1)*width:base+idx*width]; fixed_rows.append({'file':fn,'language':LANG[fn],'index':idx,'rom_offset':f'0x{base+(idx-1)*width:06X}','raw_hex':rec.hex().upper(),'trimmed_raw_hex':rec.rstrip(b'\x50').hex().upper()})
with (OUT/'jp_kr_pokemon_name_table_locations.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fixed_summary[0].keys()); w.writeheader(); w.writerows(fixed_summary)
with (OUT/'jp_kr_pokemon_name_records_raw.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fixed_rows[0].keys()); w.writeheader(); w.writerows(fixed_rows)
summary=[]
for fn in ROM_FILES:
    rows=[r for r in atlas if r['file']==fn]; by=Counter(r['semantic_class'] for r in rows)
    for cls,n in sorted(by.items()): summary.append({'file':fn,'language':LANG[fn],'semantic_class':cls,'banks':n,'bytes':n*0x4000,'zero_banks':sum(int(r['all_zero']) for r in rows if r['semantic_class']==cls)})
with (OUT/'semantic_class_summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
print('Stage 2 complete:', OUT)
print('Western name records:', len(name_rows), 'unknown decoded bytes:', len(unknown))
