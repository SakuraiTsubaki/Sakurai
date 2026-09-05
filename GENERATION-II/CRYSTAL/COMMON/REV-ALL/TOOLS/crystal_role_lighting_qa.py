#!/usr/bin/env python3
"""QA Crystal-role HGSS front candidates against Crystal's original 4-color lighting grammar."""
from __future__ import annotations
import argparse, csv, math, re
from collections import deque
from pathlib import Path
from PIL import Image

def build_name_map(root):
    text=(Path(root)/'data/pokemon/palettes.asm').read_text(encoding='utf-8')
    names=re.findall(r'INCBIN "gfx/pokemon/([^/]+)/normal\.gbcpal", middle_colors', text)
    if len(names)!=251: raise ValueError(f'expected 251 species, got {len(names)}')
    return {i+1:n for i,n in enumerate(names)}

def load_dims(path):
    out={}
    with Path(path).open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'): out[int(r['species'])]=int(r['front_tiles'])
    if len(out)!=251: raise ValueError('dimension map incomplete')
    return out

def decode_2bpp(data,tiles):
    w=h=tiles*8; idx=[[0]*w for _ in range(h)]; p=0
    for ty in range(tiles):
        for tx in range(tiles):
            for y in range(8):
                lo=data[p]; hi=data[p+1]; p+=2
                for x in range(8):
                    bit=7-x; idx[ty*8+y][tx*8+x]=((lo>>bit)&1)|(((hi>>bit)&1)<<1)
    if p!=len(data): raise ValueError(f'2bpp size mismatch {p} != {len(data)}')
    return idx

def png_first_frame(path,canvas):
    im=Image.open(path)
    if im.mode!='P': raise ValueError(f'expected indexed Crystal PNG: {path}')
    if im.width!=canvas or im.height<canvas: raise ValueError(f'bad Crystal front sheet dimensions: {path}: {im.size}')
    im=im.crop((0,0,canvas,canvas)); pix=im.load()
    return [[pix[x,y] for x in range(canvas)] for y in range(canvas)]

def interior_mask(idx):
    h=len(idx); w=len(idx[0]); bg=[[False]*w for _ in range(h)]; q=deque()
    def add(x,y):
        if 0<=x<w and 0<=y<h and not bg[y][x] and idx[y][x]==0:
            bg[y][x]=True; q.append((x,y))
    for x in range(w): add(x,0); add(x,h-1)
    for y in range(h): add(0,y); add(w-1,y)
    while q:
        x,y=q.popleft(); add(x-1,y); add(x+1,y); add(x,y-1); add(x,y+1)
    return [[not bg[y][x] for x in range(w)] for y in range(h)]

def metrics(idx):
    h=len(idx); w=len(idx[0]); inside=interior_mask(idx)
    pts=[(x,y) for y in range(h) for x in range(w) if inside[y][x]]
    if not pts:
        return dict(area=0,bbox_w=0,bbox_h=0,occupancy=0,p0=0,p1=0,p2=0,p3=0,highlight_x=-1,highlight_y=-1,black_x=-1,black_y=-1,n0=0,n1=0,n2=0,n3=0)
    xs=[x for x,y in pts]; ys=[y for x,y in pts]; x0,x1=min(xs),max(xs); y0,y1=min(ys),max(ys); bw=x1-x0+1; bh=y1-y0+1; area=len(pts)
    counts=[0,0,0,0]; coords=[[],[],[],[]]
    for x,y in pts:
        v=idx[y][x]; counts[v]+=1; coords[v].append((x,y))
    def cent(v):
        if not coords[v]: return (-1.0,-1.0)
        cx=sum(x for x,y in coords[v])/len(coords[v]); cy=sum(y for x,y in coords[v])/len(coords[v])
        return ((cx-x0)/(bw-1) if bw>1 else .5,(cy-y0)/(bh-1) if bh>1 else .5)
    hx,hy=cent(0); bx,by=cent(3)
    return dict(area=area,bbox_w=bw,bbox_h=bh,occupancy=area/(bw*bh),p0=counts[0]/area,p1=counts[1]/area,p2=counts[2]/area,p3=counts[3]/area,highlight_x=hx,highlight_y=hy,black_x=bx,black_y=by,n0=counts[0],n1=counts[1],n2=counts[2],n3=counts[3])

def evaluate(orig,cand):
    flags=[]; area_ratio=cand['area']/orig['area'] if orig['area'] else 0
    if area_ratio < .55: flags.append('SILHOUETTE_TOO_SMALL')
    if area_ratio > 1.75: flags.append('SILHOUETTE_TOO_LARGE')
    if orig['p3']>.04 and cand['p3'] < orig['p3']*.35: flags.append('BLACK_TOO_THIN')
    if cand['p3'] > max(.58,orig['p3']*2.15+.04): flags.append('BLACK_TOO_HEAVY')
    if orig['p0']>.015 and cand['p0'] < orig['p0']*.18: flags.append('HIGHLIGHT_TOO_WEAK')
    if cand['p0'] > max(.42,orig['p0']*2.8+.05): flags.append('HIGHLIGHT_TOO_HEAVY')
    if orig['p1']>.015 and cand['p1']<.004: flags.append('COLOR1_MISSING')
    if orig['p2']>.008 and cand['p2']<.002: flags.append('COLOR2_MISSING')
    light_shift=-1.0
    if orig['n0']>=6 and cand['n0']>=6 and orig['highlight_x']>=0 and cand['highlight_x']>=0:
        dx=cand['highlight_x']-orig['highlight_x']; dy=cand['highlight_y']-orig['highlight_y']; light_shift=math.sqrt(dx*dx+dy*dy)
        if light_shift>.72: flags.append('HIGHLIGHT_DIRECTION_SHIFT')
    return area_ratio,light_shift,flags

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate-root',required=True); ap.add_argument('--pokecrystal-root',required=True); ap.add_argument('--dimensions',required=True); ap.add_argument('--output',required=True); ns=ap.parse_args()
    dims=load_dims(ns.dimensions); names=build_name_map(ns.pokecrystal_root); root=Path(ns.candidate_root); rows=[]
    for sp in list(range(1,201))+list(range(202,252)):
        tiles=dims[sp]; canvas=tiles*8; name=names[sp]; f=root/'2BPP'/'FRONT'/f'{sp:03d}.{tiles}x{tiles}.2bpp'
        cand=metrics(decode_2bpp(f.read_bytes(),tiles)); orig=metrics(png_first_frame(Path(ns.pokecrystal_root)/'gfx'/'pokemon'/name/'front.png',canvas)); area_ratio,light_shift,flags=evaluate(orig,cand)
        rows.append({'species':sp,'name':name,'tiles':tiles,'status':'REVIEW' if flags else 'PASS','flags':','.join(flags),'area_ratio':f'{area_ratio:.4f}','light_shift':f'{light_shift:.4f}' if light_shift>=0 else '','orig_highlight':f"{orig['p0']:.4f}",'cand_highlight':f"{cand['p0']:.4f}",'orig_color1':f"{orig['p1']:.4f}",'cand_color1':f"{cand['p1']:.4f}",'orig_color2':f"{orig['p2']:.4f}",'cand_color2':f"{cand['p2']:.4f}",'orig_black':f"{orig['p3']:.4f}",'cand_black':f"{cand['p3']:.4f}",'orig_bbox':f"{orig['bbox_w']}x{orig['bbox_h']}",'cand_bbox':f"{cand['bbox_w']}x{cand['bbox_h']}",'orig_highlight_xy':f"{orig['highlight_x']:.3f},{orig['highlight_y']:.3f}" if orig['highlight_x']>=0 else '','cand_highlight_xy':f"{cand['highlight_x']:.3f},{cand['highlight_y']:.3f}" if cand['highlight_x']>=0 else ''})
    out=Path(ns.output); out.parent.mkdir(parents=True,exist_ok=True); fields=list(rows[0])
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); w.writeheader(); w.writerows(rows)
    review=[r for r in rows if r['status']=='REVIEW']; flag_counts={}
    for r in review:
        for fl in filter(None,r['flags'].split(',')): flag_counts[fl]=flag_counts.get(fl,0)+1
    md=out.with_suffix('.summary.md'); lines=['# Crystal-role front lighting QA','',f'- PASS: {len(rows)-len(review)} / {len(rows)}',f'- REVIEW: {len(review)} / {len(rows)}','','## Flag counts','']
    for k,v in sorted(flag_counts.items(),key=lambda kv:(-kv[1],kv[0])): lines.append(f'- {k}: {v}')
    lines += ['','## Manual-review species','']
    for r in review: lines.append(f"- #{r['species']:03d} {r['name']}: {r['flags']}")
    md.write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(f'PASS {len(rows)-len(review)} REVIEW {len(review)} TOTAL {len(rows)}')
    for k,v in sorted(flag_counts.items()): print(k,v)
if __name__=='__main__': main()
