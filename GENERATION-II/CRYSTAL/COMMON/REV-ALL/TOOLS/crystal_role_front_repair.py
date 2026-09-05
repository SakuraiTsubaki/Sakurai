#!/usr/bin/env python3
"""Second-pass repair for Crystal-role HGSS front candidates.

Only sprites flagged by LIGHTING_QA.tsv are altered. PASS sprites are copied byte-for-byte.
Repairs are driven by the original Crystal first frame and by projected semantic-role
pixels from the HGSS source, so the tool does not invent a new palette.
"""
from __future__ import annotations
import argparse,csv,importlib.util,math,shutil
from collections import Counter,defaultdict,deque
from pathlib import Path
from PIL import Image

TRANSPARENT=255

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def decode_2bpp(data,tiles):
    w=h=tiles*8; a=[[0]*w for _ in range(h)]; p=0
    for ty in range(tiles):
        for tx in range(tiles):
            for y in range(8):
                lo,hi=data[p],data[p+1]; p+=2
                for x in range(8):
                    bit=7-x; a[ty*8+y][tx*8+x]=((lo>>bit)&1)|(((hi>>bit)&1)<<1)
    return a

def encode_2bpp(a):
    h=len(a); w=len(a[0]); out=bytearray()
    for ty in range(0,h,8):
        for tx in range(0,w,8):
            for y in range(8):
                lo=hi=0
                for x in range(8):
                    v=a[ty+y][tx+x]&3; bit=7-x; lo|=(v&1)<<bit; hi|=((v>>1)&1)<<bit
                out.extend((lo,hi))
    return bytes(out)

def outside_white(a):
    h=len(a); w=len(a[0]); out=[[False]*w for _ in range(h)]; q=deque()
    def add(x,y):
        if 0<=x<w and 0<=y<h and not out[y][x] and a[y][x]==0: out[y][x]=True; q.append((x,y))
    for x in range(w): add(x,0); add(x,h-1)
    for y in range(h): add(0,y); add(w-1,y)
    while q:
        x,y=q.popleft(); add(x-1,y); add(x+1,y); add(x,y-1); add(x,y+1)
    return out

def inside_mask(a):
    bg=outside_white(a); return [[not bg[y][x] for x in range(len(a[0]))] for y in range(len(a))]

def metrics(a):
    ins=inside_mask(a); h=len(a); w=len(a[0]); pts=[(x,y) for y in range(h) for x in range(w) if ins[y][x]]
    if not pts: return {'area':0,'p0':0,'p1':0,'p2':0,'p3':0,'bbox_w':0,'bbox_h':0,'n0':0,'n1':0,'n2':0,'n3':0}
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; c=[0,0,0,0]
    for x,y in pts: c[a[y][x]]+=1
    area=len(pts); return {'area':area,**{f'p{i}':c[i]/area for i in range(4)},**{f'n{i}':c[i] for i in range(4)},'bbox_w':max(xs)-min(xs)+1,'bbox_h':max(ys)-min(ys)+1}

def original_array(path,canvas):
    im=Image.open(path)
    if im.mode!='P': raise ValueError(f'Crystal PNG must be indexed: {path}')
    im=im.crop((0,0,canvas,canvas)); p=im.load(); return [[p[x,y] for x in range(canvas)] for y in range(canvas)]

def array_to_image(a):
    h=len(a); w=len(a[0]); im=Image.new('L',(w,h)); p=im.load()
    for y in range(h):
        for x in range(w): p[x,y]=a[y][x]
    return im

def image_to_array(im):
    p=im.load(); return [[p[x,y] for x in range(im.width)] for y in range(im.height)]

def transparent_roles(conv,src,palette):
    mapping,_,_=conv.semantic_mapping(src,palette); return conv.role_image(src,mapping),mapping

def projected_support(role,canvas,scale_mul=1.0):
    """Return a role-support map and an initial placed index image."""
    bbox=(lambda b:b)(role.getbbox())
    if bbox is None: raise ValueError('empty source role image')
    crop=role.crop(bbox); sw,sh=crop.size
    base=min(canvas/sw,canvas/sh,1.0); scale=min(canvas/sw,canvas/sh,base*scale_mul)
    if scale_mul>1.0 and base==1.0: scale=min(canvas/sw,canvas/sh,scale_mul)
    nw=max(1,round(sw*scale)); nh=max(1,round(sh*scale))
    if (nw,nh)!=(sw,sh): crop=conv_resize_roles(crop,nw,nh)
    ox=(canvas-nw)//2; oy=canvas-nh
    # final role image
    placed=Image.new('L',(canvas,canvas),0); pp=placed.load(); cp=crop.load()
    for y in range(nh):
        for x in range(nw):
            v=cp[x,y]
            if v!=TRANSPARENT: pp[ox+x,oy+y]=v
    # support: project every original source-role pixel into the placed geometry
    support=defaultdict(lambda:[0,0,0,0])
    sp=role.load(); bx0,by0,bx1,by1=bbox
    for sy in range(by0,by1):
        for sx in range(bx0,bx1):
            v=sp[sx,sy]
            if v==TRANSPARENT: continue
            rx=(sx-bx0+.5)/max(1,(bx1-bx0)); ry=(sy-by0+.5)/max(1,(by1-by0))
            x=min(canvas-1,max(0,ox+int(rx*nw))); y=min(canvas-1,max(0,oy+int(ry*nh)))
            support[(x,y)][v]+=1
    return support,placed,(bbox,nw,nh,ox,oy)

# bound at runtime to the converter's indexed resizer
conv_resize_roles=None

def boundary_pixels(a,ins):
    h=len(a); w=len(a[0]); b=set()
    for y in range(h):
        for x in range(w):
            if not ins[y][x]: continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                xx,yy=x+dx,y+dy
                if xx<0 or yy<0 or xx>=w or yy>=h or not ins[yy][xx]: b.add((x,y)); break
    return b

def role_candidates(a,support,role,prefer_nonblack=True):
    ins=inside_mask(a); bound=boundary_pixels(a,ins); rows=[]
    for (x,y),counts in support.items():
        if not ins[y][x] or counts[role]<=0: continue
        cur=a[y][x]
        penalty=0
        if prefer_nonblack and cur==3: penalty+=4
        if role!=3 and (x,y) in bound: penalty+=5
        if role==0 and (x,y) in bound: penalty+=3
        rows.append((counts[role]-penalty,sum(counts),x,y,cur))
    rows.sort(reverse=True)
    return rows

def ensure_role(a,support,role,target_count):
    m=metrics(a); need=max(0,target_count-m[f'n{role}']); changed=0
    if need<=0: return changed
    for score,total,x,y,cur in role_candidates(a,support,role):
        if need<=0: break
        if a[y][x]==role: continue
        a[y][x]=role; need-=1; changed+=1
    return changed

def demote_highlight(a,support,target_count):
    m=metrics(a); need=max(0,m['n0']-target_count); changed=0
    if need<=0:return 0
    ins=inside_mask(a); candidates=[]
    for y in range(len(a)):
        for x in range(len(a[0])):
            if ins[y][x] and a[y][x]==0:
                s=support.get((x,y),[0,0,0,0]); best=1 if s[1]>=s[2] else 2; strength=s[best]-s[0]
                candidates.append((strength,x,y,best))
    candidates.sort(reverse=True)
    for strength,x,y,best in candidates:
        if need<=0: break
        a[y][x]=best; need-=1; changed+=1
    return changed

def soften_black(a,support,target_count):
    m=metrics(a); need=max(0,m['n3']-target_count); changed=0
    if need<=0:return 0
    ins=inside_mask(a); bound=boundary_pixels(a,ins); candidates=[]
    for y in range(len(a)):
        for x in range(len(a[0])):
            if not ins[y][x] or a[y][x]!=3 or (x,y) in bound: continue
            s=support.get((x,y),[0,0,0,0]); best=1 if s[1]>=s[2] else 2; strength=s[best]-s[3]
            candidates.append((strength,x,y,best))
    candidates.sort(reverse=True)
    for strength,x,y,best in candidates:
        if need<=0: break
        a[y][x]=best; need-=1; changed+=1
    return changed

def strengthen_black(a,support,target_count):
    m=metrics(a); need=max(0,target_count-m['n3']); changed=0
    if need<=0:return 0
    ins=inside_mask(a); bound=boundary_pixels(a,ins); candidates=[]
    for x,y in bound:
        if a[y][x]==3: continue
        s=support.get((x,y),[0,0,0,0]); candidates.append((s[3],x,y))
    candidates.sort(reverse=True)
    for strength,x,y in candidates:
        if need<=0: break
        a[y][x]=3; need-=1; changed+=1
    return changed

def preview(a,palette,path,scale=4):
    h=len(a); w=len(a[0]); im=Image.new('RGB',(w,h)); p=im.load()
    for y in range(h):
        for x in range(w): p[x,y]=palette[a[y][x]]
    im.resize((w*scale,h*scale),Image.Resampling.NEAREST).save(path)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--converter',required=True); ap.add_argument('--source-root',required=True); ap.add_argument('--candidate-root',required=True); ap.add_argument('--output-root',required=True); ap.add_argument('--pokecrystal-root',required=True); ap.add_argument('--dimensions',required=True); ap.add_argument('--qa-tsv',required=True); ns=ap.parse_args()
    global conv_resize_roles
    conv=load_module('role_converter',ns.converter); conv_resize_roles=conv.resize_roles
    dims=conv.load_dims(ns.dimensions); names=conv.build_name_map(ns.pokecrystal_root)
    qa={}
    with Path(ns.qa_tsv).open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'): qa[int(r['species'])]=r
    srcroot=Path(ns.source_root); candroot=Path(ns.candidate_root); out=Path(ns.output_root)
    if out.exists(): shutil.rmtree(out)
    (out/'2BPP'/'FRONT').mkdir(parents=True); (out/'PREVIEW'/'FRONT').mkdir(parents=True)
    rows=[]
    species=list(range(1,201))+list(range(202,252))
    for sp in species:
        tiles=dims[sp]; canvas=tiles*8; q=qa[sp]; flags=set(filter(None,q['flags'].split(','))); name=names[sp]
        infile=candroot/'2BPP'/'FRONT'/f'{sp:03d}.{tiles}x{tiles}.2bpp'; outfile=out/'2BPP'/'FRONT'/infile.name
        ref=Path(ns.pokecrystal_root)/'gfx'/'pokemon'/name/'front.png'; pal=conv.crystal_palette(ref)
        orig=metrics(original_array(ref,canvas))
        before=decode_2bpp(infile.read_bytes(),tiles); before_m=metrics(before)
        if not flags:
            outfile.write_bytes(infile.read_bytes()); preview(before,pal,out/'PREVIEW'/'FRONT'/f'{sp:03d}.{tiles}x{tiles}.png')
            rows.append({'species':sp,'name':name,'action':'UNCHANGED_PASS','flags_before':'','changed_pixels':0,'area_before':before_m['area'],'area_after':before_m['area'],'p0_before':f"{before_m['p0']:.4f}",'p0_after':f"{before_m['p0']:.4f}",'p1_after':f"{before_m['p1']:.4f}",'p2_after':f"{before_m['p2']:.4f}",'p3_after':f"{before_m['p3']:.4f}"}); continue
        src=Image.open(srcroot/'FRONT'/f'{sp:03d}.png').convert('RGBA'); role,_=transparent_roles(conv,src,pal)
        # Geometry repair only when QA says silhouette is too small.
        scale_mul=1.0
        if 'SILHOUETTE_TOO_SMALL' in flags and before_m['area']:
            ratio=before_m['area']/max(1,orig['area']); scale_mul=min(1.24,max(1.04,math.sqrt(.92/max(.01,ratio))))
        support,placed,geom=projected_support(role,canvas,scale_mul)
        a=image_to_array(placed) if 'SILHOUETTE_TOO_SMALL' in flags else [row[:] for row in before]
        changed=sum(a[y][x]!=before[y][x] for y in range(canvas) for x in range(canvas))
        # Recompute support with repaired geometry (same projection already matches placed).
        m=metrics(a); area=max(1,m['area'])
        if 'COLOR1_MISSING' in flags:
            target=max(1,round(min(.12,max(.012,orig['p1']*.38))*area)); changed+=ensure_role(a,support,1,target)
        if 'COLOR2_MISSING' in flags:
            target=max(1,round(min(.12,max(.012,orig['p2']*.38))*area)); changed+=ensure_role(a,support,2,target)
        if 'HIGHLIGHT_TOO_WEAK' in flags:
            target=max(1,round(min(.22,max(.015,orig['p0']*.58))*area)); changed+=ensure_role(a,support,0,target)
        if 'HIGHLIGHT_TOO_HEAVY' in flags:
            target=max(1,round(min(.34,orig['p0']*1.55+.015)*area)); changed+=demote_highlight(a,support,target)
        if 'BLACK_TOO_HEAVY' in flags:
            target=max(1,round(min(.48,orig['p3']*1.55+.035)*area)); changed+=soften_black(a,support,target)
        if 'BLACK_TOO_THIN' in flags:
            target=max(1,round(max(.08,orig['p3']*.55)*area)); changed+=strengthen_black(a,support,target)
        after=metrics(a); outfile.write_bytes(encode_2bpp(a)); preview(a,pal,out/'PREVIEW'/'FRONT'/f'{sp:03d}.{tiles}x{tiles}.png')
        rows.append({'species':sp,'name':name,'action':'REPAIRED','flags_before':','.join(sorted(flags)),'changed_pixels':changed,'area_before':before_m['area'],'area_after':after['area'],'p0_before':f"{before_m['p0']:.4f}",'p0_after':f"{after['p0']:.4f}",'p1_after':f"{after['p1']:.4f}",'p2_after':f"{after['p2']:.4f}",'p3_after':f"{after['p3']:.4f}"})
    report=out/'REPAIR_REPORT.tsv'; fields=list(rows[0])
    with report.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); w.writeheader(); w.writerows(rows)
    print('unchanged',sum(r['action']=='UNCHANGED_PASS' for r in rows),'repaired',sum(r['action']=='REPAIRED' for r in rows))
if __name__=='__main__': main()
