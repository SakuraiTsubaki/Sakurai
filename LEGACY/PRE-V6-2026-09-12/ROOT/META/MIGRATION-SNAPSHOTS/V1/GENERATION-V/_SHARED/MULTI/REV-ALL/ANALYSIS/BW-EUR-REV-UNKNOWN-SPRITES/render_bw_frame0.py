import struct, pathlib, math
from PIL import Image
NARC='/mnt/data/bw_pokegra_0004.narc'
OUT=pathlib.Path('/mnt/data/sprite_preserve_trial/rom_reconstructed'); OUT.mkdir(parents=True,exist_ok=True)
D=pathlib.Path(NARC).read_bytes(); pos=0x10; fatsz=struct.unpack_from('<I',D,pos+4)[0]; count=struct.unpack_from('<H',D,pos+8)[0]
fat=[struct.unpack_from('<II',D,pos+12+i*8) for i in range(count)]; pos2=pos+fatsz; pos3=pos2+struct.unpack_from('<I',D,pos2+4)[0]; GB=pos3+8

def lz(d):
 if not d or d[0]!=0x11:return d
 n=d[1]|d[2]<<8|d[3]<<16; si=4; out=bytearray()
 while len(out)<n:
  flags=d[si];si+=1
  for bit in range(7,-1,-1):
   if len(out)>=n: break
   if not(flags>>bit&1): out.append(d[si]);si+=1
   else:
    b1=d[si];si+=1; h=b1>>4
    if h==0:
     b2,b3=d[si:si+2];si+=2; ln=((b1&15)<<4|(b2>>4))+0x11; disp=((b2&15)<<8|b3)+1
    elif h==1:
     b2,b3,b4=d[si:si+3];si+=3; ln=((b1&15)<<12|b2<<4|(b3>>4))+0x111; disp=((b3&15)<<8|b4)+1
    else:
     b2=d[si];si+=1; ln=h+1; disp=((b1&15)<<8|b2)+1
    for _ in range(ln): out.append(out[-disp])
 return bytes(out[:n])
def mem(i):
 s,e=fat[i]; return lz(D[GB+s:GB+e])
def s8(v): return v-256 if v>=128 else v
def s9(v): return v-512 if v>=256 else v
OBJ_SIZES=[[(8,8),(16,8),(8,16),(0,0)],[(16,16),(32,8),(8,32),(0,0)],[(32,32),(32,16),(16,32),(0,0)],[(64,64),(64,32),(32,64),(0,0)]]

def parse_ncgr(d):
 mg,size,h_tiles,w_tiles,bit,vram,tiled,dsize,unk=struct.unpack_from('<4sIHHIIIII',d,16)
 raw=d[48:48+dsize]
 pix=[]
 for b in raw: pix += [b&15,b>>4]
 return {'w':w_tiles*8,'h':h_tiles*8,'pix':pix,'vram':vram,'tiled':tiled,'bit':bit}

def get_cell_pixels(g,tile,w,h):
 if (g['tiled']&0xff)!=0:
  start_y=(tile//(g['w']//8))*8; start_x=(tile%(g['w']//8))*8
  out=[0]*(w*h)
  for y in range(h):
   sy=start_y+y
   if sy>=g['h']: break
   st=sy*g['w']+start_x
   row=g['pix'][st:st+w]
   out[y*w:y*w+len(row)]=row
  return out
 raise NotImplementedError('linear/tiled=0 not needed here')

def parse_ncer(d):
 mg,size,cc,ct,cdo,flags,pdo,p1,p2=struct.unpack_from('<4sIHHIIIII',d,16)
 off=48; cells=[]
 for i in range(cc):
  oc,un,oo=struct.unpack_from('<HHI',d,off); off+=8
  ex=None
  if ct==1: ex=struct.unpack_from('<hhhh',d,off);off+=8
  cells.append((oc,un,oo,ex))
 return {'cells':cells,'obj_base':off,'data':d}

def get_objs(n,cell_idx):
 oc,un,oo,ex=n['cells'][cell_idx]; d=n['data']; base=n['obj_base']+oo; arr=[]
 for j in range(oc):
  a0,a1,a2=struct.unpack_from('<HHH',d,base+j*6)
  arr.append({'y':s8(a0&255),'rs':(a0>>8)&3,'mode':(a0>>10)&3,'mosaic':(a0>>12)&1,'color_mode':(a0>>13)&1,'shape':(a0>>14)&3,'x':s9(a1&0x1ff),'rs_param':(a1>>9)&31,'size':(a1>>14)&3,'tile':a2&0x3ff,'priority':(a2>>10)&3,'pal':(a2>>12)&15})
 return arr

def parse_nanr(d):
 mg,size,acn,frn,aoff,foff,fdoff,p1,p2=struct.unpack_from('<4sIHHIIIII',d,16); A=lambda o:24+o
 acells=[struct.unpack_from('<IHHII',d,A(aoff)+i*16) for i in range(acn)]
 return {'data':d,'acells':acells,'frames_base':A(foff),'fdata_base':A(fdoff)}

def first_frame(n,ai):
 fc,ft,cty,unk,froff=n['acells'][ai]
 do,dur,pad=struct.unpack_from('<IHH',n['data'],n['frames_base']+froff); p=n['fdata_base']+do
 if ft==0:
  ci,un=struct.unpack_from('<HH',n['data'],p); return ci,(256,0,0,256),(0,0)
 if ft==1:
  ci,theta,xmag,ymag,x,y=struct.unpack_from('<HhIIhh',n['data'],p)
  st=int(math.sin(theta*2*math.pi/65536)*4096); ct=int(math.cos(theta*2*math.pi/65536)*4096)
  return ci,(int(256*ct/xmag),int(256*st/xmag),int(-256*st/ymag),int(256*ct/ymag)),(x,y)
 if ft==2:
  ci,pad,x,y=struct.unpack_from('<HHhh',n['data'],p); return ci,(256,0,0,256),(x,y)
 raise ValueError(ft)

def parse_nmcr(d):
 mg,size,cnt,pad,hoff,doff,p1,p2=struct.unpack_from('<4sIHHIIII',d,16); A=lambda o:24+o
 headers=[struct.unpack_from('<HHI',d,A(hoff)+i*8) for i in range(cnt)]; maps=[]
 for hc,hu,ho in headers:
  p=A(doff)+ho; maps.append([struct.unpack_from('<HhhBB',d,p+i*8) for i in range(hc)])
 return maps

def parse_palette(d):
 mg,size,bit,unk,pad,dsize,doff=struct.unpack_from('<4sIHHIII',d,16); raw=d[40:40+dsize]; cols=[]
 for i in range(16):
  c=struct.unpack_from('<H',raw,i*2)[0]; r=c&31;g=(c>>5)&31;b=(c>>10)&31; conv=lambda q:(q<<3)|(q>>2)
  cols.append((conv(r),conv(g),conv(b),0 if i==0 else 255))
 return cols

def render_species(dex):
 base=dex*20; g=parse_ncgr(mem(base+2)); ncer=parse_ncer(mem(base+4)); nanr=parse_nanr(mem(base+5)); maps=parse_nmcr(mem(base+6)); pal=parse_palette(mem(base+19))
 W,H=192,128; canvas=[0]*(W*H); offset=(96,112)
 def draw_obj(o,fo,m):
  cw,ch=OBJ_SIZES[o['size']][o['shape']]; src=get_cell_pixels(g,o['tile'],cw,ch); fw,fh=cw,ch
  if o['rs']&2: fw*=2;fh*=2
  tx,ty=fw//2,fh//2; rs=o['rs']
  for y in range(fh):
   dy=o['y']+fo[1]+y
   if dy<0 or dy>=H: continue
   for x in range(fw):
    dx=o['x']+fo[0]+x
    if dx<0 or dx>=W: continue
    if rs&1:
     xp=(((x-tx)*m[0]+(y-ty)*m[1])>>8)+tx; yp=(((x-tx)*m[2]+(y-ty)*m[3])>>8)+ty
    else: xp,yp=x,y
    if rs&2: xp-=cw//2;yp-=ch//2
    if 0<=xp<cw and 0<=yp<ch:
     di=dy*W+dx
     if canvas[di]==0: canvas[di]=src[yp*cw+xp]
 def draw_cell(ci,fo,m):
  for o in get_objs(ncer,ci): draw_obj(o,fo,m)
 for ai,mx,my,unk,pri in maps[0]:
  ci,m,co=first_frame(nanr,ai); draw_cell(ci,(offset[0]+mx+co[0],offset[1]+my+co[1]),m)
 im=Image.new('RGBA',(W,H),(0,0,0,0)); P=im.load()
 for y in range(H):
  for x in range(W): P[x,y]=pal[canvas[y*W+x]]
 bbox=im.getbbox(); cr=im.crop(bbox) if bbox else im; im.save(OUT/f'{dex}_rom_frame0_full.png'); cr.save(OUT/f'{dex}_rom_frame0_crop.png')
 region=im.crop((48,16,144,112)); region.save(OUT/f'{dex}_rom_frame0_96.png'); print(dex,'bbox',bbox,'crop',cr.size,'region bbox',region.getbbox())
 return region
for d in [643,644,646]: render_species(d)
