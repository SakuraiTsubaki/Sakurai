#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, hashlib, json, struct
from collections import Counter

GBA = 0x08000000
INPUT_EXPECTED_SHA1 = 'ccff6ab32f5f139d8346366fd5a169e5ddaa533f'
ORIGINAL_EVOLUTION_OFF = 0x32531C
ORIGINAL_EVOLUTION_COUNT = 412
EVOS_PER_MON = 5
EVOLUTION_SLOT_SIZE = 8   # retail BPEE ABI: 3*u16 + 2 bytes ABI padding
EVOLUTION_SPECIES_STRIDE = EVOS_PER_MON * EVOLUTION_SLOT_SIZE  # 40
EXTENDED_SPECIES_COUNT = 703
HOOK_OFF = 0x1810000
CORRECTED_EVOLUTION_OFF = 0x1812000
GET_EVOLUTION_TARGET_OFF = 0x6D098
BROKEN_EVOLUTION_PTR = 0x090E83F4
CORRECTED_EVOLUTION_PTR = GBA + CORRECTED_EVOLUTION_OFF
HOOK_ARM_ADDR = GBA + HOOK_OFF
EVOLUTION_PTR_SITES = [0x6D140, 0x6D190, 0x6D234, 0x6D384, 0x70030, 0x13E558]
NATIONAL_MAP_OFF = 0x10F25FC  # inherited expanded internal->National map in the activated BPEE build

BW_STONE_TO_EMERALD = {80:93, 81:94, 82:95, 83:96, 84:97, 85:98}
DIRECT_METHOD_MAP = {1:1, 2:2, 3:3, 4:4, 5:5}

CUSTOM_ACTIVE_METHODS = {21, 22, 23, 24}
CUSTOM_ACTIVE_RECORDS = {
    (108,21,205,463),
    (114,21,246,465),
    (193,21,246,469),
    (221,21,246,473),
    (438,21,102,185),
    (439,21,102,122),
    (412,24,20,413),
    (412,23,20,414),
    (415,24,21,416),
    (458,22,223,226),
}

def u16(d,o=0): return struct.unpack_from('<H',d,o)[0]
def u32(d,o=0): return struct.unpack_from('<I',d,o)[0]
def p16(v): return struct.pack('<H',v)
def p32(v): return struct.pack('<I',v)
def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()

NAT_TO_INTERNAL = {}

def internal_species(nat:int)->int:
    if nat not in NAT_TO_INTERNAL:
        raise KeyError(f"National species {nat} is absent from the input internal->National map")
    return NAT_TO_INTERNAL[nat]

def walk_nitrofs(nds:bytes):
    fnt_off=u32(nds,0x40); fnt_size=u32(nds,0x44); fnt=nds[fnt_off:fnt_off+fnt_size]; files={}
    def walk(did,prefix=''):
        t=(did-0xF000)*8; pos=u32(fnt,t); fid=u16(fnt,t+4)
        while True:
            desc=fnt[pos]; pos+=1
            if desc==0: break
            n=desc&0x7F; name=fnt[pos:pos+n].decode('ascii'); pos+=n
            if desc&0x80:
                child=u16(fnt,pos); pos+=2; walk(child,prefix+name+'/')
            else:
                files[prefix+name]=fid; fid+=1
    walk(0xF000); return files

def read_nitro(nds,path,files):
    fat=u32(nds,0x48); fid=files[path]; s=u32(nds,fat+fid*8); e=u32(nds,fat+fid*8+4); return nds[s:e]

def parse_narc(n):
    assert n[:4]==b'NARC'; chunks={}; pos=0x10
    while pos+8<=len(n):
        magic=n[pos:pos+4]; size=u32(n,pos+4); assert size>=8 and pos+size<=len(n); chunks[magic]=pos; pos+=size
    b=chunks[b'BTAF']; g=chunks[b'GMIF']; count=u16(n,b+8); base=g+8; out=[]
    for i in range(count):
        rs=u32(n,b+0x0C+i*8); re=u32(n,b+0x10+i*8); out.append(n[base+rs:base+re])
    return out

def decode_bw_evos(member):
    assert len(member)==42
    vals=struct.unpack('<21H',member)
    return [(vals[i],vals[i+1],vals[i+2]) for i in range(0,21,3) if vals[i]]

def write_evo_slot(table, species, slot, method, param, target):
    off=species*EVOLUTION_SPECIES_STRIDE + slot*EVOLUTION_SLOT_SIZE
    struct.pack_into('<HHH',table,off,method,param,target)
    table[off+6:off+8]=b'\0\0'

def read_evo_slots(buf, base, species):
    return [struct.unpack_from('<HHH',buf,base+species*EVOLUTION_SPECIES_STRIDE+i*EVOLUTION_SLOT_SIZE) for i in range(EVOS_PER_MON)]

def classify_edge(src,m,param,tgt):
    if m in DIRECT_METHOD_MAP:
        note = 'Emerald native evolution method'
        if m in (2,3): note += '; uses Emerald RTC day/night policy in V1'
        return 'active_table', note
    if m==8 and param in BW_STONE_TO_EMERALD:
        return 'active_table', f'BW stone {param} mapped to existing Emerald stone item {BW_STONE_TO_EMERALD[param]}'
    if (src,m,param,tgt) in CUSTOM_ACTIVE_RECORDS:
        if m==21: return 'active_hook', 'level-up while knowing existing Gen III move'
        if m==22: return 'active_hook', 'level-up with required non-Egg species in player party'
        if m in (23,24): return 'active_hook', 'level threshold plus gender check'
    reasons={
        6:'pending_item_system: Gen IV/V held trade item is not yet a valid Emerald item',
        7:'pending_trade_context: trade-for-specific-species method needs trade partner adapter',
        8:'pending_item_system: required Gen IV/V evolution stone is not yet a valid Emerald item',
        17:'pending_item_system: Dawn Stone + male condition requires new item',
        18:'pending_item_system: Dawn Stone + female condition requires new item',
        19:'pending_item_system: Oval Stone held/day condition requires new item',
        20:'pending_item_system: Razor Claw/Fang held/night condition requires new item',
        21:'pending_move_system: required move ID is not yet implemented in Emerald',
        25:'pending_field_system: magnetic-field location condition needs mapped field locations',
        26:'pending_field_system: Moss Rock location condition needs mapped field location',
        27:'pending_field_system: Ice Rock location condition needs mapped field location',
    }
    return 'pending_dependency', reasons.get(m,'pending_unimplemented_method')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-rom',type=Path,default=Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_387_649_DEX649_BANKED_UI.gba'))
    ap.add_argument('--original-emerald',type=Path,default=Path('/mnt/data/Pokemon - Emerald Version (USA, Europe).gba'))
    ap.add_argument('--bw-rom',type=Path,default=Path('/mnt/data/Pokemon.Black.Version.EUR.NDS-SweeTnDs.nds'))
    ap.add_argument('--hook-bin',type=Path,default=Path('/mnt/data/gen5_evolution_ext_hooks.bin'))
    ap.add_argument('--output-rom',type=Path,default=Path('/mnt/data/gen3_gen5_sprite_roms/Pokemon_-_Emerald_Version_(USA,_Europe)_GEN5_387_649_DEX649_BANKED_UI_EVOLUTION_V1.gba'))
    ap.add_argument('--manifest',type=Path,default=Path('/mnt/data/gen3_gen5_sprite_roms/GEN5_387_649_EVOLUTION_V1_MANIFEST.json'))
    ap.add_argument('--audit-csv',type=Path,default=Path('/mnt/data/GEN5_387_649_EVOLUTION_V1_EDGES.csv'))
    args=ap.parse_args()

    inp=args.input_rom.read_bytes(); assert sha1(inp)==INPUT_EXPECTED_SHA1,(sha1(inp),INPUT_EXPECTED_SHA1)

    NAT_TO_INTERNAL.clear()
    for sid in range(1, EXTENDED_SPECIES_COUNT):
        nat=u16(inp, NATIONAL_MAP_OFF+(sid-1)*2)
        if 1 <= nat <= 649:
            if nat >= 387 and sid < 440:
                continue
            NAT_TO_INTERNAL.setdefault(nat, sid)
    assert all(n in NAT_TO_INTERNAL for n in range(1,650))
    assert NAT_TO_INTERNAL[252]==277
    assert NAT_TO_INTERNAL[290]==301
    assert NAT_TO_INTERNAL[351]==385
    assert NAT_TO_INTERNAL[358]==411
    assert NAT_TO_INTERNAL[386]==410
    assert NAT_TO_INTERNAL[387]==440
    assert NAT_TO_INTERNAL[649]==702

    orig=args.original_emerald.read_bytes(); assert len(orig)>=ORIGINAL_EVOLUTION_OFF+ORIGINAL_EVOLUTION_COUNT*EVOLUTION_SPECIES_STRIDE
    hook=args.hook_bin.read_bytes(); assert len(hook)<0x1000
    nds=args.bw_rom.read_bytes(); files=walk_nitrofs(nds); evo_members=parse_narc(read_nitro(nds,'a/0/1/9',files))
    assert len(evo_members)==668 and all(len(x)==42 for x in evo_members)

    rom=bytearray(inp)
    assert all(x==0xFF for x in rom[HOOK_OFF:HOOK_OFF+len(hook)])
    table_size=EXTENDED_SPECIES_COUNT*EVOLUTION_SPECIES_STRIDE
    assert all(x==0xFF for x in rom[CORRECTED_EVOLUTION_OFF:CORRECTED_EVOLUTION_OFF+table_size])

    table=bytearray(table_size)
    original_table=orig[ORIGINAL_EVOLUTION_OFF:ORIGINAL_EVOLUTION_OFF+ORIGINAL_EVOLUTION_COUNT*EVOLUTION_SPECIES_STRIDE]
    table[:len(original_table)]=original_table

    edge_rows=[]; all_edges=[]; active_table_edges=[]; active_hook_edges=[]; pending_edges=[]
    for src in range(1,650):
        for method,param,tgt in decode_bw_evos(evo_members[src]):
            if src>=387 or tgt>=387:
                status,note=classify_edge(src,method,param,tgt)
                si=internal_species(src); ti=internal_species(tgt)
                row={'source_nat':src,'source_internal':si,'bw_method':method,'bw_param':param,'target_nat':tgt,'target_internal':ti,'status':status,'note':note}
                edge_rows.append(row); all_edges.append((src,method,param,tgt))
                if status=='active_table': active_table_edges.append((src,method,param,tgt))
                elif status=='active_hook': active_hook_edges.append((src,method,param,tgt))
                else: pending_edges.append((src,method,param,tgt,note))

    direct_written=[]
    for src,method,param,tgt in active_table_edges:
        si=internal_species(src); ti=internal_species(tgt)
        assert src>=387
        if method in DIRECT_METHOD_MAP:
            gm=DIRECT_METHOD_MAP[method]; gp=param
        elif method==8 and param in BW_STONE_TO_EMERALD:
            gm=7; gp=BW_STONE_TO_EMERALD[param]
        else: raise AssertionError((src,method,param,tgt))
        slots=[struct.unpack_from('<HHH',table,si*EVOLUTION_SPECIES_STRIDE+i*EVOLUTION_SLOT_SIZE) for i in range(EVOS_PER_MON)]
        free=next((i for i,s in enumerate(slots) if s==(0,0,0)),None); assert free is not None,(src,slots)
        write_evo_slot(table,si,free,gm,gp,ti); direct_written.append((src,si,free,gm,gp,tgt,ti))

    rom[HOOK_OFF:HOOK_OFF+len(hook)]=hook
    rom[CORRECTED_EVOLUTION_OFF:CORRECTED_EVOLUTION_OFF+len(table)]=table

    for pos in EVOLUTION_PTR_SITES:
        assert u32(rom,pos)==BROKEN_EVOLUTION_PTR,(hex(pos),hex(u32(rom,pos)))
        struct.pack_into('<I',rom,pos,CORRECTED_EVOLUTION_PTR)

    original_entry=bytes(rom[GET_EVOLUTION_TARGET_OFF:GET_EVOLUTION_TARGET_OFF+8])
    assert original_entry.hex()=='f0b557464e464546',original_entry.hex()
    rom[GET_EVOLUTION_TARGET_OFF:GET_EVOLUTION_TARGET_OFF+8]=b'\x00\x4B\x18\x47'+p32(HOOK_ARM_ADDR)

    checks=[]
    checks.append(('original_vanilla_table_preserved_0_411', table[:len(original_table)]==original_table))
    checks.append(('correct_abi_stride_40', EVOLUTION_SPECIES_STRIDE==40))
    checks.append(('hook_blob_exact', bytes(rom[HOOK_OFF:HOOK_OFF+len(hook)])==hook))
    checks.append(('hook_entry_stub', bytes(rom[GET_EVOLUTION_TARGET_OFF:GET_EVOLUTION_TARGET_OFF+4])==b'\x00\x4B\x18\x47' and u32(rom,GET_EVOLUTION_TARGET_OFF+4)==HOOK_ARM_ADDR))
    for pos in EVOLUTION_PTR_SITES: checks.append((f'evolution_ptr_{pos:06X}',u32(rom,pos)==CORRECTED_EVOLUTION_PTR))
    checks.append(('vanilla_bulbasaur', (4,16,internal_species(2)) in read_evo_slots(rom,CORRECTED_EVOLUTION_OFF,internal_species(1))))
    checks.append(('vanilla_eevee_exact', read_evo_slots(rom,CORRECTED_EVOLUTION_OFF,internal_species(133)) == read_evo_slots(orig,ORIGINAL_EVOLUTION_OFF,internal_species(133))))
    checks.append(('vanilla_wurmple_exact', read_evo_slots(rom,CORRECTED_EVOLUTION_OFF,internal_species(265)) == read_evo_slots(orig,ORIGINAL_EVOLUTION_OFF,internal_species(265))))
    checks.append(('vanilla_nincada_exact', read_evo_slots(rom,CORRECTED_EVOLUTION_OFF,internal_species(290)) == read_evo_slots(orig,ORIGINAL_EVOLUTION_OFF,internal_species(290))))
    checks.append(('mapping_castform_351_to_385', internal_species(351)==385))
    checks.append(('mapping_chimecho_358_to_411', internal_species(358)==411))
    checks.append(('mapping_deoxys_386_to_410', internal_species(386)==410))
    reps={
        387:(4,18,internal_species(388)),
        388:(4,32,internal_species(389)),
        511:(7,98,internal_species(512)),
        517:(7,94,internal_species(518)),
        603:(7,96,internal_species(604)),
    }
    for nat,expected in reps.items():
        slots=read_evo_slots(rom,CORRECTED_EVOLUTION_OFF,internal_species(nat))
        checks.append((f'direct_{nat}',expected in slots))
    for rec in sorted(CUSTOM_ACTIVE_RECORDS):
        src,m,p,tgt=rec; raw=struct.pack('<HHHH',internal_species(src),m,(internal_species(p) if m==22 else p),internal_species(tgt))
        checks.append((f'hook_record_{src}_{tgt}',raw in hook))
    broken_raw=p32(BROKEN_EVOLUTION_PTR)
    broken_refs=[p for p in range(0,0x1000000-3) if rom[p:p+4]==broken_raw]
    checks.append(('broken_30byte_table_refs_removed', len(broken_refs)==0))

    allowed=[(GET_EVOLUTION_TARGET_OFF,GET_EVOLUTION_TARGET_OFF+8)]
    allowed += [(p,p+4) for p in EVOLUTION_PTR_SITES]
    allowed += [(HOOK_OFF,HOOK_OFF+len(hook)),(CORRECTED_EVOLUTION_OFF,CORRECTED_EVOLUTION_OFF+len(table))]
    unexpected=[]; changed=0
    for i,(a,b) in enumerate(zip(inp,rom)):
        if a!=b:
            changed+=1
            if not any(lo<=i<hi for lo,hi in allowed): unexpected.append(i)
    checks.append(('diff_only_declared_regions', len(unexpected)==0))
    checks += [
        ('edge_count_136',len(edge_rows)==136),
        ('active_table_103',len(active_table_edges)==103),
        ('active_hook_10',len(active_hook_edges)==10),
        ('pending_23',len(pending_edges)==23),
    ]
    assert all(ok for _,ok in checks),[n for n,ok in checks if not ok]

    args.output_rom.parent.mkdir(parents=True,exist_ok=True); args.output_rom.write_bytes(rom)
    with args.audit_csv.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(edge_rows[0].keys())); w.writeheader(); w.writerows(edge_rows)

    status_counts=Counter(r['status'] for r in edge_rows)
    method_counts=Counter(r['bw_method'] for r in edge_rows)
    manifest={
        'target':'Pokemon Emerald (USA, Europe) BPEE rev0',
        'input_rom':args.input_rom.name,'input_sha1':sha1(inp),
        'output_rom':args.output_rom.name,'output_sha1':sha1(rom),'output_sha256':sha256(rom),'output_size':len(rom),
        'bw_rom':args.bw_rom.name,'bw_sha1':sha1(nds),'source_evolution_path':'a/0/1/9',
        'evolution_narc':{'members':len(evo_members),'member_size':42,'slots_per_member':7,'slot_layout':'method u16, param u16, target national species u16'},
        'retail_bpee_evolution_abi':{'source_offset':hex(ORIGINAL_EVOLUTION_OFF),'species_count':ORIGINAL_EVOLUTION_COUNT,'evos_per_mon':5,'slot_size':8,'species_stride':40,'note':'retail ABI pads each 3*u16 Evolution to 8 bytes'},
        'corrected_evolution_table':{'offset':hex(CORRECTED_EVOLUTION_OFF),'gba_ptr':hex(CORRECTED_EVOLUTION_PTR),'species_count':EXTENDED_SPECIES_COUNT,'size':len(table),'pointer_sites':[hex(x) for x in EVOLUTION_PTR_SITES]},
        'runtime_hook':{'function':'GetEvolutionTargetSpecies','retail_offset':hex(GET_EVOLUTION_TARGET_OFF),'arm_hook':hex(HOOK_ARM_ADDR),'hook_size':len(hook),'original_entry':original_entry.hex(),'policy':'run vanilla first; if no result, evaluate supported Gen V-only methods'},
        'species_id_mapping':{'source':'input ROM expanded internal->National table','offset':hex(NATIONAL_MAP_OFF),'policy':'invert with first/canonical internal ID; never assume National+constant for Gen III Hoenn species','samples':{'252':internal_species(252),'290':internal_species(290),'351':internal_species(351),'358':internal_species(358),'386':internal_species(386),'387':internal_species(387),'649':internal_species(649)}},
        'binary_diff':{'changed_bytes':changed,'unexpected_changed_bytes':len(unexpected),'broken_30byte_pointer_refs_first_16MiB':len(broken_refs)},
        'edge_scope':'all BW evolution edges where source or target National Dex number is 387-649',
        'edge_counts':{'total':len(edge_rows),**status_counts},
        'method_counts':{str(k):v for k,v in sorted(method_counts.items())},
        'active_table_policy':{'methods':'BW 1-5 map to Emerald 1-5; BW method 8 maps to Emerald EVO_ITEM only for legacy stones','legacy_stone_map':BW_STONE_TO_EMERALD,'day_night_note':'friendship day/night currently uses Emerald RTC policy; Gen V seasonal time-of-day integration remains separate'},
        'active_hook_policy':{'methods':[21,22,23,24],'records':len(active_hook_edges),'known_move_limit':'only move IDs already present in Emerald; Aipom/Double Hit remains pending','party_species':'non-Egg party member required'},
        'pending_dependencies':{'count':len(pending_edges),'items':'new stones, trade items, Oval Stone, Razor Claw/Fang, Dawn Stone','field':'magnetic field / Moss Rock / Ice Rock location semantics','moves':'Double Hit ID 458','trade':'Karrablast/Shelmet partner-species context'},
        'static_validation':{'passed':sum(ok for _,ok in checks),'total':len(checks),'checks':[{'name':n,'pass':ok} for n,ok in checks]},
        'emulator_boot_tested':False,'rom_binary_committed_to_github':False,
    }
    args.manifest.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['input_sha1','output_sha1','output_sha256','edge_counts','corrected_evolution_table','runtime_hook','static_validation']},indent=2))

if __name__=='__main__': main()
