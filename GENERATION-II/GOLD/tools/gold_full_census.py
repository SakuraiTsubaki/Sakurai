#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from collections import Counter, defaultdict
import csv, hashlib, itertools, json, math, re

ROOT=Path('/mnt/data')
OUT=ROOT/'gold-full-census'
OUT.mkdir(exist_ok=True)
BANK=0x4000

FILES={
 'JP0': ROOT/'Pocket Monsters Kin (Japan).gbc',
 'JPA': ROOT/'Pocket Monsters Kin (Japan) (Rev A).gbc',
 'EN': ROOT/'Pokemon - Gold Version (USA, Europe).gbc',
 'DE': ROOT/'Pokemon - Goldene Edition (Germany).gbc',
 'FR': ROOT/'Pokemon - Version Or (France).gbc',
 'IT': ROOT/'Pokemon - Versione Oro (Italy).gbc',
 'ES': ROOT/'Pokemon - Edicion Oro (Spain).gbc',
 'KR': ROOT/'Pocket Monsters Geum (Korea).gbc',
}
ROMS={k:p.read_bytes() for k,p in FILES.items()}

def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()
def entropy(b):
 c=Counter(b); n=len(b)
 return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0.0

def longest_run(b, val):
 best=cur=0
 for x in b:
  if x==val: cur+=1; best=max(best,cur)
  else: cur=0
 return best

def trailing_run(b,val):
 n=0
 for x in reversed(b):
  if x==val:n+=1
  else:break
 return n

def chunksig(b, n=64):
 return {hashlib.blake2s(b[i:i+n],digest_size=8).digest() for i in range(0,len(b),n)}

def jaccard(a,b):
 return len(a&b)/len(a|b) if a|b else 1.0

def aligned_equal(a,b):
 n=min(len(a),len(b)); return sum(x==y for x,y in zip(a[:n],b[:n]))/n if n else 1.0

# Reference layouts (from exact-match disassemblies noted in report).
EN_ROLES={
0x00:'Header/Home/RST/interrupts',0x01:'Core engine/menu/items',0x02:'Palette/player/math/predef',0x03:'Events/items/pokemon core',0x04:'Movement/menus/naming/events',0x05:'RTC/overworld/save/marts/breeding',
0x06:'Tileset Data 1',0x07:'Roofs/Tileset Data 2/Extra Songs 1',0x08:'Clock Reset/Tileset Data 3/Catch Tutorial/Egg Moves',0x09:'Menus/text buffers/battle menu',0x0A:'Link/Mystery Gift/Wildmons',0x0B:'Descriptions/trainers/TMHM/Pokerus',0x0C:'Tileset Data 4',0x0D:'Effect Commands',0x0E:'Enemy Trainers',0x0F:'Battle Core',0x10:'Pokedex/moves/evolution',0x11:'AI/Pokedex2/events',0x12:'Pic pointers/Pics 1',0x14:'Party/base stats/names/pics loader',
0x15:'Pics 2',0x16:'Pics 3',0x17:'Pics 4',0x18:'Pics 5',0x19:'Pics 6',0x1A:'Pics 7',0x1B:'Pics 8',0x1C:'Pics 9',0x1D:'Pics 10',0x1E:'Pics 11',0x1F:'Unown pic pointers/Pics 12',0x20:'Trainer pic pointers/Pics 13',0x21:'Printer/Battle anim GFX/Hall of Fame/Credits',0x23:'Save/phone tilemap, field moves, sprite anims, icons',0x24:'Phone/RTC/Pokegear/landmarks/slot machine',0x25:'Maps/Events',0x26:'Title Screen',0x2A:'Map Blocks 1',0x2B:'Map Blocks 2',0x2E:'Pics 14/bank2E',0x30:'Sprites 1',0x31:'Sprites 2/bank31',0x32:'Battle anim BG/The End',0x33:'Move Animations/Extra Songs 2',0x36:'Font Inversed',0x37:'Map Blocks 3/Tileset Data 5',0x38:'Diploma/minigames/Bills PC',0x39:'Copyright/Title Screen 2',0x3A:'Audio/Songs 1',0x3B:'Songs 2',0x3C:'Songs 3/SFX/Cries',0x3D:'Songs 4',0x3E:'Font/collision/time capsule/etc',0x3F:'Debug dummy/tileset anims/NPC trade/etc',
0x40:'Standard Scripts',0x41:'Phone Scripts',0x42:'Map Scripts 1',0x43:'Map Scripts 2',0x44:'Map Scripts 3',0x45:'Map Scripts 4',0x46:'Map Scripts 5',0x47:'Map Scripts 6',0x48:'Map Scripts 7',0x49:'Map Scripts 8',0x4A:'Map Scripts 9',0x4B:'Map Scripts 10',0x4C:'Map Scripts 11',0x4D:'Map Scripts 12',0x4E:'Map Scripts 13',0x4F:'Map Scripts 14',0x50:'Map Scripts 15',0x51:'Map Scripts 16',0x52:'Map Scripts 17',0x53:'Map Scripts 18',0x54:'Map Scripts 19',0x55:'Map Scripts 20',0x56:'Map Scripts 21',0x57:'Map Scripts 22',0x59:'Map Scripts 23',0x5A:'Map Scripts 24',0x5B:'Map Scripts 25',0x5C:'Map Scripts 26',0x5D:'Map Scripts 27',0x5E:'Map Scripts 28',0x5F:'Map Scripts 29',0x60:'Map Scripts 30',0x61:'Map Scripts 31',0x62:'Map Scripts 32',0x64:'Text 1',0x65:'Text 2',0x66:'Text 3',0x68:'Pokedex 001-064',0x69:'Pokedex 065-128',0x6A:'Pokedex 129-192',0x6B:'Pokedex 193-251',0x6C:'Names',0x6D:'Move Descriptions',0x6E:'Item Descriptions',0x70:'Tileset 6/Pokegear GFX/Credits Strings',0x7F:'Stadium 2 checksums'}
JP_ROLES={
0x00:'Header/Home/RST/interrupts',0x01:'Core engine/menu/items',0x02:'Palette/player/math/predef',0x03:'Events/items/pokemon core',0x04:'Movement/menus/naming/events',0x05:'RTC/overworld/save/marts/breeding',0x06:'Tileset Data 1',0x07:'Roofs/Tileset Data 2/Extra Songs 1',0x08:'Clock Reset/Tileset Data 3/Catch Tutorial/Egg Moves',0x09:'Menus/text buffers/battle menu',0x0A:'Link/Mystery Gift/Wildmons',0x0B:'Item/move descriptions/trainers',0x0C:'Tileset Data 4',0x0D:'Effect Commands',0x0E:'Enemy Trainers',0x0F:'Battle Core',0x10:'Pokedex/moves/evolution',0x11:'Pokedex Entries/Pokemon Mail',0x12:'Pic pointers/Pics 1',0x13:'Map Scripts 1',0x14:'Party/base stats/names',0x15:'Pics 2',0x16:'Pics 3',0x17:'Pics 4',0x18:'Pics 5',0x19:'Pics 6',0x1A:'Pics 7',0x1B:'Pics 8',0x1C:'Pics 9',0x1D:'Pics 10',0x1E:'Pics 11',0x1F:'Unown Pics',0x20:'Trainer Pics',0x21:'Printer/HOF/Credits',0x22:'Map Scripts 2',0x23:'Field moves/Sprite anims/icons',0x24:'Phone/RTC/Pokegear',0x25:'Maps/Events',0x26:'Map Scripts 3',0x27:'Map Scripts 4',0x28:'Map Scripts 5',0x29:'Map Scripts 6',0x2A:'Map Blocks 1',0x2B:'Map Blocks 2',0x2C:'Map Scripts 7',0x2D:'Map Scripts 8',0x2E:'Pics 14/bank2E',0x2F:'Map Scripts 9',0x30:'Sprites 1',0x31:'Sprites 2',0x32:'Battle anim BG/The End',0x33:'Move Animations/Extra Songs 2',0x34:'Map Scripts 10',0x35:'Map Scripts 11',0x36:'Standard/Phone/Map Scripts 12',0x37:'Map Blocks 3/Tileset 5',0x38:'Diploma/minigames/Bills PC',0x39:'Copyright/Title/Options/Font/Intro',0x3A:'Audio/Songs 1',0x3B:'Songs 2',0x3C:'Songs 3/SFX/Cries',0x3D:'Songs 4',0x3E:'Font/collision/time capsule/etc',0x3F:'Debug/tileset anims/NPC trade/etc'}
KR_ROLES=dict(EN_ROLES)
for b in list(range(0x54,0x58)) + list(range(0x59,0x63)):
 KR_ROLES[b] = EN_ROLES[b] + ' (ROM present; KR WIP source not yet sectioned)'
KR_ROLES.update({0x68:'Pokedex Entries 001-128',0x69:'Pokedex Entries 129-251',0x6A:'unassigned/padding',0x6B:'unassigned/padding',0x71:'Hangul naming/composition tables + naming-screen GFX (KR)',0x72:'DMG Error Screen',0x78:'Hangul Tables 1',0x79:'Hangul Tables 2',0x7A:'Hangul Tables 3',0x7B:'Diploma GFX',0x7F:'Hangul/double-byte renderer + core support (KR)'})

# bank inventory
bank_rows=[]
for code,data in ROMS.items():
 roles=JP_ROLES if code.startswith('JP') else KR_ROLES if code=='KR' else EN_ROLES
 for i in range(0,len(data),BANK):
  bank=i//BANK; b=data[i:i+BANK]; c=Counter(b)
  bank_rows.append({
   'rom':code,'bank':f'{bank:02X}','role_reference':roles.get(bank,'unassigned/padding/unknown'),
   'sha1':sha1(b),'entropy':f'{entropy(b):.6f}','unique_bytes':len(c),
   'zero_fraction':f'{c[0]/len(b):.6f}','ff_fraction':f'{c[255]/len(b):.6f}',
   'nonzero_bytes':len(b)-c[0],'non_ff_bytes':len(b)-c[255],
   'longest_zero_run':longest_run(b,0),'longest_ff_run':longest_run(b,255),
   'trailing_zero_run':trailing_run(b,0),'trailing_ff_run':trailing_run(b,255),
   'all_zero':all(x==0 for x in b),'all_ff':all(x==255 for x in b),
  })
with (OUT/'bank_inventory.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=bank_rows[0].keys());w.writeheader();w.writerows(bank_rows)

# pairwise exact/shared + same-index byte similarity
pair_rows=[]
for a,b in itertools.combinations(ROMS,2):
 A=ROMS[a];B=ROMS[b]; nb=min(len(A),len(B))//BANK
 exact=[]; sim=[]
 for i in range(nb):
  aa=A[i*BANK:(i+1)*BANK];bb=B[i*BANK:(i+1)*BANK]
  eq=aligned_equal(aa,bb);sim.append(eq)
  if aa==bb:exact.append(i)
 pair_rows.append({'rom_a':a,'rom_b':b,'banks_compared':nb,'exact_same_index_banks':len(exact),'exact_bank_list':' '.join(f'{i:02X}' for i in exact),'mean_same_index_byte_equality':f'{sum(sim)/len(sim):.6f}','median_same_index_byte_equality':f'{sorted(sim)[len(sim)//2]:.6f}'})
with (OUT/'pairwise_bank_comparison.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=pair_rows[0].keys());w.writeheader();w.writerows(pair_rows)

# similarity to EN: same index plus best EN bank by 64-byte exact-chunk Jaccard
EN=ROMS['EN']; en_banks=[EN[i:i+BANK] for i in range(0,len(EN),BANK)]; en_sigs=[chunksig(x) for x in en_banks]
sim_rows=[]
for code,data in ROMS.items():
 if code=='EN':continue
 for i in range(0,len(data),BANK):
  bi=i//BANK; b=data[i:i+BANK]; sig=chunksig(b)
  scores=[jaccard(sig,s) for s in en_sigs]
  best=max(range(len(scores)), key=scores.__getitem__)
  same=aligned_equal(b,en_banks[bi]) if bi<len(en_banks) else 0
  sim_rows.append({'rom':code,'bank':f'{bi:02X}','same_index_en_role':EN_ROLES.get(bi,'unassigned/padding/unknown'),'same_index_byte_equality':f'{same:.6f}','best_en_bank':f'{best:02X}','best_en_role':EN_ROLES.get(best,'unassigned/padding/unknown'),'chunk_jaccard':f'{scores[best]:.6f}','best_is_same_index':best==bi})
with (OUT/'bank_similarity_to_en.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=sim_rows[0].keys());w.writeheader();w.writerows(sim_rows)

# Pointer-like far triples. Keep source->target-bank counts; this is heuristic, explicitly labeled.
ptr_rows=[]
for code,data in ROMS.items():
 nb=len(data)//BANK
 matrix=defaultdict(int)
 for off in range(0,len(data)-2):
  bank=data[off]; addr=data[off+1] | (data[off+2]<<8)
  if bank < nb and 0x4000 <= addr <= 0x7fff:
   matrix[(off//BANK,bank)] += 1
 for (src,tgt),n in sorted(matrix.items()):
  if n>=3:
   ptr_rows.append({'rom':code,'source_bank':f'{src:02X}','target_bank_candidate':f'{tgt:02X}','triple_hits':n,'note':'heuristic bank+little-endian-ROMX-address pattern; may include false positives'})
with (OUT/'far_pointer_candidate_matrix.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=ptr_rows[0].keys());w.writeheader();w.writerows(ptr_rows)

# Text-likeness estimators by encoding family. These are detection metrics, not authoritative extraction.
west_char=set([0x7f,*range(0x80,0x9a),*range(0x9a,0xa0),*range(0xa0,0xba),*range(0xc0,0xc6),*range(0xd0,0xd7),0xdf,0xe0,0xe1,0xe2,0xe3,0xe6,0xe7,0xe8,0xe9,0xea,0xeb,0xec,0xed,0xee,0xef,0xf0,0xf1,0xf2,0xf3,0xf4,0xf5,*range(0xf6,0x100)])
west_ctrl=set(range(0x4a,0x60))|{0x1f,0x22,0x24,0x25,0x38,0x39,0x3f,0x49}
jp_char=set(range(0x05,0x49))|set(range(0x6e,0x100))
jp_ctrl=set(range(0x14,0x60))

def text_metric(code,b):
 if code=='KR':
  i=0; units=valid=hangul=0
  while i<len(b):
   x=b[i];units+=1
   if 1<=x<=0x0b and i+1<len(b):
    valid+=1;hangul+=1;i+=2;continue
   if x in west_char or x in {0x50,*range(0x1d,0x60)}: valid+=1
   i+=1
  return valid/units if units else 0,hangul
 allowed=(jp_char|jp_ctrl|{0x50}) if code.startswith('JP') else (west_char|west_ctrl|{0x50})
 valid=sum(x in allowed for x in b)
 return valid/len(b),0
text_rows=[]
for code,data in ROMS.items():
 roles=JP_ROLES if code.startswith('JP') else KR_ROLES if code=='KR' else EN_ROLES
 for i in range(0,len(data),BANK):
  bank=i//BANK;b=data[i:i+BANK];score,hpairs=text_metric(code,b)
  text_rows.append({'rom':code,'bank':f'{bank:02X}','role_reference':roles.get(bank,'unassigned/padding/unknown'),'text_like_fraction':f'{score:.6f}','korean_two_byte_lead_pairs':hpairs,'terminator_0x50_count':b.count(0x50)})
with (OUT/'text_likeness_by_bank.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=text_rows[0].keys());w.writeheader();w.writerows(text_rows)

# Western high-confidence terminated strings, useful for localizing language data banks.
DEC={0x7f:' '}
for i,ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ',0x80):DEC[i]=ch
for i,ch in enumerate('abcdefghijklmnopqrstuvwxyz',0xa0):DEC[i]=ch
DEC.update({0x9a:'(',0x9b:')',0x9c:':',0x9d:';',0x9e:'[',0x9f:']',0xc0:'Ä',0xc1:'Ö',0xc2:'Ü',0xc3:'ä',0xc4:'ö',0xc5:'ü',0xe0:"'",0xe3:'-',0xe6:'?',0xe7:'!',0xe8:'.',0xe9:'&',0xea:'é',0xef:'♂',0xf0:'¥',0xf1:'×',0xf2:'.',0xf3:'/',0xf4:',',0xf5:'♀'})
for i,ch in enumerate('0123456789',0xf6):DEC[i]=ch
for x in range(0x4a,0x60): DEC.setdefault(x,f'<{x:02X}>')

def extract_west(code,data):
 out=[]
 # split on terminator, accept runs with >=5 display characters and >=0.78 mapped/control ratio
 start=0
 for i,x in enumerate(data):
  if x==0x50:
   seg=data[start:i]
   if 4<=len(seg)<=240:
    mapped=sum((c in DEC) for c in seg)
    display=sum(c in DEC and not DEC[c].startswith('<') for c in seg)
    if mapped/len(seg)>=.78 and display>=5:
     txt=''.join(DEC.get(c,f'\\x{c:02X}') for c in seg)
     out.append({'rom':code,'offset':f'{start:06X}','bank':f'{start//BANK:02X}','bank_offset':f'{start%BANK:04X}','length_bytes':len(seg)+1,'decoded_preview':txt[:180]})
   start=i+1
 return out
str_rows=[]
for code in ['EN','DE','FR','IT','ES']:
 str_rows.extend(extract_west(code,ROMS[code]))
with (OUT/'western_terminated_string_candidates.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=str_rows[0].keys());w.writeheader();w.writerows(str_rows)

# JP revision exact binary diff + semantic-alignment classification.
a=ROMS['JP0'];b=ROMS['JPA']; positions=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
ranges=[]
if positions:
 s=p=positions[0]
 for x in positions[1:]:
  if x==p+1:p=x
  else:ranges.append((s,p));s=p=x
 ranges.append((s,p))
rev_rows=[]
for s,e in ranges:
 rev_rows.append({'start':f'{s:06X}','end':f'{e:06X}','length':e-s+1,'bank':f'{s//BANK:02X}','bank_offset_start':f'{s%BANK:04X}','rev0_hex':a[s:min(e+1,s+24)].hex(),'revA_hex':b[s:min(e+1,s+24)].hex()})
with (OUT/'jp_rev0_to_reva_diff_ranges.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rev_rows[0].keys());w.writeheader();w.writerows(rev_rows)

# Isolated changes outside bank23 / header, all are +5 low-byte pointer fixups in this ROM pair.
fixups=[]
for x in positions:
 if x//BANK==0x23 or 0x14c<=x<=0x14f: continue
 fixups.append({'offset':f'{x:06X}','bank':f'{x//BANK:02X}','bank_offset':f'{x%BANK:04X}','rev0':f'{a[x]:02X}','revA':f'{b[x]:02X}','delta':(b[x]-a[x])&0xff,'context_rev0':a[x-4:x+5].hex(),'context_revA':b[x-4:x+5].hex()})
with (OUT/'jp_reva_external_pointer_fixups.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=fixups[0].keys());w.writeheader();w.writerows(fixups)

# Layout reference CSV
layout=[]
for family,roles in [('EN/WEST',EN_ROLES),('JP',JP_ROLES),('KR',KR_ROLES)]:
 maxbank=0x3f if family=='JP' else 0x7f
 for i in range(maxbank+1):layout.append({'family':family,'bank':f'{i:02X}','role':roles.get(i,'unassigned/padding/unknown')})
with (OUT/'layout_reference.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=layout[0].keys());w.writeheader();w.writerows(layout)

# Summary JSON
meta={}
for code,d in ROMS.items():
 meta[code]={'file':FILES[code].name,'size':len(d),'banks':len(d)//BANK,'sha1':sha1(d),'sha256':sha256(d)}
summary={'roms':meta,'jp_revision':{'different_bytes':len(positions),'diff_ranges':len(ranges),'changed_banks':sorted({x//BANK for x in positions}),'semantic_change':'Rev A moves POP AF and inserts 5-byte zero-skip guard (7e a7 20 01 34) in _InitSpriteAnimStruct; bank23 grows by 5 bytes, causing relocated addresses and pointer fixups.'}}
(OUT/'full_census.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2,ensure_ascii=False))
print('outputs',sorted(p.name for p in OUT.iterdir()))
