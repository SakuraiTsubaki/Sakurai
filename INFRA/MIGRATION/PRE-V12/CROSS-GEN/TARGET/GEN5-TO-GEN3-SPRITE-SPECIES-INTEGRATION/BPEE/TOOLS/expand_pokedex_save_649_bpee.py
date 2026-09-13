from pathlib import Path
import struct, json, hashlib

ACTIVE = Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_387_649_ACTIVE.gba')
ACTIVE_MAN = Path('/mnt/data/gen3_gen5_sprite_roms/GEN5_387_649_ACTIVE_MANIFEST.json')
BW = Path('/mnt/data/Pokemon.Black.Version.EUR.NDS-SweeTnDs.nds')
OUT = Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_387_649_DEX649_CORE.gba')
MAN = Path('/mnt/data/gen3_gen5_sprite_roms/GEN5_387_649_DEX649_CORE_MANIFEST.json')

GBA = 0x08000000
ROM_SCAN_END = 0x1000000
ALLOC_START = 0x1800000
FIRST_NAT, LAST_NAT = 387, 649
FIRST_INT, LAST_INT = 440, 702

# Retail BPEE symbols from pret/pokeemerald symbols branch.
FN_NAT_TO_SPECIES = 0x0806D40C
FN_GETSET_DEX = 0x080C0664
FN_GET_NAT_COUNT = 0x080C07F4
SAVE1_PTR = 0x03005D8C
SAVE2_PTR = 0x03005D90

# Retail data.
OLD_POKEDEX_ENTRIES = 0x56B5B0
OLD_POKEDEX_ENTRY_COUNT = 387
POKEDEX_ENTRY_SIZE = 0x20
OLD_FOOTPRINT_TABLE = 0x56E694
OLD_FOOTPRINT_COUNT = 413

# Vanilla SaveBlock1 has a confirmed unused 0x180-byte area at 0x3598.
DEX_EXT_MAGIC_OFF = 0x3598
DEX_EXT_MAGIC = 0x35365844  # bytes: 44 58 36 35 = 'DX65'
DEX_EXT_OWNED_OFF = 0x359C
DEX_EXT_SEEN_OFF = DEX_EXT_OWNED_OFF + 30
DEX_EXT_SEEN1_OFF = DEX_EXT_SEEN_OFF + 30
DEX_EXT_SEEN2_OFF = DEX_EXT_SEEN1_OFF + 30
DEX_EXT_END = DEX_EXT_SEEN2_OFF + 30
assert DEX_EXT_END <= 0x3718

rom = bytearray(ACTIVE.read_bytes())
assert len(rom) == 0x2000000
active_manifest = json.loads(ACTIVE_MAN.read_text())

def u16(d, o=0): return struct.unpack_from('<H', d, o)[0]
def u32(d, o=0): return struct.unpack_from('<I', d, o)[0]
def p16(v): return struct.pack('<H', v & 0xFFFF)
def p32(v): return struct.pack('<I', v & 0xFFFFFFFF)

def walk_nitrofs(nds):
    fnt_off=u32(nds,0x40); fnt_size=u32(nds,0x44); fnt=nds[fnt_off:fnt_off+fnt_size]; files={}
    def walk(did,prefix=''):
        idx=did-0xF000; t=idx*8; pos=u32(fnt,t); fid=u16(fnt,t+4)
        while True:
            desc=fnt[pos]; pos+=1
            if desc==0: break
            isdir=bool(desc&0x80); n=desc&0x7F; name=fnt[pos:pos+n].decode('ascii'); pos+=n
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
    return [n[base+u32(n,b+0x0C+i*8):base+u32(n,b+0x10+i*8)] for i in range(count)]

nds=BW.read_bytes(); files=walk_nitrofs(nds)
personal=parse_narc(read_nitro(nds,'a/0/1/6',files))
assert len(personal) >= 650

alloc = ALLOC_START
allocs = {}
def alloc_put(name, data, align=4):
    global alloc
    alloc=(alloc+align-1)&~(align-1); off=alloc; end=off+len(data)
    assert end<=len(rom) and all(x==0xFF for x in rom[off:end]), (name,hex(off),hex(end))
    rom[off:end]=data; allocs[name]={'offset':off,'size':len(data),'gba_ptr':GBA+off}; alloc=end
    return off

def relocate(old_off, old_count, es, new_off):
    oldb=GBA+old_off; olde=oldb+old_count*es; newb=GBA+new_off; hits=[]
    for pos in range(0,ROM_SCAN_END-3,4):
        v=u32(rom,pos)
        if oldb<=v<olde and (v-oldb)%es==0:
            nv=newb+(v-oldb); struct.pack_into('<I',rom,pos,nv); hits.append((pos,v,nv))
    return hits

def enc_fixed(s, n):
    out=bytearray()
    for ch in s:
        if 'A'<=ch<='Z': out.append(0xBB+ord(ch)-65)
        elif ch==' ': out.append(0x00)
        elif ch=='.': out.append(0xAD)
        else: raise ValueError(ch)
    out.append(0xFF)
    assert len(out)<=n
    return bytes(out)+bytes(n-len(out))

# Replace the temporary 1..263 National Dex aliases with real #387..649.
nat_map_off = int(active_manifest['new_table_offsets']['national_map'],16)
for nat in range(FIRST_NAT,LAST_NAT+1):
    sid=nat+53
    struct.pack_into('<H',rom,nat_map_off+(sid-1)*2,nat)

# Expand gPokedexEntries so caught-page/category/height/weight reads for #387..649 are safe.
old_entries=bytes(rom[OLD_POKEDEX_ENTRIES:OLD_POKEDEX_ENTRIES+OLD_POKEDEX_ENTRY_COUNT*POKEDEX_ENTRY_SIZE])
entries=bytearray(650*POKEDEX_ENTRY_SIZE)
entries[:len(old_entries)]=old_entries
bulba=old_entries[POKEDEX_ENTRY_SIZE:2*POKEDEX_ENTRY_SIZE]
unknown_cat=enc_fixed('UNKNOWN',12)
GENERIC_DESC=0x085EC00F  # gText_Unknown
for nat in range(FIRST_NAT,LAST_NAT+1):
    rec=personal[nat]; assert len(rec)==0x3C
    e=bytearray(bulba)
    e[0:12]=unknown_cat
    struct.pack_into('<H',e,0x0C,u16(rec,0x24))
    struct.pack_into('<H',e,0x0E,u16(rec,0x26))
    struct.pack_into('<I',e,0x10,GENERIC_DESC)
    e[0x14:0x16]=b'\x00\x00'
    entries[nat*POKEDEX_ENTRY_SIZE:(nat+1)*POKEDEX_ENTRY_SIZE]=e
new_entries_off=alloc_put('pokedex_entries_000_649',entries,4)
entry_relocs=relocate(OLD_POKEDEX_ENTRIES,OLD_POKEDEX_ENTRY_COUNT,POKEDEX_ENTRY_SIZE,new_entries_off)

# Expand footprint routing to internal species 0..702; new species use a safe placeholder footprint for now.
old_foot=bytes(rom[OLD_FOOTPRINT_TABLE:OLD_FOOTPRINT_TABLE+OLD_FOOTPRINT_COUNT*4])
foot=bytearray(703*4); foot[:len(old_foot)]=old_foot
placeholder=old_foot[4:8]
for sid in range(OLD_FOOTPRINT_COUNT,703): foot[sid*4:(sid+1)*4]=placeholder
new_foot_off=alloc_put('footprint_table_000_702',foot,4)
foot_relocs=relocate(OLD_FOOTPRINT_TABLE,OLD_FOOTPRINT_COUNT,4,new_foot_off)

class Arm:
    def __init__(self, base): self.base=base; self.items=[]; self.labels={}; self.literals=[]
    def pc(self): return self.base+len(self.items)*4
    def emit(self,w): self.items.append(('w',w&0xFFFFFFFF))
    def label(self,n): self.labels[n]=len(self.items)
    def b(self,label,cond=0xE,link=False): self.items.append(('b',cond,label,link))
    def bl_abs(self,target,cond=0xE): self.items.append(('ba',cond,target,True))
    def lit(self,rd,val): self.items.append(('lit',rd,val&0xFFFFFFFF))
    def finish(self):
        vals=[]
        for x in self.items:
            if x[0]=='lit' and x[2] not in vals: vals.append(x[2])
        litbase=self.base+len(self.items)*4; litaddr={v:litbase+i*4 for i,v in enumerate(vals)}
        out=bytearray()
        for i,x in enumerate(self.items):
            addr=self.base+i*4; typ=x[0]
            if typ=='w': w=x[1]
            elif typ=='b':
                _,cond,label,link=x; target=self.base+self.labels[label]*4
                off=(target-(addr+8))>>2; assert -(1<<23)<=off<(1<<23)
                w=(cond<<28)|(0x0B000000 if link else 0x0A000000)|(off&0xFFFFFF)
            elif typ=='ba':
                _,cond,target,link=x; off=(target-(addr+8))>>2; assert -(1<<23)<=off<(1<<23)
                w=(cond<<28)|(0x0B000000 if link else 0x0A000000)|(off&0xFFFFFF)
            elif typ=='lit':
                _,rd,val=x; imm=litaddr[val]-(addr+8); assert 0<=imm<=0xFFF
                w=0xE59F0000|(rd<<12)|imm
            out+=p32(w)
        for v in vals: out+=p32(v)
        return bytes(out)

def push(a,mask): a.emit(0xE92D0000|mask)
def pop_lr(a,mask): a.emit(0xE8BD0000|mask)
def bx(a,r): a.emit(0xE12FFF10|r)
def movi(a,rd,imm,cond=0xE): assert 0<=imm<=255; a.emit((cond<<28)|0x03A00000|(rd<<12)|imm)
def movr(a,rd,rm,cond=0xE): a.emit((cond<<28)|0x01A00000|(rd<<12)|rm)
def mov_lsr(a,rd,rm,sh): a.emit(0xE1A00000|(rd<<12)|(sh<<7)|(1<<5)|rm)
def mov_lsl_reg(a,rd,rm,rs): a.emit(0xE1A00000|(rd<<12)|(rs<<8)|(1<<4)|rm)
def cmpi(a,rn,imm): assert 0<=imm<=255; a.emit(0xE3500000|(rn<<16)|imm)
def cmpr(a,rn,rm): a.emit(0xE1500000|(rn<<16)|rm)
def addi(a,rd,rn,imm,cond=0xE): assert 0<=imm<=255; a.emit((cond<<28)|0x02800000|(rn<<16)|(rd<<12)|imm)
def subi(a,rd,rn,imm): assert 0<=imm<=255; a.emit(0xE2400000|(rn<<16)|(rd<<12)|imm)
def subs(a,rd,rn,imm): assert 0<=imm<=255; a.emit(0xE2500000|(rn<<16)|(rd<<12)|imm)
def addr(a,rd,rn,rm): a.emit(0xE0800000|(rn<<16)|(rd<<12)|rm)
def subr(a,rd,rn,rm): a.emit(0xE0400000|(rn<<16)|(rd<<12)|rm)
def andi(a,rd,rn,imm): assert 0<=imm<=255; a.emit(0xE2000000|(rn<<16)|(rd<<12)|imm)
def orrr(a,rd,rn,rm): a.emit(0xE1800000|(rn<<16)|(rd<<12)|rm)
def bicr(a,rd,rn,rm): a.emit(0xE1C00000|(rn<<16)|(rd<<12)|rm)
def tst(a,rn,rm): a.emit(0xE1100000|(rn<<16)|rm)
def ldr(a,rd,rn): a.emit(0xE5900000|(rn<<16)|(rd<<12))
def strw(a,rd,rn): a.emit(0xE5800000|(rn<<16)|(rd<<12))
def ldrb_r(a,rd,rn,rm): a.emit(0xE7D00000|(rn<<16)|(rd<<12)|rm)
def strb_r(a,rd,rn,rm): a.emit(0xE7C00000|(rn<<16)|(rd<<12)|rm)
def ldrb(a,rd,rn,imm=0): a.emit(0xE5D00000|(rn<<16)|(rd<<12)|imm)
def strb(a,rd,rn,imm=0): a.emit(0xE5C00000|(rn<<16)|(rd<<12)|imm)
def ldrh(a,rd,rn): a.emit(0xE1D000B0|(rn<<16)|(rd<<12))

def build_flag(base):
    a=Arm(base); saved=0x4FF0 # r4-r11,lr
    push(a,saved); cmpi(a,0,0); a.b('ret0',0x0)
    a.lit(10,650); cmpr(a,0,10); a.b('ret0',0x2) # HS
    a.lit(4,SAVE1_PTR); ldr(a,4,4)
    a.lit(5,SAVE2_PTR); ldr(a,5,5)
    a.lit(10,417); cmpr(a,0,10); a.b('ext',0x2)
    # Vanilla flag storage 1..416.
    subi(a,2,0,1); mov_lsr(a,3,2,3); andi(a,2,2,7); movi(a,12,1); mov_lsl_reg(a,12,12,2)
    addi(a,6,5,0x28); addi(a,7,5,0x5C)
    a.lit(10,0x988); addr(a,8,4,10); a.lit(10,0x3B24); addr(a,9,4,10); a.b('dispatch')
    a.label('ext')
    # Lazy initialization makes old vanilla saves deterministic.
    a.lit(10,DEX_EXT_MAGIC_OFF); addr(a,6,4,10); ldr(a,11,6); a.lit(10,DEX_EXT_MAGIC); cmpr(a,11,10); a.b('ext_ready',0x0)
    addi(a,7,6,4); movi(a,3,120); movi(a,11,0)
    a.label('zero_loop'); strb(a,11,7); addi(a,7,7,1); subs(a,3,3,1); a.b('zero_loop',0x1); strw(a,10,6)
    a.label('ext_ready')
    a.lit(10,417); subr(a,2,0,10); mov_lsr(a,3,2,3); andi(a,2,2,7); movi(a,12,1); mov_lsl_reg(a,12,12,2)
    a.lit(10,DEX_EXT_OWNED_OFF); addr(a,6,4,10); addi(a,7,6,30); addi(a,8,7,30); addi(a,9,8,30)
    a.label('dispatch')
    cmpi(a,1,0); a.b('get_seen',0x0); cmpi(a,1,1); a.b('get_caught',0x0); cmpi(a,1,2); a.b('set_seen',0x0); cmpi(a,1,3); a.b('set_caught',0x0); a.b('ret0')
    a.label('get_seen')
    ldrb_r(a,10,7,3); tst(a,10,12); a.b('ret0',0x0)
    ldrb_r(a,11,8,3); tst(a,11,12); a.b('clear_seen',0x0)
    ldrb_r(a,2,9,3); tst(a,2,12); a.b('clear_seen',0x0); a.b('ret1')
    a.label('clear_seen')
    ldrb_r(a,10,7,3); bicr(a,10,10,12); strb_r(a,10,7,3)
    ldrb_r(a,10,8,3); bicr(a,10,10,12); strb_r(a,10,8,3)
    ldrb_r(a,10,9,3); bicr(a,10,10,12); strb_r(a,10,9,3); a.b('ret0')
    a.label('get_caught')
    ldrb_r(a,10,6,3); tst(a,10,12); a.b('ret0',0x0)
    ldrb_r(a,11,7,3); tst(a,11,12); a.b('clear_owned',0x0)
    ldrb_r(a,11,8,3); tst(a,11,12); a.b('clear_owned',0x0)
    ldrb_r(a,11,9,3); tst(a,11,12); a.b('clear_owned',0x0); a.b('ret1')
    a.label('clear_owned'); ldrb_r(a,10,6,3); bicr(a,10,10,12); strb_r(a,10,6,3); a.b('ret0')
    a.label('set_seen')
    ldrb_r(a,10,7,3); orrr(a,10,10,12); strb_r(a,10,7,3)
    ldrb_r(a,10,8,3); orrr(a,10,10,12); strb_r(a,10,8,3)
    ldrb_r(a,10,9,3); orrr(a,10,10,12); strb_r(a,10,9,3); a.b('ret0')
    a.label('set_caught'); ldrb_r(a,10,6,3); orrr(a,10,10,12); strb_r(a,10,6,3); a.b('ret0')
    a.label('ret1'); movi(a,0,1); a.b('done')
    a.label('ret0'); movi(a,0,0)
    a.label('done'); pop_lr(a,saved); bx(a,14)
    return a.finish()

def build_count(base, flag_addr):
    a=Arm(base); saved=0x40F0 # r4-r7,lr
    push(a,saved); movr(a,4,0); movi(a,5,1); movi(a,6,0); a.lit(7,650)
    a.label('loop'); movr(a,0,5); movr(a,1,4); a.bl_abs(flag_addr); cmpi(a,0,0); addi(a,6,6,1,0x1) # ADDNE
    addi(a,5,5,1); cmpr(a,5,7); a.b('loop',0xB) # LT
    movr(a,0,6); pop_lr(a,saved); bx(a,14); return a.finish()

def build_nat_to_species(base, table_ptr):
    a=Arm(base); saved=0x4070 # r4-r6,lr
    push(a,saved); cmpi(a,0,0); a.b('ret0',0x0); a.lit(6,650); cmpr(a,0,6); a.b('ret0',0x2)
    a.lit(4,table_ptr); movi(a,1,1); a.lit(6,703)
    a.label('loop'); ldrh(a,3,4); cmpr(a,3,0); a.b('found',0x0); addi(a,4,4,2); addi(a,1,1,1); cmpr(a,1,6); a.b('loop',0xB)
    a.label('ret0'); movi(a,0,0); a.b('done'); a.label('found'); movr(a,0,1)
    a.label('done'); pop_lr(a,saved); bx(a,14); return a.finish()

# Inject ARM routines.
flag_off=(alloc+3)&~3; flag_blob=build_flag(GBA+flag_off); assert flag_off==alloc_put('arm_getset_pokedex_649',flag_blob,4)
count_off=(alloc+3)&~3; count_blob=build_count(GBA+count_off,GBA+flag_off); assert count_off==alloc_put('arm_get_national_count_649',count_blob,4)
n2s_off=(alloc+3)&~3; n2s_blob=build_nat_to_species(GBA+n2s_off,GBA+nat_map_off); assert n2s_off==alloc_put('arm_national_to_species_649',n2s_blob,4)

def thumb_arm_stub(fn_addr, target_arm):
    off=fn_addr-GBA; old=bytes(rom[off:off+8]); rom[off:off+8]=p16(0x4B00)+p16(0x4718)+p32(target_arm)
    return old

stub_original={
    'GetSetPokedexFlag':thumb_arm_stub(FN_GETSET_DEX,GBA+flag_off).hex(),
    'GetNationalPokedexCount':thumb_arm_stub(FN_GET_NAT_COUNT,GBA+count_off).hex(),
    'NationalPokedexNumToSpecies':thumb_arm_stub(FN_NAT_TO_SPECIES,GBA+n2s_off).hex(),
}

checks=[]
for nat in (387,416,417,493,494,649):
    sid=nat+53; checks.append((f'natmap_{nat}',u16(rom,nat_map_off+(sid-1)*2)==nat))
    if nat>=387:
        e=new_entries_off+nat*POKEDEX_ENTRY_SIZE
        checks.append((f'entry_{nat}',u16(rom,e+0x0C)==u16(personal[nat],0x24) and u16(rom,e+0x0E)==u16(personal[nat],0x26)))
for addr,target in ((FN_GETSET_DEX,GBA+flag_off),(FN_GET_NAT_COUNT,GBA+count_off),(FN_NAT_TO_SPECIES,GBA+n2s_off)):
    off=addr-GBA; checks.append((f'stub_{addr:08X}',rom[off:off+4]==p16(0x4B00)+p16(0x4718) and u32(rom,off+4)==target))
checks += [
    ('entry_relocs',len(entry_relocs)>0),('foot_relocs',len(foot_relocs)>0),
    ('save_ext_inside_unused',DEX_EXT_MAGIC_OFF>=0x3598 and DEX_EXT_END<=0x3718),
    ('flag_code_in_rom',rom[flag_off:flag_off+len(flag_blob)]==flag_blob),
    ('count_code_in_rom',rom[count_off:count_off+len(count_blob)]==count_blob),
    ('n2s_code_in_rom',rom[n2s_off:n2s_off+len(n2s_blob)]==n2s_blob),
]
assert all(v for _,v in checks),[k for k,v in checks if not v]

OUT.write_bytes(rom)
manifest={
    'input_active_rom':ACTIVE.name,
    'input_active_sha1':hashlib.sha1(ACTIVE.read_bytes()).hexdigest(),
    'output_sha1':hashlib.sha1(rom).hexdigest(),'output_sha256':hashlib.sha256(rom).hexdigest(),
    'national_pokedex_range':[1,649],
    'new_species_national_range':[387,649],'new_species_internal_range':[440,702],
    'save_extension':{
        'container':'SaveBlock1.unused_3598','unused_region':['0x3598','0x3718'],'magic_offset':hex(DEX_EXT_MAGIC_OFF),'magic':hex(DEX_EXT_MAGIC),
        'owned_offset':hex(DEX_EXT_OWNED_OFF),'seen_offset':hex(DEX_EXT_SEEN_OFF),'seen1_offset':hex(DEX_EXT_SEEN1_OFF),'seen2_offset':hex(DEX_EXT_SEEN2_OFF),'end':hex(DEX_EXT_END),
        'policy':'#1-416 use retail arrays; #417-649 use four 30-byte extension arrays; lazy magic initialization protects vanilla saves'
    },
    'expanded_pokedex_entries':{'offset':hex(new_entries_off),'count':650,'entry_size':32,'pointer_relocations':len(entry_relocs),'new_category_text':'UNKNOWN placeholder','height_weight_source':'BW /a/0/1/6'},
    'expanded_footprint_table':{'offset':hex(new_foot_off),'count':703,'pointer_relocations':len(foot_relocs),'new_species_policy':'safe placeholder until Gen IV/V footprints are imported'},
    'runtime_hooks':{
        'GetSetPokedexFlag':{'retail':hex(FN_GETSET_DEX),'arm':hex(GBA+flag_off),'original_first8':stub_original['GetSetPokedexFlag']},
        'GetNationalPokedexCount':{'retail':hex(FN_GET_NAT_COUNT),'arm':hex(GBA+count_off),'original_first8':stub_original['GetNationalPokedexCount']},
        'NationalPokedexNumToSpecies':{'retail':hex(FN_NAT_TO_SPECIES),'arm':hex(GBA+n2s_off),'original_first8':stub_original['NationalPokedexNumToSpecies']},
    },
    'allocations':allocs,'allocation_end':hex(alloc),
    'checks_total':len(checks),'checks_passed':sum(v for _,v in checks),'validation_passed':all(v for _,v in checks),
    'ui_scope':'core save flags, real national-number routing, counts, caught-page entry safety; the main National Dex browse list remains a separate UI-bank expansion because vanilla PokedexView is sized for 386 entries',
    'rom_binary_committed_to_github':False,
}
MAN.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ('output_sha1','output_sha256','national_pokedex_range','save_extension','checks_total','checks_passed','validation_passed','allocation_end')},indent=2))
