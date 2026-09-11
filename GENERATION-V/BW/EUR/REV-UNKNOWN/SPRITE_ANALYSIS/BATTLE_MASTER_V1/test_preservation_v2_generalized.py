#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import pathlib
import sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import preservation_v2_generalized as p


def synthetic_source():
    src = np.zeros((128, 192), dtype=np.uint8)
    src[25:108, 48:146] = 1
    src[25:108, 48] = 2
    src[25:108, 145] = 2
    src[25, 48:146] = 2
    src[107, 48:146] = 2
    for i in range(34):
        src[20 + i, 40 + i] = 3
        src[20 + i, 153 - i] = 3
    src[52:54, 94:96] = 4
    return src


def static_96_source():
    src = np.zeros((96, 96), dtype=np.uint8)
    # Deliberate original composition margins; these must remain proportional.
    src[18:88, 20:79] = 1
    src[18:88, 20] = 2
    src[18:88, 78] = 2
    src[18, 20:79] = 2
    src[87, 20:79] = 2
    src[29:48, 49] = 3
    src[45:47, 50:52] = 4
    return src


def test_index_only_and_animation_margin():
    src = synthetic_source()
    tr = p.make_transform((40, 20, 154, 108), anchor_src=(96, 112))
    out = p.resize_index_frame(src, tr)
    p.validate_source_index_only(src, out)
    p.validate_no_clip(out, safe_margin=1)
    assert out.shape == (64, 64)
    assert set(np.unique(out)).issubset(set(np.unique(src)))
    assert np.count_nonzero(out) > 0


def test_static_uses_complete_96_canvas():
    src = static_96_source()
    tr = p.make_static_transform(src)
    assert tr.union_bbox == (0, 0, 96, 96)
    assert tr.out_w == 64 and tr.out_h == 64
    assert tr.dst_x == 0 and tr.dst_y == 0
    out = p.resize_static_canvas(src)
    p.validate_source_index_only(src, out)
    # Original left/top margin 20/18 px maps to about 13/12 target pixels.
    ys, xs = np.where(out != 0)
    assert xs.min() >= 12
    assert ys.min() >= 11
    # If opaque-bbox normalization had happened, the sprite would start near 0.
    assert xs.min() > 4 and ys.min() > 4


def test_deterministic():
    src = static_96_source()
    a = p.resize_static_canvas(src)
    b = p.resize_static_canvas(src)
    assert np.array_equal(a, b)
    assert hashlib.sha256(a.tobytes()).digest() == hashlib.sha256(b.tobytes()).digest()


def test_rare_indices_can_survive():
    src = synthetic_source()
    tr = p.make_transform((40, 20, 154, 108), anchor_src=(96, 112))
    out = p.resize_index_frame(src, tr)
    assert 3 in set(map(int, np.unique(out)))


def test_palette_render_uses_exact_entries():
    src = static_96_source()
    out = p.resize_static_canvas(src)
    pal = [
        (0, 0, 0, 0),
        (248, 248, 248, 255),
        (24, 24, 24, 255),
        (248, 48, 64, 255),
        (248, 216, 64, 255),
    ]
    im = p.render_indices(out, pal)
    colors = set(im.getdata())
    assert colors.issubset(set(pal))


if __name__ == '__main__':
    tests = [
        test_index_only_and_animation_margin,
        test_static_uses_complete_96_canvas,
        test_deterministic,
        test_rare_indices_can_survive,
        test_palette_render_uses_exact_entries,
    ]
    for fn in tests:
        fn()
        print('PASS', fn.__name__)
    print('ALL PASS', len(tests))
