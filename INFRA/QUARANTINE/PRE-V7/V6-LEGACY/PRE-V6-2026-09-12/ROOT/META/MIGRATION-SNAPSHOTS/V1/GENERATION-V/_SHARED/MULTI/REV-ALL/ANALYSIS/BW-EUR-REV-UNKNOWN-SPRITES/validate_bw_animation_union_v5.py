#!/usr/bin/env python3
"""Validate exact NMAR-timeline unions against conservative v4 unions.

PASS conditions per species/side:
- v5 exact played union exists;
- v4 conservative union exists;
- v5 exact union is contained in v4 conservative union;
- no recorded v5 tick bbox touches the temporary analysis-canvas boundary;
- used NMCR map indices are in range;
- period is positive.

The script never repairs data; it only reports PASS/FAIL with reasons.
"""

from __future__ import annotations
import argparse
import json
import pathlib

CANVAS_W = 768
CANVAS_H = 768


def contains(outer, inner):
    return (outer[0] <= inner[0] and outer[1] <= inner[1] and
            outer[2] >= inner[2] and outer[3] >= inner[3])


def touches_canvas_edge(b):
    if b is None:
        return False
    return b[0] <= 0 or b[1] <= 0 or b[2] >= CANVAS_W or b[3] >= CANVAS_H


def validate_side(v4, v5, side):
    failures=[]
    a=v4.get(side, {})
    e=v5.get(side, {})
    conservative=a.get('union_bbox_canvas')
    exact=e.get('union_bbox_canvas')
    if conservative is None:
        failures.append('missing v4 conservative union')
    if exact is None:
        failures.append('missing v5 exact union')
    if conservative is not None and exact is not None and not contains(conservative, exact):
        failures.append(f'exact union not contained in conservative union: v4={conservative} v5={exact}')

    period=e.get('period_ticks_60fps', 0)
    if not isinstance(period, int) or period <= 0:
        failures.append(f'invalid period: {period!r}')

    map_count=e.get('nmcr_map_count', 0)
    for m in e.get('used_nmcr_maps', []):
        if not (0 <= m < map_count):
            failures.append(f'NMCR map index out of range: {m}/{map_count}')

    edge_ticks=[]
    for rec in e.get('ticks', []):
        b=rec.get('bbox_canvas')
        if touches_canvas_edge(b):
            edge_ticks.append(rec.get('tick'))
    if edge_ticks:
        failures.append(f'{len(edge_ticks)} tick(s) touch analysis canvas edge; first={edge_ticks[:10]}')

    return {
        'status':'PASS' if not failures else 'FAIL',
        'failures':failures,
        'v4_conservative_union':conservative,
        'v5_exact_union':exact,
        'v5_exact_union_anchor_relative':e.get('union_bbox_anchor_relative'),
        'v5_union_size':e.get('union_size'),
        'period_ticks_60fps':period,
        'used_nmcr_maps':e.get('used_nmcr_maps', []),
        'nmcr_map_count':map_count,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--v4', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_union'))
    ap.add_argument('--v5', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_timeline_v5'))
    ap.add_argument('--out', type=pathlib.Path,
                    default=pathlib.Path('/mnt/data/sprite_preserve_trial/animation_timeline_v5/validation.json'))
    ap.add_argument('dex', nargs='*', type=int, default=[643,644,646])
    args=ap.parse_args()

    result=[]
    overall=True
    for dex in args.dex:
        v4=json.loads((args.v4/f'{dex}_animation_union.json').read_text('utf-8'))
        v5=json.loads((args.v5/f'{dex}_animation_union.json').read_text('utf-8'))
        row={'dex':dex}
        for side in ('front','back'):
            row[side]=validate_side(v4,v5,side)
            overall &= row[side]['status']=='PASS'
        result.append(row)

    payload={'overall':'PASS' if overall else 'FAIL','species':result}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False,indent=2))
    raise SystemExit(0 if overall else 1)

if __name__=='__main__':
    main()
