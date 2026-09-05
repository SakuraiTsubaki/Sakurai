#!/usr/bin/env python3
"""Convert HGSS battle sprite PNGs into Pokémon Crystal-compatible static 2bpp/LZ assets."""
import argparse, csv, hashlib
from pathlib import Path
from PIL import Image
BITREV=bytes(int(f'{i:08b}'[::-1],2) for i in range(256))

def load_dimensions(path):
    dims={}
    with Path(path).open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'): dims[int(r['species'])]=int(r['front_tiles'])
    if set(dims)!=set(range(1,252)) or any(d not in (5,6,7) for d in dims.values()): raise ValueError('invalid 251-species dimension map')
    return dims

def pick_three_colors(im):
    px=[p[:3] for p in im.getdata() if p[3]>=128]
    if not px: raise ValueError('empty visible sprite')
    strip=Image.new('RGB',(len(px),1)); strip.putdata(px)
    q=strip.quantize(colors=3,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE); pal=q.getpalette()[:9]
    colors=[tuple(pal[i:i+3]) for i in range(0,9,3)]; uniq=[]
    for c in colors:
        if c not in uniq: uniq.append(c)
    for c in ((224,224,224),(112,112,112),(0,0,0)):
        if len(uniq)>=3: break
        if c not in uniq: uniq.append(c)
    lum=lambda c:0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
    return sorted(uniq[:3],key=lum,reverse=True)

def png_to_indexed(path,canvas):
    im=Image.open(path).convert('RGBA'); bbox=im.getchannel('A').getbbox()
    if bbox is None: raise ValueError(f'empty sprite: {path}')
    crop=im.crop(bbox); scale=min(canvas/crop.width,canvas/crop.height,1.0)
    nw=max(1,round(crop.width*scale)); nh=max(1,round(crop.height*scale)); crop=crop.resize((nw,nh),Image.Resampling.NEAREST)
    colors=pick_three_colors(crop); idx=Image.new('L',(canvas,canvas),0); src=crop.load(); dst=idx.load(); ox=(canvas-nw)//2; oy=canvas-nh
    for y in range(nh):
        for x in range(nw):
            r,g,b,a=src[x,y]
            if a<128: continue
            rgb=(r,g,b); j=min(range(3),key=lambda i:sum((rgb[k]-colors[i][k])**2 for k in range(3)))
            dst[ox+x,oy+y]=1+j
    return idx,colors

def indexed_to_2bpp(idx):
    w,h=idx.size; p=idx.load(); out=bytearray()
    if w%8 or h%8: raise ValueError('non-tile-aligned canvas')
    for ty in range(0,h,8):
        for tx in range(0,w,8):
            for y in range(8):
                lo=hi=0
                for x in range(8):
                    v=p[tx+x,ty+y]&3; bit=7-x; lo|=(v&1)<<bit; hi|=((v>>1)&1)<<bit
                out.extend((lo,hi))
    return bytes(out)

def emit(cmd,count,payload=b''):
    n=count-1
    return (bytes([(cmd<<5)|n]) if count<=32 else bytes([0xE0|(cmd<<2)|((n>>8)&3),n&255]))+payload

def best_repeat(data,pos):
    best=(0,0); first=data[pos]; candidates=[]
    for s in range(pos-1,max(-1,pos-513),-1):
        if data[s]==first: candidates.append(s)
    if pos>512:
        step=max(1,pos//256)
        candidates += [s for s in range(0,pos-512,step) if data[s]==first]
    for s in candidates:
        m=min(1024,len(data)-pos); k=0
        while k<m and s+k<pos and data[s+k]==data[pos+k]: k+=1
        if k and s+k==pos:
            period=pos-s
            while k<m and data[s+(k%period)]==data[pos+k]: k+=1
        if k>best[0]: best=(k,s)
    return best

def lz_compress(data):
    data=bytes(data); out=bytearray(); pos=0; lit=bytearray()
    def flush():
        nonlocal lit
        while lit:
            n=min(len(lit),1024); out.extend(emit(0,n,bytes(lit[:n]))); del lit[:n]
    while pos<len(data):
        rem=len(data)-pos; z=0
        while z<min(1024,rem) and data[pos+z]==0: z+=1
        r=1
        while r<min(1024,rem) and data[pos+r]==data[pos]: r+=1
        a=0
        if rem>=2:
            x,y=data[pos],data[pos+1]
            while a<min(1024,rem) and data[pos+a]==(x if a%2==0 else y): a+=1
        rep,src=best_repeat(data,pos); choices=[]
        if z>=2: choices.append((z-1,3,z,b''))
        if r>=3: choices.append((r-2,1,r,bytes([data[pos]])))
        if a>=4: choices.append((a-3,2,a,bytes(data[pos:pos+2])))
        if rep>=4:
            dist=pos-src; payload=bytes([0x80|(dist-1)]) if 1<=dist<=128 else bytes([(src>>8)&255,src&255]); choices.append((rep-(1+len(payload)),4,rep,payload))
        if choices:
            _,cmd,n,p=max(choices,key=lambda x:(x[0],x[2])); flush(); out.extend(emit(cmd,n,p)); pos+=n
        else:
            lit.append(data[pos]); pos+=1
            if len(lit)==1024: flush()
    flush(); out.append(0xff); return bytes(out)

def lz_decompress(buf):
    out=bytearray(); pos=0
    while True:
        c=buf[pos]; pos+=1
        if c==0xff: break
        cmd=c>>5; n=c&31
        if cmd==7: cmd=n>>2; n=((n&3)<<8)|buf[pos]; pos+=1
        count=n+1
        if cmd==0: out.extend(buf[pos:pos+count]); pos+=count
        elif cmd==1: out.extend([buf[pos]]*count); pos+=1
        elif cmd==2:
            a,b=buf[pos],buf[pos+1]; pos+=2; out.extend(a if i%2==0 else b for i in range(count))
        elif cmd==3: out.extend(b'\0'*count)
        elif cmd in (4,5,6):
            a=buf[pos]; pos+=1
            if a&0x80: src=len(out)-((a&0x7f)+1)
            else: b=buf[pos]; pos+=1; src=(a<<8)|b
            if cmd==4:
                for i in range(count): out.append(out[src+i])
            elif cmd==5:
                for i in range(count): out.append(BITREV[out[src+i]])
            else:
                for i in range(count): out.append(out[src-i])
        else: raise ValueError(cmd)
    return bytes(out)

def rgb5(c): return tuple(max(0,min(31,round(v*31/255))) for v in c)
def gbc(c):
    r,g,b=rgb5(c); v=r|(g<<5)|(b<<10); return bytes((v&255,v>>8))
def sha(data): return hashlib.sha256(data).hexdigest()
def side(path,tiles):
    idx,colors=png_to_indexed(path,tiles*8); raw=indexed_to_2bpp(idx); enc=lz_compress(raw)
    if lz_decompress(enc)!=raw: raise AssertionError(f'LZ mismatch: {path}')
    return raw,enc,colors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-root',required=True); ap.add_argument('--output-root',required=True); ap.add_argument('--dimensions',required=True); ap.add_argument('--start',type=int,default=1); ap.add_argument('--end',type=int,default=251); ns=ap.parse_args()
    if not 1<=ns.start<=ns.end<=251: raise SystemExit('invalid range')
    src=Path(ns.source_root); out=Path(ns.output_root); dims=load_dimensions(ns.dimensions); rows=[]; prows=[]
    for sp in range(ns.start,ns.end+1):
        fp=src/'FRONT'/f'{sp:03d}.png'; bp=src/'BACK'/f'{sp:03d}.png'; d=dims[sp]
        if not fp.is_file() or not bp.is_file(): raise FileNotFoundError(f'missing source #{sp:03d}')
        fr,flz,fc=side(fp,d); br,blz,bc=side(bp,6)
        files=[(out/'2BPP'/'FRONT'/f'{sp:03d}.{d}x{d}.2bpp',fr),(out/'2BPP'/'BACK'/f'{sp:03d}.6x6.2bpp',br),(out/'LZ'/'FRONT'/f'{sp:03d}.{d}x{d}.2bpp.lz',flz),(out/'LZ'/'BACK'/f'{sp:03d}.6x6.2bpp.lz',blz),(out/'PALETTES'/'NORMAL_MIDDLE'/f'{sp:03d}.gbcpal',gbc(fc[0])+gbc(fc[1]))]
        for p,data in files: p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
        rows += [[f'{sp:03d}','front',d,d,len(fr),len(flz),sha(fr),sha(flz),str(fp)],[f'{sp:03d}','back',6,6,len(br),len(blz),sha(br),sha(blz),str(bp)]]
        a,b=rgb5(fc[0]),rgb5(fc[1]); prows.append([f'{sp:03d}',*fc[0],*fc[1],*a,*b,(gbc(fc[0])+gbc(fc[1])).hex()]); print(f'#{sp:03d}: F {d}x{d} {len(fr)}->{len(flz)} B 6x6 {len(br)}->{len(blz)}')
    rf=['species','side','tiles_w','tiles_h','raw_bytes','lz_bytes','raw_sha256','lz_sha256','source_path']; rp=out/'CONVERSION_MANIFEST.tsv'; old={}
    if rp.exists():
        with rp.open(encoding='utf-8',newline='') as f:
            for r in csv.DictReader(f,delimiter='\t'): old[(r['species'],r['side'])]=r
    for r in rows: old[(r[0],r[1])]=dict(zip(rf,map(str,r)))
    with rp.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rf,delimiter='\t'); w.writeheader(); [w.writerow(old[k]) for k in sorted(old,key=lambda x:(int(x[0]),x[1]))]
    pf=['species','light_r8','light_g8','light_b8','mid_r8','mid_g8','mid_b8','light_r5','light_g5','light_b5','mid_r5','mid_g5','mid_b5','gbcpal_hex']; pp=out/'NORMAL_PALETTE_MANIFEST.tsv'; po={}
    if pp.exists():
        with pp.open(encoding='utf-8',newline='') as f:
            for r in csv.DictReader(f,delimiter='\t'): po[r['species']]=r
    for r in prows: po[r[0]]=dict(zip(pf,map(str,r)))
    with pp.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=pf,delimiter='\t'); w.writeheader(); [w.writerow(po[k]) for k in sorted(po,key=int)]
if __name__=='__main__': main()
