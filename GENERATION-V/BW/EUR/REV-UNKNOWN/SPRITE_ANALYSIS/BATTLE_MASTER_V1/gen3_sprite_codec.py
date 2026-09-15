#!/usr/bin/env python3
"""Generation III 64x64 Pokémon sprite binary helpers."""
from __future__ import annotations
import numpy as np


def encode_4bpp_64x64(indices: np.ndarray) -> bytes:
    """Encode 64x64 palette indices as 64 row-major 8x8 GBA 4bpp tiles."""
    if indices.shape != (64, 64):
        raise ValueError("expected 64x64 index image")
    if int(indices.max(initial=0)) >= 16:
        raise ValueError("4bpp image contains palette index >=16")
    out = bytearray()
    for ty in range(8):
        for tx in range(8):
            for py in range(8):
                for px in range(0, 8, 2):
                    lo = int(indices[ty * 8 + py, tx * 8 + px])
                    hi = int(indices[ty * 8 + py, tx * 8 + px + 1])
                    out.append(lo | (hi << 4))
    if len(out) != 2048:
        raise AssertionError("64x64 4bpp sprite must encode to 2048 bytes")
    return bytes(out)


def decode_4bpp_64x64(raw: bytes) -> np.ndarray:
    if len(raw) != 2048:
        raise ValueError("expected 2048 bytes")
    out = np.zeros((64, 64), dtype=np.uint8)
    pos = 0
    for ty in range(8):
        for tx in range(8):
            for py in range(8):
                for px in range(0, 8, 2):
                    value = raw[pos]
                    pos += 1
                    out[ty * 8 + py, tx * 8 + px] = value & 0x0F
                    out[ty * 8 + py, tx * 8 + px + 1] = value >> 4
    return out


def lz10_compress(src: bytes) -> bytes:
    """Deterministic standard GBA/NDS type-0x10 LZ77 encoder."""
    size = len(src)
    if size >= 1 << 24:
        raise ValueError("LZ10 24-bit size header overflow")
    out = bytearray((0x10, size & 0xFF, (size >> 8) & 0xFF, (size >> 16) & 0xFF))
    pos = 0
    while pos < size:
        flag_pos = len(out)
        out.append(0)
        flags = 0
        tokens = bytearray()
        for bit in range(8):
            if pos >= size:
                break
            best_len = 0
            best_disp = 0
            start = max(0, pos - 0x1000)
            for match in range(pos - 1, start - 1, -1):
                length = 0
                max_len = min(18, size - pos)
                while length < max_len and src[match + length] == src[pos + length]:
                    length += 1
                if length >= 3 and length > best_len:
                    best_len = length
                    best_disp = pos - match
                    if length == 18:
                        break
            if best_len >= 3:
                flags |= 1 << (7 - bit)
                disp = best_disp - 1
                tokens.append(((best_len - 3) << 4) | ((disp >> 8) & 0x0F))
                tokens.append(disp & 0xFF)
                pos += best_len
            else:
                tokens.append(src[pos])
                pos += 1
        out[flag_pos] = flags
        out.extend(tokens)
    return bytes(out)


def lz10_decompress(src: bytes) -> bytes:
    if len(src) < 4 or src[0] != 0x10:
        raise ValueError("not an LZ10 stream")
    size = src[1] | (src[2] << 8) | (src[3] << 16)
    pos = 4
    out = bytearray()
    while len(out) < size:
        flags = src[pos]
        pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= size:
                break
            if not ((flags >> bit) & 1):
                out.append(src[pos])
                pos += 1
            else:
                b1, b2 = src[pos], src[pos + 1]
                pos += 2
                length = (b1 >> 4) + 3
                disp = (((b1 & 0x0F) << 8) | b2) + 1
                if disp > len(out):
                    raise ValueError("invalid LZ10 back-reference")
                for _ in range(length):
                    out.append(out[-disp])
                    if len(out) >= size:
                        break
    return bytes(out)
