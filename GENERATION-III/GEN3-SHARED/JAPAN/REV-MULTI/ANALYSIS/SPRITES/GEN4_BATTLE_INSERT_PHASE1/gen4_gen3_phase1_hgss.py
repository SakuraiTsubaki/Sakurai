#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
import struct, hashlib, json, zlib, math
import numpy as np

def nds_files(b):
 fnt_off,fnt_size,fat_off,fat_size=struct.unpack_from('<IIII',b,0x40); fnt=b[fnt_off:fnt_off+fnt_size]
 _,_,ndir=struct.unpack_from('<IHH',fnt,0); dirs=[struct.unpack_from('<IHH',fnt,i*8) for i in range(ndir)]; out={}
 def walk(di,prefix=''):
  sub,fid,_=dirs[di]; p=sub
  while True:
   l=fnt[p];p+=1
   if not l: break
   d=l&0x80; l&=0x7f; name=fnt[p:p+l].decode('ascii','replace');p+=l
   if d:
    child=struct.unpack_from('<H',fnt,p)[0]-0xF000;p+=2;walk(child,prefix+name+'/')
   else:
    s,e=struct.unpack_from('<II',b,fat_off+fid*8);out[prefix+name]=(s,e);fid+=1
 walk(0); return out

def narc(data):
 off=struct.unpack_from('<H',data,0x0c)[0]; fat=img=None
 while off<len(data):
  m=data[off:off+4];sz=struct.unpack_from('<I',data,off+4)[0]
  if m in (b'BTAF',b'FATB'):
   n=struct.unpack_from('<H',data,off+8)[0];fat=[struct.unpack_from('<II',data,off+12+i*8) for i in range(n)]
  elif m in (b'GMIF',b'FIMG'): img=data[off+8:off+sz]
  off+=sz
 return [img[s:e] for s,e in fat]

def ncgr(m):
 if not m or m[:4]!=b'RGCN': return None
 size=struct.unpack_from('<I',m,0x28)[0]; raw=bytearray(m[0x30:0x30+size])
 if len(raw)<2:return None
 state=raw[-2]|raw[-1]<<8
 for i in range(len(raw)-2,-1,-2):
  v=(raw[i]|raw[i+1]<<8)^(state&0xffff);raw[i]=v&255;raw[i+1]=(v>>8)&255;state=(state*0x41C64E6D+0x6073)&0xffffffff
 rb=np.frombuffer(bytes(raw),dtype=np.uint8);p=np.empty(rb.size*2,dtype=np.uint8);p[0::2]=rb&15;p[1::2]=rb>>4
 return p.reshape(80,160) if p.size==12800 else p.reshape(80,80)

def pal(m): return bytes(m[0x28:0x48]) if m and m[:4]==b'RLCN' else None

cc=[];ww=[]
for ty in range(64):
 y0=ty*1.25;y1=(ty+1)*1.25
 for tx in range(64):
  x0=tx*1.25;x1=(tx+1)*1.25;c=[];w=[]
  for sy in range(int(y0),int(math.ceil(y1))):
   oy=max(0,min(y1,sy+1)-max(y0,sy))
   for sx in range(int(x0),int(math.ceil(x1))):
    ox=max(0,min(x1,sx+1)-max(x0,sx))
    if ox and oy:c.append((sy,sx));w.append(ox*oy)
  while len(c)<4:c.append(c[-1]);w.append(0)
  cc.append(c[:4]);ww.append(w[:4])
cc=np.array(cc,dtype=np.int16);ww=np.array(ww);CY=cc[:,:,0];CX=cc[:,:,1]
def shrink(a):
 cnt=np.bincount(a.ravel(),minlength=16).astype(float);nz=cnt[1:][cnt[1:]>0];mx=max(nz) if len(nz) else 1
 rar=np.ones(16);mask=cnt>0;rar[mask]=(mx/cnt[mask])**.08;cand=a[CY,CX];eq=cand[:,:,None]==cand[:,None,:]
 score=(eq*ww[:,None,:]).sum(2)*rar[cand];opaque=(ww*(cand!=0)).sum(1);score[(opaque>=.78125)[:,None]&(cand==0)]=-1e30
 return cand[np.arange(4096),np.argmax(score,1)].reshape(64,64).astype(np.uint8)
def tile(a):
 out=bytearray()
 for ty in range(8):
  for tx in range(8):
   q=a[ty*8:(ty+1)*8,tx*8:(tx+1)*8].ravel();out.extend(int(q[i])|(int(q[i+1])<<4) for i in range(0,64,2))
 return bytes(out)

def lz10(data):
 n=len(data);o=bytearray([0x10,n&255,n>>8&255,n>>16&255]);chains=defaultdict(deque);pos=0
 def add(p):
  if p+2<n:
   q=chains[data[p:p+3]];q.append(p)
   while q and p-q[0]>4096:q.popleft()
 while pos<n:
  fi=len(o);o.append(0);flags=0
  for bit in range(7,-1,-1):
   if pos>=n:break
   best=0;bd=0;q=chains.get(data[pos:pos+3]) if pos+2<n else None
   if q:
    for p0 in reversed(list(q)[-32:]):
     d=pos-p0
     if d<1 or d>4096:continue
     ln=3;ml=min(18,n-pos)
     while ln<ml and data[p0+ln]==data[pos+ln]:ln+=1
     if ln>best:best=ln;bd=d
     if best==18:break
   if best>=3:
    flags|=1<<bit;v=((best-3)<<12)|(bd-1);o.extend([v>>8,v&255])
    for p in range(pos,pos+best):add(p)
    pos+=best
   else:o.append(data[pos]);add(pos);pos+=1
  o[fi]=flags
 while len(o)%4:o.append(0)
 return bytes(o)
def unlz(b,off):
 assert b[off]==0x10;n=b[off+1]|b[off+2]<<8|b[off+3]<<16;p=off+4;o=bytearray()
 while len(o)<n:
  f=b[p];p+=1
  for bit in range(7,-1,-1):
   if len(o)>=n:break
   if f>>bit&1:
    v=b[p]<<8|b[p+1];p+=2;ln=(v>>12)+3;d=(v&4095)+1
    for _ in range(ln):o.append(o[-d])
   else:o.append(b[p]);p+=1
 return bytes(o)

def nat2sid(n):return n if n<=251 else n+25

def sprite_tables(b):
 hits=[];off=0;n=len(b)
 while off+8<=n:
  p,s,t=struct.unpack_from('<IHH',b,off)
  if 0x08000000<=p<0x08000000+n and s==0x800 and t<=1000:
   q=off;r=0
   while q+8<=n:
    p2,s2,t2=struct.unpack_from('<IHH',b,q)
    if not(0x08000000<=p2<0x08000000+n and s2==0x800 and t2<=1000):break
    r+=1;q+=8
   if r>=400:hits.append((off,r));off=q;continue
  off+=4
 return hits
def palette_table(b):
 n=len(b)
 for off in range(0,n-8,4):
  q=off;r=0
  while q+8<=n:
   p,t,x=struct.unpack_from('<IHH',b,q)
   if not(0x08000000<=p<0x08000000+n and t<=1000 and x==0):break
   r+=1;q+=8
  if r>=800:return off,r
 raise RuntimeError('palette table')
def nextpow2(n):return 1<<(n-1).bit_length()

def ips32(src,tgt):
 out=bytearray(b'IPS32');i=0
 while i<len(tgt):
  if i<len(src) and tgt[i]==src[i]:i+=1;continue
  v=tgt[i];j=i+1
  while j<len(tgt) and tgt[j]==v and (j-i)<65535 and not (j<len(src) and tgt[j]==src[j]):j+=1
  if j-i>=16:
   out+=i.to_bytes(4,'big')+b'\x00\x00'+(j-i).to_bytes(2,'big')+bytes([v]);i=j;continue
  j=i+1
  while j<len(tgt) and (j-i)<65535:
   if j<len(src) and tgt[j]==src[j]:break
   if j+16<=len(tgt) and len(set(tgt[j:j+16]))==1:break
   j+=1
  out+=i.to_bytes(4,'big')+(j-i).to_bytes(2,'big')+tgt[i:j];i=j
 out+=b'EEOF';return bytes(out)

HG='/mnt/data/포켓몬스터 하트골드.nds';b=Path(HG).read_bytes();fs=nds_files(b);s,e=fs['pbr/pokegra.narc'];m=narc(b[s:e])
gfx={};pals={}
for sp in range(1,494):
 base=sp*6;pals[(sp,0)]=pal(m[base+4]);pals[(sp,1)]=pal(m[base+5])
 for side,idx in [(0,3),(1,1)]:
  a=ncgr(m[base+idx])
  if a is None or not np.any(a):a=ncgr(m[base+(2 if side==0 else 0)])
  frames=a.shape[1]//80
  for fr in (0,1):gfx[(sp,side,fr)]=tile(shrink(a[:,min(fr,frames-1)*80:min(fr,frames-1)*80+80]))

header=64;gt_off=header;gt_n=494*2*2;pt_off=gt_off+gt_n*4;pt_n=494*2;data_off=(pt_off+pt_n*4+15)&~15
bank=bytearray(data_off);bank[:8]=b'G4G3HG1\0';struct.pack_into('<IIIIII',bank,8,493,gt_off,gt_n,pt_off,pt_n,data_off);bank[40:64]=hashlib.sha256(b).digest()[:24]
ug={};up={};gh={};ph={}
for k,r in gfx.items():h=hashlib.sha256(r).digest();gh[k]=h;ug.setdefault(h,r)
for k,r in pals.items():h=hashlib.sha256(r).digest();ph[k]=h;up.setdefault(h,r)
go={}
for h,r in ug.items():go[h]=len(bank);bank.extend(lz10(r))
po={}
for h,r in up.items():po[h]=len(bank);bank.extend(lz10(r))
while len(bank)%16:bank.append(0xff)
for sp in range(1,494):
 for side in (0,1):
  for fr in (0,1):struct.pack_into('<I',bank,gt_off+(((sp*2+side)*2+fr)*4),go[gh[(sp,side,fr)]])
 for sh in (0,1):struct.pack_into('<I',bank,pt_off+((sp*2+sh)*4),po[ph[(sp,sh)]])
def grel(sp,side,fr):return struct.unpack_from('<I',bank,gt_off+(((sp*2+side)*2+fr)*4))[0]
def prel(sp,sh):return struct.unpack_from('<I',bank,pt_off+((sp*2+sh)*4))[0]

targets=[('RUBY_JP_REV0','/mnt/data/Pocket Monsters - Ruby (Japan).gba'),('SAPPHIRE_JP_REV0','/mnt/data/Pocket Monsters - Sapphire (Japan).gba'),('EMERALD_JP_REV0','/mnt/data/Pocket Monsters - Emerald (Japan).gba'),('FIRERED_JP_REV1','/mnt/data/Pocket Monsters - Fire Red (Japan) (Rev 1).gba'),('LEAFGREEN_JP_REV0','/mnt/data/Pocket Monsters - Leaf Green (Japan).gba')]
outdir=Path('/mnt/data/gen4_to_gen3_phase1_hgss');outdir.mkdir(exist_ok=True);(outdir/'HGSS_BASE_001_493.bank').write_bytes(bank);reports=[]
for label,path in targets:
 src=Path(path).read_bytes();rom=bytearray(src);st=sprite_tables(src);poff,_=palette_table(src)
 if label.startswith('EMERALD'):front,back,anim=st[0][0],st[1][0],st[2][0]
 else:front,back,anim=st[0][0],st[1][0],None
 bs=(len(rom)+0xff)&~0xff;rom.extend(b'\xff'*(bs-len(rom)));rom.extend(bank);ba=0x08000000+bs;animptr={}
 if anim is not None:
  for nat in range(1,387):animptr[nat]=0x08000000+len(rom);rom.extend(lz10(gfx[(nat,0,0)]+gfx[(nat,0,1)]))
 for nat in range(1,387):
  sid=nat2sid(nat);struct.pack_into('<I',rom,front+sid*8,ba+grel(nat,0,0));struct.pack_into('<I',rom,back+sid*8,ba+grel(nat,1,0));struct.pack_into('<I',rom,poff+sid*8,ba+prel(nat,0));struct.pack_into('<I',rom,poff+(440+sid)*8,ba+prel(nat,1))
  if anim is not None:struct.pack_into('<I',rom,anim+sid*8,animptr[nat])
 tr=len(rom);rom+=b'G4G3PH1\0'+struct.pack('<II',bs,tr)+hashlib.sha256(src).digest()+hashlib.sha256(bank).digest();final=min(max(nextpow2(len(rom)),len(src)),32*1024*1024);rom.extend(b'\xff'*(final-len(rom)))
 bad=[]
 for nat in range(1,387):
  sid=nat2sid(nat)
  for toff,expect in [(front,2048),(back,2048)]+([] if anim is None else [(anim,4096)]):
   ptr=struct.unpack_from('<I',rom,toff+sid*8)[0]
   if len(unlz(rom,ptr-0x08000000))!=expect:bad.append([nat,hex(toff)])
  for tab in (0,440):
   ptr=struct.unpack_from('<I',rom,poff+(tab+sid)*8)[0]
   if len(unlz(rom,ptr-0x08000000))!=32:bad.append([nat,'pal'])
 (outdir/(label+'.work.gba')).write_bytes(rom);patch=ips32(src,bytes(rom));(outdir/(label+'.ips32')).write_bytes(patch)
 rep={'target':label,'source_sha256':hashlib.sha256(src).hexdigest(),'work_sha256':hashlib.sha256(rom).hexdigest(),'source_size':len(src),'work_size':len(rom),'ips32_bytes':len(patch),'sprite_tables':st,'front_table':hex(front),'back_table':hex(back),'animated_front_table':None if anim is None else hex(anim),'palette_table':hex(poff),'bank_offset':hex(bs),'bank_bytes':len(bank),'active_default':'HGSS male/shared, f0; Emerald animated front uses f0+f1','active_species':386,'embedded_hgss_species':493,'old_unown_252_276_untouched':True,'verification_errors':bad};(outdir/(label+'.json')).write_text(json.dumps(rep,indent=2));reports.append(rep)
(outdir/'SUMMARY.json').write_text(json.dumps({'phase':'PHASE1_HGSS_PLAYABLE_REDIRECT','hgss_sha256':hashlib.sha256(b).hexdigest(),'bank':{'bytes':len(bank),'unique_gfx':len(ug),'unique_palettes':len(up),'species':493,'frames':'front/back f0/f1','palette':'normal/shiny'},'targets':reports,'not_yet_active':'National Dex 387-493 requires species-table expansion; female/gender switching, DP/Pt version selection, alternate forms, and Gen IV animation scripting are next phases.'},indent=2))
