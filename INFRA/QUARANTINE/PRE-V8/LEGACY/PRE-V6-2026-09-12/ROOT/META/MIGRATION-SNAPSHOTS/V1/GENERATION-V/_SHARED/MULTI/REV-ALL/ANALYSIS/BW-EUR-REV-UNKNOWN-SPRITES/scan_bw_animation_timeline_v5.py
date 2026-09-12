#!/usr/bin/env python3
"""Exact BW battle-sprite animation union scanner following the NMAR timeline.

This refines scan_bw_animation_union_bbox.py.  The earlier scanner took a
conservative spatial union of every NANR frame referenced by NMCR.  That is safe,
but it can include combinations that are never played by the game.

This version mirrors the public spriterip execution order used for BW sprites:

    NMAR (master timeline)
      -> NMCR (mapped cell selected by the current NMAR frame)
        -> NANR (per-part frame selected at the current map tick)
          -> NCER / NCGR (actual opaque pixels)

For every tick in NMAR animation cell 0 it renders an alpha mask on a large
canvas, records the tick bbox, and computes the exact played union bbox.  Front
and back are scanned independently.

Input is the extracted BW /a/0/0/4 NARC.  No generated imagery is involved.
"""

from __future__ import annotations
import argparse
import json
import pathlib
import struct
from PIL import Image, ImageChops

import scan_bw_animation_union_bbox as core


def frame_duration_and_data(abnk, anim_idx: int, frame_idx: int):
    frame_count, _frame_type, _cell_type, _unk, frames_off = abnk['acells'][anim_idx]
    if not (0 <= frame_idx < frame_count):
        raise IndexError(frame_idx)
    ent = abnk['frames_base'] + frames_off + frame_idx * 8
    data_off, duration, pad = struct.unpack_from('<IHH', abnk['data'], ent)
    return data_off, duration, pad


def frame_at_tick(nanr, anim_idx: int, tick: int) -> int:
    """Mirror nanr_get_frame_at_tick() from magical/pokemon-nds-sprites."""
    frame_count = nanr['acells'][anim_idx][0]
    total = 0
    t = int(tick)
    for i in range(frame_count):
        _off, duration, _pad = frame_duration_and_data(nanr, anim_idx, i)
        if t < duration:
            return i
        t -= duration
        total += duration
    if total == 0:
        return 0
    t %= total
    for i in range(frame_count):
        _off, duration, _pad = frame_duration_and_data(nanr, anim_idx, i)
        if t < duration:
            return i
        t -= duration
    return 0


def animation_period(abnk, anim_idx: int) -> int:
    frame_count = abnk['acells'][anim_idx][0]
    return sum(frame_duration_and_data(abnk, anim_idx, i)[1]
               for i in range(frame_count))


def nmar_state_at_tick(nmar, anim_idx: int, tick: int):
    """Mirror nmar_draw(): return selected NMAR frame and the NMCR-local tick.

    Consecutive NMAR frames that point to the same NMCR map keep accumulating
    frame_tick.  A map-index change resets it to zero.
    """
    frame_count = nmar['acells'][anim_idx][0]
    t = int(tick)
    frame_tick = 0
    prev_index = None

    for i in range(frame_count):
        data_off, duration, _pad = frame_duration_and_data(nmar, anim_idx, i)
        p = nmar['fdata_base'] + data_off
        cell_index = struct.unpack_from('<H', nmar['data'], p)[0]
        if cell_index != prev_index:
            frame_tick = 0
        if t < duration:
            fr = core.anim_frame(nmar, anim_idx, i)
            return {
                'nmar_frame': i,
                'map_index': cell_index,
                'map_tick': frame_tick + t,
                'nmar_offset': fr['cell_offset'],
                'duration': duration,
                'frame_type': fr['frame_type'],
            }
        t -= duration
        frame_tick += duration
        prev_index = cell_index

    raise ValueError(f'NMAR tick {tick} outside animation period')


def render_nmcr_tick(g, ncer, nanr, maps, state):
    map_index = state['map_index']
    if not (0 <= map_index < len(maps)):
        raise IndexError(f'NMAR references NMCR map {map_index}, count={len(maps)}')

    mask = Image.new('1', (core.CANVAS_W, core.CANVAS_H), 0)
    nmar_x, nmar_y = state['nmar_offset']
    part_records = []

    for elem_idx, (anim_idx, map_x, map_y, unk, priority) in enumerate(maps[map_index]):
        if not (0 <= anim_idx < len(nanr['acells'])):
            raise IndexError(f'NMCR map {map_index} element {elem_idx} references NANR {anim_idx}')
        fi = frame_at_tick(nanr, anim_idx, state['map_tick'])
        fr = core.anim_frame(nanr, anim_idx, fi)
        fo = (
            core.ANCHOR_X + nmar_x + map_x + fr['cell_offset'][0],
            core.ANCHOR_Y + nmar_y + map_y + fr['cell_offset'][1],
        )
        part = core.draw_cell_mask(g, ncer, fr['cell_idx'], fo, fr['matrix'])
        mask = ImageChops.lighter(mask, part)
        b = part.getbbox()
        part_records.append({
            'element': elem_idx,
            'animation': anim_idx,
            'nanr_frame': fi,
            'cell': fr['cell_idx'],
            'map_offset': [map_x, map_y],
            'cell_offset': list(fr['cell_offset']),
            'bbox_canvas': list(b) if b else None,
            'bbox_anchor_relative': core.bbox_relative_to_anchor(b),
            'priority': priority,
            'unknown': unk,
        })

    return mask, part_records


def scan_side(narc: core.Narc, dex: int, side: str):
    base = dex * 20
    if side == 'front':
        rel = {'ncgr': 2, 'ncer': 4, 'nanr': 5, 'nmcr': 6, 'nmar': 7}
    elif side == 'back':
        rel = {'ncgr': 11, 'ncer': 13, 'nanr': 14, 'nmcr': 15, 'nmar': 16}
    else:
        raise ValueError(side)

    g = core.parse_ncgr(narc.member(base + rel['ncgr']))
    ncer = core.parse_ncer(narc.member(base + rel['ncer']))
    nanr = core.parse_nanr(narc.member(base + rel['nanr']))
    maps = core.parse_nmcr(narc.member(base + rel['nmcr']))
    # NMAR and NANR share the same ABNK layout.
    nmar = core.parse_nanr(narc.member(base + rel['nmar']))

    if not nmar['acells']:
        raise ValueError(f'{dex} {side}: NMAR has no animation cells')

    master_anim = 0
    period = animation_period(nmar, master_anim)
    if period <= 0:
        raise ValueError(f'{dex} {side}: invalid NMAR period {period}')

    played_union = None
    tick_records = []
    used_maps = set()

    for tick in range(period):
        state = nmar_state_at_tick(nmar, master_anim, tick)
        used_maps.add(state['map_index'])
        mask, parts = render_nmcr_tick(g, ncer, nanr, maps, state)
        b = mask.getbbox()
        played_union = core.union_bbox(played_union, b)
        tick_records.append({
            'tick': tick,
            'nmar_frame': state['nmar_frame'],
            'map_index': state['map_index'],
            'map_tick': state['map_tick'],
            'nmar_offset': list(state['nmar_offset']),
            'bbox_canvas': list(b) if b else None,
            'bbox_anchor_relative': core.bbox_relative_to_anchor(b),
            'parts': parts,
        })

    return {
        'side': side,
        'master_nmar_animation': master_anim,
        'period_ticks_60fps': period,
        'used_nmcr_maps': sorted(used_maps),
        'nmcr_map_count': len(maps),
        'union_bbox_canvas': list(played_union) if played_union else None,
        'union_bbox_anchor_relative': core.bbox_relative_to_anchor(played_union),
        'union_size': [played_union[2]-played_union[0], played_union[3]-played_union[1]]
                      if played_union else None,
        'ticks': tick_records,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--narc', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/bw_pokegra_0004.narc'))
    ap.add_argument('--out', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_timeline_v5'))
    ap.add_argument('dex', nargs='*', type=int, default=[643, 644, 646])
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    narc = core.Narc(args.narc)
    summary = []
    for dex in args.dex:
        data = {
            'dex': dex,
            'method': 'exact NMAR timeline -> NMCR map -> NANR tick frame -> NCER/NCGR mask',
            'anchor_canvas': [core.ANCHOR_X, core.ANCHOR_Y],
            'front': scan_side(narc, dex, 'front'),
            'back': scan_side(narc, dex, 'back'),
        }
        out = args.out / f'{dex}_animation_union.json'
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        summary.append({
            'dex': dex,
            'front_period': data['front']['period_ticks_60fps'],
            'front_maps': data['front']['used_nmcr_maps'],
            'front_union': data['front']['union_bbox_anchor_relative'],
            'front_size': data['front']['union_size'],
            'back_period': data['back']['period_ticks_60fps'],
            'back_maps': data['back']['used_nmcr_maps'],
            'back_union': data['back']['union_bbox_anchor_relative'],
            'back_size': data['back']['union_size'],
        })

    (args.out / 'summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
