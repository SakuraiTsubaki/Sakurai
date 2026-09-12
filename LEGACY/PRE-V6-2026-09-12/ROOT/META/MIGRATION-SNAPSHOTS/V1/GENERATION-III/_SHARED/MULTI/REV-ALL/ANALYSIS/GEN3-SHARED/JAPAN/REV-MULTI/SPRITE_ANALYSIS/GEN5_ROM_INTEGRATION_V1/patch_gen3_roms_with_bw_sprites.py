#!/usr/bin/env python3
from pathlib import Path
import struct, json, hashlib, math

ROOT=Path('/mnt/data')
PACK=ROOT/'gen5_bw_rom_primary_pack'
RECORDS={int(k):v for k,v in json.loads((PACK/'records.json').read_text()).items()}
GFXPACK=(PACK/'gfx.pack').read_bytes(); PALPACK=(PACK/'pal.pack').read_bytes()
GFXIDX=json.loads((PACK/'gfx_index.json').read_text()); PALIDX=json.loads((PACK/'pal_index.json').read_text())
OUTDIR=ROOT/'gen3_gen5_sprite_roms';OUTDIR.mkdir(exist_ok=True)
MAN=[]

def sha1(b):return hashlib.sha1(b).hexdigest()
def sha256(b):return hashlib.sha256(b).hexdigest()
def align(buf,n=4,fill=0xff):
    while len(buf)%n:buf.append(fill)

def next_pow2(n):
    p=1
    while p<n:p<<=1
    return p

def scan_candidates(b):
    sprites=[];pals=[];shiny=[];n=len(b)
    for o in range(0,n-80,4):
        ptr,a,c=struct.unpack_from('<IHH',b,o)
        if a==0x800 and c==0 and 0x08000000<=ptr<0x0A000000:
            ok=True
            for i in range(1,8):
                p2,a2,c2=struct.unpack_from('<IHH',b,o+8*i)
                if a2!=0x800 or c2!=i or not(0x08000000<=p2<0x0A000000):ok=False;break
            if ok:sprites.append(o)
        if a==0 and c==0 and 0x08000000<=ptr<0x0A000000:
            ok=True
            for i in range(1,8):
                p2,t,pad=struct.unpack_from('<IHH',b,o+8*i)
                if t!=i or pad!=0 or not(0x08000000<=p2<0x0A000000):ok=False;break
            if ok:pals.append(o)
        if a==500 and c==0 and 0x08000000<=ptr<0x0A000000:
            ok=True
            for i in range(1,8):
                p2,t,pad=struct.unpack_from('<IHH',b,o+8*i)
                if t!=500+i or pad!=0 or not(0x08000000<=p2<0x0A000000):ok=False;break
            if ok:shiny.append(o)
    return sprites,pals,shiny

def detect_tables(b):
    code=b[0xAC:0xB0].decode('ascii','replace')
    if code.startswith(('BPE','BPR','BPG')):
        vals=[struct.unpack_from('<I',b,o)[0]-0x08000000 for o in (0x128,0x12c,0x130,0x134)]
        if all(0<=x<len(b)-440*8 for x in vals):
            return dict(front=vals[0],back=vals[1],pal=vals[2],shiny=vals[3],method='gf_header')
    sprites,pals,shin=scan_candidates(b)
    sprites=[x for x in sprites if x<0x300000]
    if len(sprites)<2 or not pals or not shin:raise RuntimeError(f'cannot detect tables for {code}')
    front,back=sprites[0],sprites[1]
    pal=min([x for x in pals if x>back],key=lambda x:x-back)
    shiny=min([x for x in shin if x>pal],key=lambda x:x-pal)
    return dict(front=front,back=back,pal=pal,shiny=shiny,method='signature_scan')

def nat_to_internal(n):
    if 1<=n<=251:return n
    if 252<=n<=386:return n+25
    if 387<=n<=649:return n+53
    raise ValueError(n)

def map_table_references(buf, old_off, new_off, old_count=440):
    old_base=0x08000000+old_off;new_base=0x08000000+new_off;end=old_base+old_count*8
    hits=[]
    for o in range(0,len(buf)-3,4):
        v=struct.unpack_from('<I',buf,o)[0]
        if old_base<=v<end and ((v-old_base)&7)==0:
            nv=new_base+(v-old_base);struct.pack_into('<I',buf,o,nv);hits.append((o,v,nv))
    return hits

def patch_rom(path):
    orig=path.read_bytes();tables=detect_tables(orig);buf=bytearray(orig);orig_len=len(buf)
    align(buf,4);gfx_base=len(buf);buf+=GFXPACK
    align(buf,4);pal_base=len(buf);buf+=PALPACK
    align(buf,4);front_new=len(buf);buf+=b'\0'*(703*8)
    back_new=len(buf);buf+=b'\0'*(703*8)
    pal_new=len(buf);buf+=b'\0'*(703*8)
    shiny_new=len(buf);buf+=b'\0'*(703*8)
    for key,noff in [('front',front_new),('back',back_new),('pal',pal_new),('shiny',shiny_new)]:
        old=tables[key];buf[noff:noff+440*8]=orig[old:old+440*8]
    def gfxptr(gid):return 0x08000000+gfx_base+GFXIDX[gid]['offset']
    def palptr(pid):return 0x08000000+pal_base+PALIDX[pid]['offset']
    for nat in range(1,387):
        iid=nat_to_internal(nat);r=RECORDS[nat]
        struct.pack_into('<IHH',buf,front_new+iid*8,gfxptr(r['front']),0x800,iid)
        struct.pack_into('<IHH',buf,back_new+iid*8,gfxptr(r['back']),0x800,iid)
        struct.pack_into('<IHH',buf,pal_new+iid*8,palptr(r['normal']),iid,0)
        struct.pack_into('<IHH',buf,shiny_new+iid*8,palptr(r['shiny']),500+iid,0)
    for nat in range(387,650):
        iid=nat_to_internal(nat);r=RECORDS[nat]
        struct.pack_into('<IHH',buf,front_new+iid*8,gfxptr(r['front']),0x800,iid)
        struct.pack_into('<IHH',buf,back_new+iid*8,gfxptr(r['back']),0x800,iid)
        struct.pack_into('<IHH',buf,pal_new+iid*8,palptr(r['normal']),iid,0)
        struct.pack_into('<IHH',buf,shiny_new+iid*8,palptr(r['shiny']),500+iid,0)
    refs={}
    for key,new_off in [('front',front_new),('back',back_new),('pal',pal_new),('shiny',shiny_new)]:
        refs[key]=map_table_references(buf,tables[key],new_off,440)
    needed=len(buf);final_size=next_pow2(needed)
    if final_size<orig_len:final_size=orig_len
    if final_size>0x2000000:raise RuntimeError(f'patched ROM exceeds 32 MiB: {final_size}')
    buf.extend(b'\xff'*(final_size-len(buf)))
    for iid in list(range(1,252))+list(range(277,412))+list(range(440,703)):
        for noff in (front_new,back_new):
            ptr,size,tag=struct.unpack_from('<IHH',buf,noff+iid*8);assert size==0x800 and tag==iid and 0x08000000<=ptr<0x08000000+len(buf)
        ptr,tag,pad=struct.unpack_from('<IHH',buf,pal_new+iid*8);assert tag==iid and pad==0 and 0x08000000<=ptr<0x08000000+len(buf)
        ptr,tag,pad=struct.unpack_from('<IHH',buf,shiny_new+iid*8);assert tag==500+iid and pad==0 and 0x08000000<=ptr<0x08000000+len(buf)
    for key,noff in [('front',front_new),('back',back_new),('pal',pal_new),('shiny',shiny_new)]:
        assert bytes(buf[noff+412*8:noff+440*8])==orig[tables[key]+412*8:tables[key]+440*8]
    code=orig[0xAC:0xB0].decode('ascii','replace');rev=orig[0xBC]
    stem=path.stem.replace(' ','_').replace('/','_')
    out=OUTDIR/(stem+'_GEN5_64x64_SPRITES.gba');out.write_bytes(buf)
    meta={
      'input':path.name,'game_code':code,'revision':rev,'input_size':orig_len,'output_size':len(buf),
      'input_sha1':sha1(orig),'output_sha1':sha1(buf),'output_sha256':sha256(buf),
      'source_bw_narc_sha256':json.loads((PACK/'summary.json').read_text())['source_narc_sha256'],
      'old_tables':{k:hex(v) for k,v in tables.items() if k!='method'},'table_detection':tables['method'],
      'new_tables':{'front':hex(front_new),'back':hex(back_new),'normal_palette':hex(pal_new),'shiny_palette':hex(shiny_new)},
      'data':{'gfx_pack_offset':hex(gfx_base),'gfx_pack_bytes':len(GFXPACK),'palette_pack_offset':hex(pal_base),'palette_pack_bytes':len(PALPACK)},
      'reference_rewrites':{k:len(v) for k,v in refs.items()},
      'species_mapping':{'nat_1_251':'internal 1..251','nat_252_386':'internal nat+25 = 277..411','vanilla_special_412_439':'preserved byte-for-byte','nat_387_649':'internal nat+53 = 440..702'},
      'runtime_status':'001-386 sprite/palette lookups are redirected immediately; 387-649 assets and expanded tables are physically present, but full new-species gameplay still requires expansion of base stats/names/learnsets/dex/coords/animation and NUM_SPECIES bounds.'
    }
    (OUTDIR/(stem+'_GEN5_64x64_SPRITES.json')).write_text(json.dumps(meta,indent=2,ensure_ascii=False))
    return out,meta

for p in sorted(ROOT.glob('*.gba')):
    if 'GEN5_64x64_SPRITES' in p.name:continue
    out,meta=patch_rom(p);MAN.append(meta);print('PATCHED',p.name,'->',out.name,meta['output_sha1'],meta['reference_rewrites'],flush=True)
(OUTDIR/'MANIFEST.json').write_text(json.dumps(MAN,indent=2,ensure_ascii=False))
print('done',len(MAN))
