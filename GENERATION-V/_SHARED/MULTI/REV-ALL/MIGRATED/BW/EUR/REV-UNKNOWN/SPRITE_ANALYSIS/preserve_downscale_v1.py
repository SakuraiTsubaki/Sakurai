from PIL import Image, ImageDraw
from pathlib import Path
from collections import Counter
import math, json
SRC=Path('/mnt/data/sprite_preserve_trial/rom_reconstructed')
OUT=Path('/mnt/data/sprite_preserve_trial/downscale_v1'); OUT.mkdir(parents=True,exist_ok=True)
NAMES={643:'Reshiram',644:'Zekrom',646:'Kyurem'}

def palette_and_indices(im):
    im=im.convert('RGBA'); pixels=list(im.getdata()); color_to_idx={(0,0,0,0):0}; pal=[(0,0,0,0)]; idx=[]
    for c in pixels:
        if c[3]==0: idx.append(0); continue
        key=(c[0],c[1],c[2],255)
        if key not in color_to_idx: color_to_idx[key]=len(pal); pal.append(key)
        idx.append(color_to_idx[key])
    return pal,idx

def make_image(pal,idx,w,h):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); px=im.load()
    for y in range(h):
        for x in range(w): px[x,y]=pal[idx[y*w+x]]
    return im

def components_by_color(idx,w,h):
    seen=[False]*(w*h); comps=[]
    for pos,c in enumerate(idx):
        if c==0 or seen[pos]: continue
        q=[pos]; seen[pos]=True; pts=[]
        while q:
            p=q.pop(); pts.append(p); x=p%w; y=p//w
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=nx<w and 0<=ny<h:
                    np=ny*w+nx
                    if not seen[np] and idx[np]==c: seen[np]=True; q.append(np)
        comps.append((c,pts))
    return comps

def preserve_downscale(im,n):
    pal,src=palette_and_indices(im); sw,sh=im.size; out=[0]*(n*n)
    for oy in range(n):
        sy=min(sh-1,int((oy+0.5)*sh/n))
        for ox in range(n):
            sx=min(sw-1,int((ox+0.5)*sw/n)); out[oy*n+ox]=src[sy*sw+sx]
    for oy in range(n):
        y0=oy*sh/n; y1=(oy+1)*sh/n; sy0=max(0,int(math.floor(y0))); sy1=min(sh-1,int(math.ceil(y1)-1))
        for ox in range(n):
            if out[oy*n+ox]!=0: continue
            x0=ox*sw/n; x1=(ox+1)*sw/n; sx0=max(0,int(math.floor(x0))); sx1=min(sw-1,int(math.ceil(x1)-1)); counts=Counter(); total=0; non=0
            for sy in range(sy0,sy1+1):
                for sx in range(sx0,sx1+1):
                    total+=1; c=src[sy*sw+sx]
                    if c: counts[c]+=1; non+=1
            if non>=2 and non/max(1,total)>=0.28:
                def lum(ci):
                    r,g,b,_=pal[ci]; return 0.2126*r+0.7152*g+0.0722*b
                out[oy*n+ox]=max(counts,key=lambda ci:(counts[ci],-lum(ci)))
    global_counts=Counter(c for c in src if c); sprite_pixels=sum(global_counts.values())
    for c,pts in components_by_color(src,sw,sh):
        if len(pts)>14: continue
        if len(pts)>6 and global_counts[c]>sprite_pixels*0.055: continue
        xs=[p%sw for p in pts]; ys=[p//sw for p in pts]
        tx0=max(0,int(min(xs)*n/sw)-1); tx1=min(n-1,int(max(xs)*n/sw)+1); ty0=max(0,int(min(ys)*n/sh)-1); ty1=min(n-1,int(max(ys)*n/sh)+1)
        if any(out[y*n+x]==c for y in range(ty0,ty1+1) for x in range(tx0,tx1+1)): continue
        cx=sum(xs)/len(xs); cy=sum(ys)/len(ys); ox=min(n-1,max(0,int((cx+0.5)*n/sw))); oy=min(n-1,max(0,int((cy+0.5)*n/sh)))
        if out[oy*n+ox]!=0 or len(pts)>=2: out[oy*n+ox]=c
    return make_image(pal,out,n,n)

def naive(im,n): return im.resize((n,n),Image.Resampling.NEAREST)

def checker(size,cell=8):
    bg=Image.new('RGBA',size,(235,235,235,255)); d=ImageDraw.Draw(bg)
    for y in range(0,size[1],cell):
        for x in range(0,size[0],cell):
            if ((x//cell)+(y//cell))%2: d.rectangle((x,y,x+cell-1,y+cell-1),fill=(205,205,205,255))
    return bg

def zoom_on_checker(im,box=288):
    scale=max(1,min(box//im.width,box//im.height)); z=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST); bg=checker((box,box),12); bg.alpha_composite(z,((box-z.width)//2,(box-z.height)//2)); return bg

manifest=[]
for dex,name in NAMES.items():
    src=Image.open(SRC/f'{dex}_rom_frame0_96.png').convert('RGBA'); outputs={'source96':src}
    for n in (64,56):
        a=naive(src,n); p=preserve_downscale(src,n); a.save(OUT/f'{dex}_{name.lower()}_naive_{n}.png'); p.save(OUT/f'{dex}_{name.lower()}_preserve_v1_{n}.png'); outputs[f'naive{n}']=a; outputs[f'preserve{n}']=p
    def stats(im):
        px=list(im.getdata()); return {'size':im.size,'visible_pixels':sum(c[3]>0 for c in px),'visible_colors':len(set((c[0],c[1],c[2]) for c in px if c[3]>0))}
    manifest.append({'dex':dex,'name':name,**{k:stats(v) for k,v in outputs.items()}})
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
