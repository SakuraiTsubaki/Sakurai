from PIL import Image
from pathlib import Path
from collections import Counter
import colorsys, json, math

SRC = Path('/mnt/data/sprite_preserve_trial/rom_reconstructed')
OUT = Path('/mnt/data/sprite_preserve_trial/downscale_v3')
OUT.mkdir(parents=True, exist_ok=True)

NAMES = {643:'Reshiram', 644:'Zekrom', 646:'Kyurem'}


def q5(c):
    return tuple(min(255, round(round(float(v) * 31 / 255) * 255 / 31)) for v in c[:3])


def lum(c):
    return .2126*c[0] + .7152*c[1] + .0722*c[2]


def sat(c):
    return colorsys.rgb_to_hsv(*(x/255 for x in c[:3]))[1]


def fit_canvas(src, n, inset=1):
    """Preserve full alpha silhouette; bottom-align and horizontally center without clipping."""
    src = src.convert('RGBA')
    bbox = src.getchannel('A').getbbox()
    if not bbox:
        return Image.new('RGBA', (n,n), (0,0,0,0)), 1.0
    cr = src.crop(bbox)
    maxw = n - inset*2
    maxh = n - inset*2
    scale = min(maxw/cr.width, maxh/cr.height)
    tw = max(1, int(math.floor(cr.width * scale)))
    th = max(1, int(math.floor(cr.height * scale)))
    # nearest is only the initial geometry pass; later functions repixel/requantize.
    z = cr.resize((tw, th), Image.Resampling.NEAREST)
    out = Image.new('RGBA', (n,n), (0,0,0,0))
    x = (n - tw)//2
    y = n - inset - th
    out.alpha_composite(z, (x,y))
    return out, scale


def gen3(src, n=64):
    base, scale = fit_canvas(src, n, inset=1)
    px = list(base.getdata())
    cnt = Counter((r,g,b) for r,g,b,a in px if a)
    pal=[]
    for c,_ in cnt.most_common():
        z=q5(c)
        if z not in pal: pal.append(z)
    pal=pal[:14]
    out=Image.new('RGBA',(n,n),(0,0,0,0)); op=out.load(); bp=base.load()
    for y in range(n):
        for x in range(n):
            r,g,b,a=bp[x,y]
            if not a: continue
            qc=q5((r,g,b))
            if qc not in pal:
                qc=min(pal,key=lambda p:sum((p[i]-qc[i])**2 for i in range(3)))
            op[x,y]=(*qc,255)
    return out, scale


def gen2_palette(src):
    cnt=Counter((r,g,b) for r,g,b,a in src.getdata() if a)
    total=sum(cnt.values()) or 1
    candidates=[]
    for c,n in cnt.most_common():
        if lum(c)>245 or lum(c)<24: continue
        candidates.append((c,n))
    body=q5(candidates[0][0]) if candidates else (165,165,165)
    accent=None
    for c,n in candidates:
        qc=q5(c)
        d=sum((qc[i]-body[i])**2 for i in range(3))**.5
        if n/total>=.025 and sat(c)>=.30 and d>48:
            accent=qc; break
    if accent is None:
        accent=(82,82,82)
        for c,n in candidates[1:]:
            qc=q5(c)
            if sum((qc[i]-body[i])**2 for i in range(3))**.5>28:
                accent=qc; break
    mids=sorted([body,accent],key=lum,reverse=True)
    return [(255,255,255), mids[0], mids[1], (0,0,0)]


def gen2(src, n=56):
    base, scale = fit_canvas(src, n, inset=1)
    pal=gen2_palette(src)
    out=Image.new('RGBA',(n,n),(0,0,0,0)); op=out.load(); bp=base.load()
    for y in range(n):
        for x in range(n):
            r,g,b,a=bp[x,y]
            if not a: continue
            c=min(pal,key=lambda p:sum((p[i]-v)**2 for i,v in enumerate((r,g,b))))
            op[x,y]=(*c,255)
    return out, pal, scale


def stats(im):
    a=im.getchannel('A'); bbox=a.getbbox()
    colors=set((r,g,b) for r,g,b,a in im.getdata() if a)
    return {'bbox':bbox,'colors':len(colors),'visible_pixels':sum(1 for *_,a in im.getdata() if a)}

manifest=[]
for dex,name in NAMES.items():
    # v3 MASTER SOURCE: complete alpha crop reconstructed from 192x128 composition canvas.
    src=Image.open(SRC/f'{dex}_rom_frame0_crop.png').convert('RGBA')
    g3,s3=gen3(src,64)
    g2,p2,s2=gen2(src,56)
    g3.save(OUT/f'{dex}_{name.lower()}_gen3_64_preserve_v3.png')
    g2.save(OUT/f'{dex}_{name.lower()}_gen2_56_preserve_v3.png')
    manifest.append({
        'dex':dex,'name':name,'source_complete_size':src.size,
        'gen3_scale':s3,'gen2_scale':s2,'gen2_palette':p2,
        'source':stats(src),'gen3_v3':stats(g3),'gen2_v3':stats(g2)
    })

(OUT/'manifest_v3.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
