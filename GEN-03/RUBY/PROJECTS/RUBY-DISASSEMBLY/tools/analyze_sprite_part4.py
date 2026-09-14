#!/usr/bin/env python3
"""Verify/fingerprint the final Pokémon Ruby sprite.c block.

Scope: SetSubspriteTables through AddSubspritesToOamBuffer.
The end offset is the verified sprite.o -> text.o boundary.
ROMs are read-only inputs and are never emitted.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import defaultdict
from pathlib import Path

ROM_BASE = 0x08000000

def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rom-dir", required=True, type=Path)
    p.add_argument("--source-manifest", type=Path, default=Path("manifests/source_roms.json"))
    p.add_argument("--layouts", type=Path, default=Path("symbols/sprite_part4_layouts.csv"))
    p.add_argument("--targets", type=Path, default=Path("symbols/sprite_part4_targets.csv"))
    p.add_argument("--out", type=Path, default=Path("symbols/sprite_part4_fingerprints.csv"))
    p.add_argument("--verify-only", action="store_true")
    args = p.parse_args()

    sources = {r["id"]: r for r in json.loads(args.source_manifest.read_text(encoding="utf-8"))["roms"]}
    layouts = defaultdict(list)
    with args.layouts.open(encoding="utf-8", newline="") as fp:
        for r in csv.DictReader(fp):
            layouts[r["layout"]].append((r["symbol"], int(r["relative_offset"], 16), int(r["size"])))
    with args.targets.open(encoding="utf-8", newline="") as fp:
        targets = list(csv.DictReader(fp))

    records = []
    for target in targets:
        tid = target["target"]
        source = sources[tid]
        data = (args.rom_dir / source["file"]).read_bytes()
        if sha1(data) != source["sha1"]:
            raise SystemExit(f"{tid}: whole-ROM SHA-1 mismatch")

        base = int(target["part4_base_offset"], 16)
        end = int(target["sprite_end_offset"], 16)
        region = data[base:end]
        if len(region) != int(target["mapped_size"]) or sha1(region) != target["mapped_sha1"]:
            raise SystemExit(f"{tid}: Part-4 region verification failed")

        layout_name = target["layout"]
        for symbol, rel, size in layouts[layout_name]:
            start = base + rel
            chunk = data[start:start + size]
            records.append({
                "target": tid,
                "symbol": symbol,
                "file_offset": f"0x{start:X}",
                "address": f"0x{ROM_BASE + start:08X}",
                "thumb_address": f"0x{ROM_BASE + start + 1:08X}",
                "size": size,
                "sha1": sha1(chunk),
            })

        # text.o starts with UpdateBGRegs; compiler output differs in Japanese.
        prefix = data[end:end + 4]
        expected = bytes.fromhex("10b5074c") if layout_name == "japanese" else bytes.fromhex("02780b49")
        if prefix != expected:
            raise SystemExit(f"{tid}: sprite.o -> text.o boundary verification failed")

    if args.verify_only:
        print(f"verified {len(targets)} targets / {len(records)} function records")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fp:
        fields = ["target","symbol","file_offset","address","thumb_address","size","sha1"]
        w = csv.DictWriter(fp, fieldnames=fields, lineterminator="\n")
        w.writeheader(); w.writerows(records)
    print(f"verified {len(targets)} targets / {len(records)} function records")
    print(f"wrote {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
