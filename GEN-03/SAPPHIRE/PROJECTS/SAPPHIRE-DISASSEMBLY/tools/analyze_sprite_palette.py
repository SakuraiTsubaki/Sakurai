#!/usr/bin/env python3
"""Fingerprint the sprite-palette allocation/tag block in a local Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROM_BASE = 0x08000000
AXPE = [
    ("FreeAllSpritePalettes", 0x25C8, 0x2600),
    ("LoadSpritePalette", 0x2600, 0x264C),
    ("LoadSpritePalettes", 0x264C, 0x2678),
    ("DoLoadSpritePalette", 0x2678, 0x2690),
    ("AllocSpritePalette", 0x2690, 0x26C0),
    ("IndexOfSpritePaletteTag", 0x26C0, 0x26F8),
    ("GetSpritePaletteTagByPaletteNum", 0x26F8, 0x2708),
    ("FreeSpritePaletteByTag", 0x2708, 0x2730),
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
    return {"file": path.name, "target_id": TARGET_ID[key], "game_code": code,
            "software_version": version, "family": family, "functions": funcs}

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
        w = csv.writer(sys.stdout)
        w.writerow(["file", "target_id", "game_code", "software_version", "family", "function",
                    "file_offset", "runtime_address", "size", "sha256"])
        for f in result["functions"]:
            w.writerow([result["file"], result["target_id"], result["game_code"],
                        result["software_version"], result["family"], f["name"],
                        f["file_offset"], f["runtime_address"], f["size"], f["sha256"]])

if __name__ == "__main__":
    main()
