#!/usr/bin/env python3
"""Native BW static battle-sprite decode helpers.

The dedicated static NCGR is a 96x96 / 12x12-tile / 4bpp resource, but its
144 character tiles are not serialized as one ordinary 12-tile-wide raster.
For the verified BW source set the tile stream is four rectangles in this
order, matching the 64x64 OBJ-size boundary:

  1. top-left     8x8 tiles  (64x64 px) : tile 0..63
  2. top-right    4x8 tiles  (32x64 px) : tile 64..95
  3. bottom-left  8x4 tiles  (64x32 px) : tile 96..127
  4. bottom-right 4x4 tiles  (32x32 px) : tile 128..143

This layout was independently cross-checked against preserved BW 96x96 PNGs:
Bulbasaur front/back/normal/shiny and Wailord front reconstruct to the same
9216 palette-index pixels after palette-index reconciliation. External PNGs
are validation references only; the canonical source remains the ROM NCGR.
"""
from __future__ import annotations
import struct
import numpy as np


def _u16(buf: bytes, off: int) -> int:
    return struct.unpack_from("<H", buf, off)[0]


def _u32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def static_tile_destination(tile_index: int) -> tuple[int, int]:
    if not 0 <= tile_index < 144:
        raise ValueError("BW static NCGR tile index must be 0..143")
    if tile_index < 64:
        return tile_index % 8, tile_index // 8
    if tile_index < 96:
        i = tile_index - 64
        return 8 + i % 4, i // 4
    if tile_index < 128:
        i = tile_index - 96
        return i % 8, 8 + i // 8
    i = tile_index - 128
    return 8 + i % 4, 8 + i // 4


def decode_static_ncgr_indices(ncgr: bytes) -> np.ndarray:
    """Return canonical 96x96 uint8 palette-index canvas."""
    if ncgr[:4] != b"RGCN" or ncgr[16:20] != b"RAHC":
        raise ValueError("not a decoded BW NCGR/RAHC resource")

    width_tiles = _u16(ncgr, 0x18)
    height_tiles = _u16(ncgr, 0x1A)
    color_format = _u32(ncgr, 0x1C)
    graphics_type = _u32(ncgr, 0x24)
    data_size = _u32(ncgr, 0x28)
    data_offset = _u32(ncgr, 0x2C)

    if (width_tiles, height_tiles) != (12, 12):
        raise ValueError(f"unexpected static NCGR tile dimensions: {width_tiles}x{height_tiles}")
    if color_format != 3:
        raise ValueError(f"expected palette16/4bpp color format 3, got {color_format}")
    if graphics_type != 0:
        raise ValueError(f"expected character graphics type 0, got {graphics_type}")
    if data_size != 0x1200:
        raise ValueError(f"expected 0x1200 bytes of static graphics, got 0x{data_size:X}")

    # NCGR's pointer is relative to RAHC+8; in this BW resource it is 0x18,
    # making the actual file offset 0x30.
    start = 0x10 + 8 + data_offset
    raw = ncgr[start:start + data_size]
    if len(raw) != 0x1200:
        raise ValueError("truncated static NCGR graphics payload")

    out = np.zeros((96, 96), dtype=np.uint8)
    for tile_index in range(144):
        tile_x, tile_y = static_tile_destination(tile_index)
        tile = raw[tile_index * 32:(tile_index + 1) * 32]
        for y in range(8):
            for x in range(8):
                p = y * 8 + x
                value = tile[p // 2]
                out[tile_y * 8 + y, tile_x * 8 + x] = (value & 0x0F) if (p & 1) == 0 else (value >> 4)
    return out


def extract_nclr_palette_bgr555(nclr: bytes) -> bytes:
    """Return the 16-color / 32-byte BGR555 payload from a BW NCLR."""
    if nclr[:4] != b"RLCN" or nclr[16:20] != b"TTLP":
        raise ValueError("not a decoded BW NCLR/TTLP resource")
    data_size = _u32(nclr, 0x20)
    data_offset = _u32(nclr, 0x24)
    start = 0x10 + 8 + data_offset
    raw = nclr[start:start + data_size]
    if len(raw) < 32:
        raise ValueError("palette has fewer than 16 BGR555 colors")
    return raw[:32]


def bgr555_to_rgba(raw_palette: bytes) -> list[tuple[int, int, int, int]]:
    if len(raw_palette) != 32:
        raise ValueError("expected exactly 32 bytes / 16 BGR555 colors")
    colors = []
    for i in range(16):
        value = _u16(raw_palette, i * 2)
        r, g, b = value & 31, (value >> 5) & 31, (value >> 10) & 31
        expand = lambda c: (c << 3) | (c >> 2)
        colors.append((expand(r), expand(g), expand(b), 0 if i == 0 else 255))
    return colors
