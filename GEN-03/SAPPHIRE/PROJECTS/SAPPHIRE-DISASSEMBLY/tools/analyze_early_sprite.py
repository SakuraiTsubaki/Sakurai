#!/usr/bin/env python3
"""Fingerprint the first reconstructed sprite.c function block in a local Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROM_BASE = 0x08000000
US = [
("ResetSpriteData",0x748,0x794),("AnimateSprites",0x794,0x7E0),("BuildOamBuffer",0x7E0,0x82C),
("UpdateOamCoords",0x82C,0x8F0),("BuildSpritePriorities",0x8F0,0x930),("SortSprites",0x930,0xAF0),
("CopyMatricesToOamBuffer",0xAF0,0xB44),("AddSpritesToOamBuffer",0xB44,0xBDC),("CreateSprite",0xBDC,0xC30),
("CreateSpriteAtEnd",0xC30,0xC9C),("CreateInvisibleSprite",0xC9C,0xCE4),("CreateSpriteAt",0xCE4,0xE3C),
("CreateSpriteAndAnimate",0xE3C,0xED0),("DestroySprite",0xED0,0xF38),("ResetOamRange",0xF38,0xF70),
("LoadOam",0xF70,0xFA0),("ClearSpriteCopyRequests",0xFA0,0xFE0),("ResetOamMatrices",0xFE0,0x100C),
("SetOamMatrix",0x100C,0x102C),("ResetSprite",0x102C,0x1040),("CalcCenterToCornerVec",0x1040,0x1084),
]
JP = [
("ResetSpriteData",0x74C,0x798),("AnimateSprites",0x798,0x7E4),("BuildOamBuffer",0x7E4,0x830),
("UpdateOamCoords",0x830,0x8F4),("BuildSpritePriorities",0x8F4,0x934),("SortSprites",0x934,0xAF4),
("CopyMatricesToOamBuffer",0xAF4,0xB40),("AddSpritesToOamBuffer",0xB40,0xBCC),("CreateSprite",0xBCC,0xC20),
("CreateSpriteAtEnd",0xC20,0xC8C),("CreateInvisibleSprite",0xC8C,0xCD4),("CreateSpriteAt",0xCD4,0xE2C),
("CreateSpriteAndAnimate",0xE2C,0xEC0),("DestroySprite",0xEC0,0xF28),("ResetOamRange",0xF28,0xF60),
("LoadOam",0xF60,0xF90),("ClearSpriteCopyRequests",0xF90,0xFD0),("ResetOamMatrices",0xFD0,0xFFC),
("SetOamMatrix",0xFFC,0x101C),("ResetSprite",0x101C,0x1030),("CalcCenterToCornerVec",0x1030,0x1074),
]
FAMILY={"AXPJ":("jp",JP,0),"AXPE":("axpe",US,0),"AXPD":("extended_european",US,0x134),"AXPF":("extended_european",US,0x134),"AXPI":("extended_european",US,0x134)}

def analyze(path: Path):
    data=path.read_bytes()
    code=data[0xAC:0xB0].decode("ascii",errors="replace")
    if code not in FAMILY: raise ValueError(f"unsupported game code: {code!r}")
    fam,ranges,delta=FAMILY[code]
    funcs=[]
    for name,start,end in ranges:
        start+=delta; end+=delta; chunk=data[start:end]
        funcs.append({"name":name,"file_offset":f"0x{start:08X}","runtime_address":f"0x{ROM_BASE+start:08X}","size":end-start,"sha256":hashlib.sha256(chunk).hexdigest()})
    return {"file":path.name,"game_code":code,"software_version":data[0xBC],"family":fam,"functions":funcs}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("rom",type=Path); ap.add_argument("--format",choices=("json","csv"),default="json"); a=ap.parse_args(); r=analyze(a.rom)
    if a.format=="json": json.dump(r,sys.stdout,indent=2); print()
    else:
        w=csv.writer(sys.stdout); w.writerow(["file","game_code","software_version","family","function","file_offset","runtime_address","size","sha256"])
        for f in r["functions"]: w.writerow([r["file"],r["game_code"],r["software_version"],r["family"],f["name"],f["file_offset"],f["runtime_address"],f["size"],f["sha256"]])
if __name__=="__main__": main()
