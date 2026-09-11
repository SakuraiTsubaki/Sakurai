from PIL import Image, ImageDraw
from pathlib import Path
from collections import Counter
import math, json, colorsys, numpy as np
SRC=Path('/mnt/data/sprite_preserve_trial/rom_reconstructed')
V1=Path('/mnt/data/sprite_preserve_trial/downscale_v1')
OUT=Path('/mnt/data/sprite_preserve_trial/downscale_v2')
NAMES={643:'Reshiram',644:'Zekrom',646:'Kyurem'}
def q5(c): return tuple(min(255,round(round(float(v)*31/255)*255/31)) for v in c[:3])
def lum(c): return .2126*c[0]+.7152*c[1]+.0722*c[2]
def sat(c): return colorsys.rgb_to_hsv(*(x/255 for x in c))[1]
def arr(im):
 a=np.array(im.convert('RGBA')); return a[:,:,:3].astype(float),a[:,:,3]>0
def fb(o,n,s):
 a=o*s/n;b=(o+1)*s/n;return max(0,int(math.floor(a))),min(s-1,int(math.ceil(b)-1))
def g3(im,n=64):
 rgb,m=arr(im); h,w=m.shape
 cols=Counter(map(tuple,rgb[m].astype(np.uint8)))
 pal=[]
 for c,_ in cols.most_common():
  z=q5(c)
  if z not in pal:pal.append(z)
 if len(pal)>14:
  pal=pal[:14]
 out=np.zeros((n,n,4),dtype=np.uint8); om=np.zeros((n,n),bool)
 for y in range(n):
  y0,y1=fb(y,n,h)
  for x in range(n):
   x0,x1=fb(x,n,w); sm=m[y0:y1+1,x0:x1+1]; cov=sm.mean(); cy=min(h-1,int((y+.5)*h/n));cx=min(w-1,int((x+.5)*w/n))
   if cov<.24 and not m[cy,cx]:continue
   om[y,x]=1; pix=rgb[y0:y1+1,x0:x1+1][sm]
   if len(pix)==0:pix=np.array([rgb[cy,cx]])
   cnt=Counter(q5(tuple(map(int,p))) for p in pix); c=max(cnt,key=lambda z:(cnt[z],-lum(z)))
   if c not in pal:c=min(pal,key=lambda p:sum((p[i]-c[i])**2 for i in range(3)))
   out[y,x,:3]=c;out[y,x,3]=255
 l=np.array([lum(p) for p in rgb[m]]);thr=np.percentile(l,18);dark=min(pal,key=lum)
 for y in range(n):
  for x in range(n):
   if not om[y,x]:continue
   bd=any(nx<0 or nx>=n or ny<0 or ny>=n or not om[ny,nx] for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
   if not bd:continue
   y0,y1=fb(y,n,h);x0,x1=fb(x,n,w);sm=m[y0:y1+1,x0:x1+1];pix=rgb[y0:y1+1,x0:x1+1][sm]
   if len(pix) and min(lum(p) for p in pix)<=thr:out[y,x,:3]=dark
 present=set(map(tuple,out[:,:,:3][out[:,:,3]>0]))
 for c,count in cols.items():
  qc=q5(c)
  if qc in present or qc not in pal or count>24: continue
  pts=np.argwhere(np.all(rgb==np.array(c,float),axis=2) & m)
  if len(pts)==0: continue
  sy,sx=pts[len(pts)//2]; ox=min(n-1,max(0,int((sx+.5)*n/w))); oy=min(n-1,max(0,int((sy+.5)*n/h)))
  if om[oy,ox]: out[oy,ox,:3]=qc; present.add(qc)
 return Image.fromarray(out,'RGBA')
def g2pal(im):
 rgb,m=arr(im); X=rgb[m].astype(np.uint8); cnt=Counter(map(tuple,X)); total=sum(cnt.values())
 candidates=[]
 for c,n in cnt.most_common():
  L=lum(c)
  if L>245 or L<28: continue
  candidates.append((c,n))
 body=q5(candidates[0][0]) if candidates else (165,165,165)
 accent=None
 for c,n in candidates:
  qc=q5(c)
  d=sum((qc[i]-body[i])**2 for i in range(3))**.5
  if n/total>=.025 and sat(c)>=.32 and d>55:
   accent=qc; break
 if accent is not None:
  chosen=[body,accent]
 else:
  chosen=[body]
  for c,n in candidates[1:]:
   qc=q5(c)
   if sum((qc[i]-body[i])**2 for i in range(3))**.5>28:
    chosen.append(qc);break
 while len(chosen)<2: chosen.append((82,82,82))
 chosen=sorted(chosen,key=lum,reverse=True)
 return [(255,255,255),chosen[0],chosen[1],(0,0,0)]
def g2(im,n=56):
 rgb,m=arr(im);h,w=m.shape;pal=g2pal(im);out=np.zeros((n,n,4),dtype=np.uint8);om=np.zeros((n,n),bool)
 for y in range(n):
  y0,y1=fb(y,n,h)
  for x in range(n):
   x0,x1=fb(x,n,w);sm=m[y0:y1+1,x0:x1+1];cov=sm.mean();cy=min(h-1,int((y+.5)*h/n));cx=min(w-1,int((x+.5)*w/n))
   if cov<.21 and not m[cy,cx]:continue
   om[y,x]=1;pix=rgb[y0:y1+1,x0:x1+1][sm];avg=pix.mean(0) if len(pix) else rgb[cy,cx]
   c=min(pal,key=lambda p:sum((p[i]-avg[i])**2 for i in range(3)));out[y,x,:3]=c;out[y,x,3]=255
 l=np.array([lum(p) for p in rgb[m]]);thr=np.percentile(l,20)
 for y in range(n):
  for x in range(n):
   if not om[y,x]:continue
   bd=any(nx<0 or nx>=n or ny<0 or ny>=n or not om[ny,nx] for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
   if not bd:continue
   y0,y1=fb(y,n,h);x0,x1=fb(x,n,w);sm=m[y0:y1+1,x0:x1+1];pix=rgb[y0:y1+1,x0:x1+1][sm]
   if len(pix) and min(lum(p) for p in pix)<=thr+18:out[y,x,:3]=pal[3]
 return Image.fromarray(out,'RGBA'),pal
def checker(sz,cell=8):
 bg=Image.new('RGBA',sz,(235,235,235,255));d=ImageDraw.Draw(bg)
 for y in range(0,sz[1],cell):
  for x in range(0,sz[0],cell):
   if ((x//cell+y//cell)&1):d.rectangle((x,y,x+cell-1,y+cell-1),fill=(205,205,205,255))
 return bg
def zoom(im,b):
 s=max(1,min(b//im.width,b//im.height));z=im.resize((im.width*s,im.height*s),Image.Resampling.NEAREST);bg=checker((b,b),12);bg.alpha_composite(z,((b-z.width)//2,(b-z.height)//2));return bg
def st(im):
 a=np.array(im);m=a[:,:,3]>0;bb=im.getchannel('A').getbbox();return {'pixels':int(m.sum()),'colors':len(set(map(tuple,a[:,:,:3][m]))),'bbox':bb}
mani=[]
for dex,name in NAMES.items():
 src=Image.open(SRC/f'{dex}_rom_frame0_96.png').convert('RGBA');a=g3(src);b,p=g2(src)
 a.save(OUT/f'{dex}_{name.lower()}_gen3_64_preserve_v2.png');b.save(OUT/f'{dex}_{name.lower()}_gen2_56_preserve_v2.png')
 mani.append({'dex':dex,'name':name,'gen2_palette':p,'source':st(src),'gen3_v2':st(a),'gen2_v2':st(b)})
 ims=[src,Image.open(V1/f'{dex}_{name.lower()}_preserve_v1_64.png'),a,Image.open(V1/f'{dex}_{name.lower()}_preserve_v1_56.png'),b];labs=['BW ROM 96','v1 64','Gen III v2 64','v1 56','Gen II v2 56'];cw=256;top=38
 sh=Image.new('RGBA',(cw*5,cw+top),'white');d=ImageDraw.Draw(sh)
 for i,(z,l) in enumerate(zip(ims,labs)):
  sh.alpha_composite(zoom(z,cw),(i*cw,top));bb=d.textbbox((0,0),l);d.text((i*cw+(cw-(bb[2]-bb[0]))//2,12),l,fill='black')
 sh.save(OUT/f'{dex}_{name.lower()}_v2_comparison.png')
cw=220;top=32;rh=cw+top;combo=Image.new('RGBA',(cw*5,rh*3),'white');d=ImageDraw.Draw(combo);labs=['BW ROM 96','v1 64','Gen III v2 64','v1 56','Gen II v2 56']
for r,(dex,name) in enumerate(NAMES.items()):
 ims=[Image.open(SRC/f'{dex}_rom_frame0_96.png'),Image.open(V1/f'{dex}_{name.lower()}_preserve_v1_64.png'),Image.open(OUT/f'{dex}_{name.lower()}_gen3_64_preserve_v2.png'),Image.open(V1/f'{dex}_{name.lower()}_preserve_v1_56.png'),Image.open(OUT/f'{dex}_{name.lower()}_gen2_56_preserve_v2.png')]
 for c,(z,l) in enumerate(zip(ims,labs)):
  combo.alpha_composite(zoom(z,cw),(c*cw,r*rh+top));t=name+' — '+l if c==0 else l;bb=d.textbbox((0,0),t);d.text((c*cw+(cw-(bb[2]-bb[0]))//2,r*rh+9),t,fill='black')
combo.save(OUT/'bw_legendaries_preserve_v2_comparison.png')
(OUT/'manifest_v2.json').write_text(json.dumps(mani,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(mani,ensure_ascii=False,indent=2))
