#!/usr/bin/env python3
"""Scan BW battle-sprite animation geometry and compute unclipped union bounds.

Purpose
-------
The earlier frame-0 prototype rendered a multipart BW sprite into 192x128 and then
cropped a fixed 96x96 window. That is useful for inspection, but it can clip wide
Pokemon. This scanner removes the fixed-window assumption.

For each requested species it scans BOTH:
  front: NCGR +2, NCER +4, NANR +5, NMCR +6
  back : NCGR +11, NCER +13, NANR +14, NMCR +15
within the species' 20-member /a/0/0/4 block.

It walks every NANR frame referenced by NMCR map 0, renders geometry on a large
canvas, records per-frame-element bounds, and computes a spatial union. The union
is expressed both in canvas coordinates and relative to the battle anchor.

This is a geometry/coverage scanner. It intentionally does NOT assume that all
animation elements are synchronized to the same frame index. For safe clipping
bounds that is unnecessary: the spatial union of each referenced element's legal
frames is the exact set of positions that can ever be occupied by that element.

No generative image tooling is involved; all geometry comes from the ROM archive.
"""

from __future__ import annotations
import argparse
import json
import math
import pathlib
import struct
from dataclasses import dataclass
from typing import Iterable

from PIL import Image

OBJ_SIZES = [
    [(8, 8), (16, 8), (8, 16), (0, 0)],
    [(16, 16), (32, 8), (8, 32), (0, 0)],
    [(32, 32), (32, 16), (16, 32), (0, 0)],
    [(64, 64), (64, 32), (32, 64), (0, 0)],
]

CANVAS_W = 768
CANVAS_H = 768
ANCHOR_X = 384
ANCHOR_Y = 384


def s8(v: int) -> int:
    return v - 256 if v >= 128 else v


def s9(v: int) -> int:
    return v - 512 if v >= 256 else v


def union_bbox(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (
        min(a[0], b[0]), min(a[1], b[1]),
        max(a[2], b[2]), max(a[3], b[3]),
    )


def bbox_relative_to_anchor(b):
    if b is None:
        return None
    return [b[0] - ANCHOR_X, b[1] - ANCHOR_Y,
            b[2] - ANCHOR_X, b[3] - ANCHOR_Y]


def lz11(data: bytes) -> bytes:
    if not data or data[0] != 0x11:
        return data
    n = data[1] | (data[2] << 8) | (data[3] << 16)
    si = 4
    out = bytearray()
    while len(out) < n:
        flags = data[si]
        si += 1
        for bit in range(7, -1, -1):
            if len(out) >= n:
                break
            if not ((flags >> bit) & 1):
                out.append(data[si])
                si += 1
                continue
            b1 = data[si]
            si += 1
            h = b1 >> 4
            if h == 0:
                b2, b3 = data[si:si + 2]
                si += 2
                ln = (((b1 & 15) << 4) | (b2 >> 4)) + 0x11
                disp = (((b2 & 15) << 8) | b3) + 1
            elif h == 1:
                b2, b3, b4 = data[si:si + 3]
                si += 3
                ln = (((b1 & 15) << 12) | (b2 << 4) | (b3 >> 4)) + 0x111
                disp = (((b3 & 15) << 8) | b4) + 1
            else:
                b2 = data[si]
                si += 1
                ln = h + 1
                disp = (((b1 & 15) << 8) | b2) + 1
            for _ in range(ln):
                out.append(out[-disp])
    return bytes(out[:n])


class Narc:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.data = path.read_bytes()
        d = self.data
        if d[:4] != b'NARC':
            raise ValueError(f'not NARC: {path}')
        pos = 0x10
        fat_size = struct.unpack_from('<I', d, pos + 4)[0]
        count = struct.unpack_from('<H', d, pos + 8)[0]
        self.fat = [struct.unpack_from('<II', d, pos + 12 + i * 8)
                    for i in range(count)]
        pos2 = pos + fat_size
        pos3 = pos2 + struct.unpack_from('<I', d, pos2 + 4)[0]
        self.gmif_base = pos3 + 8

    def member(self, i: int) -> bytes:
        s, e = self.fat[i]
        return lz11(self.data[self.gmif_base + s:self.gmif_base + e])


def parse_ncgr(d: bytes):
    _mg, _size, h_tiles, w_tiles, bit, vram, tiled, dsize, _unk = \
        struct.unpack_from('<4sIHHIIIII', d, 16)
    raw = d[48:48 + dsize]
    pix = []
    for b in raw:
        pix += [b & 15, b >> 4]
    return {
        'w': w_tiles * 8, 'h': h_tiles * 8,
        'pix': pix, 'vram': vram, 'tiled': tiled, 'bit': bit,
    }


def get_cell_pixels(g, tile, w, h):
    if (g['tiled'] & 0xff) == 0:
        raise NotImplementedError('linear NCGR not handled by this BW scanner')
    tiles_per_row = g['w'] // 8
    start_y = (tile // tiles_per_row) * 8
    start_x = (tile % tiles_per_row) * 8
    out = [0] * (w * h)
    for y in range(h):
        sy = start_y + y
        if sy >= g['h']:
            break
        st = sy * g['w'] + start_x
        row = g['pix'][st:st + w]
        out[y * w:y * w + len(row)] = row
    return out


def parse_ncer(d: bytes):
    _mg, _size, cell_count, cell_type, _cdo, _flags, _pdo, _p1, _p2 = \
        struct.unpack_from('<4sIHHIIIII', d, 16)
    off = 48
    cells = []
    for _ in range(cell_count):
        obj_count, unk, obj_off = struct.unpack_from('<HHI', d, off)
        off += 8
        ext = None
        if cell_type == 1:
            ext = struct.unpack_from('<hhhh', d, off)
            off += 8
        cells.append((obj_count, unk, obj_off, ext))
    return {'cells': cells, 'obj_base': off, 'data': d}


def get_objs(ncer, cell_idx):
    obj_count, _unk, obj_off, _ext = ncer['cells'][cell_idx]
    d = ncer['data']
    base = ncer['obj_base'] + obj_off
    arr = []
    for j in range(obj_count):
        a0, a1, a2 = struct.unpack_from('<HHH', d, base + j * 6)
        arr.append({
            'y': s8(a0 & 255),
            'rs': (a0 >> 8) & 3,
            'mode': (a0 >> 10) & 3,
            'mosaic': (a0 >> 12) & 1,
            'color_mode': (a0 >> 13) & 1,
            'shape': (a0 >> 14) & 3,
            'x': s9(a1 & 0x1ff),
            'rs_param': (a1 >> 9) & 31,
            'size': (a1 >> 14) & 3,
            'tile': a2 & 0x3ff,
            'priority': (a2 >> 10) & 3,
            'pal': (a2 >> 12) & 15,
        })
    return arr


def parse_nanr(d: bytes):
    _mg, _size, anim_count, _frame_total, aoff, foff, fdoff, _p1, _p2 = \
        struct.unpack_from('<4sIHHIIIII', d, 16)
    A = lambda o: 24 + o
    acells = [struct.unpack_from('<IHHII', d, A(aoff) + i * 16)
              for i in range(anim_count)]
    return {
        'data': d,
        'acells': acells,
        'frames_base': A(foff),
        'fdata_base': A(fdoff),
    }


def anim_frame(nanr, anim_idx, frame_idx):
    frame_count, frame_type, cell_type, unk, frames_off = nanr['acells'][anim_idx]
    if frame_idx >= frame_count:
        raise IndexError(frame_idx)
    ent = nanr['frames_base'] + frames_off + frame_idx * 8
    data_off, duration, pad = struct.unpack_from('<IHH', nanr['data'], ent)
    p = nanr['fdata_base'] + data_off
    if frame_type == 0:
        cell_idx, _u = struct.unpack_from('<HH', nanr['data'], p)
        matrix = (256, 0, 0, 256)
        co = (0, 0)
    elif frame_type == 1:
        cell_idx, theta, xmag, ymag, x, y = struct.unpack_from('<HhIIhh', nanr['data'], p)
        st = int(math.sin(theta * 2 * math.pi / 65536) * 4096)
        ct = int(math.cos(theta * 2 * math.pi / 65536) * 4096)
        matrix = (int(256 * ct / xmag), int(256 * st / xmag),
                  int(-256 * st / ymag), int(256 * ct / ymag))
        co = (x, y)
    elif frame_type == 2:
        cell_idx, _pad, x, y = struct.unpack_from('<HHhh', nanr['data'], p)
        matrix = (256, 0, 0, 256)
        co = (x, y)
    else:
        raise ValueError(f'unsupported NANR frame type {frame_type}')
    return {
        'cell_idx': cell_idx,
        'matrix': matrix,
        'cell_offset': co,
        'duration': duration,
        'frame_type': frame_type,
        'cell_type': cell_type,
        'unk': unk,
    }


def parse_nmcr(d: bytes):
    _mg, _size, count, _pad, headers_off, data_off, _p1, _p2 = \
        struct.unpack_from('<4sIHHIIII', d, 16)
    A = lambda o: 24 + o
    headers = [struct.unpack_from('<HHI', d, A(headers_off) + i * 8)
               for i in range(count)]
    maps = []
    for elem_count, _hu, elem_off in headers:
        p = A(data_off) + elem_off
        maps.append([struct.unpack_from('<HhhBB', d, p + i * 8)
                     for i in range(elem_count)])
    return maps


def draw_cell_mask(g, ncer, cell_idx, frame_offset, matrix):
    """Render one NCER cell as a 1-bit alpha mask on the large canvas."""
    canvas = Image.new('1', (CANVAS_W, CANVAS_H), 0)
    cp = canvas.load()

    for o in get_objs(ncer, cell_idx):
        cw, ch = OBJ_SIZES[o['size']][o['shape']]
        if cw == 0 or ch == 0:
            continue
        src = get_cell_pixels(g, o['tile'], cw, ch)
        fw, fh = cw, ch
        if o['rs'] & 2:
            fw *= 2
            fh *= 2
        tx, ty = fw // 2, fh // 2
        rs = o['rs']

        for y in range(fh):
            dy = o['y'] + frame_offset[1] + y
            if dy < 0 or dy >= CANVAS_H:
                continue
            for x in range(fw):
                dx = o['x'] + frame_offset[0] + x
                if dx < 0 or dx >= CANVAS_W:
                    continue
                if rs & 1:
                    xp = (((x - tx) * matrix[0] + (y - ty) * matrix[1]) >> 8) + tx
                    yp = (((x - tx) * matrix[2] + (y - ty) * matrix[3]) >> 8) + ty
                else:
                    xp, yp = x, y
                if rs & 2:
                    xp -= cw // 2
                    yp -= ch // 2
                if 0 <= xp < cw and 0 <= yp < ch:
                    if src[yp * cw + xp] != 0:
                        cp[dx, dy] = 1
    return canvas


def scan_side(narc: Narc, dex: int, side: str):
    base = dex * 20
    if side == 'front':
        rel = {'ncgr': 2, 'ncer': 4, 'nanr': 5, 'nmcr': 6}
    elif side == 'back':
        rel = {'ncgr': 11, 'ncer': 13, 'nanr': 14, 'nmcr': 15}
    else:
        raise ValueError(side)

    g = parse_ncgr(narc.member(base + rel['ncgr']))
    ncer = parse_ncer(narc.member(base + rel['ncer']))
    nanr = parse_nanr(narc.member(base + rel['nanr']))
    maps = parse_nmcr(narc.member(base + rel['nmcr']))
    if not maps:
        raise ValueError(f'{dex} {side}: NMCR contains no maps')

    union = None
    records = []
    map0 = maps[0]

    for elem_idx, (anim_idx, map_x, map_y, unk, priority) in enumerate(map0):
        if anim_idx >= len(nanr['acells']):
            records.append({
                'element': elem_idx, 'animation': anim_idx,
                'error': 'animation index outside NANR acell table',
            })
            continue
        frame_count = nanr['acells'][anim_idx][0]
        for fi in range(frame_count):
            fr = anim_frame(nanr, anim_idx, fi)
            fo = (
                ANCHOR_X + map_x + fr['cell_offset'][0],
                ANCHOR_Y + map_y + fr['cell_offset'][1],
            )
            mask = draw_cell_mask(g, ncer, fr['cell_idx'], fo, fr['matrix'])
            b = mask.getbbox()
            union = union_bbox(union, b)
            records.append({
                'element': elem_idx,
                'animation': anim_idx,
                'frame': fi,
                'frame_count': frame_count,
                'duration': fr['duration'],
                'cell': fr['cell_idx'],
                'frame_type': fr['frame_type'],
                'map_offset': [map_x, map_y],
                'cell_offset': list(fr['cell_offset']),
                'bbox_canvas': list(b) if b else None,
                'bbox_anchor_relative': bbox_relative_to_anchor(b),
                'priority': priority,
                'unknown': unk,
            })

    if union is None:
        size = None
    else:
        size = [union[2] - union[0], union[3] - union[1]]

    return {
        'side': side,
        'members': {k: base + v for k, v in rel.items()},
        'nmcr_map_index': 0,
        'map_elements': len(map0),
        'nanr_animations': len(nanr['acells']),
        'scanned_element_frames': len(records),
        'union_bbox_canvas': list(union) if union else None,
        'union_bbox_anchor_relative': bbox_relative_to_anchor(union),
        'union_size': size,
        'records': records,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--narc', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/bw_pokegra_0004.narc'))
    ap.add_argument('--out', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_union'))
    ap.add_argument('dex', nargs='*', type=int, default=[643, 644, 646])
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    narc = Narc(args.narc)
    all_results = []

    for dex in args.dex:
        result = {
            'dex': dex,
            'block_base': dex * 20,
            'canvas': [CANVAS_W, CANVAS_H],
            'anchor': [ANCHOR_X, ANCHOR_Y],
            'front': scan_side(narc, dex, 'front'),
            'back': scan_side(narc, dex, 'back'),
        }
        all_results.append(result)
        (args.out / f'{dex}_animation_union.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(
            dex,
            'front', result['front']['union_bbox_anchor_relative'],
            'size', result['front']['union_size'],
            'back', result['back']['union_bbox_anchor_relative'],
            'size', result['back']['union_size'],
        )

    (args.out / 'manifest.json').write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
