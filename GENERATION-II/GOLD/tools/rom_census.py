#!/usr/bin/env python3
"""Safe metadata census for Game Boy / Game Boy Color ROM images.

Outputs only metadata, cryptographic hashes, header checks, and bank-level
fingerprints/statistics. It never embeds or copies ROM bytes into reports.
"""
from __future__ import annotations
import argparse, csv, hashlib, itertools, json, os
from collections import Counter
from pathlib import Path

BANK_SIZE = 0x4000
CART_TYPES = {0x10: "MBC3+TIMER+RAM+BATTERY"}
ROM_SIZES = {0x05: 1 << 20, 0x06: 2 << 20}
RAM_SIZES = {0x03: 32 << 10}

def sha(data: bytes, name: str) -> str:
    return hashlib.new(name, data).hexdigest()

def header_checksum(data: bytes) -> int:
    x = 0
    for i in range(0x134, 0x14D):
        x = (x - data[i] - 1) & 0xFF
    return x

def global_checksum(data: bytes) -> int:
    return (sum(data) - data[0x14E] - data[0x14F]) & 0xFFFF

def inspect(path: Path) -> dict:
    data = path.read_bytes()
    stored_global = (data[0x14E] << 8) | data[0x14F]
    hc = header_checksum(data)
    gc = global_checksum(data)
    return {
        "file": path.name,
        "size_bytes": len(data),
        "banks_16KiB": len(data) // BANK_SIZE,
        "title": data[0x134:0x13F].decode("ascii", "replace").rstrip("\x00"),
        "manufacturer": data[0x13F:0x143].decode("ascii", "replace"),
        "cgb_flag": f"0x{data[0x143]:02X}",
        "cgb_mode": "CGB-only" if data[0x143] == 0xC0 else "CGB-compatible" if data[0x143] == 0x80 else "DMG/other",
        "new_licensee": data[0x144:0x146].decode("ascii", "replace"),
        "sgb_flag": f"0x{data[0x146]:02X}",
        "cart_type": f"0x{data[0x147]:02X} {CART_TYPES.get(data[0x147], '')}".strip(),
        "rom_size_code": f"0x{data[0x148]:02X}",
        "rom_size_declared": ROM_SIZES.get(data[0x148]),
        "ram_size_code": f"0x{data[0x149]:02X}",
        "ram_size_declared": RAM_SIZES.get(data[0x149]),
        "destination": "Japan" if data[0x14A] == 0 else "Non-Japan",
        "old_licensee": f"0x{data[0x14B]:02X}",
        "mask_rom_version": data[0x14C],
        "header_checksum_stored": f"0x{data[0x14D]:02X}",
        "header_checksum_calc": f"0x{hc:02X}",
        "header_checksum_ok": hc == data[0x14D],
        "global_checksum_stored": f"0x{stored_global:04X}",
        "global_checksum_calc": f"0x{gc:04X}",
        "global_checksum_ok": gc == stored_global,
        "md5": sha(data, "md5"),
        "sha1": sha(data, "sha1"),
        "sha256": sha(data, "sha256"),
    }

def bank_hashes(path: Path) -> list[str]:
    data = path.read_bytes()
    return [hashlib.sha1(data[i:i+BANK_SIZE]).hexdigest() for i in range(0, len(data), BANK_SIZE)]

def byte_diff(a: bytes, b: bytes) -> dict:
    n = min(len(a), len(b))
    positions = [i for i in range(n) if a[i] != b[i]]
    ranges = []
    if positions:
        start = prev = positions[0]
        for pos in positions[1:]:
            if pos == prev + 1:
                prev = pos
            else:
                ranges.append((start, prev))
                start = prev = pos
        ranges.append((start, prev))
    by_bank = Counter(pos // BANK_SIZE for pos in positions)
    return {
        "compared_bytes": n,
        "different_bytes": len(positions) + abs(len(a)-len(b)),
        "contiguous_ranges_within_overlap": len(ranges),
        "changed_banks": {f"0x{k:02X}": v for k, v in sorted(by_bank.items())},
        "ranges": [{"start": f"0x{s:X}", "end": f"0x{e:X}", "length": e-s+1} for s,e in ranges],
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", nargs="?", default=".")
    ap.add_argument("--out", default="rom-census")
    args = ap.parse_args()
    root = Path(args.directory)
    files = sorted(root.glob("*.gbc"))
    rows = [inspect(p) for p in files]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    with (out / "rom_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

    hashes = {p.name: bank_hashes(p) for p in files}
    pairs = []
    for pa, pb in itertools.combinations(files, 2):
        n = min(len(hashes[pa.name]), len(hashes[pb.name]))
        same = [i for i in range(n) if hashes[pa.name][i] == hashes[pb.name][i]]
        pairs.append({"a": pa.name, "b": pb.name, "banks_compared": n,
                      "identical_same_index_banks": len(same),
                      "bank_indices": [f"0x{i:02X}" for i in same]})

    payload = {"roms": rows, "pairwise_identical_banks": pairs}
    jp0 = root / "Pocket Monsters Kin (Japan).gbc"
    jpa = root / "Pocket Monsters Kin (Japan) (Rev A).gbc"
    if jp0.exists() and jpa.exists():
        payload["japan_rev0_vs_reva"] = byte_diff(jp0.read_bytes(), jpa.read_bytes())

    (out / "baseline_census.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
