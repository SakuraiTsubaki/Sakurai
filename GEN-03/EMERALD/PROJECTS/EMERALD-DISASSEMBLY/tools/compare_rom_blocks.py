#!/usr/bin/env python3
"""Compare same-offset blocks across multiple local ROMs.

The output is intended for coarse address-space surveying. It records equality
relationships only; it does not copy ROM payloads into the repository.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--block-size", type=lambda s: int(s, 0), default=0x10000)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("rom", nargs="+", help="LABEL=path/to/reference.gba")
    args = p.parse_args()

    roms: dict[str, bytes] = {}
    for spec in args.rom:
        label, sep, raw_path = spec.partition("=")
        if not sep:
            p.error(f"ROM argument must be LABEL=PATH: {spec}")
        roms[label] = Path(raw_path).read_bytes()

    sizes = {len(data) for data in roms.values()}
    if len(sizes) != 1:
        raise SystemExit(f"ROM sizes differ: {sorted(sizes)}")

    size = sizes.pop()
    if size % args.block_size:
        raise SystemExit("ROM size is not divisible by block size")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["block", "start", "end", "distinct_payloads",
                    "same_offset_equality_groups"])

        for index, start in enumerate(range(0, size, args.block_size)):
            end = start + args.block_size
            groups: dict[str, list[str]] = {}
            for label, data in roms.items():
                digest = hashlib.sha1(data[start:end]).hexdigest()
                groups.setdefault(digest, []).append(label)

            equality = ";".join(sorted("+".join(labels)
                                       for labels in groups.values()))
            w.writerow([index, f"0x{start:08X}", f"0x{end - 1:08X}",
                        len(groups), equality])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
