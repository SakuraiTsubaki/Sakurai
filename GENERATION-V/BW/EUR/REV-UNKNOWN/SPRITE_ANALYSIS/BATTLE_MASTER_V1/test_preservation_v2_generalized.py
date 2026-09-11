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
    # Main body, palette 1.
    src[25:108, 48:146] = 1
    # Dark contour, palette 2.
    src[25:108, 48] = 2
    src[25:108, 145] = 2
    src[25, 48:146] = 2
    src[107, 48:146] = 2
    # Thin identifying horn/wing lines, rare palette 3.
    for i in range(34):
        src[20 + i, 40 + i] = 3
        src[20 + i, 153 - i] = 3
    # Tiny accent, palette 4.
    src[52:54, 94:96] = 4
    return src


def test_index_only_and_margin():
    src = synthetic_source()
    tr = p.make_transform((40, 20, 154, 108), anchor_src=(96, 112))
    out = p.resize_index_frame(src, tr)
    p.validate_source_index_only(src, out)
    p.validate_no_clip(out)
    assert out.shape == (64, 64)
    assert set(np.unique(out)).issubset(set(np.unique(src)))
    assert np.count_nonzero(out) > 0


def test_deterministic():
    src = synthetic_source()
    tr = p.make_transform((40, 20, 154, 108), anchor_src=(96, 112))
    a = p.resize_index_frame(src, tr)
    b = p.resize_index_frame(src, tr)
    assert np.array_equal(a, b)
    assert hashlib.sha256(a.tobytes()).digest() == hashlib.sha256(b.tobytes()).digest()


def test_rare_indices_can_survive():
    src = synthetic_source()
    tr = p.make_transform((40, 20, 154, 108), anchor_src=(96, 112))
    out = p.resize_index_frame(src, tr)
    # The structural rare diagonal was deliberately long enough to overlap
    # target footprints; preservation-v2 should keep at least some index 3.
    assert 3 in set(map(int, np.unique(out)))


def test_palette_render_uses_exact_entries():
    src = synthetic_source()
    tr = p.make_transform((40, 20, 154, 108), anchor_src=(96, 112))
    out = p.resize_index_frame(src, tr)
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
        test_index_only_and_margin,
        test_deterministic,
        test_rare_indices_can_survive,
        test_palette_render_uses_exact_entries,
    ]
    for fn in tests:
        fn()
        print('PASS', fn.__name__)
    print('ALL PASS', len(tests))
