#!/usr/bin/env python3
from pathlib import Path
import hashlib, zlib, math, csv, json
from collections import Counter

BANK=0x4000
ROMS={
 'JP0': '/mnt/data/Pocket Monsters - Crystal Version (Japan).gbc',
 'EN0': '/mnt/data/Pokemon - Crystal Version (USA, Europe).gbc',
 'EN1': '/mnt/data/Pokemon - Crystal Version (USA, Europe) (Rev A).gbc',
 'ES0': '/mnt/data/Pokemon - Edicion Cristal (Spain).gbc',
 'DE0': '/mnt/data/Pokemon - Kristall-Edition (Germany).gbc',
 'FR0': '/mnt/data/Pokemon - Version Cristal (France).gbc',
 'IT0': '/mnt/data/Pokemon - Versione Cristallo (Italy).gbc',
}
# Exact pret/pokecrystal linker section map for English layout.link (current upstream checked 2026-09-09).
LABELS={
0x00:'ROM0: RST/interrupt vectors, Header, Home',
0x01:'bank1: link/OAM/map objects/intro/learn/math/items/NPC/events',
0x02:'bank2: player object/sine/predef/color',
0x03:'bank3: time/specials/HP/overworld/items/step/PC/item effects',
0x04:'bank4: pack/time/TMHM/naming/menu/events/party corrections',
0x05:'bank5: RTC/overworld/save/map setup/PC/mart/mom/daycare/breeding',
0x06:'Tileset Data 1',
0x07:'Roofs + Tileset Data 2 + Extra Songs 1',
0x08:'Clock Reset + Tileset Data 3 + Egg Moves',
0x09:'bank9: menus/battle menu/trainer card/decorations/move effects',
0x0A:'bankA + Trainer Backpics',
0x0B:'bankB: trainer HUDs/class names/TMHM/start battle/etc',
0x0C:'Tileset Data 4',
0x0D:'Effect Commands',
0x0E:'Enemy Trainers / battle AI trainer data',
0x0F:'Battle Core + effect command pointers',
0x10:'Pokédex + move data + evolution engine + Evolutions/Attacks',
0x11:'fruit trees/battle AI/Pokédex 2/mail',
0x12:'Crystal Features 1 / mobile / Celebi / main menu',
0x13:'map palettes/collision/save/link/stats/evolution movie/etc',
0x14:'party menu/events/types/stats/base stats/Pokémon names',
0x15:'Map Scripts 1',0x16:'Map Scripts 2',0x17:'Map Scripts 3',0x18:'Map Scripts 4',
0x19:'Crystal Phone Text',0x1A:'Map Scripts 5',0x1B:'Map Scripts 6',0x1C:'Map Scripts 7',
0x1D:'Map Scripts 8',0x1E:'Map Scripts 9',0x1F:'Map Scripts 10',
0x20:'player movement/engine flags/variables/battle text',
0x21:'printer + battle animation gfx + Hall of Fame',
0x22:'Crystal Features 2 / Kurt/player gfx/mobile/Unown walls/Battle Tower rules',
0x23:'timeofday palettes/battle transition/field moves/sprite anims/icons',
0x24:'phone/RTC/Pokégear/fishing/slot machine',
0x25:'Maps + Events',0x26:'Map Scripts 11',0x27:'Map Scripts 12',
0x28:'Phone Scripts 1',0x29:'Phone Text',0x2A:'Map Blocks 1',0x2B:'Map Blocks 2',
0x2C:'Map Blocks 3',0x2D:'Tileset Data 5',0x2E:'map-name/hidden items/trees/radio/mail',
0x2F:'Phone Scripts 2 + trainer scripts',
0x30:'Sprites 1',0x31:'Sprites 2',0x32:'battle anim bg/effects + move animations ptr/The End',
0x33:'Move Animations + Extra Songs 2',0x34:'Pic Animations 1',0x35:'Pic Animations 2',
0x36:'Font Inversed + Pic Animations 3',0x37:'Tileset Data 6',
0x38:'Unown/card flip/puzzle/memory/Bill PC',0x39:'Copyright + options/splash/intro',
0x3A:'Audio + Songs 1',0x3B:'Songs 2',0x3C:'Songs 3 + SFX + cries',0x3D:'Songs 4',
0x3E:'font/time capsule/name rater/new dex/Unown dex/Hidden Power',
0x3F:'tileset animations/NPC trade/mom phone',0x40:'Mobile 40',
0x41:'DMA/emotes/warp/mystery gift/used move text/mobile/font',
0x42:'Mobile 42 + Intro Logo + Credits',0x43:'Title',0x44:'Mobile Adapter SDK',
0x45:'Mobile Adapter SDK Mail + Mobile 45',0x46:'Mobile 46',0x47:'Battle Tower',
0x48:'Pic pointers + Pics 1',0x49:'Unown pic pointers + Pics 2',0x4A:'Trainer pic pointers + Pics 3',
0x4B:'Pics 4',0x4C:'Pics 5',0x4D:'Pics 6',0x4E:'Pics 7',0x4F:'Pics 8',
0x50:'Pics 9',0x51:'Pics 10',0x52:'Pics 11',0x53:'Pics 12',0x54:'Pics 13',
0x55:'Pics 14',0x56:'Pics 15',0x57:'Pics 16',0x58:'Pics 17',0x59:'Pics 18',0x5A:'Pics 19',
0x5B:'link trade/mobile + Pics 20',0x5C:'Mobile 5C + Pics 21',0x5D:'Crystal Phone Text 2 + Pics 22',
0x5E:'Battle HUD/Songs 5/Crystal SFX/Mobile 5E + Pics 23',0x5F:'Mobile 5F + Pics 24',
0x60:'Map Scripts 13 + Pokédex Entries 001-064',0x61:'Map Scripts 14',0x62:'Map Scripts 15',
0x63:'Map Scripts 16',0x64:'Map Scripts 17',0x65:'Map Scripts 18',0x66:'Map Scripts 19',
0x67:'Map Scripts 20',0x68:'Map Scripts 21',0x69:'Map Scripts 22',0x6A:'Map Scripts 23',
0x6B:'Map Scripts 24',0x6C:'Phone Text 2 + Map Scripts 25',0x6D:'Special Phone Text',
0x6E:'Pokédex Entries 065-128',0x6F:'Text 1',0x70:'Text 2',0x71:'Text 3',
0x72:'Misc text: item names/move names/landmarks',0x73:'Pokédex Entries 129-192',0x74:'Pokédex Entries 193-251',
0x77:'Unown font/Print Party/Tileset Data 7/Pokégear GFX/European Mail',
0x78:'Debug Room (conditional) + Tileset Data 8',0x7B:'Battle Tower Text',0x7C:'Battle Tower Trainer Data',
0x7D:'Mobile News Data',0x7E:'Crystal Events / Battle Tower load + Odd Egg',
0x7F:'Stadium 2 checksums at $7DE0-$7FFF',
}

def entropy(b):
    c=Counter(b); n=len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def longest_run(b, val):
    best=cur=0
    for x in b:
        if x==val: cur+=1; best=max(best,cur)
        else: cur=0
    return best

def diffcount(a,b): return sum(x!=y for x,y in zip(a,b))

def ptr16_count(b):
    n0=nx=0
    for i in range(len(b)-1):
        v=b[i]|(b[i+1]<<8)
        if 0x0150 <= v <= 0x3FFF: n0+=1
        if 0x4000 <= v <= 0x7FFF: nx+=1
    return n0,nx

out=Path('/mnt/data/crystal_work'); out.mkdir(exist_ok=True)
data={k:Path(v).read_bytes() for k,v in ROMS.items()}
assert all(len(v)==0x200000 for v in data.values())

rows=[]
for bank in range(128):
    chunks={k:v[bank*BANK:(bank+1)*BANK] for k,v in data.items()}
    shas={k:hashlib.sha1(c).hexdigest() for k,c in chunks.items()}
    unique=len(set(shas.values()))
    common_groups={}
    for k,s in shas.items(): common_groups.setdefault(s,[]).append(k)
    largest=max((len(v) for v in common_groups.values()))
    for k,b in chunks.items():
        p0,px=ptr16_count(b)
        rows.append({
            'rom':k,'bank':f'{bank:02X}','file_offset_start':f'0x{bank*BANK:06X}',
            'cpu_window': '0000-3FFF' if bank==0 else '4000-7FFF',
            'semantic_label_en':LABELS.get(bank,'UNMAPPED in upstream layout.link; investigate auto-placement/free/reserved'),
            'sha1':shas[k],'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','entropy':f'{entropy(b):.6f}',
            'zero_bytes':b.count(0),'ff_bytes':b.count(0xff),'longest_00_run':longest_run(b,0),'longest_ff_run':longest_run(b,0xff),
            'pointer_like_rom0':p0,'pointer_like_romx':px,
            'diff_vs_EN0':diffcount(b,chunks['EN0']),'diff_vs_EN1':diffcount(b,chunks['EN1']),'diff_vs_JP0':diffcount(b,chunks['JP0']),
            'unique_variants_in_7':unique,'largest_identical_group':largest,
        })

with (out/'bank_manifest.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

matrix=[]
for bank in range(128):
    chunks={k:v[bank*BANK:(bank+1)*BANK] for k,v in data.items()}
    r={'bank':f'{bank:02X}','semantic_label_en':LABELS.get(bank,'UNMAPPED')}
    for k in ROMS:
        r[f'{k}_diff_vs_EN0']=diffcount(chunks[k],chunks['EN0'])
        r[f'{k}_same_as_EN0']=chunks[k]==chunks['EN0']
    r['all7_identical']=len({hashlib.sha1(x).digest() for x in chunks.values()})==1
    matrix.append(r)
with (out/'bank_diff_matrix.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=matrix[0].keys());w.writeheader();w.writerows(matrix)

ranges=[]
a=data['EN0']; b=data['EN1']; i=0
while i<len(a):
    if a[i]==b[i]: i+=1; continue
    s=i
    while i<len(a) and a[i]!=b[i]: i+=1
    e=i
    bank=s//BANK
    ranges.append({'start':f'0x{s:06X}','end_exclusive':f'0x{e:06X}','length':e-s,'bank':f'{bank:02X}',
                   'bank_offset':f'0x{s%BANK:04X}','cpu_addr':f'0x{(s if bank==0 else 0x4000+s%BANK):04X}',
                   'en0':a[s:e].hex(),'en1':b[s:e].hex(),'label':LABELS.get(bank,'UNMAPPED')})
with (out/'en0_en1_diff_ranges.json').open('w',encoding='utf-8') as f: json.dump(ranges,f,ensure_ascii=False,indent=2)

lines=['# Pokémon Crystal 7-ROM Bank Survey','',
       'All 7 uploaded ROMs are 2 MiB / 128 × 16 KiB banks. English semantic labels are anchored to pret/pokecrystal `layout.link`; non-English banks are provisional until symbol/address matching is completed.','',
       '|Bank|English semantic anchor|All 7 identical|JP diff|EN1 diff|ES diff|DE diff|FR diff|IT diff|',
       '|---:|---|:---:|---:|---:|---:|---:|---:|---:|']
for r in matrix:
    lines.append('|{bank}|{label}|{all7}|{jp}|{en1}|{es}|{de}|{fr}|{it}|'.format(
        bank=r['bank'],label=r['semantic_label_en'].replace('|','/'),all7='✓' if r['all7_identical'] else '',
        jp=r['JP0_diff_vs_EN0'],en1=r['EN1_diff_vs_EN0'],es=r['ES0_diff_vs_EN0'],de=r['DE0_diff_vs_EN0'],fr=r['FR0_diff_vs_EN0'],it=r['IT0_diff_vs_EN0']))
(out/'BANK_SURVEY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

meta={'roms':{k:{'path':v,'sha1':hashlib.sha1(data[k]).hexdigest(),'size':len(data[k])} for k,v in ROMS.items()},
      'bank_size':BANK,'bank_count':128,'semantic_anchor':'pret/pokecrystal layout.link',
      'warning':'Do not publish ROM binaries or byte-complete db dumps. Semantic source/address maps/scripts only.'}
(out/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('wrote',out)
print('EN0/EN1 diff ranges',len(ranges),'bytes',sum(x['length'] for x in ranges))
