#!/usr/bin/env python3
from pathlib import Path
import struct, hashlib, json, csv

ROMS = [
    ("DIAMOND", "US-EN", "ADAE-HV5", "LGC-a46233d8", Path('/mnt/data/Pokemon_Diamond_USA_NDS-LGC.nds')),
    ("PEARL", "US-EN", "APAE-HV5", "LGC-99083bf1", Path('/mnt/data/Pokemon_Pearl_USA_NDS-LGC.nds')),
    ("PLATINUM", "KR-KO", "CPUK-HV0", "UPLOAD-f811d9c7", Path('/mnt/data/포켓몬스터Pt 기라티나.nds')),
    ("HEARTGOLD", "KR-KO", "IPKK-HV0", "UPLOAD-5834fb3a", Path('/mnt/data/포켓몬스터 하트골드.nds')),
    ("SOULSILVER", "KR-KO", "IPGK-HV0", "UPLOAD-0330e644", Path('/mnt/data/포켓몬스터 소울실버.nds')),
]

def h(data, alg):
    x=hashlib.new(alg); x.update(data); return x.hexdigest()

def parse_fnt(data, fnt_off, fnt_size, fat_entries):
    fnt=data[fnt_off:fnt_off+fnt_size]
    if len(fnt)<8: return {},0
    _,_,dir_count=struct.unpack_from('<IHH',fnt,0)
    dirs=[]
    for i in range(dir_count):
        off=i*8
        if off+8>len(fnt): break
        dirs.append(struct.unpack_from('<IHH',fnt,off))
    named={}; children={}
    for i,(sub,first,parent) in enumerate(dirs):
        dir_id=0xF000+i; p=sub; file_id=first; ents=[]
        while p<len(fnt):
            n=fnt[p]; p+=1
            if n==0: break
            isdir=bool(n&0x80); ln=n&0x7F
            name=fnt[p:p+ln].decode('ascii','replace'); p+=ln
            if isdir:
                if p+2>len(fnt): break
                child=struct.unpack_from('<H',fnt,p)[0]; p+=2; ents.append(('dir',name,child))
            else:
                ents.append(('file',name,file_id)); file_id+=1
        children[dir_id]=ents
    seen=set()
    def walk(dir_id,prefix=''):
        if dir_id in seen: return
        seen.add(dir_id)
        for typ,name,val in children.get(dir_id,[]):
            if typ=='file':
                if 0<=val<fat_entries: named[val]=prefix+name
            else: walk(val,prefix+name+'/')
    walk(0xF000,'')
    return named,len(dirs)

def parse_rom(game,locale,release_id,dump_id,path):
    data=path.read_bytes(); size=len(data)
    md5=h(data,'md5'); sha1=h(data,'sha1'); sha256=h(data,'sha256')
    b=data[:0x200]
    title=b[0:12].rstrip(b'\0').decode('ascii','replace'); game_code=b[12:16].decode('ascii','replace'); maker=b[16:18].decode('ascii','replace')
    unit=b[18]; device_type=b[19]; cap=b[20]; romver=b[30]; flags=b[31]
    vals=struct.unpack_from('<16I',b,0x20)
    arm9_off,arm9_entry,arm9_ram,arm9_size,arm7_off,arm7_entry,arm7_ram,arm7_size,fnt_off,fnt_size,fat_off,fat_size,ov9_off,ov9_size,ov7_off,ov7_size=vals
    banner_off=struct.unpack_from('<I',b,0x68)[0]; secure_crc=struct.unpack_from('<H',b,0x6C)[0]; secure_delay=struct.unpack_from('<H',b,0x6E)[0]
    arm9_autoload,arm7_autoload=struct.unpack_from('<II',b,0x70); secure_disable=struct.unpack_from('<Q',b,0x78)[0]
    used_size=struct.unpack_from('<I',b,0x80)[0]; header_size=struct.unpack_from('<I',b,0x84)[0]
    logo_crc=struct.unpack_from('<H',b,0x15C)[0]; header_crc=struct.unpack_from('<H',b,0x15E)[0]
    fat_entries=fat_size//8; named,dir_count=parse_fnt(data,fnt_off,fnt_size,fat_entries)
    files=[]
    for fid in range(fat_entries):
        s,e=struct.unpack_from('<II',data,fat_off+fid*8)
        if e<s or e>size: fs=0; chunk=b''
        else: fs=e-s; chunk=data[s:e]
        magic=chunk[:4].decode('ascii','replace') if len(chunk)>=4 and all(32<=x<127 for x in chunk[:4]) else ''
        files.append({'file_id':fid,'path':named.get(fid,''),'start':s,'end':e,'size':fs,'magic':magic,'sha256':hashlib.sha256(chunk).hexdigest()})
    header={'schema':'nds-header-observation-v9','game':game,'locale':locale,'release_id':release_id,'dump_id':dump_id,'title':title,'game_code':game_code,'maker_code':maker,'unit_code':unit,'device_type':device_type,'device_capacity_exponent':cap,'nominal_capacity_bytes':128*1024*(2**cap),'header_version':romver,'autostart_flags':flags,'arm9':{'rom_offset':arm9_off,'entry_address':arm9_entry,'ram_address':arm9_ram,'size':arm9_size},'arm7':{'rom_offset':arm7_off,'entry_address':arm7_entry,'ram_address':arm7_ram,'size':arm7_size},'fnt':{'offset':fnt_off,'size':fnt_size,'directory_count':dir_count,'named_file_count':len(named)},'fat':{'offset':fat_off,'size':fat_size,'entry_count':fat_entries},'overlay9':{'offset':ov9_off,'size':ov9_size},'overlay7':{'offset':ov7_off,'size':ov7_size},'banner_offset':banner_off,'secure_area_crc16':secure_crc,'secure_transfer_delay':secure_delay,'arm9_autoload':arm9_autoload,'arm7_autoload':arm7_autoload,'secure_disable':secure_disable,'used_rom_size':used_size,'header_size':header_size,'logo_crc16':logo_crc,'header_crc16':header_crc}
    manifest={'schema':'rom-observation-v9','generation':'GEN-04','game':game,'platform':'NDS-NTR','package_kind':'CART','release_id':release_id,'dump_id':dump_id,'locale':locale,'source_filename':path.name,'rom_binary_committed':False,'size':size,'hashes':{'md5':md5,'sha1':sha1,'sha256':sha256},'header':{'title':title,'game_code':game_code,'maker_code':maker,'unit_code':unit,'header_version':romver},'nitrofs':{'fat_entries':fat_entries,'fnt_directories':dir_count,'named_files':len(named),'named_narc_files':sum(1 for f in files if f['path'] and f['magic']=='NARC')},'canonical_source_path':f'GEN-04/{game}/SOURCE/NDS-NTR/CART/{release_id}','canonical_dump_path':f'GEN-04/{game}/SOURCE/NDS-NTR/CART/{release_id}/DUMPS/{dump_id}'}
    return manifest,header,files

if __name__=='__main__':
    out=Path('/mnt/data/gen4_v9_package'); out.mkdir(exist_ok=True); allm=[]
    for row in ROMS:
        m,hd,files=parse_rom(*row); allm.append(m); d=out/m['game']; d.mkdir(exist_ok=True)
        (d/'rom-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'header.json').write_text(json.dumps(hd,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        with (d/'nitrofs-files.tsv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['file_id','path','start','end','size','magic','sha256'],delimiter='\t'); w.writeheader(); w.writerows(files)
        summary={k:m[k] for k in ['schema','generation','game','platform','package_kind','release_id','dump_id','locale','size','hashes','nitrofs']}
        (d/'nitrofs-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'rom-set.json').write_text(json.dumps({'schema':'rom-set-v9','id':'GEN04-USER-SOURCESET-2026-09-13','rom_binary_committed':False,'sources':allm},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(allm,ensure_ascii=False,indent=2))
