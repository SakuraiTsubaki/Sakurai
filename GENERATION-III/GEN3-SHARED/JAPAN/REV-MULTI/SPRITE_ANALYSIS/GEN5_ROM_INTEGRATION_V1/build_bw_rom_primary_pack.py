#!/usr/bin/env python3
from pathlib import Path
import struct, hashlib, json, math
from collections import defaultdict, deque
import numpy as np

BW_NARC=Path('/mnt/data/bw_a_0_0_4.narc')
NCER_PATH=Path('/mnt/data/bw-pokemon.ncer')
OUT=Path('/mnt/data/gen5_bw_rom_primary_pack')
OUT.mkdir(exist_ok=True)

NARC=BW_NARC.read_bytes(); p=0x10; chunks=[]
for _ in range(3):
    tag=NARC[p:p+4]; sz=struct.unpack_from('<I',NARC,p+4)[0]; chunks.append((tag,p,sz)); p+=sz
FP=[x[1] for x in chunks if x[0]==b'BTAF'][0]
IP=[x[1] for x in chunks if x[0]==b'GMIF'][0]
BASE=IP+8
COUNT=struct.unpack_from('<H',NARC,FP+8)[0]
def member(i):
    s,e=struct.unpack_from('<II',NARC,FP+12+i*8); return NARC[BASE+s:BASE+e]

def lz11(src):
    if not src or src[0]!=0x11:return src
    size=src[1]|(src[2]<<8)|(src[3]<<16); pos=4
    if size==0:size=struct.unpack_from('<I',src,pos)[0];pos+=4
    out=bytearray()
    while len(out)<size:
        flags=src[pos];pos+=1
        for bit in range(7,-1,-1):
            if len(out)>=size: break
            if not(flags&(1<<bit)):
                out.append(src[pos]);pos+=1;continue
            b1=src[pos];pos+=1;hi=b1>>4
            if hi==0:
                b2,b3=src[pos],src[pos+1];pos+=2;ln=((b1&15)<<4|(b2>>4))+0x11;disp=((b2&15)<<8)|b3
            elif hi==1:
                b2,b3,b4=src[pos],src[pos+1],src[pos+2];pos+=3;ln=((b1&15)<<12|b2<<4|(b3>>4))+0x111;disp=((b3&15)<<8)|b4
            else:
                b2=src[pos];pos+=1;ln=hi+1;disp=((b1&15)<<8)|b2
            cp=len(out)-disp-1
            if cp<0: raise ValueError('bad LZ11 displacement')
            for _ in range(ln):
                if len(out)>=size:break
                out.append(out[cp]);cp+=1
    return bytes(out)

OBJ_SIZES={(0,0):(8,8),(0,1):(16,8),(0,2):(8,16),(1,0):(16,16),(1,1):(32,8),(1,2):(8,32),(2,0):(32,32),(2,1):(32,16),(2,2):(16,32),(3,0):(64,64),(3,1):(64,32),(3,2):(32,64)}
NCER=NCER_PATH.read_bytes(); OBJS=[]
for j in range(4):
    a0,a1,a2=struct.unpack_from('<HHH',NCER,0x38+j*6)
    y=a0&0xff; y=y-256 if y>=128 else y; shape=(a0>>14)&3
    x=a1&0x1ff; x=x-512 if x>=256 else x; size=(a1>>14)&3
    tile=a2&0x3ff
    OBJS.append((x,y,shape,size,tile))

def ncgr_info(data):
    d=lz11(data); assert d[:4]==b'RGCN'; pos=0x10; assert d[pos:pos+4]==b'RAHC'
    wt,ht=struct.unpack_from('<HH',d,pos+8); bdepth=struct.unpack_from('<I',d,pos+0xc)[0]
    vram=struct.unpack_from('<I',d,pos+0x10)[0]; tiled=struct.unpack_from('<I',d,pos+0x14)[0]
    datasz=struct.unpack_from('<I',d,pos+0x18)[0]; off=pos+0x20
    if datasz==0 or off+datasz>len(d):datasz=len(d)-off
    assert bdepth==3
    return wt*8,ht*8,vram,tiled,d[off:off+datasz]

def cell_pixels(data,vram,tiled,tile,w,h):
    if (tiled&0xff)!=0: raise NotImplementedError('static BW NCGR expected tiled==0')
    boundary=5 if (vram&0x10)==0 else 5+((vram>>20)&3)
    start_pix=(tile<<boundary)*2; sb=start_pix//2
    unpack=np.empty(w*h,dtype=np.uint8)
    raw=data[sb:sb+(w*h)//2]
    if len(raw)!=(w*h)//2: raise ValueError('cell overrun')
    a=np.frombuffer(raw,dtype=np.uint8)
    unpack[0::2]=a&15;unpack[1::2]=a>>4
    raster=np.zeros((h,w),dtype=np.uint8); k=0
    for ty in range(h//8):
        for tx in range(w//8):
            raster[ty*8:ty*8+8,tx*8:tx*8+8]=unpack[k:k+64].reshape(8,8);k+=64
    return raster

def render_indices(species,side):
    base=species*20; gi=base+(0 if side=='front' else 9)
    W,H,vram,tiled,data=ncgr_info(member(gi))
    out=np.zeros((H,W),dtype=np.uint8)
    for x0,y0,shape,size,tile in OBJS:
        w,h=OBJ_SIZES[(size,shape)]; cell=cell_pixels(data,vram,tiled,tile,w,h)
        for y in range(h):
            yy=y0+y
            if not(0<=yy<H):continue
            for x in range(w):
                xx=x0+x
                if not(0<=xx<W):continue
                if out[yy,xx]==0:out[yy,xx]=cell[y,x]
    return out

def nclr_raw(species,shiny):
    d=member(species*20+(19 if shiny else 18)); assert d[:4]==b'RLCN';pos=0x10;assert d[pos:pos+4]==b'TTLP'
    sz=struct.unpack_from('<I',d,pos+0x10)[0];off=pos+0x18
    if sz==0 or off+sz>len(d):off=0x28;sz=len(d)-off
    raw=d[off:off+sz]
    if len(raw)<32: raw=raw+b'\0'*(32-len(raw))
    return raw[:32]

TARGET=64; RARITY_EXPONENT=.08; FORCE=.50

def make_overlap(sh,sw):
    rows=[];wrows=[];maxk=0
    for oy in range(TARGET):
        sy0=oy*sh/TARGET; sy1=(oy+1)*sh/TARGET
        for ox in range(TARGET):
            sx0=ox*sw/TARGET; sx1=(ox+1)*sw/TARGET;cc=[];ww=[]
            for sy in range(max(0,int(math.floor(sy0))),min(sh,int(math.ceil(sy1)))):
                wy=max(0.,min(sy1,sy+1)-max(sy0,sy))
                for sx in range(max(0,int(math.floor(sx0))),min(sw,int(math.ceil(sx1)))):
                    wx=max(0.,min(sx1,sx+1)-max(sx0,sx));w=wx*wy
                    if w>0:cc.append((sy,sx));ww.append(w)
            maxk=max(maxk,len(cc));rows.append(cc);wrows.append(ww)
    C=np.zeros((4096,maxk,2),np.int16);W=np.zeros((4096,maxk),np.float64)
    for i,(cc,ww) in enumerate(zip(rows,wrows)):
        for j,((y,x),w) in enumerate(zip(cc,ww)):C[i,j]=(y,x);W[i,j]=w
    return C[:,:,0],C[:,:,1],W,W.sum(axis=1)
CY,CX,OW,OT=make_overlap(96,96)
def resize_v2(src):
    counts=np.bincount(src.ravel(),minlength=max(1,int(src.max())+1)).astype(np.float64);nz=counts[1:][counts[1:]>0];mx=float(nz.max()) if len(nz) else 1.;rar=np.ones_like(counts);m=counts>0;rar[m]=(mx/counts[m])**RARITY_EXPONENT
    if len(rar):rar[0]=1.
    cand=src[CY,CX];eq=(cand[:,:,None]==cand[:,None,:]);scores=(eq*OW[:,None,:]).sum(axis=2)*rar[cand];opaque=(OW*(cand!=0)).sum(axis=1);force=(opaque/np.maximum(OT,1e-12))>=FORCE;scores[force[:,None]&(cand==0)]=-1e30;pick=np.argmax(scores,axis=1);return cand[np.arange(4096),pick].reshape(64,64).astype(np.uint8)

def to_gba4(idx):
    out=bytearray()
    for ty in range(8):
        for tx in range(8):
            flat=idx[ty*8:(ty+1)*8,tx*8:(tx+1)*8].ravel()
            for i in range(0,64,2):out.append(int(flat[i])|(int(flat[i+1])<<4))
    assert len(out)==2048
    return bytes(out)

def lz77(data):
    n=len(data);out=bytearray((0x10,n&255,(n>>8)&255,(n>>16)&255));pos=0;chains=defaultdict(deque)
    def add(p):
        if p+2>=n:return
        q=chains[data[p:p+3]];q.append(p)
        while len(q)>128:q.popleft()
    while pos<n:
        fa=len(out);out.append(0);flags=0;pay=bytearray()
        for bit in range(8):
            if pos>=n:break
            best=0;bp=-1;q=chains.get(data[pos:pos+3]) if pos+2<n else None;checked=0
            if q:
                for cand in reversed(q):
                    disp=pos-cand-1
                    if disp>0xfff:break
                    checked+=1;ln=3;lim=min(18,n-pos)
                    while ln<lim and data[cand+ln]==data[pos+ln]:ln+=1
                    if ln>best:best=ln;bp=cand
                    if ln==18 or checked>=64:break
            if best>=3:
                flags|=1<<(7-bit);disp=pos-bp-1;tok=((best-3)<<12)|disp;pay+=bytes((tok>>8,tok&255));old=pos;pos+=best
                for qpos in range(old,pos):add(qpos)
            else:pay.append(data[pos]);add(pos);pos+=1
        out[fa]=flags;out+=pay
    while len(out)&3:out.append(0)
    return bytes(out)

def lz77dec(blob):
    assert blob[0]==0x10;target=blob[1]|blob[2]<<8|blob[3]<<16;out=bytearray();p=4
    while len(out)<target:
        fl=blob[p];p+=1
        for bit in range(8):
            if len(out)>=target:break
            if fl&(1<<(7-bit)):
                a,b=blob[p],blob[p+1];p+=2;ln=(a>>4)+3;disp=((a&15)<<8)|b;src=len(out)-disp-1
                for _ in range(ln):out.append(out[src]);src+=1
            else:out.append(blob[p]);p+=1
    return bytes(out[:target])

records={}; gfx_unique={}; pal_unique={}; gfx_blobs=[];pal_blobs=[]
for sp in range(1,650):
    rec={}
    for side in ('front','back'):
        idx64=resize_v2(render_indices(sp,side)); raw=to_gba4(idx64); h=hashlib.sha256(raw).hexdigest()
        if h not in gfx_unique:
            comp=lz77(raw); assert lz77dec(comp)==raw; gfx_unique[h]=len(gfx_blobs);gfx_blobs.append((h,comp,raw))
        rec[side]=gfx_unique[h]
    for sh in (False,True):
        raw=nclr_raw(sp,sh);h=hashlib.sha256(raw).hexdigest()
        if h not in pal_unique:
            comp=lz77(raw); assert lz77dec(comp)==raw; pal_unique[h]=len(pal_blobs);pal_blobs.append((h,comp,raw))
        rec['shiny' if sh else 'normal']=pal_unique[h]
    records[sp]=rec
    if sp%100==0:print('built',sp,flush=True)

with (OUT/'records.json').open('w') as f:json.dump(records,f)
for name,blobs in [('gfx',gfx_blobs),('pal',pal_blobs)]:
    pack=bytearray();index=[]
    for i,(h,comp,raw) in enumerate(blobs):
        while len(pack)&3:pack.append(0)
        off=len(pack);pack+=comp;index.append({'id':i,'sha256':h,'offset':off,'compressed_size':len(comp),'raw_size':len(raw)})
    (OUT/f'{name}.pack').write_bytes(pack);(OUT/f'{name}_index.json').write_text(json.dumps(index,indent=2))
summary={'source_narc_sha256':hashlib.sha256(NARC).hexdigest(),'species':649,'front_back_records':1298,'unique_gfx':len(gfx_blobs),'unique_palettes':len(pal_blobs),'gfx_pack_bytes':(OUT/'gfx.pack').stat().st_size,'pal_pack_bytes':(OUT/'pal.pack').stat().st_size,'conversion':'BW ROM /a/0/0/4 static NCGR+NCER -> indexed 96x96 -> preservation-v2 64x64 -> GBA OBJ 4bpp; source palette order preserved','narc_members':COUNT}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
