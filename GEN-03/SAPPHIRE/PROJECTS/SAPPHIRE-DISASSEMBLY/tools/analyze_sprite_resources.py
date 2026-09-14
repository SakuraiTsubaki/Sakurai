#!/usr/bin/env python3
"""Fingerprint the sprite tile/copy/resource-management block in a local Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROM_BASE = 0x08000000
AXPE = [
    ("AllocSpriteTiles",0x1084,0x11A0),
    ("SpriteTileAllocBitmapOp",0x11A0,0x1210),
    ("SpriteCallbackDummy",0x1210,0x1214),
    ("ProcessSpriteCopyRequests",0x1214,0x1270),
    ("RequestSpriteFrameImageCopy",0x1270,0x12D4),
    ("RequestSpriteCopy",0x12D4,0x1324),
    ("CopyFromSprites",0x1324,0x134C),
    ("CopyToSprites",0x134C,0x1374),
    ("ResetAllSprites",0x1374,0x13B4),
    ("FreeSpriteTiles",0x13B4,0x13D0),
    ("FreeSpritePalette",0x13D0,0x13E0),
    ("FreeSpriteOamMatrix",0x13E0,0x140C),
    ("DestroySpriteAndFreeResources",0x140C,0x142C),
]
JP = [
    ("AllocSpriteTiles",0x1074,0x1190),
    ("SpriteTileAllocBitmapOp",0x1190,0x1200),
    ("SpriteCallbackDummy",0x1200,0x1204),
    ("ProcessSpriteCopyRequests",0x1204,0x1260),
    ("RequestSpriteFrameImageCopy",0x1260,0x12C4),
    ("RequestSpriteCopy",0x12C4,0x1314),
    ("CopyFromSprites",0x1314,0x133C),
    ("CopyToSprites",0x133C,0x1364),
    ("ResetAllSprites",0x1364,0x13A0),
    ("FreeSpriteTiles",0x13A0,0x13BC),
    ("FreeSpritePalette",0x13BC,0x13CC),
    ("FreeSpriteOamMatrix",0x13CC,0x13F8),
    ("DestroySpriteAndFreeResources",0x13F8,0x1418),
]
FAMILY = {
    "AXPJ": ("jp", JP, 0),
    "AXPE": ("axpe", AXPE, 0),
    "AXPD": ("extended_european", AXPE, 0x134),
    "AXPF": ("extended_european", AXPE, 0x134),
    "AXPI": ("extended_european", AXPE, 0x134),
}
TARGET_ID = {
    ("AXPJ",0): "JPN-AXPJ-v0",
    ("AXPE",0): "USA-AXPE-v0",
    ("AXPE",1): "EUR-AXPE-v1",
    ("AXPE",2): "USA-EUR-AXPE-v2",
    ("AXPD",1): "DEU-AXPD-v1",
    ("AXPF",0): "FRA-AXPF-v0",
    ("AXPF",1): "FRA-AXPF-v1",
    ("AXPI",0): "ITA-AXPI-v0",
    ("AXPI",1): "ITA-AXPI-v1",
}

def analyze(path: Path):
    data = path.read_bytes()
    code = data[0xAC:0xB0].decode("ascii", errors="replace")
    version = data[0xBC]
    if code not in FAMILY:
        raise ValueError(f"unsupported game code: {code!r}")
    if (code, version) not in TARGET_ID:
        raise ValueError(f"unsupported Sapphire revision: {code} v{version}")
    family, ranges, delta = FAMILY[code]
    funcs = []
    for name, start, end in ranges:
        start += delta
        end += delta
        chunk = data[start:end]
        funcs.append({
            "name": name,
            "file_offset": f"0x{start:08X}",
            "runtime_address": f"0x{ROM_BASE+start:08X}",
            "size": end-start,
            "sha256": hashlib.sha256(chunk).hexdigest(),
        })
    return {
        "file": path.name,
        "target_id": TARGET_ID[(code, version)],
        "game_code": code,
        "software_version": version,
        "family": family,
        "functions": funcs,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--format", choices=("json","csv"), default="json")
    a = ap.parse_args()
    r = analyze(a.rom)
    if a.format == "json":
        json.dump(r, sys.stdout, indent=2)
        print()
    else:
        w = csv.writer(sys.stdout)
        w.writerow(["file","target_id","game_code","software_version","family","function","file_offset","runtime_address","size","sha256"])
        for f in r["functions"]:
            w.writerow([r["file"],r["target_id"],r["game_code"],r["software_version"],r["family"],f["name"],f["file_offset"],f["runtime_address"],f["size"],f["sha256"]])

if __name__ == "__main__":
    main()
