#!/usr/bin/env python3
"""
Convert HGSS battle sprites to Pokémon Crystal 2bpp while preserving Crystal's
original four-color palette roles.

Principle:
- HGSS supplies silhouette, pose, anatomy, and pixel detail.
- Crystal supplies the 4-color index semantics: 0=white/highlight,
  1=middle color A, 2=middle color B, 3=black/deep shadow/outline.
- Bright/dark shades inside each HGSS hue family collapse toward Crystal
  white/black instead of flattening into a median-cut palette.
- Existing Crystal normal/shiny palettes therefore remain usable unchanged.
"""
from __future__ import annotations
import argparse, csv, colorsys, math, re
from collections import Counter
from pathlib import Path
from PIL import Image

TRANSPARENT = 255

def lum(rgb):
    r,g,b = rgb
    return 0.2126*r + 0.7152*g + 0.0722*b

def hsv(rgb):
    r,g,b = (x/255.0 for x in rgb)
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    return h*360.0, s, v

def hdist(a,b):
    d=abs(a-b)%360
    return min(d,360-d)

def circular_mean(items):
    x=y=0.0
    for h,w in items:
        a=math.radians(h)
        x += math.cos(a)*w
        y += math.sin(a)*w
    if x==0 and y==0:
        return items[0][0]
    return math.degrees(math.atan2(y,x))%360

def crystal_palette(path):
    im=Image.open(path)
    if im.mode != 'P':
        raise ValueError(f'Crystal reference PNG is not indexed P mode: {path}')
    pal=im.getpalette()
    return [tuple(pal[i:i+3]) for i in range(0,12,3)]

def build_name_map(pokecrystal_root):
    text=(Path(pokecrystal_root)/'data/pokemon/palettes.asm').read_text(encoding='utf-8')
    names=re.findall(r'INCBIN "gfx/pokemon/([^/]+)/normal\.gbcpal", middle_colors', text)
    if len(names)!=251:
        raise ValueError(f'expected 251 Pokémon palette entries, got {len(names)}')
    return {i+1:name for i,name in enumerate(names)}

def opaque_palette(im):
    c=Counter()
    for r,g,b,a in im.convert('RGBA').getdata():
        if a>=128:
            c[(r,g,b)] += 1
    return c

def cluster_chromatic(color_counts, hue_join=34.0):
    entries=[]; grays=[]
    for rgb,count in color_counts.items():
        h,s,v=hsv(rgb)
        if v < 0.20 or s < 0.16:
            grays.append((rgb,count,h,s,v))
        else:
            entries.append((rgb,count,h,s,v))
    entries.sort(key=lambda z:z[1], reverse=True)
    clusters=[]
    for ent in entries:
        rgb,count,h,s,v=ent
        best=None
        for i,cl in enumerate(clusters):
            d=hdist(h,cl['hue'])
            if d <= hue_join and (best is None or d<best[0]):
                best=(d,i)
        if best is None:
            clusters.append({'colors':[ent],'hue':h})
        else:
            cl=clusters[best[1]]
            cl['colors'].append(ent)
            cl['hue']=circular_mean([(e[2],e[1]) for e in cl['colors']])
    return clusters,grays

def semantic_mapping(im, target_palette):
    counts=opaque_palette(im)
    c1,c2=target_palette[1],target_palette[2]
    h1,s1,v1=hsv(c1); h2,s2,v2=hsv(c2)
    tonal = (hdist(h1,h2) < 26 and min(s1,s2) > 0.05) or (max(s1,s2) < 0.18)
    mapping={}
    clusters,grays=cluster_chromatic(counts)

    for rgb,count,h,s,v in grays:
        L=lum(rgb)
        if L >= 155: mapping[rgb]=0
        elif L <= 95: mapping[rgb]=3
        else: mapping[rgb]=1 if abs(L-lum(c1)) <= abs(L-lum(c2)) else 2

    if tonal:
        mid_order=sorted([(lum(c1),1),(lum(c2),2)], reverse=True)
        light_idx=mid_order[0][1]; dark_idx=mid_order[1][1]
        vals=[]
        for cl in clusters:
            for e in cl['colors']:
                vals.append((lum(e[0]),e[0],e[1]))
        if vals:
            expanded=[]
            for L,rgb,count in vals: expanded.extend([L]*min(count,200))
            expanded.sort()
            def q(p): return expanded[min(len(expanded)-1,max(0,round((len(expanded)-1)*p)))]
            q20,q70,q90=q(.20),q(.70),q(.90)
            for L,rgb,count in vals:
                if L <= q20: mapping[rgb]=3
                elif L >= q90: mapping[rgb]=0
                elif L >= q70: mapping[rgb]=light_idx
                else: mapping[rgb]=dark_idx
        return mapping, tonal, clusters

    for cl in clusters:
        target_idx = 1 if hdist(cl['hue'],h1) <= hdist(cl['hue'],h2) else 2
        cols=sorted(cl['colors'], key=lambda e:lum(e[0]))
        total=sum(e[1] for e in cols); n=len(cols)
        for rank,e in enumerate(cols):
            rgb,count,h,s,v=e; L=lum(rgb); idx=target_idx
            if total >= 48:
                if n >= 4:
                    if rank==0 and L < 125: idx=3
                    elif rank==n-1 and L > 175: idx=0
                elif n==3:
                    if rank==0 and L < 75: idx=3
                    elif rank==2 and L > 225: idx=0
            mapping[rgb]=idx
    return mapping, tonal, clusters

def role_image(src, mapping):
    im=src.convert('RGBA'); out=Image.new('L',im.size,TRANSPARENT)
    a=out.load(); p=im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,alpha=p[x,y]
            if alpha>=128: a[x,y]=mapping[(r,g,b)]
    return out

def content_bbox(role):
    p=role.load(); xs=[]; ys=[]
    for y in range(role.height):
        for x in range(role.width):
            if p[x,y] != TRANSPARENT: xs.append(x); ys.append(y)
    if not xs: raise ValueError('empty sprite')
    return min(xs),min(ys),max(xs)+1,max(ys)+1

def resize_roles(role, dst_w, dst_h):
    sw,sh=role.size; src=role.load(); dst=Image.new('L',(dst_w,dst_h),TRANSPARENT); out=dst.load()
    for dy in range(dst_h):
        y0=dy*sh/dst_h; y1=(dy+1)*sh/dst_h
        sy0=max(0,int(math.floor(y0))); sy1=min(sh,int(math.ceil(y1)))
        for dx in range(dst_w):
            x0=dx*sw/dst_w; x1=(dx+1)*sw/dst_w
            sx0=max(0,int(math.floor(x0))); sx1=min(sw,int(math.ceil(x1)))
            vals=[src[x,y] for y in range(sy0,sy1) for x in range(sx0,sx1)]
            c=Counter(vals); non={k:v for k,v in c.items() if k!=TRANSPARENT}
            if not non: continue
            if TRANSPARENT in c and 3 in non:
                out[dx,dy]=3; continue
            weights={0:1.08,1:1.0,2:1.08,3:1.22}
            out[dx,dy]=max(non,key=lambda k:(non[k]*weights[k],non[k]))
    return dst

def place(role, canvas):
    bbox=content_bbox(role); crop=role.crop(bbox); w,h=crop.size
    scale=min(canvas/w,canvas/h,1.0)
    if scale<1.0:
        nw=max(1,round(w*scale)); nh=max(1,round(h*scale)); crop=resize_roles(crop,nw,nh)
    else: nw,nh=w,h
    dst=Image.new('L',(canvas,canvas),0); cp=crop.load(); dp=dst.load()
    ox=(canvas-nw)//2; oy=canvas-nh
    for y in range(nh):
        for x in range(nw):
            v=cp[x,y]
            if v!=TRANSPARENT: dp[ox+x,oy+y]=v
    return dst,(bbox,nw,nh,ox,oy)

def indexed_to_2bpp(idx):
    w,h=idx.size; p=idx.load(); out=bytearray()
    if w%8 or h%8: raise ValueError('canvas must be tile aligned')
    for ty in range(0,h,8):
        for tx in range(0,w,8):
            for y in range(8):
                lo=hi=0
                for x in range(8):
                    v=p[tx+x,ty+y]&3; bit=7-x
                    lo|=(v&1)<<bit; hi|=((v>>1)&1)<<bit
                out += bytes((lo,hi))
    return bytes(out)

def preview(idx,palette,scale=4):
    rgb=Image.new('RGB',idx.size); p=idx.load(); q=rgb.load()
    for y in range(idx.height):
        for x in range(idx.width): q[x,y]=palette[p[x,y]]
    return rgb.resize((rgb.width*scale,rgb.height*scale),Image.Resampling.NEAREST)

def load_dims(path):
    out={}
    with Path(path).open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'): out[int(r['species'])]=int(r['front_tiles'])
    if len(out)!=251: raise ValueError('dimension map incomplete')
    return out

def convert_one(sp,source_path,crystal_front_path,tiles,out_root):
    src=Image.open(source_path).convert('RGBA'); pal=crystal_palette(crystal_front_path)
    mapping,tonal,clusters=semantic_mapping(src,pal); roles=role_image(src,mapping)
    idx,placement=place(roles,tiles*8); raw=indexed_to_2bpp(idx); out=Path(out_root)
    (out/'2BPP'/'FRONT').mkdir(parents=True,exist_ok=True); (out/'PREVIEW'/'FRONT').mkdir(parents=True,exist_ok=True)
    (out/'2BPP'/'FRONT'/f'{sp:03d}.{tiles}x{tiles}.2bpp').write_bytes(raw)
    preview(idx,pal).save(out/'PREVIEW'/'FRONT'/f'{sp:03d}.{tiles}x{tiles}.png')
    return {'species':sp,'tiles':tiles,'raw_bytes':len(raw),'tonal_palette':int(tonal),'target_palette':'|'.join('%02X%02X%02X'%c for c in pal),'source_bbox':','.join(map(str,placement[0])),'placed_wh':f'{placement[1]}x{placement[2]}','offset_xy':f'{placement[3]},{placement[4]}','mapping':' ; '.join(f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}->{idx}' for rgb,idx in sorted(mapping.items()))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-root',required=True); ap.add_argument('--pokecrystal-root',required=True); ap.add_argument('--dimensions',required=True); ap.add_argument('--output-root',required=True); ap.add_argument('--species',default='1')
    ns=ap.parse_args(); dims=load_dims(ns.dimensions); names=build_name_map(ns.pokecrystal_root); chosen=[]
    for part in ns.species.split(','):
        part=part.strip()
        if '-' in part:
            a,b=map(int,part.split('-',1)); chosen.extend(range(a,b+1))
        else: chosen.append(int(part))
    rows=[]
    for sp in chosen:
        name=names[sp]; src=Path(ns.source_root)/'FRONT'/f'{sp:03d}.png'; ref=Path(ns.pokecrystal_root)/'gfx'/'pokemon'/name/'front.png'
        rows.append(convert_one(sp,src,ref,dims[sp],ns.output_root)); print(f'#{sp:03d} {name}: {dims[sp]}x{dims[sp]} done')
    report=Path(ns.output_root)/'ROLE_MAPPING_REPORT.tsv'; report.parent.mkdir(parents=True,exist_ok=True); fields=list(rows[0]) if rows else []
    with report.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); w.writeheader(); w.writerows(rows)
if __name__=='__main__': main()
