from PIL import Image, ImageDraw
from pathlib import Path
from collections import Counter
import json, math

SRC = Path('/mnt/data/sprite_preserve_trial/rom_reconstructed')
OLD = Path('/mnt/data/sprite_preserve_trial/downscale_v2')
OUT = Path('/mnt/data/sprite_preserve_trial/downscale_v3_uncropped')
OUT.mkdir(parents=True, exist_ok=True)

NAMES = {643:'reshiram', 644:'zekrom', 646:'kyurem'}
TARGETS = {'gen3':64, 'gen2':56}
SAFE_MARGIN = 1


def rgba(im):
    return im.convert('RGBA')


def visible_bbox(im):
    return rgba(im).getbbox()


def quantize_gba(c):
    r,g,b,a = c
    if not a:
        return (0,0,0,0)
    def q(v):
        n = int(round(v * 31 / 255))
        return (n << 3) | (n >> 2)
    return (q(r), q(g), q(b), 255)


def luminance(c):
    r,g,b,_ = c
    return 0.2126*r + 0.7152*g + 0.0722*b


def palette_reduce_gen2(im):
    """Reduce visible pixels to 4 total sprite colors: darkest, dark-mid, light-mid, lightest.
    Transparent remains transparent and is not counted as one of the four visible colors.
    This is an automatic preservation candidate, not final manual pixel art.
    """
    im = rgba(im)
    px = list(im.getdata())
    vis = [c for c in px if c[3]]
    if not vis:
        return im

    # Use luminance quartile representatives, but keep chroma by averaging RGB inside each bucket.
    ordered = sorted(vis, key=luminance)
    reps = []
    for k in range(4):
        lo = int(len(ordered) * k / 4)
        hi = max(lo + 1, int(len(ordered) * (k+1) / 4))
        bucket = ordered[lo:hi]
        if not bucket:
            bucket = [ordered[min(lo, len(ordered)-1)]]
        reps.append((
            round(sum(c[0] for c in bucket)/len(bucket)),
            round(sum(c[1] for c in bucket)/len(bucket)),
            round(sum(c[2] for c in bucket)/len(bucket)),
            255
        ))

    out = Image.new('RGBA', im.size, (0,0,0,0))
    op = out.load(); sp = im.load()
    for y in range(im.height):
        for x in range(im.width):
            c = sp[x,y]
            if not c[3]:
                continue
            op[x,y] = min(reps, key=lambda q: (c[0]-q[0])**2 + (c[1]-q[1])**2 + (c[2]-q[2])**2)
    return out


def fit_dimensions(sw, sh, canvas):
    inner = canvas - SAFE_MARGIN*2
    scale = min(inner/sw, inner/sh)
    return max(1, round(sw*scale)), max(1, round(sh*scale))


def preserve_resize(im, nw, nh):
    """Nearest baseline plus footprint restoration. No RGB interpolation."""
    im = rgba(im)
    sw,sh = im.size
    src = list(im.getdata())
    out = [(0,0,0,0)] * (nw*nh)

    # Center-sample nearest baseline.
    for oy in range(nh):
        sy = min(sh-1, int((oy+0.5)*sh/nh))
        for ox in range(nw):
            sx = min(sw-1, int((ox+0.5)*sw/nw))
            out[oy*nw+ox] = src[sy*sw+sx]

    # Restore source footprint when an output cell incorrectly became transparent.
    for oy in range(nh):
        y0 = oy*sh/nh; y1 = (oy+1)*sh/nh
        sy0 = max(0, int(math.floor(y0))); sy1 = min(sh-1, int(math.ceil(y1)-1))
        for ox in range(nw):
            pos = oy*nw+ox
            if out[pos][3]:
                continue
            x0 = ox*sw/nw; x1 = (ox+1)*sw/nw
            sx0 = max(0, int(math.floor(x0))); sx1 = min(sw-1, int(math.ceil(x1)-1))
            samples=[]
            for sy in range(sy0, sy1+1):
                for sx in range(sx0, sx1+1):
                    c=src[sy*sw+sx]
                    if c[3]: samples.append(c)
            total=max(1,(sy1-sy0+1)*(sx1-sx0+1))
            if len(samples)>=2 and len(samples)/total>=0.28:
                cnt=Counter(samples)
                out[pos]=max(cnt, key=lambda c:(cnt[c], -luminance(c)))

    dst=Image.new('RGBA',(nw,nh),(0,0,0,0)); dst.putdata(out)
    return dst


def place_on_canvas(sprite, n):
    """Horizontal center, bottom-safe alignment. Never crops the sprite."""
    canvas = Image.new('RGBA',(n,n),(0,0,0,0))
    x = (n - sprite.width)//2
    y = n - SAFE_MARGIN - sprite.height
    if x < SAFE_MARGIN: x = SAFE_MARGIN
    if y < SAFE_MARGIN: y = SAFE_MARGIN
    canvas.alpha_composite(sprite,(x,y))
    return canvas, (x,y)


def stats(im):
    px=list(rgba(im).getdata())
    vis=[c for c in px if c[3]]
    return {
        'size': list(im.size),
        'bbox': list(im.getbbox()) if im.getbbox() else None,
        'visible_pixels': len(vis),
        'visible_colors': len(set((c[0],c[1],c[2]) for c in vis))
    }


def checker(size, cell=8):
    bg=Image.new('RGBA',size,(236,236,236,255)); d=ImageDraw.Draw(bg)
    for y in range(0,size[1],cell):
        for x in range(0,size[0],cell):
            if ((x//cell)+(y//cell))&1:
                d.rectangle((x,y,x+cell-1,y+cell-1),fill=(208,208,208,255))
    return bg


def zoom(im, box=256):
    scale=max(1,min(box//im.width, box//im.height))
    z=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
    bg=checker((box,box),16)
    bg.alpha_composite(z,((box-z.width)//2,(box-z.height)//2))
    return bg

manifest=[]
comparison_rows=[]

for dex,name in NAMES.items():
    source_path = SRC / f'{dex}_rom_frame0_crop.png'
    source = rgba(Image.open(source_path))
    entry={'dex':dex,'name':name,'source_uncropped':stats(source),'outputs':{}}

    row=[zoom(source)]
    for target,n in TARGETS.items():
        nw,nh=fit_dimensions(source.width, source.height, n)
        resized=preserve_resize(source,nw,nh)
        if target=='gen3':
            resized=resized.point(lambda v:v)  # keep alpha/data path explicit
            rp=resized.load()
            for y in range(resized.height):
                for x in range(resized.width):
                    rp[x,y]=quantize_gba(rp[x,y])
        else:
            resized=palette_reduce_gen2(resized)

        canvas,pos=place_on_canvas(resized,n)
        out_path=OUT/f'{dex}_{name}_{target}_{n}_preserve_v3_uncropped.png'
        canvas.save(out_path)
        entry['outputs'][target]={
            **stats(canvas),
            'scaled_sprite_size':[nw,nh],
            'placement':list(pos),
            'safe_margin':SAFE_MARGIN,
            'source':'full alpha bbox, not 96x96 crop'
        }
        row.append(zoom(canvas))

    manifest.append(entry)
    comparison_rows.append(row)

# Combined comparison: uncropped source / Gen III v3 / Gen II v3
cell=256; cols=3; rows=len(comparison_rows)
sheet=Image.new('RGBA',(cell*cols,cell*rows),(255,255,255,255))
for ry,row in enumerate(comparison_rows):
    for cx,im in enumerate(row):
        sheet.alpha_composite(im,(cx*cell,ry*cell))
sheet.save(OUT/'bw_legendaries_v3_uncropped_comparison.png')

(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
