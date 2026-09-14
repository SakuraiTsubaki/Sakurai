#!/usr/bin/env python3
"""Fingerprint the affine-frame/public-animation API block in a local Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROM_BASE = 0x08000000
AXPE = [
    ("ApplyAffineAnimFrameRelativeAndUpdateMatrix", 0x1DFC, 0x1E94),
    ("ConvertScaleParam", 0x1E94, 0x1EAC),
    ("GetAffineAnimFrame", 0x1EAC, 0x1F18),
    ("ApplyAffineAnimFrame", 0x1F18, 0x1F58),
    ("StartSpriteAnim", 0x1F58, 0x1F70),
    ("StartSpriteAnimIfDifferent", 0x1F70, 0x1F8C),
    ("SeekSpriteAnim", 0x1F8C, 0x2008),
    ("StartSpriteAffineAnim", 0x2008, 0x2034),
    ("StartSpriteAffineAnimIfDifferent", 0x2034, 0x2068),
    ("ChangeSpriteAffineAnim", 0x2068, 0x20A0),
    ("ChangeSpriteAffineAnimIfDifferent", 0x20A0, 0x20D4),
    ("SetSpriteSheetFrameTileNum", 0x20D4, 0x212C),
    ("ResetAffineAnimData", 0x212C, 0x2160),
    ("AllocOamMatrix", 0x2160, 0x2198),
    ("FreeOamMatrix", 0x2198, 0x21D8),
    ("InitSpriteAffineAnim", 0x21D8, 0x2228),
    ("SetOamMatrixRotationScaling", 0x2228, 0x22A8),
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
    if len(data) < 0xC0:
        raise ValueError("file too small to be a GBA ROM")
    code = data[0xAC:0xB0].decode("ascii", errors="replace")
    version = data[0xBC]
    key = (code, version)
    if code not in FAMILY:
        raise ValueError(f"unsupported game code: {code!r}")
    if key not in TARGET_ID:
        raise ValueError(f"unsupported Sapphire revision: {code} v{version}")
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
        writer.writerow([
            "file", "target_id", "game_code", "software_version", "family",
            "function", "file_offset", "runtime_address", "size", "sha256"
        ])
        for func in result["functions"]:
            writer.writerow([
                result["file"], result["target_id"], result["game_code"],
                result["software_version"], result["family"], func["name"],
                func["file_offset"], func["runtime_address"], func["size"], func["sha256"]
            ])

if __name__ == "__main__":
    main()
