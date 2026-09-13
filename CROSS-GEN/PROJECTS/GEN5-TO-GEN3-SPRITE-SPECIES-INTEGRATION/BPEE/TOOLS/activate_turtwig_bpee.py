from pathlib import Path
import struct, math, json, hashlib

BASE = Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_64x64_SPRITES.gba')
OUT = Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_TURTWIG_ACTIVE.gba')
MAN = Path('/mnt/data/gen3_gen5_sprite_roms/TURTWIG_ACTIVE_MANIFEST.json')
rom = bytearray(BASE.read_bytes())
assert len(rom) == 0x2000000

GBA = 0x08000000
SPEC = 440
MAX_INTERNAL = 702
NEW_COUNT = 703
ALLOC_START = 0x10E0000
alloc = ALLOC_START
allocs = {}

def put_alloc(name, data, align=4):
    global alloc
    alloc = (alloc + align-1) & ~(align-1)
    off = alloc
    end = off + len(data)
    assert end <= len(rom)
    assert all(b == 0xFF for b in rom[off:end]), (name, hex(off), hex(end))
    rom[off:end] = data
    allocs[name] = {'offset': off, 'size': len(data), 'gba_ptr': GBA+off}
    alloc = end
    return off

def u16(x): return struct.pack('<H', x & 0xffff)
def u32(x): return struct.pack('<I', x & 0xffffffff)

def lz77(data, off):
    assert data[off] == 0x10, (hex(off), data[off])
    size = data[off+1] | (data[off+2]<<8) | (data[off+3]<<16)
    p=off+4; out=bytearray()
    while len(out)<size:
        flags=data[p]; p+=1
        for bit in range(8):
            if len(out)>=size: break
            if flags & (0x80>>bit):
                a=data[p]; b=data[p+1]; p+=2
                ln=(a>>4)+3; disp=((a&0xf)<<8 | b)+1
                for _ in range(ln): out.append(out[-disp])
            else:
                out.append(data[p]); p+=1
    return bytes(out[:size])

def bbox_coord(table_off, species):
    ptr, sz, tag = struct.unpack_from('<IHH', rom, table_off + species*8)
    off = ptr-GBA
    raw = lz77(rom, off)
    assert len(raw) == 2048
    xs=[]; ys=[]
    for ty in range(8):
        for tx in range(8):
            tile=(ty*8+tx)*32
            for y in range(8):
                for pair in range(4):
                    v=raw[tile+y*4+pair]
                    for sub,pix in [(0,v&15),(1,v>>4)]:
                        if pix:
                            xs.append(tx*8+pair*2+sub)
                            ys.append(ty*8+y)
    if not xs:
        return bytes([0x88,0,0,0]), {'bbox':None,'width':64,'height':64,'y_offset':0}
    minx,miny,maxx,maxy=min(xs),min(ys),max(xs),max(ys)
    w=maxx-minx+1; h=maxy-miny+1
    sizebyte=(math.ceil(w/8)<<4) | math.ceil(h/8)
    yoff=63-maxy
    return bytes([sizebyte,yoff,0,0]), {'bbox':[minx,miny,maxx,maxy], 'width':w,'height':h,'y_offset':yoff,'sizebyte':sizebyte,'sprite_ptr':ptr,'tag':tag}

FRONT_SPR=0x10D0E74
BACK_SPR=0x10D246C
NORMAL_PAL=0x10D3A64
SHINY_PAL=0x10D505C
front_coord, front_meta = bbox_coord(FRONT_SPR, SPEC)
back_coord, back_meta = bbox_coord(BACK_SPR, SPEC)

learn_moves=[(1,33),(5,110),(9,71),(13,75),(17,174),(21,44),(25,72),(29,73),(33,235),(37,242),(41,202)]
learn_blob=b''.join(u16((lv<<9)|mv) for lv,mv in learn_moves)+u16(0xFFFF)
empty_learn_off=put_alloc('empty_learnset', u16(0xFFFF), 2)
turtwig_learn_off=put_alloc('turtwig_learnset', learn_blob, 2)

tables = {
    'species_names': dict(old=0x3185C8, old_count=440, es=11, new_count=NEW_COUNT),
    'species_info': dict(old=0x3203CC, old_count=412, es=28, new_count=NEW_COUNT),
    'evolution': dict(old=0x32531C, old_count=412, es=30, new_count=NEW_COUNT),
    'levelup_ptrs': dict(old=0x32937C, old_count=412, es=4, new_count=NEW_COUNT),
    'front_coords': dict(old=0x300D38, old_count=440, es=4, new_count=NEW_COUNT),
    'still_front': dict(old=0x301418, old_count=440, es=8, new_count=NEW_COUNT),
    'back_coords': dict(old=0x3021D8, old_count=440, es=4, new_count=NEW_COUNT),
    'elevation': dict(old=0x305DCC, old_count=412, es=1, new_count=NEW_COUNT),
    'front_anim_ptrs': dict(old=0x309AAC, old_count=440, es=4, new_count=NEW_COUNT),
    'front_anim_ids': dict(old=0x3299EC, old_count=411, es=1, new_count=MAX_INTERNAL),
    'anim_delays': dict(old=0x329B87, old_count=411, es=1, new_count=MAX_INTERNAL),
    'hoenn_map': dict(old=0x31D94C, old_count=411, es=2, new_count=MAX_INTERNAL),
    'national_map': dict(old=0x31DC82, old_count=411, es=2, new_count=MAX_INTERNAL),
    'tmhm': dict(old=0x31E898, old_count=412, es=8, new_count=NEW_COUNT),
    'cry_map': dict(old=0x31F61C, old_count=136, es=2, new_count=(MAX_INTERNAL-276)+1),
    'icons': dict(old=0x57BCA8, old_count=440, es=4, new_count=NEW_COUNT),
    'icon_pal_ids': dict(old=0x57C388, old_count=440, es=1, new_count=NEW_COUNT),
    'back_anim_ids': dict(old=0x60A8C8, old_count=412, es=1, new_count=NEW_COUNT),
}

new_data={}
for name,t in tables.items():
    old=bytes(rom[t['old']:t['old']+t['old_count']*t['es']])
    if name=='species_names': default=bytes(rom[t['old']:t['old']+11])
    elif name=='species_info': default=bytes(28)
    elif name=='evolution': default=bytes(30)
    elif name=='levelup_ptrs': default=u32(GBA+empty_learn_off)
    elif name in ('front_coords','back_coords'): default=bytes(rom[t['old']:t['old']+4])
    elif name=='still_front': default=bytes(rom[t['old']:t['old']+8])
    elif name=='elevation': default=b'\x00'
    elif name=='front_anim_ptrs': default=bytes(rom[t['old']+4:t['old']+8])
    elif name=='front_anim_ids': default=bytes([rom[t['old']]])
    elif name=='anim_delays': default=bytes([rom[t['old']]])
    elif name in ('hoenn_map','national_map'): default=b'\x00\x00'
    elif name=='tmhm': default=bytes(8)
    elif name=='cry_map': default=u16(1)
    elif name=='icons': default=bytes(rom[t['old']+4:t['old']+8])
    elif name=='icon_pal_ids': default=bytes([rom[t['old']+1]])
    elif name=='back_anim_ids': default=bytes([rom[t['old']+1]])
    else: raise KeyError(name)
    data=bytearray(default*t['new_count'])
    data[:len(old)] = old
    new_data[name]=data

def enc_name(s, length=11):
    out=bytearray()
    for ch in s:
        if 'A'<=ch<='Z': out.append(0xBB+ord(ch)-ord('A'))
        elif ch=='-': out.append(0xAE)
        else: raise ValueError(ch)
    out.append(0xFF)
    out.extend(b'\x00'*(length-len(out)))
    return bytes(out[:length])

new_data['species_names'][SPEC*11:(SPEC+1)*11] = enc_name('TURTWIG')
turtwig_stats = bytes.fromhex('3744401f2d370c0c2d400400000000001f1446030107410000030000')
assert len(turtwig_stats)==28
new_data['species_info'][SPEC*28:(SPEC+1)*28] = turtwig_stats
struct.pack_into('<I',new_data['levelup_ptrs'],SPEC*4,GBA+turtwig_learn_off)
new_data['front_coords'][SPEC*4:(SPEC+1)*4]=front_coord
new_data['back_coords'][SPEC*4:(SPEC+1)*4]=back_coord
new_data['still_front'][SPEC*8:(SPEC+1)*8]=rom[FRONT_SPR+SPEC*8:FRONT_SPR+(SPEC+1)*8]
new_data['front_anim_ptrs'][SPEC*4:(SPEC+1)*4]=rom[0x309AAC+4:0x309AAC+8]
new_data['front_anim_ids'][SPEC-1] = rom[0x3299EC]
new_data['anim_delays'][SPEC-1] = rom[0x329B87]
struct.pack_into('<H',new_data['hoenn_map'],(SPEC-1)*2,0)
struct.pack_into('<H',new_data['national_map'],(SPEC-1)*2,1)
cry_idx=SPEC-276
struct.pack_into('<H',new_data['cry_map'],cry_idx*2,1)
new_data['icons'][SPEC*4:(SPEC+1)*4]=rom[0x57BCA8+4:0x57BCA8+8]
new_data['icon_pal_ids'][SPEC]=rom[0x57C388+1]
new_data['back_anim_ids'][SPEC]=rom[0x60A8C8+1]

new_offsets={}
for name in tables:
    new_offsets[name]=put_alloc(name,new_data[name],4)

def relocate_range(old_off, old_count, es, new_off):
    old_base=GBA+old_off; old_end=old_base+old_count*es; new_base=GBA+new_off
    hits=[]
    for pos in range(0,0x1000000-3,4):
        v=struct.unpack_from('<I',rom,pos)[0]
        if old_base <= v < old_end and (v-old_base)%es==0:
            nv=new_base+(v-old_base)
            struct.pack_into('<I',rom,pos,nv)
            hits.append((pos,v,nv))
    return hits

relocs={name:relocate_range(t['old'],t['old_count'],t['es'],new_offsets[name]) for name,t in tables.items()}

guard_offsets = [
    0x345F8,0x346D0,0x34A10,0x34ABC,0x34B2C,0x34BF8,
    0x39A08,0x6E74A,
    0xA5EB0,0xA5F7C,0xA5FE8,0xA86AC,0xA8774,0xA8850,
    0xD2D1E,0xD2E32,0xD2EBA,0xD2F2E,0xD2FC6,0xD3086,0xD30B6,
]
for off in guard_offsets:
    old=bytes(rom[off:off+4])
    if old != bytes.fromhex('ce204000'):
        raise AssertionError((hex(off),old.hex()))
    rom[off:off+4]=bytes.fromhex('b0208000')

route_off=0x5507E4
assert bytes(rom[route_off:route_off+4]) == bytes.fromhex('02022201')
struct.pack_into('<H',rom,route_off+2,SPEC)
OUT.write_bytes(rom)

def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()
base_bytes=BASE.read_bytes(); out_bytes=bytes(rom)
checks={
    'rom_size_32MiB':len(rom)==0x2000000,
    'species_name_turtwig':bytes(rom[new_offsets['species_names']+SPEC*11:new_offsets['species_names']+(SPEC+1)*11])==enc_name('TURTWIG'),
    'species_stats_turtwig':bytes(rom[new_offsets['species_info']+SPEC*28:new_offsets['species_info']+(SPEC+1)*28])==turtwig_stats,
    'route101_turtwig':struct.unpack_from('<H',rom,route_off+2)[0]==SPEC,
    'front_sprite_lz10':rom[struct.unpack_from('<I',rom,FRONT_SPR+SPEC*8)[0]-GBA]==0x10,
    'back_sprite_lz10':rom[struct.unpack_from('<I',rom,BACK_SPR+SPEC*8)[0]-GBA]==0x10,
    'front_coord':bytes(rom[new_offsets['front_coords']+SPEC*4:new_offsets['front_coords']+(SPEC+1)*4])==front_coord,
    'back_coord':bytes(rom[new_offsets['back_coords']+SPEC*4:new_offsets['back_coords']+(SPEC+1)*4])==back_coord,
    'national_compat_alias_1':struct.unpack_from('<H',rom,new_offsets['national_map']+(SPEC-1)*2)[0]==1,
    'cry_compat_1':struct.unpack_from('<H',rom,new_offsets['cry_map']+cry_idx*2)[0]==1,
    'icon_ptr_valid':GBA <= struct.unpack_from('<I',rom,new_offsets['icons']+SPEC*4)[0] < GBA+len(rom),
    'all_guards_patched':all(rom[o:o+4]==bytes.fromhex('b0208000') for o in guard_offsets),
}
lp=struct.unpack_from('<I',rom,new_offsets['levelup_ptrs']+SPEC*4)[0]
checks['learnptr_in_rom']=GBA <= lp < GBA+len(rom)
lo=lp-GBA
checks['learnset_ends_ffff']=rom[lo+len(learn_blob)-2:lo+len(learn_blob)]==b'\xff\xff'
for name,t in tables.items():
    old=base_bytes[t['old']:t['old']+t['old_count']*t['es']]
    new=bytes(rom[new_offsets[name]:new_offsets[name]+len(old)])
    checks[f'preserve_{name}']=old==new
for name,tab in [('front',FRONT_SPR),('back',BACK_SPR),('pal',NORMAL_PAL),('shiny',SHINY_PAL)]:
    checks[f'preserve_special_sprite_{name}']=base_bytes[tab+412*8:tab+440*8]==rom[tab+412*8:tab+440*8]

manifest={
    'base_rom': str(BASE), 'output_rom': str(OUT),
    'base_sha1': sha1(base_bytes), 'output_sha1': sha1(out_bytes), 'output_sha256': sha256(out_bytes),
    'internal_species': SPEC, 'national_species': 387, 'species_name': 'TURTWIG',
    'new_species_layout': {'first_new_internal':440,'last_new_internal':702,'table_count':703,'preserved_special_internal':[412,439]},
    'turtwig_front_coord':front_meta, 'turtwig_back_coord':back_meta,
    'new_tables': {name:{**allocs[name], 'offset_hex':hex(allocs[name]['offset']), 'gba_ptr_hex':hex(allocs[name]['gba_ptr']), 'old_offset_hex':hex(tables[name]['old']), 'old_count':tables[name]['old_count'], 'new_count':tables[name]['new_count'], 'entry_size':tables[name]['es'], 'relocated_pointer_count':len(relocs[name])} for name in tables},
    'guard_patches': [hex(x) for x in guard_offsets],
    'route101_patch': {'offset':hex(route_off+2),'old_internal_species':290,'new_internal_species':SPEC,'level':2,'slot':0},
    'learnset_staged': [{'level':lv,'move_id':mv} for lv,mv in learn_moves],
    'compatibility_placeholders': {
        'national_dex_mapping':'Internal 440 temporarily aliases National Dex #1 to keep vanilla Emerald save Pokédex bitfields in range.',
        'cry':'Temporary Bulbasaur-compatible cry ID 1.',
        'icon':'Temporary Bulbasaur icon/palette.',
        'front_back_animation':'Temporary Bulbasaur animation IDs/pointers.',
        'tmhm':'Zeroed in smoke build.',
        'evolution':'Disabled until Grotle internal 441 is activated.',
        'hidden_ability':'Shell Armor deferred to ability-system expansion.',
        'gen4plus_moves':'Leaf Storm omitted until move-system expansion.'
    },
    'validation': checks, 'validation_passed': all(checks.values()), 'emulator_boot_tested': False,
    'allocation_end_hex':hex(alloc)
}
MAN.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if not all(checks.values()):
    raise SystemExit([k for k,v in checks.items() if not v])
print(json.dumps({'output':str(OUT),'manifest':str(MAN),'sha1':manifest['output_sha1'],'checks_passed':sum(checks.values()),'checks_total':len(checks)},indent=2))
