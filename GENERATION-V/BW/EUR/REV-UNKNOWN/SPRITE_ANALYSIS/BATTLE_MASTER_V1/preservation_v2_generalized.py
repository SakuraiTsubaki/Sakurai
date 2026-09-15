#!/usr/bin/env python3
"""Generation V preservation-v2 palette-index resampler.

Static master: map the complete native BW static source canvas to the complete
Generation III 64x64 target canvas. Multipart animation uses a separate union-
envelope transform. All conversion operates on palette indices only.
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

def make_transform(union_bbox: Sequence[int], *, anchor_src: tuple[int, int], target: int = TARGET, safe_margin: int = ANIMATION_SAFE_MARGIN) -> EnvelopeTransform:
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
    anchor_dst = (dst_x + (ax - l) * (out_w / uw), dst_y + (ay - t) * (out_h / uh))
    return EnvelopeTransform((l, t, r, b), scale, out_w, out_h, dst_x, dst_y, tuple(map(int, anchor_src)), anchor_dst)

def make_static_transform(src_canvas: np.ndarray, *, target: int = TARGET) -> EnvelopeTransform:
    if src_canvas.ndim != 2:
        raise ValueError("src_canvas must be HxW palette-index array")
    h, w = src_canvas.shape
    return make_transform((0, 0, w, h), anchor_src=(w // 2, h), target=target, safe_margin=0)

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

def resize_index_frame(src_canvas: np.ndarray, transform: EnvelopeTransform, *, target: int = TARGET) -> np.ndarray:
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
    return resize_index_frame(src_canvas, make_static_transform(src_canvas, target=target), target=target)

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
    extra = set(map(int, np.unique(out))) - set(map(int, np.unique(src)))
    if extra:
        raise AssertionError(f"output invented palette indices: {sorted(extra)}")
