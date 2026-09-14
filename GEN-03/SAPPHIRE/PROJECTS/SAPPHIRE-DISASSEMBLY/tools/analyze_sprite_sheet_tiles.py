#!/usr/bin/env python3
"""Fingerprint the sprite-sheet/tile-range block in a local Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROM_BASE = 0x08000000
AXPE = [
    ("LoadSpriteSheet", 0x22A8, 0x22EC),
    ("LoadSpriteSheets", 0x22EC, 0x2318),
    ("AllocTilesForSpriteSheet", 0x2318, 0x2344),
    ("AllocTilesForSpriteSheets", 0x2344, 0x2370),
    ("LoadTilesForSpriteSheet", 0x2370, 0x239C),
    ("LoadTilesForSpriteSheets", 0x239C, 0x23C8),
    ("FreeSpriteTilesByTag", 0x23C8, 0x2440),
    ("FreeSpriteTileRanges", 0x2440, 0x2480),
    ("GetSpriteTileStartByTag", 0x2480, 0x24AC),
    ("IndexOfSpriteTileTag", 0x24AC, 0x24D8),
    ("GetSpriteTileTagByTileStart", 0x24D8, 0x2524),
    ("AllocSpriteTileRange", 0x2524, 0x256C),
    ("RequestSpriteSheetCopy", 0x256C, 0x2594),
    ("LoadSpriteSheetDeferred", 0x2594, 0x25C8),
]
FAMILY = {
    "AXPJ": ("jp", -0xE4),
    "AXPE": ("axpe", 0),
    "AXPD": ("extended_european", 0x134),
    "AXPF": ("extended_european", 0x134),
    "AXPI": ("extended_european", 0x134),
}
TARGET_ID = {
    ("AXPJ", 0): "JPN-AXPJ-v0",
    ("AXPE", 0): "USA-AXPE-v0",
    ("AXPE", 1): "EUR-AXPE-v1",
    ("AXPE", 2): "USA-EUR-AXPE-v2",
    ("AXPD", 1): "DEU-AXPD-v1",
    ("AXPF", 0): "FRA-AXPF-v0",
    ("AXPF", 1): "FRA-AXPF-v1",
    ("AXPI", 0): "ITA-AXPI-v0",
    ("AXPI", 1): "ITA-AXPI-v1",
}

def analyze(path: Path):
    data = path.read_bytes()
    code = data[0xAC:0xB0].decode("ascii", errors="replace")
    version = data[0xBC]
    key = (code, version)
    if code not in FAMILY or key not in TARGET_ID:
        raise ValueError(f"unsupported Sapphire target: {code} v{version}")
    family, delta = FAMILY[code]
    funcs = []
    for name, start, end in AXPE:
        start += delta
        end += delta
        chunk = data[start:end]
        funcs.append({
            "name": name,
            "file_offset": f"0x{start:08X}",
            "runtime_address": f"0x{ROM_BASE + start:08X}",
            "size": end - start,
            "sha256": hashlib.sha256(chunk).hexdigest(),
        })
    return {
        "file": path.name,
        "target_id": TARGET_ID[key],
        "game_code": code,
        "software_version": version,
        "family": family,
        "functions": funcs,
    }

def main():
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
        writer.writerow(["file", "target_id", "game_code", "software_version", "family", "function", "file_offset", "runtime_address", "size", "sha256"])
        for func in result["functions"]:
            writer.writerow([result["file"], result["target_id"], result["game_code"], result["software_version"], result["family"], func["name"], func["file_offset"], func["runtime_address"], func["size"], func["sha256"]])

if __name__ == "__main__":
    main()
