#!/usr/bin/env python3
"""Build target-generation static candidates using full-animation union bounds.

This consumes:
  1) frame-0 full reconstruction (`*_rom_frame0_full.png`) whose battle anchor in
     the original prototype canvas is (96, 112), and
  2) `<dex>_animation_union.json` produced by `scan_bw_animation_union_bbox.py`.

The visible artwork remains the representative frame-0 pose, but its scale and
placement are constrained by the FULL legal animation union. This prevents a
static-looking conversion from choosing a scale that would necessarily clip if
Gen V motion is later reproduced.

No generative image tooling is used.
"""

from __future__ import annotations
import argparse
import json
import math
import pathlib
from collections import Counter
from PIL import Image

SOURCE_ANCHOR = (96, 112)
SAFE_MARGIN = 1
NAMES = {643: 'reshiram', 644: 'zekrom', 646: 'kyurem'}


def rgba(im):
    return im.convert('RGBA')


def luminance(c):
    r, g, b, _ = c
    return 0.2126*r + 0.7152*g + 0.0722*b


def quantize_gba(c):
    r, g, b, a = c
    if not a:
        return (0,0,0,0)
    def q(v):
        n = int(round(v * 31 / 255))
        return (n << 3) | (n >> 2)
    return (q(r), q(g), q(b), 255)


def palette_reduce_gen2(im):
    im = rgba(im)
    px = list(im.getdata())
    vis = [c for c in px if c[3]]
    if not vis:
        return im
    ordered = sorted(vis, key=luminance)
    reps = []
    for k in range(4):
        lo = int(len(ordered) * k / 4)
        hi = max(lo + 1, int(len(ordered) * (k + 1) / 4))
        bucket = ordered[lo:hi] or [ordered[min(lo, len(ordered)-1)]]
        reps.append((
            round(sum(c[0] for c in bucket) / len(bucket)),
            round(sum(c[1] for c in bucket) / len(bucket)),
            round(sum(c[2] for c in bucket) / len(bucket)),
            255,
        ))
    out = Image.new('RGBA', im.size, (0,0,0,0))
    sp = im.load(); op = out.load()
    for y in range(im.height):
        for x in range(im.width):
            c = sp[x,y]
            if not c[3]:
                continue
            op[x,y] = min(reps, key=lambda q:
                (c[0]-q[0])**2 + (c[1]-q[1])**2 + (c[2]-q[2])**2)
    return out


def preserve_resize(im, nw, nh):
    """Nearest center sample plus transparent-footprint restoration."""
    im = rgba(im)
    sw, sh = im.size
    src = list(im.getdata())
    out = [(0,0,0,0)] * (nw * nh)

    for oy in range(nh):
        sy = min(sh - 1, int((oy + 0.5) * sh / nh))
        for ox in range(nw):
            sx = min(sw - 1, int((ox + 0.5) * sw / nw))
            out[oy*nw + ox] = src[sy*sw + sx]

    for oy in range(nh):
        y0 = oy * sh / nh; y1 = (oy + 1) * sh / nh
        sy0 = max(0, int(math.floor(y0)))
        sy1 = min(sh - 1, int(math.ceil(y1) - 1))
        for ox in range(nw):
            pos = oy*nw + ox
            if out[pos][3]:
                continue
            x0 = ox * sw / nw; x1 = (ox + 1) * sw / nw
            sx0 = max(0, int(math.floor(x0)))
            sx1 = min(sw - 1, int(math.ceil(x1) - 1))
            samples = []
            for sy in range(sy0, sy1 + 1):
                for sx in range(sx0, sx1 + 1):
                    c = src[sy*sw + sx]
                    if c[3]:
                        samples.append(c)
            total = max(1, (sy1-sy0+1) * (sx1-sx0+1))
            if len(samples) >= 2 and len(samples) / total >= 0.28:
                cnt = Counter(samples)
                out[pos] = max(cnt, key=lambda c:(cnt[c], -luminance(c)))

    dst = Image.new('RGBA', (nw,nh), (0,0,0,0))
    dst.putdata(out)
    return dst


def safe_scale(union_rel, canvas_n):
    """Uniform scale that fits the whole anchor-relative union inside margins."""
    xmin, ymin, xmax, ymax = union_rel
    uw = xmax - xmin
    uh = ymax - ymin
    inner = canvas_n - 2*SAFE_MARGIN
    return min(inner / uw, inner / uh)


def target_anchor(union_rel, scale, canvas_n):
    """Choose anchor with bottom preference while keeping whole union in bounds."""
    xmin, ymin, xmax, ymax = union_rel

    ax_lo = SAFE_MARGIN - scale*xmin
    ax_hi = canvas_n - SAFE_MARGIN - scale*xmax
    ax = (ax_lo + ax_hi) / 2.0

    # Prefer union bottom to sit exactly at bottom safe margin.
    ay = canvas_n - SAFE_MARGIN - scale*ymax
    # Numerical guard: if top violates margin, push down/up as needed.
    top = ay + scale*ymin
    if top < SAFE_MARGIN:
        ay += SAFE_MARGIN - top
    bottom = ay + scale*ymax
    if bottom > canvas_n - SAFE_MARGIN:
        ay -= bottom - (canvas_n - SAFE_MARGIN)
    return ax, ay


def place_frame0(full_im, union_rel, canvas_n, generation):
    full_im = rgba(full_im)
    bbox = full_im.getbbox()
    if not bbox:
        return Image.new('RGBA', (canvas_n,canvas_n), (0,0,0,0)), {}

    crop = full_im.crop(bbox)
    # Anchor coordinate inside cropped frame-0 art.
    src_anchor_crop = (SOURCE_ANCHOR[0] - bbox[0], SOURCE_ANCHOR[1] - bbox[1])

    scale = safe_scale(union_rel, canvas_n)
    # Use the exact union-driven scale for the representative frame too.
    nw = max(1, round(crop.width * scale))
    nh = max(1, round(crop.height * scale))
    resized = preserve_resize(crop, nw, nh)

    if generation == 'gen3':
        rp = resized.load()
        for y in range(resized.height):
            for x in range(resized.width):
                rp[x,y] = quantize_gba(rp[x,y])
    elif generation == 'gen2':
        resized = palette_reduce_gen2(resized)
    else:
        raise ValueError(generation)

    ax, ay = target_anchor(union_rel, scale, canvas_n)
    scaled_anchor_in_crop = (src_anchor_crop[0]*scale, src_anchor_crop[1]*scale)
    px = round(ax - scaled_anchor_in_crop[0])
    py = round(ay - scaled_anchor_in_crop[1])

    canvas = Image.new('RGBA', (canvas_n,canvas_n), (0,0,0,0))
    canvas.alpha_composite(resized, (px,py))

    # Compute projected full-animation union after placement for verification.
    proj = [
        ax + scale*union_rel[0],
        ay + scale*union_rel[1],
        ax + scale*union_rel[2],
        ay + scale*union_rel[3],
    ]
    meta = {
        'source_frame0_bbox': list(bbox),
        'source_anchor': list(SOURCE_ANCHOR),
        'source_anchor_in_crop': list(src_anchor_crop),
        'union_anchor_relative': list(union_rel),
        'scale': scale,
        'scaled_frame0_size': [nw,nh],
        'target_anchor_float': [ax,ay],
        'frame0_placement': [px,py],
        'projected_animation_union_float': proj,
        'safe_margin': SAFE_MARGIN,
        'canvas': canvas_n,
    }
    return canvas, meta


def visible_stats(im):
    im = rgba(im)
    p = list(im.getdata())
    vis = [c for c in p if c[3]]
    return {
        'bbox': list(im.getbbox()) if im.getbbox() else None,
        'visible_pixels': len(vis),
        'visible_colors': len(set(c[:3] for c in vis)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/rom_reconstructed'))
    ap.add_argument('--unions', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_union'))
    ap.add_argument('--out', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/downscale_v4_animation_safe'))
    ap.add_argument('dex', nargs='*', type=int, default=[643,644,646])
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    manifest = []
    for dex in args.dex:
        name = NAMES.get(dex, str(dex))
        union_data = json.loads((args.unions / f'{dex}_animation_union.json').read_text('utf-8'))
        full = rgba(Image.open(args.frames / f'{dex}_rom_frame0_full.png'))
        entry = {'dex':dex, 'name':name, 'front':{}}

        union_rel = union_data['front']['union_bbox_anchor_relative']
        if union_rel is None:
            raise ValueError(f'{dex}: front animation union is empty')

        for generation, n in [('gen3',64), ('gen2',56)]:
            canvas, meta = place_frame0(full, union_rel, n, generation)
            out = args.out / f'{dex}_{name}_{generation}_{n}_animation_safe_v4.png'
            canvas.save(out)
            entry['front'][generation] = {**meta, **visible_stats(canvas), 'path':str(out)}

        manifest.append(entry)

    (args.out / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
