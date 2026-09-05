#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, struct, zlib

BANK_SIZE = 0x4000
TARGET_BANK = 0x7E
TARGET_OFFSET = TARGET_BANK * BANK_SIZE
TARGET_ROM_SIZE = 0x200000
MAGIC = b"SJ256P1\0"
FORMAT_VERSION = 1
HEADER_SIZE = 64

ROMS = {
    "Pokemon - Edicion Plata (Spain).gbc": {"sha256": "6797010c052e8f9373ea2b9e855ec078b34fda12e5ccf742eb19bb5e8f6947c2", "newdex_offset": 0x40D62, "base_offset": 0x51B19, "family": "INTL-ES"},
    "Pokemon - Versione Argento (Italy).gbc": {"sha256": "04c442246d1ae0ed6bf5e072bb7e3d06376e584b953d6b14047b39e45fbb0cb4", "newdex_offset": 0x40D71, "base_offset": 0x51B19, "family": "INTL-IT"},
    "Pokemon - Silver Version (USA, Europe).gbc": {"sha256": "72b190859a59623cbef6c49d601f8de52c1d2331b4f08a8d2acc17274fc19a8c", "newdex_offset": 0x40D60, "base_offset": 0x51B0B, "family": "INTL-EN"},
    "Pocket Monsters Gin (Japan).gbc": {"sha256": "0a532063a3ff5750a464582aa7bbee2b6d42e1a92a136d9f4590e373487b615c", "newdex_offset": 0x40C2C, "base_offset": 0x51AA9, "family": "JP-REV0"},
    "Pocket Monsters Gin (Japan) (Rev A).gbc": {"sha256": "99e5267fbf5a7748d4f3b75ba1990cb5d91348339468607a04bfbc6081c62d71", "newdex_offset": 0x40C2C, "base_offset": 0x51AA9, "family": "JP-REVA"},
    "Pokemon - Silberne Edition (Germany).gbc": {"sha256": "c3d1fd0dec1d5fa9aa7f85275e79c52aa9175d191c63cbed7b406c306d946348", "newdex_offset": 0x40D5A, "base_offset": 0x51B00, "family": "INTL-DE"},
    "Pocket Monsters Eun (Korea).gbc": {"sha256": "ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22", "newdex_offset": 0x40C61, "base_offset": 0x51BDF, "family": "KR"},
    "Pokemon - Version Argent (France).gbc": {"sha256": "e120c4ddb0dc3e25b95c9c71b3ffd59ff57ce689cf4d79d04913ba59140c18c2", "newdex_offset": 0x40D68, "base_offset": 0x51B10, "family": "INTL-FR"},
}

NEW_SPECIES = {
    252: dict(name="Yanmega", national=469, parent=193, stats=[86,76,86,95,116,56], types=[7,2], catch=30, base_exp=198, growth=0, egg_group=0x33, trigger_move=246),
    253: dict(name="Ambipom", national=424, parent=190, stats=[75,100,66,115,60,66], types=[0,0], catch=45, base_exp=186, growth=4, egg_group=0x55, trigger_move=252),
    254: dict(name="Lickilicky", national=463, parent=108, stats=[110,85,95,50,80,95], types=[0,0], catch=30, base_exp=193, growth=0, egg_group=0x11, trigger_move=205),
    255: dict(name="Tangrowth", national=465, parent=114, stats=[100,100,125,50,110,50], types=[22,22], catch=30, base_exp=211, growth=0, egg_group=0x77, trigger_move=246),
    256: dict(name="Mamoswine", national=473, parent=221, stats=[110,130,80,80,70,60], types=[25,4], catch=50, base_exp=207, growth=5, egg_group=0x55, trigger_move=246),
}
INSERT_AFTER = {193:252,190:253,108:254,114:255,221:256}
BASE32, BASE16 = 32, 33

def sha256(data): return hashlib.sha256(data).hexdigest()

def fix_header(rom):
    x=0
    for i in range(0x134,0x14D): x=(x-rom[i]-1)&0xFF
    rom[0x14D]=x
    rom[0x14E]=rom[0x14F]=0
    total=(sum(rom[:0x14E])+sum(rom[0x150:]))&0xFFFF
    rom[0x14E],rom[0x14F]=(total>>8)&0xFF,total&0xFF

def validate_header(rom):
    x=0
    for i in range(0x134,0x14D): x=(x-rom[i]-1)&0xFF
    return x==rom[0x14D]

def build_order(old):
    assert len(old)==251 and sorted(old)==list(range(1,252))
    out=[]
    for sid in old:
        out.append(sid)
        if sid in INSERT_AFTER: out.append(INSERT_AFTER[sid])
    assert sorted(out)==list(range(1,257))
    return out

def national_map():
    return list(range(1,252))+[NEW_SPECIES[s]["national"] for s in range(252,257)]

def base16(base251):
    records=[]
    for sid in range(1,252):
        r=bytearray(base251[(sid-1)*BASE32:sid*BASE32]); assert r[0]==sid
        records.append(struct.pack('<H',sid)+r[1:])
    for sid in range(252,257):
        s=NEW_SPECIES[sid]; p=s['parent']; old=bytearray(base251[(p-1)*BASE32:p*BASE32]); tail=bytearray(old[1:])
        tail[0:6]=bytes(s['stats']); tail[6:8]=bytes(s['types']); tail[8]=s['catch']; tail[9]=s['base_exp']; tail[21]=s['growth']; tail[22]=s['egg_group']
        records.append(struct.pack('<H',sid)+tail)
    blob=b''.join(records); assert len(blob)==256*BASE16; return blob

def payload(old_order, base251, newdex_offset, base_offset):
    nat=b''.join(struct.pack('<H',n) for n in national_map())
    order=b''.join(struct.pack('<H',n) for n in build_order(old_order))
    base=base16(base251)
    evo=b''.join(struct.pack('<HHBHB',NEW_SPECIES[t]['parent'],t,1,NEW_SPECIES[t]['trigger_move'],0) for t in range(252,257))
    move=struct.pack('<HBBBBBB',252,0,35,90,10,2,2)
    no=HEADER_SIZE; oo=no+len(nat); bo=oo+len(order); eo=bo+len(base); mo=eo+len(evo); end=mo+len(move); assert end<=BANK_SIZE
    body=nat+order+base+evo+move; crc=zlib.crc32(body)&0xFFFFFFFF
    h=bytearray(HEADER_SIZE); h[:8]=MAGIC
    struct.pack_into('<HHHHHHHHHH',h,8,FORMAT_VERSION,HEADER_SIZE,256,256,BASE16,0xF,no,oo,bo,eo)
    struct.pack_into('<HHI',h,28,mo,end,crc); struct.pack_into('<II',h,36,newdex_offset,base_offset)
    return bytes(h)+body, f'{crc:08x}'

def main():
    root=Path('/mnt/data'); outdir=root/'silver_hgss_johto256_stage1'/'roms'; outdir.mkdir(parents=True,exist_ok=True)
    report={'format':'SILVER-HGSS-JOHTO-256-stage1','target_bank':'0x7E','target_offset':'0x1F8000','roms':[]}
    canon_order=None; canon_base=None
    for filename,cfg in ROMS.items():
        raw=(root/filename).read_bytes(); assert sha256(raw)==cfg['sha256']
        old=list(raw[cfg['newdex_offset']:cfg['newdex_offset']+251]); assert sorted(old)==list(range(1,252))
        b=raw[cfg['base_offset']:cfg['base_offset']+251*BASE32]; assert all(b[i*BASE32]==i+1 for i in range(251))
        bh=sha256(b); canon_base=canon_base or bh; assert bh==canon_base
        order=build_order(old); canon_order=canon_order or order; assert order==canon_order
        rom=bytearray(raw); original_size=len(rom)
        if len(rom)<TARGET_ROM_SIZE: rom.extend(b'\0'*(TARGET_ROM_SIZE-len(rom))); rom[0x148]=0x06
        assert len(rom)==TARGET_ROM_SIZE and not any(rom[TARGET_OFFSET:TARGET_OFFSET+BANK_SIZE])
        pl,crc=payload(old,b,cfg['newdex_offset'],cfg['base_offset']); rom[TARGET_OFFSET:TARGET_OFFSET+len(pl)]=pl; fix_header(rom); assert validate_header(rom)
        outname=filename[:-4]+' - HGSS Johto 256 DATA-STAGED.gbc'; (outdir/outname).write_bytes(rom)
        report['roms'].append({'file':filename,'family':cfg['family'],'original_size':original_size,'output_file':outname,'output_size':len(rom),'source_sha256':cfg['sha256'],'output_sha256':sha256(rom),'newdex_offset':f"0x{cfg['newdex_offset']:X}",'base_offset':f"0x{cfg['base_offset']:X}",'payload_length':len(pl),'payload_crc32':crc,'header_checksum_ok':validate_header(rom),'rom_size_header':f"0x{rom[0x148]:02X}"})
    m={'schema_version':1,'logical_species_count':256,'logical_species_id_policy':'1..251 retain Gen-II IDs; 252..256 are new HGSS-Johto additions','new_species':[{'internal_id':s,**NEW_SPECIES[s]} for s in range(252,257)],'johto_order_internal_ids':canon_order,'johto_order_national_dex':[national_map()[s-1] for s in canon_order],'base_data_source_sha256':canon_base,'payload_bank':'0x7E','payload_offset':'0x1F8000','stage1_note':'Data payload is present but the vanilla engine is not yet routed to 16-bit species tables.'}
    work=root/'silver_hgss_johto256_stage1'; (work/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n'); (work/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
