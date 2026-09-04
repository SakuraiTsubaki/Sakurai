#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, math, json
from collections import Counter

ROOT=Path('/mnt/data')
OUT=ROOT/'blue_rom_census'
OUT.mkdir(exist_ok=True)
BANK=0x4000
ROMS={
 'JP_AO': ROOT/'Pocket Monsters - Ao (Japan) (SGB Enhanced).gb',
 'DE_BLUE': ROOT/'Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb',
 'EN_BLUE': ROOT/'Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb',
 'ES_BLUE': ROOT/'Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb',
 'FR_BLUE': ROOT/'Pokemon - Version Bleue (France) (SGB Enhanced).gb',
 'IT_BLUE': ROOT/'Pokemon - Versione Blu (Italy) (SGB Enhanced).gb',
}
WEST=['DE_BLUE','EN_BLUE','ES_BLUE','FR_BLUE','IT_BLUE']
DATA={k:p.read_bytes() for k,p in ROMS.items()}

WEST_ROLES={
0:'ROM0 / interrupts / header / home engine',
1:'system engine / menus / naming / marts / Pokédex display',
2:'audio headers + SFX + audio engine 1 + music 1',
3:'overworld core / items / hidden-event dispatch / field logic',
4:'NPC sprites 1 + font + battle engine 1',
5:'NPC sprites 2 + battle engine 2',
6:'maps 1-2 + play time + doors/ledges',
7:'maps 3-4 + Pokémon names + hidden events 1',
8:'audio headers + SFX + audio engine 2 + music 2',
9:'Pokémon pics 1 + battle engine 3',
10:'Pokémon pics 2 + battle engine 4',
11:'Pokémon pics 3 + battle engine 5',
12:'Pokémon pics 4 + battle engine 6',
13:'Pokémon pics 5 + slot machines',
14:'battle engine 7 + move/base-stat/cry/evolution data',
15:'battle core + battle effects',
16:'Pokédex menu + trade/intro movies',
17:'maps 5-6 + Pokédex rating + hidden-event core',
18:'maps 7-8 + screen effects',
19:'trainer pics + maps 9 + predefs',
20:'maps 10 + battle engine 8 + hidden events 2',
21:'maps 11-12 + battle engine 9 + diploma + trainer sight',
22:'maps 13-14 + battle engine 10 + Saffron guards',
23:'maps 15-16 + starter dex + hidden events 3',
24:'maps 17-18 + Cinnabar lab + hidden events 4',
25:'tilesets 1',
26:'battle engine 11 + version gfx + tilesets 2',
27:'tilesets 3',
28:'splash/Hall of Fame/healing/player anims/transitions/map/icons/trades/palettes/save',
29:'maps 19-21 + itemfinder + vending + hidden items',
30:'battle animations + overworld effects + evolution + TM prices',
31:'audio headers + SFX + audio engine 3 + music 3',
32:'Text 1',33:'Text 2',34:'Text 3',35:'Text 4',36:'Text 5',37:'Text 6',38:'Text 7',39:'Text 8',40:'Text 9',41:'Text 10',42:'Text 11',
43:'Pokédex text',44:'move names',
}
for b in range(45,64): WEST_ROLES[b]='physical blank bank (outside linked 0x00-0x2C content)'

JP_ROLES={
0:'ROM0 / interrupts / header / home engine + garbage padding',
1:'system engine / menus / naming / marts / Pokédex display + garbage',
2:'audio 1 + garbage',
3:'overworld core / items / hidden-event dispatch + garbage',
4:'move names + NPC sprites 1 + font + battle engine 1 + garbage',
5:'NPC sprites 2 + battle engine 2 + garbage',
6:'maps 1-2 + play time + doors/ledges + garbage',
7:'maps 3-4 + clear save + hidden events 1 + garbage',
8:'audio 2',
9:'Pokémon pics 1 + battle engine 3 + garbage',
10:'Pokémon pics 2 + battle engine 4 + garbage',
11:'Pokémon pics 3 + battle engine 5 + garbage',
12:'Pokémon pics 4 + battle engine 6 + garbage',
13:'Pokémon pics 5 + slots + garbage',
14:'battle engine 7 incl. Pokémon names/data + garbage',
15:'battle core',
16:'Pokédex/trade/intro + garbage',
17:'maps 5-6 + rating + hidden core + garbage',
18:'maps 7-8 + screen effects + garbage',
19:'trainer pics + maps 9 + predefs + garbage',
20:'maps 10 + battle engine 8 + hidden 2 + garbage',
21:'maps 11-12 + battle engine 9 + diploma/trainer sight + garbage',
22:'maps 13-14 + battle engine 10 + Saffron guards + garbage',
23:'maps 15-16 + starter dex + hidden 3 + garbage',
24:'maps 17-18 + Cinnabar lab + hidden 4 + garbage',
25:'tilesets 1 + garbage',
26:'battle engine 11 + version gfx + tilesets 2 + garbage',
27:'tilesets 3',
28:'credits/splash/HOF/etc + garbage',
29:'maps 19-21 + itemfinder/vending/hidden items + garbage',
30:'battle animation/status/effects/evolution/TM prices + garbage',
31:'audio 3 + garbage',
}

# Exact source-confirmed EN linker-map free bytes, from pret/pokered symbols branch pokeblue.map.
EN_FREE={
0:0x009c,1:0x03b7,2:0x000c,3:0x03b6,4:0x0560,5:0x00a1,6:0x18e8,7:0x133e,8:0x00ae,9:0x0048,
10:0x0104,11:0x00c4,12:0x0070,13:0x0178,14:0x041a,15:0x0438,16:0x180d,17:0x0f55,18:0x1c71,19:0x005e,
20:0x15be,21:0x15b5,22:0x1a45,23:0x20eb,24:0x1ad6,25:0x0020,26:0x0011,27:0x0000,28:0x0463,29:0x1784,
30:0x0040,31:0x0006,32:0x1551,33:0x135f,34:0x1307,35:0x13f7,36:0x16fd,37:0x15c8,38:0x1485,39:0x155c,
40:0x15c9,41:0x146c,42:0x3cd0,43:0x07c8,44:0x39f1,
}
assert sum(EN_FREE[b] for b in range(1,45))==161714

def entropy(buf):
    if not buf:return 0.0
    c=Counter(buf); n=len(buf)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def trailing(buf,val=0):
    n=0
    for x in reversed(buf):
        if x==val:n+=1
        else:break
    return n

def longest_run(buf,val):
    best=cur=0; best_s=0; s=0
    for i,x in enumerate(buf):
        if x==val:
            if cur==0:s=i
            cur+=1
            if cur>best: best, best_s=cur,s
        else: cur=0
    return best_s,best

def runs_of(buf,val,minlen):
    out=[]; s=None
    for i,x in enumerate(buf):
        if x==val and s is None:s=i
        if x!=val and s is not None:
            if i-s>=minlen: out.append((s,i-1,i-s))
            s=None
    if s is not None and len(buf)-s>=minlen: out.append((s,len(buf)-1,len(buf)-s))
    return out

def bank_addr(bank,off):
    if bank==0:return off
    return 0x4000+off

def pct(a,b):
    return 100.0*a/b if b else 0.0

# source verification
source_rows=[
 ['JP_AO','0da501e3e5c51ab8fef55b092dcdd7e6b050e424','Narishma-gb/pokeblue','exact','layout.link + symbols map available'],
 ['EN_BLUE','d7037c83e1ae5b39bde3c30787637ba1d4c48ce2','pret/pokered','exact','layout.link + symbols map available'],
 ['DE_BLUE','20e72dc6f41493eee1fdd0cef54214e6c3389688','einstein95/pokered-de','exact','layout.link + exact SHA source; symbols available'],
 ['FR_BLUE','47faa910d0e073c600665bf9c83b6bd17babdf8a','einstein95/pokered-fr','exact','layout.link + exact SHA source'],
 ['ES_BLUE','7715e7b133e8634df48918b9138374110212a108','einstein95/pokered-es','exact','layout.link + exact SHA source'],
 ['IT_BLUE','f69ed1a1332f04c24c7db899a09019bb045fa8b3','','raw-only','no exact public disassembly verified in this pass'],
]
with (OUT/'source_verification.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['rom','sha1','source_repo','verification','notes']); w.writerows(source_rows)

# per-bank raw stats and topology
rows=[]
for rk,data in DATA.items():
    nb=len(data)//BANK
    for b in range(nb):
        buf=data[b*BANK:(b+1)*BANK]
        z=buf.count(0); ff=buf.count(0xff)
        lzs,lzl=longest_run(buf,0); ffs,ffl=longest_run(buf,0xff)
        role=(JP_ROLES if rk=='JP_AO' else WEST_ROLES).get(b,'')
        en_sim=''
        if rk!='JP_AO' and b < len(DATA['EN_BLUE'])//BANK:
            e=DATA['EN_BLUE'][b*BANK:(b+1)*BANK]
            same=sum(x==y for x,y in zip(buf,e)); en_sim=f'{pct(same,BANK):.6f}'
        west_same=''
        if rk!='JP_AO':
            chunks=[DATA[x][b*BANK:(b+1)*BANK] for x in WEST]
            same=sum(len(set(vs))==1 for vs in zip(*chunks)); west_same=f'{pct(same,BANK):.6f}'
        rows.append({
            'rom':rk,'bank_dec':b,'bank_hex':f'{b:02X}','file_start':f'{b*BANK:06X}','file_end':f'{(b+1)*BANK-1:06X}',
            'role':role,'sha1':hashlib.sha1(buf).hexdigest(),'entropy':f'{entropy(buf):.6f}','zero_bytes':z,'ff_bytes':ff,
            'trailing_00':trailing(buf,0),'trailing_ff':trailing(buf,0xff),'longest_00_start':f'{lzs:04X}','longest_00_len':lzl,
            'longest_ff_start':f'{ffs:04X}','longest_ff_len':ffl,'same_position_vs_EN_pct':en_sim,
            'western_all5_same_pct':west_same,'EN_source_free_bytes':EN_FREE.get(b,'') if rk=='EN_BLUE' else ''
        })
with (OUT/'bank_role_matrix.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# Western same-position consensus and language comparisons
wr=[]
shared_runs=[]
for b in range(64):
    chunks=[DATA[x][b*BANK:(b+1)*BANK] for x in WEST]
    eq=[len(set(vals))==1 for vals in zip(*chunks)]
    same=sum(eq)
    runs=[]; s=None
    for i,v in enumerate(eq+[False]):
        if v and s is None:s=i
        if not v and s is not None:
            runs.append((s,i-1,i-s)); s=None
    big=[r for r in runs if r[2]>=32]
    for s,e,n in big:
        shared_runs.append({
            'bank_dec':b,'bank_hex':f'{b:02X}','role':WEST_ROLES.get(b,''),'bank_offset_start':f'{s:04X}','bank_offset_end':f'{e:04X}',
            'cpu_addr_start':f'{bank_addr(b,s):04X}','cpu_addr_end':f'{bank_addr(b,e):04X}','file_offset_start':f'{b*BANK+s:06X}','file_offset_end':f'{b*BANK+e:06X}','length':n
        })
    used_lens=[BANK-trailing(c,0) for c in chunks]
    union_used=max(used_lens)
    common_used=min(used_lens)
    union_same=sum(eq[:union_used]) if union_used else 0
    common_same=sum(eq[:common_used]) if common_used else 0
    row={'bank_dec':b,'bank_hex':f'{b:02X}','role':WEST_ROLES.get(b,''),'all5_same_bytes':same,'all5_same_pct':f'{pct(same,BANK):.6f}',
         'used_union_len':union_used,'all5_same_pct_used_union':f'{pct(union_same,union_used):.6f}' if union_used else '',
         'used_common_len':common_used,'all5_same_pct_used_common':f'{pct(common_same,common_used):.6f}' if common_used else '',
         'shared_runs_ge32':len(big),'shared_runs_ge32_bytes':sum(r[2] for r in big),'longest_shared_run':max([r[2] for r in runs] or [0])}
    en=chunks[1]
    for idx,rk in enumerate(WEST):
        same_en=sum(a==bb for a,bb in zip(chunks[idx],en))
        row[f'{rk}_vs_EN_pct']=f'{pct(same_en,BANK):.6f}'
        row[f'{rk}_trailing_00']=trailing(chunks[idx],0)
    wr.append(row)
with (OUT/'western_bank_diff.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(wr[0])); w.writeheader(); w.writerows(wr)
with (OUT/'western_shared_runs.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(shared_runs[0])); w.writeheader(); w.writerows(shared_runs)

# Filler run candidates (raw heuristic; not safe-space claim)
fr=[]
for rk,data in DATA.items():
    nb=len(data)//BANK
    for b in range(nb):
        buf=data[b*BANK:(b+1)*BANK]
        for val in (0,0xff):
            for s,e,n in runs_of(buf,val,256):
                fr.append({'rom':rk,'bank_dec':b,'bank_hex':f'{b:02X}','value':f'{val:02X}','bank_offset_start':f'{s:04X}','bank_offset_end':f'{e:04X}',
                           'cpu_addr_start':f'{bank_addr(b,s):04X}','cpu_addr_end':f'{bank_addr(b,e):04X}','file_offset_start':f'{b*BANK+s:06X}','file_offset_end':f'{b*BANK+e:06X}',
                           'length':n,'reaches_bank_end':e==BANK-1,'classification':'trailing padding candidate' if e==BANK-1 else 'internal filler candidate'})
with (OUT/'filler_runs_ge256.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(fr[0])); w.writeheader(); w.writerows(fr)

# EN exact linker free map
free_rows=[]
# bank0 has two ranges
for s,e in [(0x00be,0x00ff),(0x3fa6,0x3fff)]:
    free_rows.append({'bank_dec':0,'bank_hex':'00','role':WEST_ROLES[0],'cpu_start':f'{s:04X}','cpu_end':f'{e:04X}','file_start':f'{s:06X}','file_end':f'{e:06X}','length':e-s+1,'authority':'pret/pokered pokeblue.map'})
for b in range(1,45):
    n=EN_FREE[b]
    if n:
        s=0x8000-n; e=0x7fff
        free_rows.append({'bank_dec':b,'bank_hex':f'{b:02X}','role':WEST_ROLES[b],'cpu_start':f'{s:04X}','cpu_end':f'{e:04X}','file_start':f'{b*BANK+(s-0x4000):06X}','file_end':f'{(b+1)*BANK-1:06X}','length':n,'authority':'pret/pokered pokeblue.map'})
with (OUT/'EN_source_confirmed_free_space.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(free_rows[0])); w.writeheader(); w.writerows(free_rows)

# topology comparison JP vs western for banks 0..31
tr=[]
for b in range(32):
    tr.append({'bank_dec':b,'bank_hex':f'{b:02X}','JP_role':JP_ROLES[b],'Western_role':WEST_ROLES[b],
               'same_position_JP_vs_EN_pct':f'{pct(sum(x==y for x,y in zip(DATA["JP_AO"][b*BANK:(b+1)*BANK],DATA["EN_BLUE"][b*BANK:(b+1)*BANK])),BANK):.6f}'})
with (OUT/'JP_vs_Western_topology.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(tr[0])); w.writeheader(); w.writerows(tr)

# machine summary
summary={
 'roms':{k:{'file':ROMS[k].name,'size':len(v),'banks':len(v)//BANK,'sha1':hashlib.sha1(v).hexdigest()} for k,v in DATA.items()},
 'western':{
   'linked_active_banks':'0x00-0x2C (45 banks including ROM0)',
   'physical_blank_tail_banks':'0x2D-0x3F (19 banks)',
   'physical_blank_tail_bytes':19*BANK,
   'EN_source_confirmed_ROMX_free_bytes_banks_01_2C':sum(EN_FREE[b] for b in range(1,45)),
   'EN_source_confirmed_ROM0_free_bytes':EN_FREE[0],
   'EN_source_confirmed_text_area_free_bytes_banks_20_2C':sum(EN_FREE[b] for b in range(32,45)),
   'all5_exact_nonblank_banks':[b for b in range(45) if all(DATA[WEST[0]][b*BANK:(b+1)*BANK]==DATA[r][b*BANK:(b+1)*BANK] for r in WEST[1:])],
 },
 'jp':{'linked_banks':'0x00-0x1F','source_map_ROM0_free':0,'source_map_ROMX_free':1},
 'notes':['Western exact layout is source-verified for EN/DE/FR/ES; IT role mapping is inferred from bank topology and raw alignment.','Raw zero/FF runs are heuristics and are not safe-space claims. EN_source_confirmed_free_space.csv is authoritative for the canonical EN ROM.']
}
(OUT/'deep_census_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')

print(json.dumps(summary,indent=2,ensure_ascii=False))
