from PIL import Image
import numpy as np, os, io, csv, json, zipfile, hashlib, struct, math, time, shutil

ROMSETS = {
    'DP_US': {
        'rom': '/mnt/data/Pokemon_Diamond_USA_NDS-LGC.nds',
        'games': ['Pokemon Diamond USA','Pokemon Pearl USA'],
        'main_path': 'poketool/pokegra/pokegra.narc',
        'other_path': 'poketool/pokegra/otherpoke.narc',
        'kind':'DP',
    },
    'PT_KOR': {
        'rom': '/mnt/data/포켓몬스터Pt 기라티나.nds',
        'games':['Pokemon Platinum Korea'],
        'main_path':'poketool/pokegra/pl_pokegra.narc',
        'other_path':'poketool/pokegra/pl_otherpoke.narc',
        'kind':'PT',
    },
    'HGSS_KOR': {
        'rom':'/mnt/data/포켓몬스터 하트골드.nds',
        'games':['Pokemon HeartGold Korea','Pokemon SoulSilver Korea'],
        'main_path':'a/0/0/4',
        'other_path':'a/1/1/4',
        'kind':'HGSS',
    },
}
GAME_ROMS={
 'Pokemon Diamond USA':'/mnt/data/Pokemon_Diamond_USA_NDS-LGC.nds',
 'Pokemon Pearl USA':'/mnt/data/Pokemon_Pearl_USA_NDS-LGC.nds',
 'Pokemon Platinum Korea':'/mnt/data/포켓몬스터Pt 기라티나.nds',
 'Pokemon HeartGold Korea':'/mnt/data/포켓몬스터 하트골드.nds',
 'Pokemon SoulSilver Korea':'/mnt/data/포켓몬스터 소울실버.nds',
}
OUTDIR='/mnt/data/gen4_battle_sprite_master_v1'
os.makedirs(OUTDIR,exist_ok=True)
for fn in os.listdir(OUTDIR):
    p=os.path.join(OUTDIR,fn)
    if os.path.isfile(p): os.remove(p)

# ---------- filesystem ----------
def nds_files(data):
    fnt_off,fnt_size,fat_off,fat_size=struct.unpack_from('<IIII',data,0x40)
    fnt=data[fnt_off:fnt_off+fnt_size]; fat=data[fat_off:fat_off+fat_size]
    _,_,dir_count=struct.unpack_from('<IHH',fnt,0)
    dirs=[struct.unpack_from('<IHH',fnt,i*8) for i in range(dir_count)]
    names={}
    def walk(did,prefix):
        sub,first,parent=dirs[did-0xF000]; p=sub; fid=first
        while True:
            n=fnt[p]; p+=1
            if n==0: break
            isdir=n&0x80; ln=n&0x7f
            name=fnt[p:p+ln].decode('ascii',errors='replace'); p+=ln
            if isdir:
                child=struct.unpack_from('<H',fnt,p)[0]; p+=2
                walk(child,prefix+name+'/')
            else:
                names[prefix+name]=fid; fid+=1
    walk(0xF000,'')
    out={}
    for name,fid in names.items():
        s,e=struct.unpack_from('<II',fat,fid*8); out[name]=data[s:e]
    return out

def narc_members(blob):
    bt=blob.find(b'BTAF'); gm=blob.find(b'GMIF')
    count=struct.unpack_from('<H',blob,bt+8)[0]; gb=gm+8
    out=[]
    for i in range(count):
        s,e=struct.unpack_from('<II',blob,bt+12+i*8); out.append(blob[gb+s:gb+e])
    return out

# ---------- NCGR/NCLR ----------
def decrypt_payload(blob):
    size=struct.unpack_from('<I',blob,0x10+0x18)[0]
    raw=bytearray(blob[0x10+0x20:0x10+0x20+size])
    enc=raw[0] | (raw[1]<<8)
    for i in range(0,len(raw),2):
        v=(raw[i] | (raw[i+1]<<8)) ^ (enc & 0xffff)
        raw[i]=v&255; raw[i+1]=(v>>8)&255
        enc=(enc*1103515245 + 24691) & 0xffffffff
    return raw

def ncgr_idx(blob):
    raw=decrypt_payload(blob)
    b=np.frombuffer(raw,dtype=np.uint8)
    pix=np.empty(b.size*2,dtype=np.uint8)
    pix[0::2]=b&15; pix[1::2]=b>>4
    if pix.size!=12800: raise RuntimeError('unexpected battle NCGR size')
    return pix.reshape(80,160)

def nclr(blob):
    vals=np.frombuffer(blob[0x28:0x28+32],dtype='<u2',count=16)
    pal=np.zeros((16,4),dtype=np.uint8)
    pal[:,0]=(vals&31)*255//31; pal[:,1]=((vals>>5)&31)*255//31; pal[:,2]=((vals>>10)&31)*255//31
    pal[:,3]=255; pal[0,3]=0
    return pal

# ---------- fixed v2 overlap ----------
coords=[]; ws=[]
for ty in range(64):
    y0=ty*1.25; y1=(ty+1)*1.25
    for tx in range(64):
        x0=tx*1.25; x1=(tx+1)*1.25
        cc=[]; ww=[]
        for sy in range(int(y0),int(math.ceil(y1))):
            oy=max(0.0,min(y1,sy+1)-max(y0,sy))
            for sx in range(int(x0),int(math.ceil(x1))):
                ox=max(0.0,min(x1,sx+1)-max(x0,sx))
                if ox>0 and oy>0: cc.append((sy,sx)); ww.append(ox*oy)
        while len(cc)<4: cc.append(cc[-1]); ww.append(0.0)
        coords.append(cc[:4]); ws.append(ww[:4])
coords=np.array(coords,np.int16); ws=np.array(ws,np.float32)
CY=coords[:,:,0]; CX=coords[:,:,1]

def v2(idx80):
    counts=np.bincount(idx80.ravel(),minlength=16).astype(np.float32)
    nz=counts[1:][counts[1:]>0]; maxc=float(nz.max()) if len(nz) else 1.0
    rarity=np.ones(16,np.float32); mask=counts>0; rarity[mask]=(maxc/counts[mask])**0.08
    cand=idx80[CY,CX]
    eq=(cand[:,:,None]==cand[:,None,:])
    score=(eq*ws[:,None,:]).sum(axis=2)*rarity[cand]
    opaque=(ws*(cand!=0)).sum(axis=1)>=0.78125
    score[(opaque[:,None]) & (cand==0)] = -1e9
    pick=np.argmax(score,axis=1)
    return cand[np.arange(4096),pick].reshape(64,64).astype(np.uint8)

# ---------- forms ----------
SPECIES_IDS={'PICHU':172,'UNOWN':201,'CASTFORM':351,'DEOXYS':386,'BURMY':412,'WORMADAM':413,'CHERRIM':421,
             'SHELLOS':422,'GASTRODON':423,'ROTOM':479,'GIRATINA':487,'SHAYMIN':492,'ARCEUS':493,'EGG':494}
UNOWN=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')+['!','?']

def specs(kind):
    out=[]
    def add(name,count,cf,pf,labels=None,note=''):
        for f in range(count): out.append((name,f,cf,pf,labels[f] if labels else '',note))
    if kind=='DP':
        add('DEOXYS',4,lambda s,f:s+f*2,lambda sh,f:0x86+sh,['Normal','Attack','Defense','Speed'])
        add('UNOWN',28,lambda s,f:8+s+f*2,lambda sh,f:0x88+sh,UNOWN)
        add('CASTFORM',4,lambda s,f:0x40+s*4+f,lambda sh,f:0x8A+sh*4+f)
        add('BURMY',3,lambda s,f:0x48+s+f*2,lambda sh,f:0x92+sh+f*2)
        add('WORMADAM',3,lambda s,f:0x4E+s+f*2,lambda sh,f:0x98+sh+f*2)
        add('SHELLOS',2,lambda s,f:0x54+s*2+f,lambda sh,f:0x9E+sh+f*2)
        add('GASTRODON',2,lambda s,f:0x58+s*2+f,lambda sh,f:0xA2+sh+f*2)
        add('CHERRIM',2,lambda s,f:0x5C+s*2+f,lambda sh,f:0xA6+sh*2+f)
        add('ARCEUS',18,lambda s,f:0x60+s+f*2,lambda sh,f:0xAA+sh+f*2,note='form IDs 0..17 preserved including reserved/unused type-form slot')
        add('EGG',2,lambda s,f:0x84+f,lambda sh,f:0xCE+f,['Egg','Manaphy Egg'])
    elif kind=='PT':
        add('DEOXYS',4,lambda s,f:s+f*2,lambda sh,f:154+sh,['Normal','Attack','Defense','Speed'])
        add('UNOWN',28,lambda s,f:8+s+f*2,lambda sh,f:156+sh,UNOWN)
        add('CASTFORM',4,lambda s,f:64+s*4+f,lambda sh,f:158+sh*4+f)
        add('BURMY',3,lambda s,f:72+s+f*2,lambda sh,f:166+sh+f*2)
        add('WORMADAM',3,lambda s,f:78+s+f*2,lambda sh,f:172+sh+f*2)
        add('SHELLOS',2,lambda s,f:84+s*2+f,lambda sh,f:178+sh+f*2)
        add('GASTRODON',2,lambda s,f:88+s*2+f,lambda sh,f:182+sh+f*2)
        add('CHERRIM',2,lambda s,f:92+s*2+f,lambda sh,f:186+sh*2+f)
        add('ARCEUS',18,lambda s,f:96+s+f*2,lambda sh,f:190+sh+f*2,note='form IDs 0..17 preserved including reserved/unused type-form slot')
        add('EGG',2,lambda s,f:132+f,lambda sh,f:226+f,['Egg','Manaphy Egg'])
        add('SHAYMIN',2,lambda s,f:134+s+f*2,lambda sh,f:228+sh+f*2,['Land','Sky'])
        add('ROTOM',6,lambda s,f:138+s+f*2,lambda sh,f:232+sh+f*2)
        add('GIRATINA',2,lambda s,f:150+s+f*2,lambda sh,f:244+sh+f*2,['Altered','Origin'])
    else:
        add('DEOXYS',4,lambda s,f:s+f*2,lambda sh,f:0x9E+sh,['Normal','Attack','Defense','Speed'])
        add('UNOWN',28,lambda s,f:8+s+f*2,lambda sh,f:0xA0+sh,UNOWN)
        add('CASTFORM',4,lambda s,f:0x40+s*4+f,lambda sh,f:0xA2+sh*4+f)
        add('BURMY',3,lambda s,f:0x48+s+f*2,lambda sh,f:0xAA+sh+f*2)
        add('WORMADAM',3,lambda s,f:0x4E+s+f*2,lambda sh,f:0xB0+sh+f*2)
        add('SHELLOS',2,lambda s,f:0x54+s*2+f,lambda sh,f:0xB6+sh+f*2)
        add('GASTRODON',2,lambda s,f:0x58+s*2+f,lambda sh,f:0xBA+sh+f*2)
        add('CHERRIM',2,lambda s,f:0x5C+s*2+f,lambda sh,f:0xBE+sh*2+f)
        add('ARCEUS',18,lambda s,f:0x60+s+f*2,lambda sh,f:0xC2+sh+f*2,note='form IDs 0..17 preserved including reserved/unused type-form slot')
        add('EGG',2,lambda s,f:0x84+f,lambda sh,f:0xE6+f,['Egg','Manaphy Egg'])
        add('SHAYMIN',2,lambda s,f:0x86+s+f*2,lambda sh,f:0xE8+sh+f*2,['Land','Sky'])
        add('ROTOM',6,lambda s,f:0x8A+s+f*2,lambda sh,f:0xEC+sh+f*2)
        add('GIRATINA',2,lambda s,f:0x96+s+f*2,lambda sh,f:0xF8+sh+f*2,['Altered','Origin'])
        add('PICHU',2,lambda s,f:0x9A+s+f*2,lambda sh,f:0xFC+sh+f*2,['Normal','Spiky-eared'])
    return out

# ---------- assets ----------
manifest=[]; arch_rows=[]; other_inv=[]; aliases=[]
asset_hash_to_id={}; asset_bytes=[]; asset_meta=[]
render_cache={}; decode_cache={}; palette_cache={}

def asset_id(rgba):
    h=hashlib.sha256(rgba.tobytes()).hexdigest()
    if h in asset_hash_to_id: return asset_hash_to_id[h]
    aid=len(asset_bytes); asset_hash_to_id[h]=aid
    asset_bytes.append(rgba.tobytes())
    ys,xs=np.where(rgba[:,:,3]>0)
    bb='' if len(xs)==0 else f'{int(xs.min())},{int(ys.min())},{int(xs.max())},{int(ys.max())}'
    asset_meta.append({'asset_id':aid,'sha256':h,'bbox':bb})
    return aid

def get_char(setid,archname,idx,members):
    key=(setid,archname,idx)
    if key not in decode_cache:
        full=ncgr_idx(members[idx]); decode_cache[key]=(v2(full[:,:80]),v2(full[:,80:]))
    return decode_cache[key]

def get_pal(setid,archname,idx,members):
    key=(setid,archname,idx)
    if key not in palette_cache: palette_cache[key]=nclr(members[idx])
    return palette_cache[key]

def get_render(setid,archname,ci,pi,frame,members):
    key=(setid,archname,ci,pi,frame)
    if key in render_cache: return render_cache[key]
    idx64=get_char(setid,archname,ci,members)[frame]; pal=get_pal(setid,archname,pi,members)
    aid=asset_id(pal[idx64]); render_cache[key]=aid; return aid

def addrow(setid,atype,sid,sname,form,label,side,gender,frame,pname,ci,pi,status,members,note=''):
    aid=get_render(setid,atype,ci,pi,frame,members)
    am=asset_meta[aid]; bb=am['bbox']
    if bb:
        l,t,r,b=map(int,bb.split(',')); yoff=63-b; cw=((r-l+8)//8)*8; ch=((b-t+8)//8)*8
    else: yoff=''; cw=''; ch=''
    manifest.append({'source_set':setid,'archive_type':atype,'species_id':sid,'species_name':sname,'form_id':form,'form_label':label,
                     'side':side,'gender':gender,'frame':frame,'palette':pname,'character_member':ci,'palette_member':pi,
                     'source_status':status,'asset_id':aid,'asset_sha256':am['sha256'],'target64_bbox':bb,
                     'MON_COORDS_width_candidate':cw,'MON_COORDS_height_candidate':ch,'y_offset_candidate':yoff,'notes':note})

t0=time.time()
for setid,cfg in ROMSETS.items():
    print('processing',setid,flush=True)
    rd=open(cfg['rom'],'rb').read(); fs=nds_files(rd)
    mb=fs[cfg['main_path']]; ob=fs[cfg['other_path']]
    main=narc_members(mb); other=narc_members(ob)
    arch_rows.append({'source_set':setid,'archive':'main','path':cfg['main_path'],'bytes':len(mb),'members':len(main),'sha256':hashlib.sha256(mb).hexdigest()})
    arch_rows.append({'source_set':setid,'archive':'other','path':cfg['other_path'],'bytes':len(ob),'members':len(other),'sha256':hashlib.sha256(ob).hexdigest()})
    for species in range(494):
        b=species*6
        if b+5>=len(main) or main[b+4][:4]!=b'RLCN': continue
        for side,fslt,mslt in [('back',0,1),('front',2,3)]:
            f_ok=main[b+fslt][:4]==b'RGCN'; m_ok=main[b+mslt][:4]==b'RGCN'
            if not m_ok and not f_ok: continue
            for gender in ['female','male']:
                if gender=='female' and f_ok: ci=b+fslt; status='actual_female_slot'
                elif gender=='female' and m_ok: ci=b+mslt; status='alias_shared_slot'
                elif gender=='male' and m_ok: ci=b+mslt; status='actual_male_or_shared_slot'
                else: continue
                for frame in (0,1):
                    addrow(setid,'main',species,'',0,'',side,gender,frame,'normal',ci,b+4,status,main)
                    addrow(setid,'main',species,'',0,'',side,gender,frame,'shiny',ci,b+5,status,main)
    refc=set(); refp=set()
    for name,form,cf,pf,label,note in specs(cfg['kind']):
        sid=SPECIES_IDS.get(name,'')
        for side,sidx in [('back',0),('front',1)]:
            ci=cf(sidx,form)
            if ci>=len(other) or other[ci][:4]!=b'RGCN': continue
            refc.add(ci)
            for sh,pname in [(0,'normal'),(1,'shiny')]:
                pi=pf(sh,form)
                if pi>=len(other) or other[pi][:4]!=b'RLCN': continue
                refp.add(pi)
                for frame in (0,1): addrow(setid,'other_form',sid,name,form,label,side,'none',frame,pname,ci,pi,'source_code_referenced',other,note)
    for i,m in enumerate(other):
        typ='RGCN' if m[:4]==b'RGCN' else ('RLCN' if m[:4]==b'RLCN' else ('EMPTY' if not m else m[:4].hex()))
        other_inv.append({'source_set':setid,'member':i,'type':typ,'bytes':len(m),'sha256':hashlib.sha256(m).hexdigest(),'source_code_referenced':(i in refc or i in refp)})

for game,rp in GAME_ROMS.items():
    rd=open(rp,'rb').read(); setid='DP_US' if game.startswith('Pokemon D') or game.startswith('Pokemon P') and 'Platinum' not in game else ('PT_KOR' if 'Platinum' in game else 'HGSS_KOR')
    if 'HeartGold' in game or 'SoulSilver' in game: setid='HGSS_KOR'
    aliases.append({'game':game,'source_set':setid,'game_code':rd[12:16].decode('ascii'),'rom_sha256':hashlib.sha256(rd).hexdigest()})

def write_csv(path,rows):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
write_csv(os.path.join(OUTDIR,'logical_slots.csv'),manifest)
write_csv(os.path.join(OUTDIR,'asset_index.csv'),asset_meta)
write_csv(os.path.join(OUTDIR,'archive_hashes.csv'),arch_rows)
write_csv(os.path.join(OUTDIR,'otherpoke_member_inventory.csv'),other_inv)
write_csv(os.path.join(OUTDIR,'game_aliases.csv'),aliases)

COLS=32; ROWS=16; PER=COLS*ROWS
atlas_map=[]
for page,start in enumerate(range(0,len(asset_bytes),PER)):
    n=min(PER,len(asset_bytes)-start)
    canvas=np.zeros((ROWS*64,COLS*64,4),dtype=np.uint8)
    for j in range(n):
        aid=start+j; r=j//COLS; c=j%COLS
        rgba=np.frombuffer(asset_bytes[aid],dtype=np.uint8).reshape(64,64,4)
        canvas[r*64:(r+1)*64,c*64:(c+1)*64]=rgba
        atlas_map.append({'asset_id':aid,'atlas_page':page,'cell_index':j,'cell_x':c,'cell_y':r,'pixel_x':c*64,'pixel_y':r*64})
    Image.fromarray(canvas,'RGBA').save(os.path.join(OUTDIR,f'atlas_{page:03d}.png'),compress_level=1)
write_csv(os.path.join(OUTDIR,'atlas_map.csv'),atlas_map)

summary={
 'scope':'Generation IV Pokemon battle sprites: DP, Platinum, HGSS',
 'logical_slot_records':len(manifest),
 'unique_target64_assets':len(asset_bytes),
 'atlas_pages':math.ceil(len(asset_bytes)/PER),
 'otherpoke_members_inventoried':len(other_inv),
 'conversion':'80x80 NCGR -> 64x64 preservation-v2 using source palette indices only; no AA/new colors',
 'dedupe':'global SHA-256 of 64x64 RGBA',
 'archive_hashes':arch_rows,
 'elapsed_seconds':round(time.time()-t0,2),
}
with open(os.path.join(OUTDIR,'summary.json'),'w',encoding='utf-8') as f: json.dump(summary,f,ensure_ascii=False,indent=2)
with open(os.path.join(OUTDIR,'README.md'),'w',encoding='utf-8') as f:
    f.write('# Generation IV battle sprite master v1\n\n')
    f.write('- DP / Platinum / HGSS active battle sprite archives\n- species 0..493 base slots\n- front/back, logical gender, frame 0/1, normal/shiny\n- all source-code-addressed alternate forms\n- duplicate rendered assets merged by SHA-256\n- unreferenced `otherpoke` members inventoried for unused/leftover follow-up\n- no generative image tools; no antialiasing; no new colors\n')
    f.write('\nSee `logical_slots.csv`, `asset_index.csv`, `atlas_map.csv`, and `archive_hashes.csv`.\n')

shutil.copy('/tmp/build_gen4_sprite_master.py',os.path.join(OUTDIR,'build_gen4_sprite_master.py'))

zip_path='/mnt/data/gen4_battle_sprite_master_v1.zip'
if os.path.exists(zip_path): os.remove(zip_path)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for fn in sorted(os.listdir(OUTDIR)):
        z.write(os.path.join(OUTDIR,fn),arcname=fn)
with zipfile.ZipFile(zip_path,'r') as z:
    bad=z.testzip()
    if bad: raise RuntimeError('bad zip '+bad)
summary['zip_sha256']=hashlib.sha256(open(zip_path,'rb').read()).hexdigest(); summary['zip_bytes']=os.path.getsize(zip_path)
with open(os.path.join(OUTDIR,'summary.json'),'w',encoding='utf-8') as f: json.dump(summary,f,ensure_ascii=False,indent=2)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for fn in sorted(os.listdir(OUTDIR)): z.write(os.path.join(OUTDIR,fn),arcname=fn)
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('ZIP',zip_path)
