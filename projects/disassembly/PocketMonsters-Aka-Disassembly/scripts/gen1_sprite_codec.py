#!/usr/bin/env python3
"""Decode a Generation I Pokemon .pic bitstream directly from a ROM.

The script never modifies the source ROM. It writes the exact compressed stream
(.pic), decoded Game Boy 2bpp tiles (.2bpp), a directly viewable grayscale PNG,
and a small JSON metadata record. The 2bpp SHA-1 is the canonical pixel-content
hash used for cross-build deduplication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path


class BitReader:
    def __init__(self, data: bytes, byte_offset: int = 0):
        self.data = data
        self.start_bit = byte_offset * 8
        self.bitpos = self.start_bit

    def bit(self) -> int:
        if self.bitpos >= len(self.data) * 8:
            raise EOFError("compressed sprite extends past end of ROM")
        value = (self.data[self.bitpos >> 3] >> (7 - (self.bitpos & 7))) & 1
        self.bitpos += 1
        return value

    def integer(self, count: int) -> int:
        value = 0
        for _ in range(count):
            value = (value << 1) | self.bit()
        return value

    @property
    def consumed_bytes(self) -> int:
        return (self.bitpos + 7) // 8 - self.start_bit // 8


CODES = (
    (0x0, 0x1, 0x3, 0x2, 0x7, 0x6, 0x4, 0x5,
     0xF, 0xE, 0xC, 0xD, 0x8, 0x9, 0xB, 0xA),
    (0xF, 0xE, 0xC, 0xD, 0x8, 0x9, 0xB, 0xA,
     0x0, 0x1, 0x3, 0x2, 0x7, 0x6, 0x4, 0x5),
)


def _fill_plane(reader: BitReader, width: int) -> bytearray:
    mode = reader.bit()
    group_count = width * width * 0x20
    groups: list[int] = []

    while len(groups) < group_count:
        if mode:
            while len(groups) < group_count:
                group = reader.integer(2)
                if group == 0:
                    break
                groups.append(group)
        else:
            run_width = 0
            while reader.bit():
                run_width += 1
                if run_width >= 16:
                    raise ValueError("invalid zero-run width")
            run = (1 << (run_width + 1)) - 1 + reader.integer(run_width + 1)
            groups.extend([0] * min(run, group_count - len(groups)))
        mode ^= 1

    reordered: list[int] = []
    for y in range(width):
        for x in range(width * 8):
            for i in range(4):
                reordered.append(groups[(y * 4 + i) * width * 8 + x])

    plane = bytearray(width * width * 8)
    for i in range(0, len(reordered), 4):
        plane[i // 4] = (
            (reordered[i] << 6)
            | (reordered[i + 1] << 4)
            | (reordered[i + 2] << 2)
            | reordered[i + 3]
        )
    return plane


def _differential_decode(plane: bytearray, width: int) -> None:
    for x in range(width * 8):
        carry = 0
        for y in range(width):
            i = y * width * 8 + x
            hi = CODES[carry][plane[i] >> 4]
            carry = hi & 1
            lo = CODES[carry][plane[i] & 0xF]
            carry = lo & 1
            plane[i] = (hi << 4) | lo


def decode_pic(rom: bytes, offset: int) -> tuple[int, bytes, int]:
    reader = BitReader(rom, offset)
    width = reader.integer(4)
    height = reader.integer(4)
    if width != height or not 1 <= width <= 15:
        raise ValueError(f"invalid sprite dimensions {width}x{height} at 0x{offset:X}")

    order = reader.bit()
    planes: list[bytearray | None] = [None, None]
    planes[order] = _fill_plane(reader, width)

    mode = reader.bit()
    if mode:
        mode += reader.bit()
    planes[order ^ 1] = _fill_plane(reader, width)

    p0 = planes[0]
    p1 = planes[1]
    assert p0 is not None and p1 is not None
    ordered = (p0, p1)

    _differential_decode(ordered[order], width)
    if mode != 1:
        _differential_decode(ordered[order ^ 1], width)
    if mode != 0:
        for i in range(width * width * 8):
            ordered[order ^ 1][i] ^= ordered[order][i]

    tiles = bytearray(width * width * 16)
    for i in range(width * width * 8):
        tiles[i * 2] = p0[i]
        tiles[i * 2 + 1] = p1[i]

    tile_count = width * width
    for i in range(tile_count):
        j = (i * width + i // width) % tile_count
        if i < j:
            a, b = i * 16, j * 16
            tmp = tiles[a:a + 16]
            tiles[a:a + 16] = tiles[b:b + 16]
            tiles[b:b + 16] = tmp

    return width, bytes(tiles), reader.consumed_bytes


def pixels_from_2bpp(tiles: bytes, width_tiles: int) -> bytes:
    width = width_tiles * 8
    out = bytearray(width * width)
    for tile in range(width_tiles * width_tiles):
        tx, ty = tile % width_tiles, tile // width_tiles
        base = tile * 16
        for y in range(8):
            lo = tiles[base + y * 2]
            hi = tiles[base + y * 2 + 1]
            for x in range(8):
                bit = 7 - x
                value = ((lo >> bit) & 1) | (((hi >> bit) & 1) << 1)
                out[(ty * 8 + y) * width + tx * 8 + x] = value
    return bytes(out)


def write_png(path: Path, pixels: bytes, width: int) -> None:
    shades = bytes((255, 170, 85, 0))
    raw = bytearray()
    for y in range(width):
        raw.append(0)
        row = pixels[y * width:(y + 1) * width]
        raw.extend(shades[p] for p in row)

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        )

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, width, 8, 0, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path)
    parser.add_argument("offset", type=lambda s: int(s, 0))
    parser.add_argument("output_prefix", type=Path)
    args = parser.parse_args()

    rom = args.rom.read_bytes()
    width_tiles, tiles, compressed_bytes = decode_pic(rom, args.offset)
    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)

    pic = rom[args.offset:args.offset + compressed_bytes]
    prefix.with_suffix(".pic").write_bytes(pic)
    prefix.with_suffix(".2bpp").write_bytes(tiles)
    pixels = pixels_from_2bpp(tiles, width_tiles)
    write_png(prefix.with_suffix(".png"), pixels, width_tiles * 8)

    metadata = {
        "rom_offset": f"0x{args.offset:05X}",
        "compressed_bytes": compressed_bytes,
        "width_tiles": width_tiles,
        "pixel_size": width_tiles * 8,
        "pic_sha1": hashlib.sha1(pic).hexdigest(),
        "2bpp_sha1": hashlib.sha1(tiles).hexdigest(),
        "png_sha1": hashlib.sha1(prefix.with_suffix('.png').read_bytes()).hexdigest(),
    }
    prefix.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
