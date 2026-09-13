from pathlib import Path
import struct, hashlib, json, shutil

def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def parse_fnt(fnt):
    if len(fnt)<8: return {}
    dir_count=u16(fnt,6)
    if dir_count<=0 or dir_count>4096: return {}
    dirs=[]
    for i in range(dir_count):
        o=i*8
        if o+8>len(fnt): break
        dirs.append(struct.unpack_from('<IHH',fnt,o))
    out={}; seen=set()
    def walk(did,prefix):
        idx=did-0xF000
        if idx<0 or idx>=len(dirs) or did in seen:return
        seen.add(did); suboff,fid,parent=dirs[idx]; p=suboff
        while p<len(fnt):
            n=fnt[p];p+=1
            if n==0: break
            isdir=n&0x80; ln=n&0x7f
            if p+ln>len(fnt): break
            name=fnt[p:p+ln].decode('ascii','replace');p+=ln
            if isdir:
                if p+2>len(fnt): break
                child=u16(fnt,p);p+=2
                walk(child,prefix+name+'/')
            else:
                out[fid]=prefix+name;fid+=1
    walk(0xF000,'')
    return out

def sha256(data): return hashlib.sha256(data).hexdigest()
def safe_write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)

def extract(src,out):
    b=Path(src).read_bytes(); out=Path(out); out.mkdir(parents=True,exist_ok=True)
    fields={'arm9':(u32(b,0x20),u32(b,0x2c)),'arm7':(u32(b,0x30),u32(b,0x3c)),'fnt':(u32(b,0x40),u32(b,0x44)),'fat':(u32(b,0x48),u32(b,0x4c)),'overlay9_table':(u32(b,0x50),u32(b,0x54)),'overlay7_table':(u32(b,0x58),u32(b,0x5c))}
    banner_off=u32(b,0x68); banner_size=0x840 if banner_off and banner_off+0x840<=len(b) else max(0,min(0x840,len(b)-banner_off))
    system={}; header=b[:0x200]; safe_write(out/'system/header.bin',header); system['header.bin']={'size':len(header),'sha256':sha256(header)}
    for name,(off,sz) in fields.items():
        data=b[off:off+sz] if off and sz else b''; safe_write(out/f'system/{name}.bin',data); system[f'{name}.bin']={'offset':off,'size':len(data),'sha256':sha256(data)}
    banner=b[banner_off:banner_off+banner_size] if banner_off else b''; safe_write(out/'system/banner.bin',banner); system['banner.bin']={'offset':banner_off,'size':len(banner),'sha256':sha256(banner)}
    fat_off,fat_sz=fields['fat']; fnt_off,fnt_sz=fields['fnt']; fatraw=b[fat_off:fat_off+fat_sz]; fntraw=b[fnt_off:fnt_off+fnt_sz]; count=fat_sz//8; names=parse_fnt(fntraw)
    overlays=[]; overlay_ids=set()
    for cpu,key in [('arm9','overlay9_table'),('arm7','overlay7_table')]:
        off,sz=fields[key]; tbl=b[off:off+sz]
        for i in range(0,len(tbl)//32):
            e=tbl[i*32:(i+1)*32]; ov_id,file_id=struct.unpack_from('<I',e,0)[0],struct.unpack_from('<I',e,0x18)[0]; overlay_ids.add(file_id)
            if file_id<count:
                s,eoff=struct.unpack_from('<II',fatraw,file_id*8); dat=b[s:eoff]; rel=f'overlays/{cpu}/overlay_{ov_id:04d}_file_{file_id:04d}.bin'; safe_write(out/rel,dat); overlays.append({'cpu':cpu,'overlay_id':ov_id,'file_id':file_id,'offset':s,'size':len(dat),'sha256':sha256(dat),'path':rel})
    files=[]
    for fid in range(count):
        s,e=struct.unpack_from('<II',fatraw,fid*8); dat=b[s:e]; nm=names.get(fid); rel=('nitrofs/'+nm) if nm else f'nitrofs/_unnamed/file_{fid:04d}.bin'; safe_write(out/rel,dat); files.append({'file_id':fid,'offset':s,'end':e,'size':len(dat),'sha256':sha256(dat),'magic':dat[:4].hex(),'name':nm,'path':rel,'overlay':fid in overlay_ids})
    man={'schema':'tsubaki.nds-materialization.v11','source_filename':Path(src).name,'source_size':len(b),'source_sha256':sha256(b),'rom_binary_in_output':False,'system':system,'overlay_count':len(overlays),'fat_file_count':count,'named_file_count':len(names),'nitrofs_payload_bytes':sum(x['size'] for x in files),'overlays':overlays,'files':files}
    (out/'manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2),encoding='utf-8'); return man

items=[('DIAMOND','/mnt/data/Pokemon_Diamond_USA_NDS-LGC.nds'),('PEARL','/mnt/data/Pokemon_Pearl_USA_NDS-LGC.nds'),('PLATINUM','/mnt/data/포켓몬스터Pt 기라티나.nds'),('HEARTGOLD','/mnt/data/포켓몬스터 하트골드.nds'),('SOULSILVER','/mnt/data/포켓몬스터 소울실버.nds')]
root=Path('/mnt/data/gen4_v11_materialization')
if root.exists(): shutil.rmtree(root)
summary=[]
for game,src in items:
    m=extract(src,root/game); summary.append({k:m[k] for k in ['source_filename','source_size','source_sha256','overlay_count','fat_file_count','named_file_count','nitrofs_payload_bytes']}|{'game':game})
(root/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
