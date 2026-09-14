#!/usr/bin/env python3
"""Analyze aligned similarities/differences across Pokémon FireRed ROM baselines.

This tool never modifies ROMs. It emits compact block-equivalence ranges and
pairwise similarity statistics suitable for tracking language/revision layout.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

DEFAULT_BLOCK_SIZE = 0x1000


def sha1_blocks(data: bytes, block_size: int) -> list[bytes]:
    return [
        hashlib.sha1(data[i : i + block_size]).digest()
        for i in range(0, len(data), block_size)
    ]


def partition_pattern(hashes: dict[str, list[bytes]], names: list[str], index: int) -> tuple[int, ...]:
    labels: dict[bytes, int] = {}
    next_label = 0
    pattern: list[int] = []
    for name in names:
        h = hashes[name][index]
        if h not in labels:
            labels[h] = next_label
            next_label += 1
        pattern.append(labels[h])
    return tuple(pattern)


def ranges_from_patterns(patterns: list[tuple[int, ...]]) -> list[tuple[int, int, tuple[int, ...]]]:
    if not patterns:
        return []
    out = []
    start = 0
    for i in range(1, len(patterns) + 1):
        if i == len(patterns) or patterns[i] != patterns[start]:
            out.append((start, i, patterns[start]))
            start = i
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path, help="JSON mapping baseline id -> ROM path")
    ap.add_argument("--out", type=Path, default=Path("analysis/rom_layout"))
    ap.add_argument("--block-size", type=lambda s: int(s, 0), default=DEFAULT_BLOCK_SIZE)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    names = list(manifest)
    roms = {name: Path(path).read_bytes() for name, path in manifest.items()}
    sizes = {len(data) for data in roms.values()}
    if len(sizes) != 1:
        raise SystemExit(f"ROM sizes differ: {sorted(sizes)}")
    size = sizes.pop()
    if size % args.block_size:
        raise SystemExit("ROM size is not a whole number of blocks")

    hashes = {name: sha1_blocks(data, args.block_size) for name, data in roms.items()}
    block_count = size // args.block_size
    patterns = [partition_pattern(hashes, names, i) for i in range(block_count)]
    ranges = ranges_from_patterns(patterns)

    args.out.mkdir(parents=True, exist_ok=True)

    with (args.out / "ranges_4k.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["start", "end_exclusive", "size", *names, "group_count"])
        for start_block, end_block, pattern in ranges:
            start = start_block * args.block_size
            end = end_block * args.block_size
            w.writerow([
                f"0x{start:06X}",
                f"0x{end:06X}",
                end - start,
                *pattern,
                len(set(pattern)),
            ])

    with (args.out / "pairwise_similarity.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["baseline_a", "baseline_b", "same_blocks", "total_blocks", "same_bytes_aligned", "same_percent"])
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                same = sum(x == y for x, y in zip(hashes[a], hashes[b]))
                same_bytes = same * args.block_size
                w.writerow([a, b, same, block_count, same_bytes, f"{100.0 * same / block_count:.4f}"])

    summary = {
        "rom_size": size,
        "block_size": args.block_size,
        "block_count": block_count,
        "baseline_order": names,
        "range_count": len(ranges),
        "all_baselines_identical_ranges": [
            {
                "start": start * args.block_size,
                "end_exclusive": end * args.block_size,
                "size": (end - start) * args.block_size,
            }
            for start, end, pattern in ranges
            if len(set(pattern)) == 1
        ],
        "last_non_ff": {
            name: max(i for i, value in enumerate(data) if value != 0xFF)
            for name, data in roms.items()
        },
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
