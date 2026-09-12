#!/usr/bin/env python3
"""Compare fixed-size ROM banks across GBA releases without modifying source ROMs."""
import argparse
import csv
import hashlib
import pathlib
import sys
from collections import defaultdict

BANK_SIZE = 0x10000


def release_id(data: bytes) -> str:
    if len(data) < 0xC0:
        raise ValueError("file too small for GBA header")
    code = data[0xAC:0xB0].decode("ascii", "replace")
    ver = data[0xBC]
    return f"{code}-R{ver}"


def load(path: pathlib.Path):
    data = path.read_bytes()
    if len(data) % BANK_SIZE:
        raise ValueError(f"{path}: size is not a multiple of 64 KiB")
    return release_id(data), data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", nargs="+", type=pathlib.Path)
    ap.add_argument("--csv", action="store_true", help="emit CSV instead of TSV")
    ns = ap.parse_args()
    loaded = [load(p) for p in ns.rom]
    sizes = {len(data) for _, data in loaded}
    if len(sizes) != 1:
        raise SystemExit("all ROMs must have the same size")
    ids = [rid for rid, _ in loaded]
    if len(ids) != len(set(ids)):
        raise SystemExit("release IDs must be unique")
    bank_count = next(iter(sizes)) // BANK_SIZE
    dialect = "excel" if ns.csv else "excel-tab"
    w = csv.writer(sys.stdout, dialect=dialect, lineterminator="\n")
    w.writerow(["bank_index", "start_offset_hex", "unique_variants", "largest_shared_group_count", "variant_groups"])
    for bank in range(bank_count):
        groups = defaultdict(list)
        start = bank * BANK_SIZE
        for rid, data in loaded:
            digest = hashlib.sha1(data[start:start + BANK_SIZE]).hexdigest()
            groups[digest].append(rid)
        ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[1], kv[0]))
        encoded = "|".join("+".join(members) + "@" + digest[:12] for digest, members in ordered)
        w.writerow([bank, f"0x{start:08X}", len(groups), max(map(len, groups.values())), encoded])


if __name__ == "__main__":
    main()
