#!/usr/bin/env python3
"""Reproducible semantic validation for the FIRE RED 8-ROM workspace.
Analysis-only: this script never modifies or emits ROM binaries.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, struct
from pathlib import Path

ROMS = {
"Pocket Monsters - Fire Red (Japan) (Rev 1).gba":dict(trainers=0x1F97F0,trainer_stride=32,species_names=0x1FF4D0,species_info=0x20C9A4,battle_moves=0x208E24,national=0x20A20E,regional=0x209ED8,cryconv=0x20BBF4,tmhm=0x20ADE8,evolutions=0x211974,levelup=0x2159D4,egg=0x217130,tutor=0x414BF0,tm_moves=0x415634,mapgroups=0x311F70,wild=0x38C2F4),
"Pocket Monsters - Fire Red (Japan).gba":dict(trainers=0x1FDFD8,trainer_stride=32,species_names=0x203CB8,species_info=0x21118C,battle_moves=0x20D60C,national=0x20E9F6,regional=0x20E6C0,cryconv=0x2103DC,tmhm=0x20F5D0,evolutions=0x21615C,levelup=0x21A1BC,egg=0x21B918,tutor=0x4192F0,tm_moves=0x419D34,mapgroups=0x316758,wild=0x390B34),
"Pokemon - Edicion Rojo Fuego (Spain).gba":dict(trainers=0x23A234,trainer_stride=40,species_names=0x24164C,species_info=0x24FF4C,battle_moves=0x24C3CC,national=0x24D7B6,regional=0x24D480,cryconv=0x24F19C,tmhm=0x24E390,evolutions=0x254F1C,levelup=0x258F7C,egg=0x25A6D4,tutor=0x4541D8,tm_moves=0x454C1C,mapgroups=0x34DE70,wild=0x3C53A8),
"Pokemon - Feuerrote Edition (Germany).gba":dict(trainers=0x23E998,trainer_stride=40,species_names=0x245DB0,species_info=0x2546A8,battle_moves=0x250B28,national=0x251F12,regional=0x251BDC,cryconv=0x2538F8,tmhm=0x252AEC,evolutions=0x259678,levelup=0x25D6D8,egg=0x25EE30,tutor=0x45AC2C,tm_moves=0x45B670,mapgroups=0x3525CC,wild=0x3C9B04),
"Pokemon - Fire Red Version (USA).gba":dict(trainers=0x23EAC8,trainer_stride=40,species_names=0x245EE0,species_info=0x254784,battle_moves=0x250C04,national=0x251FEE,regional=0x251CB8,cryconv=0x2539D4,tmhm=0x252BC8,evolutions=0x259754,levelup=0x25D7B4,egg=0x25EF0C,tutor=0x459B60,tm_moves=0x45A5A4,mapgroups=0x3526A8,wild=0x3C9CB8),
"Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba":dict(trainers=0x23EB38,trainer_stride=40,species_names=0x245F50,species_info=0x2547F4,battle_moves=0x250C74,national=0x25205E,regional=0x251D28,cryconv=0x253A44,tmhm=0x252C38,evolutions=0x2597C4,levelup=0x25D824,egg=0x25EF7C,tutor=0x459BC0,tm_moves=0x45A604,mapgroups=0x352718,wild=0x3C9D28),
"Pokemon - Version Rouge Feu (France).gba":dict(trainers=0x238ED4,trainer_stride=40,species_names=0x2402EC,species_info=0x24EBD4,battle_moves=0x24B054,national=0x24C43E,regional=0x24C108,cryconv=0x24DE24,tmhm=0x24D018,evolutions=0x253BA4,levelup=0x257C04,egg=0x25935C,tutor=0x453164,tm_moves=0x453BA8,mapgroups=0x34CAF8,wild=0x3C4030),
"Pokemon - Versione Rosso Fuoco (Italy).gba":dict(trainers=0x237B6C,trainer_stride=40,species_names=0x23EF84,species_info=0x24D864,battle_moves=0x249CE4,national=0x24B0CE,regional=0x24AD98,cryconv=0x24CAB4,tmhm=0x24BCA8,evolutions=0x252834,levelup=0x256894,egg=0x257FEC,tutor=0x450B3C,tm_moves=0x451580,mapgroups=0x34B788,wild=0x3C2CC0),
}
GROUP_COUNTS=[5,123,60,66,4,6,8,10,6,8,20,10,8,2,10,4,2,2,2,1,1,2,2,3,2,3,2,1,1,1,1,7,5,5,8,8,5,5,1,1,1,2,1]
assert len(GROUP_COUNTS)==43 and sum(GROUP_COUNTS)==425
PURE_TABLES={
'species_info':('species_info',412*28),'battle_moves':('battle_moves',355*12),
'evolutions':('evolutions',412*5*6),'tmhm_compat':('tmhm',412*8),
'egg_moves':('egg',1139*2),'national_dex_table':('national',412*2),
'second_dex_table':('regional',412*2),'cry_conversion_table':('cryconv',412*2),
'move_tutor_moves':('tutor',16*2),'tm_moves':('tm_moves',58*2)}

def u32(d,o): return struct.unpack_from('<I',d,o)[0]
def romoff(p): return p-0x08000000 if 0x08000000<=p<0x0A000000 else None
def sha(b): return hashlib.sha256(b).hexdigest()

def validate_levelup(d,o):
    ptrs=[romoff(u32(d,o+i*4)) for i in range(412)]; invalid=total=0; uniq=set(); vectors=[]
    for p in ptrs:
        if p is None: invalid+=1; vectors.append('BAD'); continue
        uniq.add(p); vals=[]; q=p
        while q+2<=len(d):
            v=struct.unpack_from('<H',d,q)[0]; q+=2
            if v==0xFFFF: break
            level=v>>9; move=v&0x1FF
            if not(1<=level<=100 and 1<=move<355): invalid+=1
            vals.append(v); total+=1
        else: invalid+=1
        vectors.append(sha(b''.join(struct.pack('<H',v) for v in vals)))
    return dict(pointer_count=412,unique_arrays=len(uniq),total_entries=total,invalid=invalid,
                vector_sha256=sha('\n'.join(vectors).encode()))

def validate_wild(d,o):
    counts=(12,5,5,10); headers=[]; infos={}; arrays={}; invalid=total=0
    for i in range(132):
        p=o+i*20; mg,mn=d[p],d[p+1]; hp=[]
        for j,c in enumerate(counts):
            ip=romoff(u32(d,p+4+j*4)); hp.append(ip)
            if ip is not None:
                if ip+8>len(d): invalid+=1; continue
                rate=d[ip]; ap=romoff(u32(d,ip+4)); infos[ip]=(rate,ap,c)
                if ap is None or ap+c*4>len(d): invalid+=1; continue
                rec=[]
                for k in range(c):
                    lo,hi,species=struct.unpack_from('<BBH',d,ap+k*4)
                    if lo>hi or species>=412: invalid+=1
                    rec.append((lo,hi,species)); total+=1
                arrays[ap]=tuple(rec)
        headers.append((mg,mn,tuple(hp)))
    sentinel=d[o+132*20:o+133*20]
    sentinel_ok=sentinel[:4]==b'\xff\xff\x00\x00' and sentinel[4:]==b'\0'*16
    sem=[]
    for mg,mn,hp in headers:
        row=[mg,mn]
        for ip in hp:
            if ip is None: row.append(None)
            else:
                rate,ap,c=infos[ip]; row.append((rate,arrays.get(ap,())))
        sem.append(row)
    return dict(headers=132,sentinel_ok=sentinel_ok,unique_map_keys=len(set((x[0],x[1]) for x in headers)),
                unique_info=len(infos),unique_arrays=len(arrays),total_slots=total,invalid=invalid,
                semantic_sha256=sha(json.dumps(sem,separators=(',',':')).encode()))

def validate_maps(d,o):
    headers=[]
    for gi,c in enumerate(GROUP_COUNTS):
        gp=romoff(u32(d,o+gi*4))
        if gp is None:return dict(ok=False)
        for mi in range(c):
            hp=romoff(u32(d,gp+mi*4))
            if hp is None or hp+0x1C>len(d):return dict(ok=False)
            headers.append(hp)
    return dict(ok=True,groups=43,headers=len(headers),unique_headers=len(set(headers)))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom_dir',nargs='?',default='/mnt/data'); ap.add_argument('-o','--out',default='fire_red_semantic_validation'); a=ap.parse_args()
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True); rows=[]; card={k:set() for k in PURE_TABLES}
    detail=[]
    for name,cfg in ROMS.items():
        p=Path(a.rom_dir)/name
        if not p.exists():continue
        d=p.read_bytes(); lvl=validate_levelup(d,cfg['levelup']); wild=validate_wild(d,cfg['wild']); maps=validate_maps(d,cfg['mapgroups'])
        pure={}
        for label,(key,size) in PURE_TABLES.items():
            h=sha(d[cfg[key]:cfg[key]+size]); pure[label]=h; card[label].add(h)
        endok=cfg['trainers']+743*cfg['trainer_stride']==cfg['species_names']
        rows.append([name,endok,lvl['invalid'],wild['invalid'],wild['sentinel_ok'],maps['ok']])
        detail.append(dict(rom=name,trainer_end_ok=endok,levelup=lvl,wild=wild,maps=maps,pure_tables=pure))
    with (out/'semantic_validation.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['rom','trainer_end_ok','levelup_invalid','wild_invalid','wild_sentinel_ok','maps_ok']); w.writerows(rows)
    result={'roms':detail,'pure_table_hash_cardinality':{k:len(v) for k,v in card.items()}}
    (out/'semantic_validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
