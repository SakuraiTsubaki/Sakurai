#!/usr/bin/env python3
"""Generation V generalized preservation-v2 index resampler.

This is the ROM-primary 64x64 conversion kernel for BW battle sprites.
It deliberately works on palette *indices*, not RGBA colors.

The Generation IV master used a fixed 80x80 -> 64x64 mapping.  Generation V
battle graphics are multipart and their legal rendered envelope is variable, so
this module generalizes the same rule to an arbitrary union envelope while
preserving a common scale and relative anchor for every frame in that logical
animation set.

Invariant: every non-transparent output pixel is one of the palette indices
already present in the source index image.  No RGB interpolation or new colors
are possible in this stage.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
import hashlib
import math
from typing import Iterable, Sequence

import numpy as np
from PIL import Image

TARGET = 64
SAFE_MARGIN = 1
INNER = TARGET - SAFE_MARGIN * 2
RARITY_EXPONENT = 0.08
OPAQUE_COVERAGE_FORCE = 0.50  # Gen IV 0.78125 / 1.5625 == 50%.


@dataclass(frozen=True)
class EnvelopeTransform:
    union_bbox: tuple[int, int, int, int]
    scale: float
    out_w: int
    out_h: int
    dst_x: int
    dst_y: int
    anchor_src: tuple[int, int]
    anchor_dst: tuple[float, float]


def _validate_bbox(bbox: Sequence[int]) -> tuple[int, int, int, int]:
    if len(bbox) != 4:
        raise ValueError("bbox must be (left, top, right, bottom)")
    l, t, r, b = map(int, bbox)
    if r <= l or b <= t:
        raise ValueError(f"empty/invalid bbox: {bbox}")
    return l, t, r, b


def make_transform(
    union_bbox: Sequence[int],
    *,
    anchor_src: tuple[int, int],
    target: int = TARGET,
    safe_margin: int = SAFE_MARGIN,
) -> EnvelopeTransform:
    """Fit the full legal animation union into the target with one uniform scale.

    The shorter dimension is centered.  Because the *union* is transformed as a
    whole, the battle anchor keeps the same relative position for all frames.
    """
    l, t, r, b = _validate_bbox(union_bbox)
    uw, uh = r - l, b - t
    inner = target - safe_margin * 2
    scale = min(inner / uw, inner / uh)
    # Floor avoids ever exceeding the safe inner box due to rounding.
    out_w = max(1, min(inner, int(math.floor(uw * scale + 1e-9))))
    out_h = max(1, min(inner, int(math.floor(uh * scale + 1e-9))))
    # Recompute effective per-axis footprint from the integer raster size only
    # for placement. Sampling still uses the exact union geometry below.
    dst_x = safe_margin + (inner - out_w) // 2
    dst_y = safe_margin + (inner - out_h) // 2
    ax, ay = anchor_src
    anchor_dst = (
        dst_x + (ax - l) * (out_w / uw),
        dst_y + (ay - t) * (out_h / uh),
    )
    return EnvelopeTransform(
        (l, t, r, b), scale, out_w, out_h, dst_x, dst_y,
        tuple(map(int, anchor_src)), anchor_dst,
    )


def _area_overlap(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def _rarity_weights(src: np.ndarray) -> np.ndarray:
    if src.dtype.kind not in "ui":
        raise TypeError("source index image must contain integer palette indices")
    max_index = int(src.max(initial=0))
    counts = np.bincount(src.ravel(), minlength=max(16, max_index + 1)).astype(np.float64)
    nonzero_opaque = counts[1:][counts[1:] > 0]
    maxc = float(nonzero_opaque.max()) if len(nonzero_opaque) else 1.0
    rarity = np.ones_like(counts, dtype=np.float64)
    mask = counts > 0
    rarity[mask] = (maxc / counts[mask]) ** RARITY_EXPONENT
    rarity[0] = 1.0
    return rarity


def resize_index_frame(
    src_canvas: np.ndarray,
    transform: EnvelopeTransform,
    *,
    target: int = TARGET,
) -> np.ndarray:
    """Convert one source-index frame with weighted area-overlap voting.

    Source index 0 is transparent.  Output is a 64x64 palette-index array.
    Every selected nonzero index is selected from source pixels overlapping the
    corresponding target pixel footprint.  Mild rarity weighting mirrors the
    Generation IV preservation-v2 strategy.
    """
    if src_canvas.ndim != 2:
        raise ValueError("src_canvas must be HxW palette-index array")
    src = np.asarray(src_canvas)
    if src.dtype.kind not in "ui":
        raise TypeError("src_canvas must use integer palette indices")

    l, t, r, b = transform.union_bbox
    H, W = src.shape
    if l < 0 or t < 0 or r > W or b > H:
        raise ValueError(f"union bbox {transform.union_bbox} outside source canvas {W}x{H}")

    crop = src[t:b, l:r]
    sh, sw = crop.shape
    rarity = _rarity_weights(crop)
    out = np.zeros((target, target), dtype=src.dtype)

    # Map only the raster rectangle allocated to the union envelope.  The rest
    # of the 64x64 target remains transparent.
    for oy in range(transform.out_h):
        sy0 = oy * sh / transform.out_h
        sy1 = (oy + 1) * sh / transform.out_h
        iy0 = max(0, int(math.floor(sy0)))
        iy1 = min(sh, int(math.ceil(sy1)))
        for ox in range(transform.out_w):
            sx0 = ox * sw / transform.out_w
            sx1 = (ox + 1) * sw / transform.out_w
            ix0 = max(0, int(math.floor(sx0)))
            ix1 = min(sw, int(math.ceil(sx1)))

            scores: dict[int, float] = {}
            opaque_area = 0.0
            total_area = max(1e-12, (sx1 - sx0) * (sy1 - sy0))
            for sy in range(iy0, iy1):
                wy = _area_overlap(sy0, sy1, sy, sy + 1)
                if wy <= 0:
                    continue
                for sx in range(ix0, ix1):
                    wx = _area_overlap(sx0, sx1, sx, sx + 1)
                    w = wx * wy
                    if w <= 0:
                        continue
                    idx = int(crop[sy, sx])
                    scores[idx] = scores.get(idx, 0.0) + w * float(rarity[idx])
                    if idx != 0:
                        opaque_area += w

            if not scores:
                continue
            if opaque_area / total_area >= OPAQUE_COVERAGE_FORCE and len(scores) > 1:
                scores.pop(0, None)
            if not scores:
                continue
            # Stable tie break: larger score, then prefer opaque, then lower
            # palette index for deterministic rebuilds.
            chosen = max(scores, key=lambda i: (scores[i], i != 0, -i))
            out[transform.dst_y + oy, transform.dst_x + ox] = chosen

    return out


def render_indices(index64: np.ndarray, palette_rgba: Sequence[Sequence[int]]) -> Image.Image:
    pal = np.asarray(palette_rgba, dtype=np.uint8)
    if pal.ndim != 2 or pal.shape[1] != 4:
        raise ValueError("palette_rgba must be Nx4")
    if int(index64.max(initial=0)) >= len(pal):
        raise ValueError("index image references outside palette")
    return Image.fromarray(pal[index64], "RGBA")


def sha256_rgba(im: Image.Image) -> str:
    return hashlib.sha256(im.convert("RGBA").tobytes()).hexdigest()


def validate_source_index_only(src: np.ndarray, out: np.ndarray) -> None:
    source = set(map(int, np.unique(src)))
    output = set(map(int, np.unique(out)))
    extra = output - source
    if extra:
        raise AssertionError(f"output invented palette indices: {sorted(extra)}")


def validate_no_clip(out: np.ndarray, *, safe_margin: int = SAFE_MARGIN) -> None:
    ys, xs = np.where(out != 0)
    if not len(xs):
        return
    if xs.min() < safe_margin or ys.min() < safe_margin:
        raise AssertionError("opaque output violates top/left safe margin")
    if xs.max() >= out.shape[1] - safe_margin or ys.max() >= out.shape[0] - safe_margin:
        raise AssertionError("opaque output violates bottom/right safe margin")


def describe(index64: np.ndarray) -> dict:
    ys, xs = np.where(index64 != 0)
    bbox = None if not len(xs) else [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    return {
        "size": [int(index64.shape[1]), int(index64.shape[0])],
        "bbox": bbox,
        "visible_pixels": int(np.count_nonzero(index64)),
        "used_palette_indices": sorted(map(int, np.unique(index64[index64 != 0]))),
    }
