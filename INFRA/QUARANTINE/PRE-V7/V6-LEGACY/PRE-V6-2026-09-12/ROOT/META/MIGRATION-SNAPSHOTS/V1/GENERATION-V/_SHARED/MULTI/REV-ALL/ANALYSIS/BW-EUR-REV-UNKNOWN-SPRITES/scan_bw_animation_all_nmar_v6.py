#!/usr/bin/env python3
"""BW battle-sprite animation coverage scanner across every NMAR animation cell.

This extends scan_bw_animation_timeline_v5.py.

v5 follows the exact played timeline for NMAR animation cell 0, matching the
public BW extraction example.  That is useful for the representative battle
animation, but it is not enough for a preservation project because other NMAR
animation cells may hold additional states, alternate timelines, or unused data.

v6 therefore scans *every* NMAR animation cell independently for both front and
back.  It records:

* per-NMAR-animation period and exact tick union;
* NMCR maps used by each NMAR animation;
* union of all valid NMAR animations on that side;
* representative animation 0 separately;
* invalid/zero-period animation cells without silently discarding them.

The result deliberately distinguishes "representative exact playback" from
"data-wide exact playback coverage".  It does not claim that every NMAR cell is
reachable in normal gameplay; reachability is a separate ROM-code/event usage
question.

No generative image tooling is involved.
"""

from __future__ import annotations
import argparse
import json
import pathlib

from PIL import Image

import scan_bw_animation_union_bbox as core
import scan_bw_animation_timeline_v5 as v5


def scan_master_animation(g, ncer, nanr, maps, nmar, anim_idx: int):
    frame_count = nmar['acells'][anim_idx][0]
    period = v5.animation_period(nmar, anim_idx)

    result = {
        'nmar_animation': anim_idx,
        'nmar_frame_count': frame_count,
        'period_ticks_60fps': period,
        'status': 'ok',
        'used_nmcr_maps': [],
        'union_bbox_canvas': None,
        'union_bbox_anchor_relative': None,
        'union_size': None,
        'ticks': [],
    }

    if period <= 0:
        result['status'] = 'zero_period'
        return result

    played_union = None
    used_maps = set()

    for tick in range(period):
        state = v5.nmar_state_at_tick(nmar, anim_idx, tick)
        used_maps.add(state['map_index'])
        mask, parts = v5.render_nmcr_tick(g, ncer, nanr, maps, state)
        b = mask.getbbox()
        played_union = core.union_bbox(played_union, b)
        result['ticks'].append({
            'tick': tick,
            'nmar_frame': state['nmar_frame'],
            'map_index': state['map_index'],
            'map_tick': state['map_tick'],
            'nmar_offset': list(state['nmar_offset']),
            'bbox_canvas': list(b) if b else None,
            'bbox_anchor_relative': core.bbox_relative_to_anchor(b),
            'parts': parts,
        })

    result['used_nmcr_maps'] = sorted(used_maps)
    if played_union:
        result['union_bbox_canvas'] = list(played_union)
        result['union_bbox_anchor_relative'] = core.bbox_relative_to_anchor(played_union)
        result['union_size'] = [
            played_union[2] - played_union[0],
            played_union[3] - played_union[1],
        ]
    return result


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
    nmar = core.parse_nanr(narc.member(base + rel['nmar']))

    if not nmar['acells']:
        raise ValueError(f'{dex} {side}: NMAR has no animation cells')

    all_union = None
    animations = []
    all_used_maps = set()

    for anim_idx in range(len(nmar['acells'])):
        try:
            rec = scan_master_animation(g, ncer, nanr, maps, nmar, anim_idx)
        except Exception as exc:
            rec = {
                'nmar_animation': anim_idx,
                'nmar_frame_count': nmar['acells'][anim_idx][0],
                'status': 'error',
                'error': f'{type(exc).__name__}: {exc}',
            }
        animations.append(rec)

        if rec.get('status') == 'ok' and rec.get('union_bbox_canvas'):
            b = tuple(rec['union_bbox_canvas'])
            all_union = core.union_bbox(all_union, b)
            all_used_maps.update(rec.get('used_nmcr_maps', []))

    representative = animations[0]
    return {
        'side': side,
        'nmar_animation_count': len(nmar['acells']),
        'nmcr_map_count': len(maps),
        'representative_animation_0': {
            k: representative.get(k) for k in (
                'status', 'nmar_frame_count', 'period_ticks_60fps',
                'used_nmcr_maps', 'union_bbox_canvas',
                'union_bbox_anchor_relative', 'union_size'
            )
        },
        'all_used_nmcr_maps': sorted(all_used_maps),
        'all_nmar_union_bbox_canvas': list(all_union) if all_union else None,
        'all_nmar_union_bbox_anchor_relative': core.bbox_relative_to_anchor(all_union),
        'all_nmar_union_size': [all_union[2]-all_union[0], all_union[3]-all_union[1]]
                               if all_union else None,
        'animations': animations,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--narc', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/bw_pokegra_0004.narc'))
    ap.add_argument('--out', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_all_nmar_v6'))
    ap.add_argument('dex', nargs='*', type=int, default=[643, 644, 646])
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    narc = core.Narc(args.narc)
    summary = []

    for dex in args.dex:
        data = {
            'dex': dex,
            'method': 'all NMAR acells, exact tick playback per acell',
            'interpretation': {
                'animation_0': 'representative playback used by public BW extraction example',
                'all_nmar': 'data-wide playback coverage; gameplay reachability not yet proven',
            },
            'anchor_canvas': [core.ANCHOR_X, core.ANCHOR_Y],
            'front': scan_side(narc, dex, 'front'),
            'back': scan_side(narc, dex, 'back'),
        }
        (args.out / f'{dex}_animation_all_nmar.json').write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

        summary.append({
            'dex': dex,
            'front_nmar_count': data['front']['nmar_animation_count'],
            'front_anim0_union': data['front']['representative_animation_0']['union_bbox_anchor_relative'],
            'front_anim0_size': data['front']['representative_animation_0']['union_size'],
            'front_all_union': data['front']['all_nmar_union_bbox_anchor_relative'],
            'front_all_size': data['front']['all_nmar_union_size'],
            'back_nmar_count': data['back']['nmar_animation_count'],
            'back_anim0_union': data['back']['representative_animation_0']['union_bbox_anchor_relative'],
            'back_anim0_size': data['back']['representative_animation_0']['union_size'],
            'back_all_union': data['back']['all_nmar_union_bbox_anchor_relative'],
            'back_all_size': data['back']['all_nmar_union_size'],
        })

    (args.out / 'summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
