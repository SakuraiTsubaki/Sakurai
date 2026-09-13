#!/usr/bin/env python3
"""Locate and decode Pokémon Crystal title-screen assets from a retail ROM.

This script does not ship ROM data. It reads a user-supplied ROM and prints the
bank/CPU/file offsets and decompressed sizes for the title Suicune, logo,
foreground crystal, and palette block.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

BANK = 0x43
BANK_SIZE = 0x4000


def bankptr_to_offset(bank: int, ptr: int) -> int:
    return bank * BANK_SIZE + (ptr - 0x4000)


def bitflip(v: int) -> int:
    return int(f"{v:08b}"[::-1], 2)


def decompress_lz(data: bytes, start: int, max_output: int = 0x20000):
    out = bytearray()
    i = start
    while i < len(data):
        head = data[i]
        i += 1
        if head == 0xFF:
            return bytes(out), i
        cmd = head >> 5
        length = head & 0x1F
        if cmd == 7:
            cmd = length >> 2
            length = ((length & 3) << 8) | data[i]
            i += 1
        length += 1
        if cmd == 0:
            out.extend(data[i:i + length]); i += length
        elif cmd == 1:
            out.extend([data[i]] * length); i += 1
        elif cmd == 2:
            a, b = data[i], data[i + 1]; i += 2
            for j in range(length): out.append(a if not (j & 1) else b)
        elif cmd == 3:
            out.extend(bytes(length))
        elif cmd in (4, 5, 6):
            raw = data[i]; i += 1
            if raw & 0x80:
                base = len(out) - ((raw & 0x7F) + 1)
            else:
                base = (raw << 8) | data[i]; i += 1
            for j in range(length):
                idx = base - j if cmd == 6 else base + j
                if idx < 0 or idx >= len(out):
                    raise ValueError("invalid lookback")
                v = out[idx]
                out.append(bitflip(v) if cmd == 5 else v)
        else:
            raise ValueError(f"invalid LZ command {cmd}")
        if len(out) > max_output:
            raise ValueError("unreasonable decompressed size")
    raise ValueError("missing LZ terminator")


def find_loads(bank_data: bytes, dest: int):
    lo, hi = dest & 0xFF, dest >> 8
    hits = []
    for i in range(len(bank_data) - 9):
        if (bank_data[i] == 0x21 and
            bank_data[i + 3:i + 6] == bytes((0x11, lo, hi)) and
            bank_data[i + 6] == 0xCD):
            ptr = bank_data[i + 1] | (bank_data[i + 2] << 8)
            call = bank_data[i + 7] | (bank_data[i + 8] << 8)
            if i > 0x2C00:
                hits.append((i, ptr, call))
    return hits


def analyze(path: Path):
    data = path.read_bytes()
    bank = data[BANK * BANK_SIZE:(BANK + 1) * BANK_SIZE]
    h88 = find_loads(bank, 0x8800)
    h80 = find_loads(bank, 0x8000)
    if len(h88) < 2 or not h80:
        raise RuntimeError("could not identify Crystal title decompression sequence")
    assets = {
        "suicune": h88[0][1],
        "logo": h88[1][1],
        "crystal": h80[-1][1],
    }
    result = {
        "rom": path.name,
        "sha1": hashlib.sha1(data).hexdigest(),
        "title_initializer": {"bank": BANK, "cpu": 0x6D67, "file": 0x10ED67},
        "assets": {},
    }
    for name, ptr in assets.items():
        off = bankptr_to_offset(BANK, ptr)
        raw, end = decompress_lz(data, off)
        result["assets"][name] = {
            "bank": BANK, "cpu": ptr, "file": off,
            "compressed_bytes": end - off,
            "decompressed_bytes": len(raw),
            "tiles": len(raw) // 16,
            "decompressed_sha1": hashlib.sha1(raw).hexdigest(),
        }
    pals = []
    for i in range(len(bank) - 9):
        if (bank[i] == 0x21 and bank[i + 3:i + 6] == b"\x11\x00\xd0" and
            bank[i + 6:i + 9] == b"\x01\x80\x00" and i > 0x2C00):
            pals.append(bank[i + 1] | (bank[i + 2] << 8))
    if pals:
        ptr = pals[0]
        off = bankptr_to_offset(BANK, ptr)
        result["palette"] = {
            "bank": BANK, "cpu": ptr, "file": off, "bytes": 128,
            "sha1": hashlib.sha1(data[off:off + 128]).hexdigest(),
        }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = analyze(args.rom)
    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return
    print(r["rom"], r["sha1"])
    print("Title initializer: 43:6D67 / file 10ED67")
    for name, a in r["assets"].items():
        print(f"{name:8} {a['bank']:02X}:{a['cpu']:04X} file {a['file']:06X} "
              f"comp={a['compressed_bytes']} out={a['decompressed_bytes']} tiles={a['tiles']}")
    if "palette" in r:
        p = r["palette"]
        print(f"palette  {p['bank']:02X}:{p['cpu']:04X} file {p['file']:06X} bytes=128")

if __name__ == "__main__":
    main()
