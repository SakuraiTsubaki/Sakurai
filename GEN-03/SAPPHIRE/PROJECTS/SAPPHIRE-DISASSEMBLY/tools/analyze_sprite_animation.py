#!/usr/bin/env python3
"""Fingerprint the sprite animation block in a local Pokémon Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROM_BASE = 0x08000000
AXPE = [
    ("DrawPartyMenuMonText",0x142C,0x14FC),
    ("AnimateSprite",0x14FC,0x1544),
    ("BeginAnim",0x1544,0x1634),
    ("ContinueAnim",0x1634,0x16D4),
    ("AnimCmd_frame",0x16D4,0x1780),
    ("AnimCmd_end",0x1780,0x1798),
    ("AnimCmd_jump",0x1798,0x1860),
    ("AnimCmd_loop",0x1860,0x1880),
    ("BeginAnimLoop",0x1880,0x18B8),
    ("ContinueAnimLoop",0x18B8,0x18D8),
    ("JumpToTopOfAnimLoop",0x18D8,0x194C),
]
JP = [
    ("AnimateSprite",0x1418,0x1460),
    ("BeginAnim",0x1460,0x1550),
    ("ContinueAnim",0x1550,0x15F0),
    ("AnimCmd_frame",0x15F0,0x169C),
    ("AnimCmd_end",0x169C,0x16B4),
    ("AnimCmd_jump",0x16B4,0x177C),
    ("AnimCmd_loop",0x177C,0x179C),
    ("BeginAnimLoop",0x179C,0x17D4),
    ("ContinueAnimLoop",0x17D4,0x17F4),
    ("JumpToTopOfAnimLoop",0x17F4,0x1868),
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
    result = {
        "file": path.name,
        "target_id": TARGET_ID[(code, version)],
        "game_code": code,
        "software_version": version,
        "family": family,
        "functions": funcs,
    }
    if family == "jp":
        result["structural_note"] = "DrawPartyMenuMonText is not present between DestroySpriteAndFreeResources and AnimateSprite in this retail sequence."
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--format", choices=("json","csv"), default="json")
    args = ap.parse_args()
    r = analyze(args.rom)
    if args.format == "json":
        json.dump(r, sys.stdout, indent=2)
        print()
    else:
        w = csv.writer(sys.stdout)
        w.writerow(["file","target_id","game_code","software_version","family","function","file_offset","runtime_address","size","sha256"])
        for f in r["functions"]:
            w.writerow([r["file"],r["target_id"],r["game_code"],r["software_version"],r["family"],f["name"],f["file_offset"],f["runtime_address"],f["size"],f["sha256"]])

if __name__ == "__main__":
    main()
