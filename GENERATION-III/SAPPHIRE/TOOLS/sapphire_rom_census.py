#!/usr/bin/env python3
"""Inventory Pokémon Sapphire GBA ROMs without redistributing ROM data.

Outputs metadata/hashes/header validation and same-game-code revision diff summaries.
No ROM bytes are emitted except individual changed byte values in the tiny revision-diff table.
"""
from pathlib import Path
import argparse, csv, hashlib, json, re

SAVE_PATTERNS = [b"FLASH1M_V", b"FLASH512_V", b"FLASH_V", b"SRAM_V", b"EEPROM_V"]

def sha(data, name):
    return hashlib.new(name, data).hexdigest()

def inspect(path: Path):
    d = path.read_bytes()
    comp = (-sum(d[0xA0:0xBD]) - 0x19) & 0xFF
    save = []
    for pat in SAVE_PATTERNS:
        for m in re.finditer(re.escape(pat), d):
            s = d[m.start():m.start()+24].split(b"\0",1)[0]
            save.append(f"0x{m.start():08X}:{s.decode('ascii','replace')}")
    tail_ff = 0
    i = len(d)-1
    while i >= 0 and d[i] == 0xFF:
        tail_ff += 1
        i -= 1
    return {
        "file": path.name,
        "size_bytes": len(d),
        "size_mib": f"{len(d)/(1024*1024):.1f}",
        "title": d[0xA0:0xAC].decode("ascii","replace").rstrip("\0 "),
        "game_code": d[0xAC:0xB0].decode("ascii","replace"),
        "maker_code": d[0xB0:0xB2].decode("ascii","replace"),
        "software_version": d[0xBC],
        "header_checksum": f"0x{d[0xBD]:02X}",
        "header_checksum_calc": f"0x{comp:02X}",
        "header_checksum_ok": d[0xBD] == comp,
        "entry_point": d[:4].hex(),
        "nintendo_logo_sha1": sha(d[4:0xA0], "sha1"),
        "save_library": ";".join(save),
        "trailing_ff_bytes": tail_ff,
        "md5": sha(d,"md5"),
        "sha1": sha(d,"sha1"),
        "sha256": sha(d,"sha256"),
    }

def diff_pair(a: Path, b: Path):
    da, db = a.read_bytes(), b.read_bytes()
    n = min(len(da), len(db))
    diffs = [i for i in range(n) if da[i] != db[i]]
    diffs += list(range(n, max(len(da),len(db))))
    runs = []
    if diffs:
        s = p = diffs[0]
        for x in diffs[1:]:
            if x == p + 1:
                p = x
            else:
                runs.append((s,p))
                s = p = x
        runs.append((s,p))
    return {
        "from_file": a.name,
        "to_file": b.name,
        "byte_differences": len(diffs),
        "first_diff": f"0x{diffs[0]:08X}" if diffs else "",
        "last_diff": f"0x{diffs[-1]:08X}" if diffs else "",
        "contiguous_runs": len(runs),
        "largest_run": max((e-s+1 for s,e in runs), default=0),
        "tiny_diff_bytes": [
            {"offset": f"0x{x:08X}", "from": f"0x{da[x]:02X}", "to": f"0x{db[x]:02X}"}
            for x in diffs if x < n
        ] if len(diffs) <= 32 else [],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom_dir", type=Path)
    ap.add_argument("--out", type=Path, default=Path("."))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    roms = sorted(args.rom_dir.glob("*.gba"))
    inv = [inspect(p) for p in roms]
    with (args.out/"ROM-INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=inv[0].keys())
        w.writeheader()
        w.writerows(inv)
    (args.out/"ROM-INVENTORY.json").write_text(json.dumps(inv, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    groups = {}
    for p, r in zip(roms, inv):
        groups.setdefault(r["game_code"], []).append((r["software_version"], p))
    diffs = []
    for code, arr in sorted(groups.items()):
        arr = sorted(arr)
        for (_,a),(_,b) in zip(arr,arr[1:]):
            rec = diff_pair(a,b)
            rec["game_code"] = code
            diffs.append(rec)
    (args.out/"REVISION-DIFFS.json").write_text(json.dumps(diffs, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    with (args.out/"REVISION-DIFFS.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["game_code","from_file","to_file","byte_differences","first_diff","last_diff","contiguous_runs","largest_run"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k:r[k] for k in fields} for r in diffs)

if __name__ == "__main__":
    main()
