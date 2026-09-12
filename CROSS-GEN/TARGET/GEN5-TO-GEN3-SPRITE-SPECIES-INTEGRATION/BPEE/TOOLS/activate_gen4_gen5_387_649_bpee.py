from pathlib import Path
import struct, math, json, hashlib, csv

BASE = Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_64x64_SPRITES.gba')
BW = Path('/mnt/data/Pokemon.Black.Version.EUR.NDS-SweeTnDs.nds')
NAMES = Path('/mnt/data/species_387_649_en.csv')
OUT = Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_387_649_ACTIVE.gba')
MAN = Path('/mnt/data/gen3_gen5_sprite_roms/GEN5_387_649_ACTIVE_MANIFEST.json')
rom = bytearray(BASE.read_bytes())
assert len(rom) == 0x2000000
GBA=0x08000000
FIRST_NAT,LAST_NAT=387,649
FIRST_INT,LAST_INT=440,702
NEW_COUNT=703
MAX_GEN3_MOVE=354
ALLOC_START=0x10E0000
alloc=ALLOC_START; allocs={}

def u16(d,o=0): return struct.unpack_from('<H',d,o)[0]
def u32(d,o=0): return struct.unpack_from('<I',d,o)[0]
def p16(x): return struct.pack('<H',x&0xffff)
def p32(x): return struct.pack('<I',x&0xffffffff)
def alloc_put(name,data,align=4):
 global alloc
 alloc=(alloc+align-1)&~(align-1); off=alloc; end=off+len(data)
 assert end<=len(rom) and all(b==0xff for b in rom[off:end]), (name,hex(off),hex(end))
 rom[off:end]=data; allocs[name]={'offset':off,'size':len(data),'gba_ptr':GBA+off}; alloc=end; return off

# NitroFS + NARC extraction (same structure as the repository's audited Gen V extractor).
def walk_nitrofs(nds):
 fnt_off=u32(nds,0x40); fnt_size=u32(nds,0x44); fnt=nds[fnt_off:fnt_off+fnt_size]; files={}
 def walk(did,prefix=''):
  idx=did-0xF000; t=idx*8; pos=u32(fnt,t); fid=u16(fnt,t+4)
  while True:
   desc=fnt[pos]; pos+=1
   if desc==0: break
   isdir=bool(desc&0x80); n=desc&0x7f; name=fnt[pos:pos+n].decode('ascii'); pos+=n
   if isdir:
    child=u16(fnt,pos); pos+=2; walk(child,prefix+name+'/')
   else:
    files[prefix+name]=fid; fid+=1
 walk(0xF000); return files

def read_nitro(nds,path,files):
 fat=u32(nds,0x48); fid=files[path]; s=u32(nds,fat+fid*8); e=u32(nds,fat+fid*8+4); return nds[s:e]
def parse_narc(n):
 assert n[:4]==b'NARC'; chunks={}; pos=0x10
 while pos+8<=len(n):
  magic=n[pos:pos+4]; sz=u32(n,pos+4); assert sz>=8 and pos+sz<=len(n); chunks[magic]=pos; pos+=sz
 b=chunks[b'BTAF']; g=chunks[b'GMIF']; count=u16(n,b+8); base=g+8
 return [n[base+u32(n,b+0x0c+i*8):base+u32(n,b+0x10+i*8)] for i in range(count)]
nds=BW.read_bytes(); files=walk_nitrofs(nds)
personal=parse_narc(read_nitro(nds,'a/0/1/6',files)); learn_narc=parse_narc(read_nitro(nds,'a/0/1/8',files)); evo_narc=parse_narc(read_nitro(nds,'a/0/1/9',files))
assert len(personal)>=650 and len(learn_narc)>=650 and len(evo_narc)>=650

names={int(r['natdex']):r['name'] for r in csv.DictReader(NAMES.open())}
assert set(names)==set(range(FIRST_NAT,LAST_NAT+1))

def internal(nat): return nat+53

def gen5_type_to_gen3(t):
 # Gen V 0..16 omits Gen III TYPE_MYSTERY at 9.
 return t if t<=8 else (t+1 if t<=16 else 9)

def enc_name(s,length=11):
 out=bytearray()
 for ch in s:
  if 'A'<=ch<='Z': out.append(0xBB+ord(ch)-65)
  elif ch==' ': out.append(0x00)
  elif ch=='.': out.append(0xAD)
  elif ch=='-': out.append(0xAE)
  elif ch=="'": out.append(0xB4)
  else: raise ValueError((s,ch))
 out.append(0xFF)
 if len(out)>length: raise ValueError((s,len(out)))
 out += b'\x00'*(length-len(out)); return bytes(out)

def lz77(data,off):
 assert data[off]==0x10
 size=data[off+1]|data[off+2]<<8|data[off+3]<<16; p=off+4; out=bytearray()
 while len(out)<size:
  flags=data[p];p+=1
  for bit in range(8):
   if len(out)>=size: break
   if flags&(0x80>>bit):
    a=data[p];b=data[p+1];p+=2; ln=(a>>4)+3; disp=((a&15)<<8|b)+1
    for _ in range(ln): out.append(out[-disp])
   else: out.append(data[p]);p+=1
 return bytes(out[:size])
def coord_for(table,species):
 ptr,sz,tag=struct.unpack_from('<IHH',rom,table+species*8); raw=lz77(rom,ptr-GBA); assert len(raw)==2048
 xs=[];ys=[]
 for ty in range(8):
  for tx in range(8):
   base=(ty*8+tx)*32
   for y in range(8):
    for pair in range(4):
     v=raw[base+y*4+pair]
     if v&15: xs.append(tx*8+pair*2);ys.append(ty*8+y)
     if v>>4: xs.append(tx*8+pair*2+1);ys.append(ty*8+y)
 if not xs: return bytes([0x88,0,0,0]),None
 w=max(xs)-min(xs)+1; h=max(ys)-min(ys)+1; sb=(math.ceil(w/8)<<4)|math.ceil(h/8); yo=63-max(ys)
 return bytes([sb,yo,0,0]),{'bbox':[min(xs),min(ys),max(xs),max(ys)],'width':w,'height':h,'y_offset':yo}

FRONT=0x10D0E74; BACK=0x10D246C; PAL=0x10D3A64; SHINY=0x10D505C
# Shared empty learnset, plus one filtered Gen V learnset per species.
empty_off=alloc_put('empty_learnset',b'\xff\xff',2)
learn_offsets={}; filtered_move_counts={}; kept_move_counts={}
for nat in range(FIRST_NAT,LAST_NAT+1):
 m=learn_narc[nat]; pairs=[]; dropped=0
 assert len(m)%4==0
 for p in range(0,len(m),4):
  move=u16(m,p); lvl=u16(m,p+2)
  if move==0xffff and lvl==0xffff: break
  if move<=MAX_GEN3_MOVE and lvl<=100:
   pairs.append((lvl,move))
  else: dropped+=1
 blob=b''.join(p16((lvl<<9)|move) for lvl,move in pairs)+b'\xff\xff'
 learn_offsets[nat]=alloc_put(f'learn_{nat}',blob,2); filtered_move_counts[nat]=dropped; kept_move_counts[nat]=len(pairs)

# Retail table layouts.
tables={
 'species_names':dict(old=0x3185C8,old_count=440,es=11,new_count=703),
 'species_info':dict(old=0x3203CC,old_count=412,es=28,new_count=703),
 'evolution':dict(old=0x32531C,old_count=412,es=30,new_count=703),
 'levelup_ptrs':dict(old=0x32937C,old_count=412,es=4,new_count=703),
 'front_coords':dict(old=0x300D38,old_count=440,es=4,new_count=703),
 'still_front':dict(old=0x301418,old_count=440,es=8,new_count=703),
 'back_coords':dict(old=0x3021D8,old_count=440,es=4,new_count=703),
 'elevation':dict(old=0x305DCC,old_count=412,es=1,new_count=703),
 'front_anim_ptrs':dict(old=0x309AAC,old_count=440,es=4,new_count=703),
 'front_anim_ids':dict(old=0x3299EC,old_count=411,es=1,new_count=702),
 'anim_delays':dict(old=0x329B87,old_count=411,es=1,new_count=702),
 'hoenn_map':dict(old=0x31D94C,old_count=411,es=2,new_count=702),
 'national_map':dict(old=0x31DC82,old_count=411,es=2,new_count=702),
 'tmhm':dict(old=0x31E898,old_count=412,es=8,new_count=703),
 'cry_map':dict(old=0x31F61C,old_count=136,es=2,new_count=427),
 'icons':dict(old=0x57BCA8,old_count=440,es=4,new_count=703),
 'icon_pal_ids':dict(old=0x57C388,old_count=440,es=1,new_count=703),
 'back_anim_ids':dict(old=0x60A8C8,old_count=412,es=1,new_count=703),
}
new={}
for name,t in tables.items():
 old=bytes(rom[t['old']:t['old']+t['old_count']*t['es']])
 if name=='species_names': d=bytes(rom[t['old']:t['old']+11])
 elif name=='species_info': d=bytes(28)
 elif name=='evolution': d=bytes(30)
 elif name=='levelup_ptrs': d=p32(GBA+empty_off)
 elif name in ('front_coords','back_coords'): d=bytes(rom[t['old']:t['old']+4])
 elif name=='still_front': d=bytes(rom[t['old']:t['old']+8])
 elif name=='elevation': d=b'\x00'
 elif name=='front_anim_ptrs': d=bytes(rom[t['old']+4:t['old']+8])
 elif name in ('front_anim_ids','anim_delays'): d=bytes([rom[t['old']]])
 elif name in ('hoenn_map','national_map'): d=b'\x00\x00'
 elif name=='tmhm': d=bytes(8)
 elif name=='cry_map': d=p16(1)
 elif name=='icons': d=bytes(rom[t['old']+4:t['old']+8])
 elif name=='icon_pal_ids': d=bytes([rom[t['old']+1]])
 elif name=='back_anim_ids': d=bytes([rom[t['old']+1]])
 else: raise KeyError(name)
 data=bytearray(d*t['new_count']); data[:len(old)]=old; new[name]=data

unsupported_ability_species=[]; exp_clamped=[]; coords={}; raw_personal_sha={}
for nat in range(FIRST_NAT,LAST_NAT+1):
 sid=internal(nat); rec=personal[nat]; assert len(rec)==60
 # name
 new['species_names'][sid*11:(sid+1)*11]=enc_name(names[nat])
 # Gen III BaseStats-compatible projection.
 base_exp=u16(rec,0x22)
 if base_exp>255: exp_clamped.append(nat)
 a1=rec[0x18] if rec[0x18]<=77 else 0
 a2=rec[0x19] if rec[0x19]<=77 else 0
 if rec[0x18]>77 or rec[0x19]>77: unsupported_ability_species.append(nat)
 stat=bytearray(28)
 stat[0:6]=rec[0:6]; stat[6]=gen5_type_to_gen3(rec[6]); stat[7]=gen5_type_to_gen3(rec[7]); stat[8]=rec[8]; stat[9]=min(base_exp,255)
 stat[0x0A:0x0C]=rec[0x0A:0x0C] # same six packed 2-bit EV yields
 # held items intentionally zero: Gen V item IDs are not raw-compatible with Gen III.
 stat[0x10]=rec[0x12]; stat[0x11]=rec[0x13]; stat[0x12]=rec[0x14]; stat[0x13]=rec[0x15]
 stat[0x14]=rec[0x16]; stat[0x15]=rec[0x17]; stat[0x16]=a1; stat[0x17]=a2; stat[0x18]=rec[0x1B]; stat[0x19]=rec[0x21]&0x7f
 new['species_info'][sid*28:(sid+1)*28]=stat
 # level-up
 struct.pack_into('<I',new['levelup_ptrs'],sid*4,GBA+learn_offsets[nat])
 # graphics metadata from actual imported 64x64 frames
 fc,fm=coord_for(FRONT,sid); bc,bm=coord_for(BACK,sid); coords[nat]={'front':fm,'back':bm}
 new['front_coords'][sid*4:(sid+1)*4]=fc; new['back_coords'][sid*4:(sid+1)*4]=bc
 new['still_front'][sid*8:(sid+1)*8]=rom[FRONT+sid*8:FRONT+(sid+1)*8]
 # placeholder animation/icon/audio compatibility
 new['front_anim_ptrs'][sid*4:(sid+1)*4]=rom[0x309AAC+4:0x309AAC+8]
 new['front_anim_ids'][sid-1]=rom[0x3299EC]; new['anim_delays'][sid-1]=rom[0x329B87]
 new['back_anim_ids'][sid]=rom[0x60A8C8+1]
 new['icons'][sid*4:(sid+1)*4]=rom[0x57BCA8+4:0x57BCA8+8]; new['icon_pal_ids'][sid]=rom[0x57C388+1]
 # unique but safe temporary dex-bit alias 1..263; final proper #387..649 requires save/Pokédex expansion.
 struct.pack_into('<H',new['hoenn_map'],(sid-1)*2,0); struct.pack_into('<H',new['national_map'],(sid-1)*2,nat-386)
 # cry map effective index in retail binary: species - 276.
 struct.pack_into('<H',new['cry_map'],(sid-276)*2,1)
 raw_personal_sha[nat]=hashlib.sha1(rec).hexdigest()

# Evolution and TM/HM stay zero for new species: their method/bit namespaces need explicit adapters.
new_off={name:alloc_put(name,new[name],4) for name in tables}

def relocate(t,newbase):
 oldb=GBA+t['old']; olde=oldb+t['old_count']*t['es']; nb=GBA+newbase; hits=[]
 for pos in range(0,0x1000000-3,4):
  v=struct.unpack_from('<I',rom,pos)[0]
  if oldb<=v<olde and (v-oldb)%t['es']==0:
   nv=nb+(v-oldb); struct.pack_into('<I',rom,pos,nv); hits.append((pos,v,nv))
 return hits
relocs={name:relocate(t,new_off[name]) for name,t in tables.items()}

guards=[0x345F8,0x346D0,0x34A10,0x34ABC,0x34B2C,0x34BF8,0x39A08,0x6E74A,0xA5EB0,0xA5F7C,0xA5FE8,0xA86AC,0xA8774,0xA8850,0xD2D1E,0xD2E32,0xD2EBA,0xD2F2E,0xD2FC6,0xD3086,0xD30B6]
for off in guards:
 assert rom[off:off+4]==bytes.fromhex('ce204000'),(hex(off),rom[off:off+4].hex()); rom[off:off+4]=bytes.fromhex('b0208000')
# Route101 slot 0 -> Turtwig internal440.
route=0x5507E4; assert rom[route:route+4]==bytes.fromhex('02022201'); struct.pack_into('<H',rom,route+2,FIRST_INT)
OUT.write_bytes(rom)

# Exhaustive static validation for all 263 new species.
checks=[]
for nat in range(FIRST_NAT,LAST_NAT+1):
 sid=internal(nat)
 assert rom[new_off['species_names']+sid*11+10] in (0,0xff) # fixed entry in bounds
 nameentry=rom[new_off['species_names']+sid*11:new_off['species_names']+(sid+1)*11]
 checks.append(('name_'+str(nat),0xff in nameentry))
 stats=rom[new_off['species_info']+sid*28:new_off['species_info']+(sid+1)*28]
 checks.append(('stats_'+str(nat),stats[0]>0 and stats[6]<=17 and stats[7]<=17))
 for label,tab in [('front',FRONT),('back',BACK)]:
  ptr=struct.unpack_from('<I',rom,tab+sid*8)[0]; checks.append((label+'_lz_'+str(nat),GBA<=ptr<GBA+len(rom) and rom[ptr-GBA]==0x10))
 lp=struct.unpack_from('<I',rom,new_off['levelup_ptrs']+sid*4)[0]; checks.append(('learnptr_'+str(nat),GBA<=lp<GBA+len(rom)))
 checks.append(('icon_'+str(nat),GBA<=struct.unpack_from('<I',rom,new_off['icons']+sid*4)[0]<GBA+len(rom)))
 checks.append(('dexalias_'+str(nat),struct.unpack_from('<H',rom,new_off['national_map']+(sid-1)*2)[0]==nat-386))
# preserve retail records exactly in each relocated table.
base=BASE.read_bytes()
for name,t in tables.items(): checks.append(('preserve_'+name,base[t['old']:t['old']+t['old_count']*t['es']]==rom[new_off[name]:new_off[name]+t['old_count']*t['es']]))
for label,tab in [('front',FRONT),('back',BACK),('pal',PAL),('shiny',SHINY)]: checks.append(('special_'+label,base[tab+412*8:tab+440*8]==rom[tab+412*8:tab+440*8]))
for off in guards: checks.append(('guard_'+hex(off),rom[off:off+4]==bytes.fromhex('b0208000')))
# no exact old base pointers remain in original 16 MiB.
oldbase_remaining={}
for name,t in tables.items():
 pat=p32(GBA+t['old']); c=sum(1 for p in range(0,0x1000000-3,4) if rom[p:p+4]==pat); oldbase_remaining[name]=c; checks.append(('oldbase_'+name,c==0))
assert all(v for _,v in checks), [k for k,v in checks if not v][:20]
manifest={
 'base_sha1':hashlib.sha1(base).hexdigest(),'output_sha1':hashlib.sha1(rom).hexdigest(),'output_sha256':hashlib.sha256(rom).hexdigest(),
 'bw_rom_sha1':hashlib.sha1(nds).hexdigest(),'source_paths':{'personal':'a/0/1/6','level_up':'a/0/1/8','evolution_observed_not_activated':'a/0/1/9'},
 'national_range':[FIRST_NAT,LAST_NAT],'internal_range':[FIRST_INT,LAST_INT],'species_count':LAST_NAT-FIRST_NAT+1,
 'new_table_offsets':{n:hex(o) for n,o in new_off.items()},'relocated_pointer_counts':{n:len(h) for n,h in relocs.items()},'old_base_pointer_remaining':oldbase_remaining,
 'route101_test':{'level':2,'internal_species':440,'national_species':387},
 'filtered_levelup_moves_total':sum(filtered_move_counts.values()),'kept_levelup_moves_total':sum(kept_move_counts.values()),
 'species_with_gen4plus_ability_ids':len(set(unsupported_ability_species)),'ability_species_natdex':sorted(set(unsupported_ability_species)),
 'species_base_exp_clamped_to_255':exp_clamped,
 'compatibility_state':{
  'names':'English names from project cross-reference; encoded in Gen III charset.',
  'base_stats':'BW personal.narc projected into vanilla Emerald 28-byte BaseStats. Type IDs adapted; held items zero; base EXP u16 clamped to u8.',
  'abilities':'Only ability IDs <=77 are retained because vanilla Emerald has no Gen IV/V abilities. Hidden abilities are not represented yet.',
  'level_up_moves':'BW level-up records retained only when move ID <=354 (exists in vanilla Emerald). Later moves are filtered pending move-system expansion.',
  'evolutions':'New-species evolution entries intentionally zero pending explicit Gen V evolution-method adapter and activation of all targets.',
  'tmhm':'New-species TM/HM flags intentionally zero pending Gen V TM bit -> Gen III TM mapping.',
  'pokedex':'Temporary unique save-safe alias natdex-386 (1..263). Proper National #387..649 requires Pokédex/save-bit expansion.',
  'cry_icon_animation':'Bulbasaur-compatible placeholders; 64x64 front/back battle sprites and palettes are the imported BW assets.'
 },
 'checks_total':len(checks),'checks_passed':sum(1 for _,v in checks if v),'validation_passed':all(v for _,v in checks),'emulator_boot_tested':False,
 'allocation_end':hex(alloc)
}
MAN.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['output_sha1','output_sha256','species_count','filtered_levelup_moves_total','kept_levelup_moves_total','species_with_gen4plus_ability_ids','species_base_exp_clamped_to_255','checks_total','checks_passed','validation_passed','allocation_end']},indent=2))
