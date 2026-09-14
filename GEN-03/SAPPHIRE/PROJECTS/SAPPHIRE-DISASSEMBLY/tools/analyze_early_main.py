#!/usr/bin/env python3
"""Analyze the early main.c function block in a local Pokémon Sapphire ROM.

The ROM is a local read-only reference. This tool never writes ROM data into the
repository. It identifies the regional layout from the GBA game code, slices the
known early-main function boundaries, and reports SHA-256 fingerprints.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

ROM_BASE = 0x08000000

AXPE_FUNCTIONS = [
    ("UpdateLinkAndCallCallbacks", 0x340, 0x388),
    ("InitMainCallbacks",          0x388, 0x3A8),
    ("CallCallbacks",              0x3A8, 0x3CC),
    ("SetMainCallback2",           0x3CC, 0x3E4),
    ("SeedRngWithRtc",             0x3E4, 0x400),
    ("InitKeys",                   0x400, 0x428),
    ("ReadKeys",                   0x428, 0x4C4),
    ("InitIntrHandlers",           0x4C4, 0x540),
    ("SetVBlankCallback",          0x540, 0x54C),
    ("SetHBlankCallback",          0x54C, 0x558),
    ("SetVCountCallback",          0x558, 0x564),
    ("SetSerialCallback",          0x564, 0x570),
    ("VBlankIntr",                 0x570, 0x5EC),
    ("InitFlashTimer",             0x5EC, 0x600),
    ("HBlankIntr",                 0x600, 0x630),
    ("VCountIntr",                 0x630, 0x660),
    ("SerialIntr",                 0x660, 0x690),
    ("IntrDummy",                  0x690, 0x694),
    ("WaitForVBlank",              0x694, 0x6B4),
    ("DoSoftReset",                0x6B4, 0x724),
    ("ClearPokemonCrySongs",       0x724, 0x748),
]

JP_FUNCTIONS = [
    ("UpdateLinkAndCallCallbacks", 0x348, 0x390),
    ("InitMainCallbacks",          0x390, 0x3B0),
    ("CallCallbacks",              0x3B0, 0x3D4),
    ("SetMainCallback2",           0x3D4, 0x3E8),
    ("SeedRngWithRtc",             0x3E8, 0x404),
    ("InitKeys",                   0x404, 0x42C),
    ("ReadKeys",                   0x42C, 0x4C8),
    ("InitIntrHandlers",           0x4C8, 0x544),
    ("SetVBlankCallback",          0x544, 0x550),
    ("SetHBlankCallback",          0x550, 0x55C),
    ("SetVCountCallback",          0x55C, 0x568),
    ("SetSerialCallback",          0x568, 0x574),
    ("VBlankIntr",                 0x574, 0x5F0),
    ("InitFlashTimer",             0x5F0, 0x604),
    ("HBlankIntr",                 0x604, 0x634),
    ("VCountIntr",                 0x634, 0x664),
    ("SerialIntr",                 0x664, 0x694),
    ("IntrDummy",                  0x694, 0x698),
    ("WaitForVBlank",              0x698, 0x6B8),
    ("DoSoftReset",                0x6B8, 0x728),
    ("ClearPokemonCrySongs",       0x728, 0x74C),
]

EXT_FUNCTIONS = [(name, start + 0x134, end + 0x134) for name, start, end in AXPE_FUNCTIONS]

FAMILY_MAP = {
    "AXPJ": ("jp", JP_FUNCTIONS),
    "AXPE": ("axpe", AXPE_FUNCTIONS),
    "AXPD": ("extended_european", EXT_FUNCTIONS),
    "AXPF": ("extended_european", EXT_FUNCTIONS),
    "AXPI": ("extended_european", EXT_FUNCTIONS),
}


def analyze(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    if len(data) < 0x800:
        raise ValueError("file is too small to be a supported Sapphire ROM")
    game_code = data[0xAC:0xB0].decode("ascii", errors="replace")
    if game_code not in FAMILY_MAP:
        raise ValueError(f"unsupported game code: {game_code!r}")
    family, funcs = FAMILY_MAP[game_code]
    result = {
        "file": path.name,
        "game_code": game_code,
        "software_version": data[0xBC],
        "family": family,
        "functions": [],
    }
    for name, start, end in funcs:
        chunk = data[start:end]
        result["functions"].append({
            "name": name,
            "file_offset": f"0x{start:08X}",
            "runtime_address": f"0x{ROM_BASE + start:08X}",
            "size": end - start,
            "sha256": hashlib.sha256(chunk).hexdigest(),
        })
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--format", choices=("json", "csv"), default="json")
    args = ap.parse_args()
    result = analyze(args.rom)
    if args.format == "json":
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(["file", "game_code", "software_version", "family", "function", "file_offset", "runtime_address", "size", "sha256"])
        for f in result["functions"]:
            writer.writerow([
                result["file"], result["game_code"], result["software_version"], result["family"],
                f["name"], f["file_offset"], f["runtime_address"], f["size"], f["sha256"],
            ])

if __name__ == "__main__":
    main()
