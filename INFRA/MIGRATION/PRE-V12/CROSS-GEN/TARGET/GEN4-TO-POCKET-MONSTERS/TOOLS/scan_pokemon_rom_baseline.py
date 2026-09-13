#!/usr/bin/env python3
"""Generate ROM identity/header catalogs and NDS FAT/FNT indexes without copying ROM bytes.

Project: GEN4-TO-POCKET-MONSTERS
The tool intentionally emits metadata/indexes only. It never writes a ROM image.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, json, re, struct, zlib
from pathlib import Path

DEFAULT_INPUTS = {
    'Pokemon_Diamond_USA_NDS-LGC.nds': ('GEN-04','DIAMOND','SOURCE','US-EN'),
    'Pokemon_Pearl_USA_NDS-LGC.nds': ('GEN-04','PEARL','SOURCE','US-EN'),
    '포켓몬스터Pt 기라티나.nds': ('GEN-04','PLATINUM','SOURCE','KR-KO'),
    '포켓몬스터 하트골드.nds': ('GEN-04','HEARTGOLD','SOURCE','KR-KO'),
    '포켓몬스터 소울실버.nds': ('GEN-04','SOULSILVER','SOURCE','KR-KO'),
    'Pocket Monsters Geum (Korea).gbc': ('GEN-02','GOLD','TARGET','KR-KO'),
    'Pocket Monsters Eun (Korea).gbc': ('GEN-02','SILVER','TARGET','KR-KO'),
    'Pocket Monsters - Crystal Version (Japan).gbc': ('GEN-02','CRYSTAL','TARGET','JP-JA'),
    'Pokemon - Crystal Version (USA, Europe) (Rev A).gbc': ('GEN-02','CRYSTAL','TARGET','US-EU-EN'),
    'Pocket Monsters - Ruby (Japan).gba': ('GEN-03','RUBY','TARGET','JP-JA'),
    'Pokemon - Ruby Version (USA, Europe) (Rev 2).gba': ('GEN-03','RUBY','TARGET','US-EU-EN'),
    'Pocket Monsters - Sapphire (Japan).gba': ('GEN-03','SAPPHIRE','TARGET','JP-JA'),
    'Pokemon - Sapphire Version (USA, Europe) (Rev 2).gba': ('GEN-03','SAPPHIRE','TARGET','US-EU-EN'),
    'Pocket Monsters - Emerald (Japan).gba': ('GEN-03','EMERALD','TARGET','JP-JA'),
    'Pokemon - Emerald Version (USA, Europe).gba': ('GEN-03','EMERALD','TARGET','US-EU-EN'),
    'Pocket Monsters - Fire Red (Japan) (Rev 1).gba': ('GEN-03','FIRERED','TARGET','JP-JA'),
    'Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba': ('GEN-03','FIRERED','TARGET','US-EU-EN'),
    'Pocket Monsters - Leaf Green (Japan).gba': ('GEN-03','LEAFGREEN','TARGET','JP-JA'),
    'Pokemon - Leaf Green Version (Europe) (Rev 1).gba': ('GEN-03','LEAFGREEN','TARGET','US-EU-EN'),
}

MAGIC_KIND = {b'NARC':'NARC', b'RGCN':'NCGR', b'RLCN':'NCLR', b'RCSN':'NSCR', b'RNAN':'NANR', b'RECN':'NCER', b'BMD0':'NSBMD', b'BTX0':'NSBTX', b'BCA0':'NSBCA', b'SDAT':'SDAT'}
EXT_KIND = {'.narc':'NARC','.ncgr':'NCGR','.nclr':'NCLR','.nscr':'NSCR','.nanr':'NANR','.ncer':'NCER','.nsbmd':'NSBMD','.nsbtx':'NSBTX','.nsbca':'NSBCA','.sdat':'SDAT','.bin':'BIN','.dat':'DAT','.txt':'TEXT'}

def ascii0(b: bytes) -> str:
    return b.split(b'\0',1)[0].decode('ascii','replace').rstrip()

def digest(data: bytes) -> dict:
    return {'crc32':f'{zlib.crc32(data)&0xffffffff:08x}', 'md5':hashlib.md5(data).hexdigest(), 'sha1':hashlib.sha1(data).hexdigest(), 'sha256':hashlib.sha256(data).hexdigest()}

def nds_header(data: bytes) -> dict:
    b=data[:0x4000]
    h={'title':ascii0(b[0:12]), 'game_code':b[12:16].decode('ascii','replace'), 'maker_code':b[16:18].decode('ascii','replace'), 'unit_code':b[18], 'device_type':b[19], 'device_capacity_exp':b[20], 'header_version':b[0x1e], 'autostart':b[0x1f]}
    fields=[('arm9_offset',0x20),('arm9_entry',0x24),('arm9_ram',0x28),('arm9_size',0x2c),('arm7_offset',0x30),('arm7_entry',0x34),('arm7_ram',0x38),('arm7_size',0x3c),('fnt_offset',0x40),('fnt_size',0x44),('fat_offset',0x48),('fat_size',0x4c),('arm9_overlay_offset',0x50),('arm9_overlay_size',0x54),('arm7_overlay_offset',0x58),('arm7_overlay_size',0x5c),('icon_banner_offset',0x68),('rom_size_header',0x80),('header_size',0x84)]
    for name,off in fields: h[name]=struct.unpack_from('<I',b,off)[0]
    h['fat_entry_count']=h['fat_size']//8
    h['nominal_capacity_bytes']=128*1024 << h['device_capacity_exp']
    return h

def gba_header(data: bytes) -> dict:
    b=data[:0xc0]
    return {'title':ascii0(b[0xa0:0xac]), 'game_code':b[0xac:0xb0].decode('ascii','replace'), 'maker_code':b[0xb0:0xb2].decode('ascii','replace'), 'fixed_value':b[0xb2], 'main_unit_code':b[0xb3], 'device_type':b[0xb4], 'software_version':b[0xbc], 'header_complement':b[0xbd]}

def gbc_header(data: bytes) -> dict:
    b=data[:0x150]; cgb=b[0x143]; end=0x13f if cgb in (0x80,0xc0) else 0x143
    return {'title':ascii0(b[0x134:end+1]), 'cgb_flag':cgb, 'new_licensee':b[0x144:0x146].decode('ascii','replace'), 'sgb_flag':b[0x146], 'cartridge_type':b[0x147], 'rom_size_code':b[0x148], 'ram_size_code':b[0x149], 'destination_code':b[0x14a], 'old_licensee':b[0x14b], 'mask_rom_version':b[0x14c], 'header_checksum':b[0x14d], 'global_checksum':struct.unpack_from('>H',b,0x14e)[0]}

def release_id(ext: str, h: dict) -> str:
    if ext=='.nds': return f"{h['game_code']}-HV{h['header_version']}"
    if ext=='.gba': return f"{h['game_code']}-HV{h['software_version']}"
    slug=re.sub(r'[^A-Z0-9]+','-',h['title'].upper()).strip('-') or 'UNTITLED'
    return f"{slug}-DC{h['destination_code']}-MV{h['mask_rom_version']}"

def platform_id(ext: str) -> str:
    return {'.nds':'NDS-NTR','.gba':'GBA-AGB','.gbc':'GBC-CGB'}[ext]

def nds_index(data: bytes, h: dict) -> list[dict]:
    fnt=data[h['fnt_offset']:h['fnt_offset']+h['fnt_size']]
    fat=data[h['fat_offset']:h['fat_offset']+h['fat_size']]
    if len(fnt)<8: return []
    n_dirs=struct.unpack_from('<H',fnt,6)[0]
    dirs=[struct.unpack_from('<IHH',fnt,i*8) for i in range(n_dirs)]
    children={i:[] for i in range(n_dirs)}; files={i:[] for i in range(n_dirs)}
    for i,(sub_off,first_id,parent) in enumerate(dirs):
        pos=sub_off; fid=first_id
        while pos < len(fnt):
            n=fnt[pos]; pos+=1
            if n==0: break
            is_dir=bool(n&0x80); ln=n&0x7f
            name=fnt[pos:pos+ln].decode('ascii','replace'); pos+=ln
            if is_dir:
                did=struct.unpack_from('<H',fnt,pos)[0]-0xf000; pos+=2; children[i].append((name,did))
            else: files[i].append((name,fid)); fid+=1
    names={}
    def walk(did:int,prefix:str=''):
        for name,fid in files.get(did,[]): names[fid]=prefix+name
        for name,sub in children.get(did,[]): walk(sub,prefix+name+'/')
    walk(0)
    out=[]
    for fid in range(h['fat_entry_count']):
        start,end=struct.unpack_from('<II',fat,fid*8); blob=data[start:end]
        path=names.get(fid,f'__unnamed__/{fid:04d}.bin'); ext=Path(path).suffix.lower(); magic=blob[:4]
        kind=EXT_KIND.get(ext) or MAGIC_KIND.get(magic) or ('BIN' if not ext else ext[1:].upper())
        out.append({'file_id':fid,'path':path,'start':start,'end':end,'size':max(0,end-start),'magic_ascii':''.join(chr(c) if 32<=c<127 else '.' for c in magic),'kind':kind,'sha1':hashlib.sha1(blob).hexdigest()})
    return out

def scan_one(path: Path, meta: tuple[str,str,str,str], out_root: Path) -> dict:
    gen,game,role,locale=meta; data=path.read_bytes(); ext=path.suffix.lower()
    header=nds_header(data) if ext=='.nds' else gba_header(data) if ext=='.gba' else gbc_header(data)
    hashes=digest(data); rid=release_id(ext,header); dump_id='DUMP-'+hashes['sha1'][:12]
    root=f"{gen}/{game}/SOURCE/{platform_id(ext)}/CART/{rid}"
    rec={'schema':'rom-observation-v9','project':'GEN4-TO-POCKET-MONSTERS','role_in_project':role,'generation':gen,'game':game,'platform':platform_id(ext),'package_kind':'CART','release_id':rid,'dump_id':dump_id,'locale_claim':locale,'source_filename':path.name,'size':len(data),**hashes,'header':header,'canonical_release_root':root,'rom_binary_committed':False}
    if ext=='.nds':
        rows=nds_index(data,header)
        rec['nitrofs']={'file_count':len(rows),'named_count':sum(not r['path'].startswith('__unnamed__') for r in rows),'total_file_bytes':sum(r['size'] for r in rows),'kind_counts':dict(collections.Counter(r['kind'] for r in rows))}
        d=out_root/'nds-indexes'/rid; d.mkdir(parents=True,exist_ok=True)
        with (d/'nitrofs-index.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    return rec

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('rom_dir',type=Path); ap.add_argument('out_dir',type=Path)
    args=ap.parse_args(); args.out_dir.mkdir(parents=True,exist_ok=True)
    missing=[name for name in DEFAULT_INPUTS if not (args.rom_dir/name).is_file()]
    if missing: raise SystemExit('Missing expected ROMs: '+', '.join(missing))
    records=[scan_one(args.rom_dir/name,meta,args.out_dir) for name,meta in DEFAULT_INPUTS.items()]
    (args.out_dir/'rom-observations.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fields=['role_in_project','generation','game','platform','package_kind','release_id','dump_id','locale_claim','source_filename','size','crc32','md5','sha1','sha256','canonical_release_root']
    with (args.out_dir/'rom-observations.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows({k:r.get(k) for k in fields} for r in records)
    print(f'wrote {len(records)} observations to {args.out_dir}')
    return 0

if __name__=='__main__': raise SystemExit(main())
