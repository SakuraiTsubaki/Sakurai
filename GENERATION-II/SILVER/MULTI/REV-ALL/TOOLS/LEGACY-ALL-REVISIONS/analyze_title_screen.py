#!/usr/bin/env python3
"""Analyze Pokémon Gold/Silver-style title-screen resources directly from ROMs.

The script does not modify or redistribute ROM data. It locates the title-screen
VRAM clear/load sequence in ROM bank 1, extracts its GFX references, runs the
Gen II LZ3 decoder, locates the BG tilemap reference, and prints component sizes
and hashes.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

TITLE_CLEAR_PATTERN = bytes.fromhex("21 00 80 01 00 20 AF CD")


def rom_offset(bank: int, address: int) -> int:
    if address < 0x4000:
        return address
    return bank * 0x4000 + (address - 0x4000)


def sha1_short(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()[:12]


def lz3_decompress(data: bytes, offset: int) -> tuple[bytes, int]:
    """Decode the Pokémon GSC LZ3 format; return (output, consumed bytes)."""
    out = bytearray()
    i = offset

    def bit_reverse(v: int) -> int:
        return int(f"{v:08b}"[::-1], 2)

    while True:
        ctrl = data[i]
        if ctrl == 0xFF:
            i += 1
            return bytes(out), i - offset

        cmd = (ctrl >> 5) & 7
        if cmd == 7:
            cmd = (ctrl >> 2) & 7
            length = (((ctrl & 3) << 8) | data[i + 1]) + 1
            i += 2
        else:
            length = (ctrl & 0x1F) + 1
            i += 1

        if cmd == 0:  # literal
            out += data[i : i + length]
            i += length
        elif cmd == 1:  # iterate
            out += bytes([data[i]]) * length
            i += 1
        elif cmd == 2:  # alternate
            a, b = data[i], data[i + 1]
            i += 2
            out.extend(a if n % 2 == 0 else b for n in range(length))
        elif cmd == 3:  # zero
            out += b"\x00" * length
        elif cmd in (4, 5, 6):  # repeat / bitflip / reverse
            ref = data[i]
            if ref & 0x80:
                src = len(out) - ((ref & 0x7F) + 1)
                i += 1
            else:
                src = (ref << 8) | data[i + 1]
                i += 2

            for _ in range(length):
                value = out[src]
                if cmd == 5:
                    value = bit_reverse(value)
                out.append(value)
                src += -1 if cmd == 6 else 1
        else:
            raise ValueError(f"unsupported LZ3 command {cmd}")


def find_title_load_point(rom: bytes) -> int:
    matches = []
    pos = 0
    while True:
        pos = rom.find(TITLE_CLEAR_PATTERN, pos)
        if pos < 0:
            break
        if 0x4000 <= pos < 0x8000:
            matches.append(pos)
        pos += 1
    if len(matches) != 1:
        raise ValueError(f"expected one title candidate in bank 1; found {matches}")
    return matches[0]


def parse_gfx_refs(rom: bytes, load_point: int):
    refs = []
    k = load_point
    end = min(len(rom), load_point + 120)
    while k < end - 14:
        if rom[k] == 0x21 and rom[k + 3] == 0x11:  # ld hl,src / ld de,dst
            addr = rom[k + 1] | (rom[k + 2] << 8)
            dest = rom[k + 4] | (rom[k + 5] << 8)

            # ld a,bank / call FarDecompress
            if rom[k + 6] == 0x3E and rom[k + 8] == 0xCD:
                bank = rom[k + 7]
                if dest in (0x9000, 0x8800, 0x8000, 0x8F80):
                    refs.append(("decompress", bank, addr, dest, None))
                k += 11
                continue

            # ld bc,count / ld a,bank / call FarCopyBytes
            if rom[k + 6] == 0x01 and rom[k + 9] == 0x3E and rom[k + 11] == 0xCD:
                count = rom[k + 7] | (rom[k + 8] << 8)
                bank = rom[k + 10]
                if dest in (0x9000, 0x8800, 0x8000, 0x8F80):
                    refs.append(("copy", bank, addr, dest, count))
                k += 14
                continue
        k += 1
    return refs[:4]


def find_tilemap_ref(rom: bytes, load_point: int) -> tuple[int, int, int]:
    # Locate "ld de,$9800 ; ld a,bank" after the title GFX setup.
    needle = bytes.fromhex("11 00 98 3E")
    k = rom.find(needle, load_point, load_point + 0x600)
    if k < 2:
        raise ValueError("title tilemap reference not found")
    address = rom[k - 2] | (rom[k - 1] << 8)
    bank = rom[k + 4]
    return bank, address, k


def decode_raw_tilemap(rom: bytes, offset: int) -> tuple[bytes, int]:
    end = rom.index(0xFF, offset)
    return rom[offset:end], end - offset + 1


def decode_rle_tilemap(rom: bytes, offset: int) -> tuple[bytes, int]:
    out = bytearray()
    i = offset
    while True:
        command = rom[i]
        i += 1
        if command == 0xFF:
            return bytes(out), i - offset
        count = command & 0x7F
        start = rom[i]
        i += 1
        if command & 0x80:
            out.extend((start + n) & 0xFF for n in range(count))
        else:
            out.extend([start] * count)


def analyze(path: Path) -> None:
    rom = path.read_bytes()
    load_point = find_title_load_point(rom)
    # In the eight Silver ROMs examined, TitleScreen begins 0x1F bytes earlier.
    title_start = load_point - 0x1F

    print(f"\n{path.name}")
    print(f"  size={len(rom):#x} banks={len(rom)//0x4000}")
    print(f"  TitleScreen start={title_start:#08x} load_point={load_point:#08x}")

    for kind, bank, addr, dest, count in parse_gfx_refs(rom, load_point):
        off = rom_offset(bank, addr)
        if kind == "decompress":
            decoded, consumed = lz3_decompress(rom, off)
            print(
                f"  GFX LZ3 {bank:02X}:{addr:04X} off={off:06X} -> {dest:04X} "
                f"consumed={consumed:#x} out={len(decoded):#x} "
                f"tiles={len(decoded)//16} sha1={sha1_short(decoded)}"
            )
        else:
            copied = rom[off : off + count]
            print(
                f"  GFX COPY {bank:02X}:{addr:04X} off={off:06X} -> {dest:04X} "
                f"count={count:#x} sha1={sha1_short(copied)}"
            )

    bank, addr, loader_pos = find_tilemap_ref(rom, load_point)
    off = rom_offset(bank, addr)
    # JP/KR title loaders contain `bit 7,a` shortly after the FF test; western
    # loaders copy bytes directly until FF.
    nearby = rom[loader_pos : loader_pos + 0x40]
    rle = bytes.fromhex("CB 7F") in nearby
    tilemap, consumed = (
        decode_rle_tilemap(rom, off) if rle else decode_raw_tilemap(rom, off)
    )
    print(
        f"  tilemap {bank:02X}:{addr:04X} off={off:06X} "
        f"format={'RLE' if rle else 'raw'} consumed={consumed:#x} "
        f"decoded={len(tilemap)} sha1={sha1_short(tilemap)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", nargs="+", type=Path, help="one or more .gbc ROM paths")
    args = parser.parse_args()
    for rom_path in args.rom:
        analyze(rom_path)
