#!/usr/bin/env python3
"""Generation V preservation-v2 palette-index resampler.

Two related uses are intentionally separated:

1. Static insertion master
   The dedicated BW static NCGR is converted as a complete source canvas to
   64x64, exactly mirroring the Generation IV philosophy of converting the
   complete 80x80 source canvas rather than cropping opaque bounds first.

2. Multipart animation track
   A legal animation union envelope can be mapped into a safe target rectangle
   with one shared scale/anchor for every frame.

All conversion operates on palette indices, never interpolated RGB.  Therefore
non-transparent output colors can only come from indices that already occur in
the ROM source image.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Sequence

import numpy as np
from PIL import Image

TARGET = 64
ANIMATION_SAFE_MARGIN = 1
RARITY_EXPONENT = 0.08
# Generation IV used opaque overlap >= 0.78125 in a 1.5625-area footprint.
# That is exactly a 50% opaque-coverage rule, generalized here to any scale.
OPAQUE_COVERAGE_FORCE = 0.50


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
    safe_margin: int = ANIMATION_SAFE_MARGIN,
) -> EnvelopeTransform:
    """Fit one source rectangle with uniform scaling.

    For animation this rectangle is the legal union envelope and safe_margin is
    normally 1.  For the static master the rectangle is the *entire decoded
    static NCGR canvas* and safe_margin is 0.
    """
    l, t, r, b = _validate_bbox(union_bbox)
    uw, uh = r - l, b - t
    inner = target - safe_margin * 2
    if inner <= 0:
        raise ValueError("safe margin leaves no target area")
    scale = min(inner / uw, inner / uh)
    out_w = max(1, min(inner, int(math.floor(uw * scale + 1e-9))))
    out_h = max(1, min(inner, int(math.floor(uh * scale + 1e-9))))
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


def make_static_transform(src_canvas: np.ndarray, *, target: int = TARGET) -> EnvelopeTransform:
    """Map the complete static source canvas to the full 64x64 target.

    This deliberately does NOT crop the visible bbox.  Transparent source
    margins are part of the original composition and preserve cross-species
    relative scale/placement, just as in the Generation IV 80x80 -> 64x64
    master.
    """
    if src_canvas.ndim != 2:
        raise ValueError("src_canvas must be HxW palette-index array")
    h, w = src_canvas.shape
    return make_transform(
        (0, 0, w, h),
        anchor_src=(w // 2, h),
        target=target,
        safe_margin=0,
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
    """Convert one palette-index image using weighted area-overlap voting."""
    if src_canvas.ndim != 2:
        raise ValueError("src_canvas must be HxW palette-index array")
    src = np.asarray(src_canvas)
    if src.dtype.kind not in "ui":
        raise TypeError("src_canvas must use integer palette indices")

    l, t, r, b = transform.union_bbox
    H, W = src.shape
    if l < 0 or t < 0 or r > W or b > H:
        raise ValueError(f"source rectangle {transform.union_bbox} outside source canvas {W}x{H}")

    crop = src[t:b, l:r]
    sh, sw = crop.shape
    rarity = _rarity_weights(crop)
    out = np.zeros((target, target), dtype=src.dtype)

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
            chosen = max(scores, key=lambda i: (scores[i], i != 0, -i))
            out[transform.dst_y + oy, transform.dst_x + ox] = chosen

    return out


def resize_static_canvas(src_canvas: np.ndarray, *, target: int = TARGET) -> np.ndarray:
    """Generation V static-master entry point: complete canvas -> 64x64."""
    tr = make_static_transform(src_canvas, target=target)
    return resize_index_frame(src_canvas, tr, target=target)


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


def validate_no_clip(out: np.ndarray, *, safe_margin: int = 0) -> None:
    ys, xs = np.where(out != 0)
    if not len(xs):
        return
    if xs.min() < safe_margin or ys.min() < safe_margin:
        raise AssertionError("opaque output violates top/left safety bound")
    if xs.max() >= out.shape[1] - safe_margin or ys.max() >= out.shape[0] - safe_margin:
        raise AssertionError("opaque output violates bottom/right safety bound")


def describe(index64: np.ndarray) -> dict:
    ys, xs = np.where(index64 != 0)
    bbox = None if not len(xs) else [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    return {
        "size": [int(index64.shape[1]), int(index64.shape[0])],
        "bbox": bbox,
        "visible_pixels": int(np.count_nonzero(index64)),
        "used_palette_indices": sorted(map(int, np.unique(index64[index64 != 0]))),
    }
