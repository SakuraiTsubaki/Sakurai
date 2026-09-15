#!/usr/bin/env python3
"""Inventory arbitrary Generation III event/e-Reader/distribution payload files.

The tool is format-agnostic on purpose: it preserves source identity first, then
records block hashes, byte-distribution statistics, and conservative printable
ASCII runs for later format-specific reverse engineering.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path


def hash_file(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def ascii_runs(data: bytes, minimum: int, limit: int) -> list[dict[str, object]]:
    out = []
    start = None
    for i, b in enumerate(data + b"\0"):
        printable = 0x20 <= b <= 0x7E
        if printable and start is None:
            start = i
        elif not printable and start is not None:
            if i - start >= minimum:
                out.append({"offset": start, "text": data[start:i].decode("ascii", errors="replace")})
                if len(out) >= limit:
                    break
            start = None
    return out


def block_summary(data: bytes, block_size: int) -> list[dict[str, object]]:
    rows = []
    for offset in range(0, len(data), block_size):
        block = data[offset:offset + block_size]
        rows.append({
            "offset": offset,
            "size": len(block),
            "sha256": hashlib.sha256(block).hexdigest(),
            "entropy": round(entropy(block), 6),
            "all_zero": not any(block),
            "all_ff": bool(block) and all(b == 0xFF for b in block),
        })
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description="Inventory an event/e-Reader/distribution payload")
    p.add_argument("payload", type=Path)
    p.add_argument("--block-size", type=lambda x: int(x, 0), default=0x1000)
    p.add_argument("--ascii-min", type=int, default=6)
    p.add_argument("--ascii-limit", type=int, default=256)
    p.add_argument("--out", type=Path)
    args = p.parse_args()

    if not args.payload.is_file():
        p.error(f"payload not found: {args.payload}")
    if args.block_size <= 0:
        p.error("--block-size must be positive")
    if args.ascii_min <= 0 or args.ascii_limit < 0:
        p.error("invalid ASCII scan limits")

    data = args.payload.read_bytes()
    report = {
        "schema_version": 1,
        "source": {
            "filename": args.payload.name,
            "size": len(data),
            "sha1": hash_file(args.payload, "sha1"),
            "sha256": hash_file(args.payload, "sha256"),
        },
        "whole_file_entropy": round(entropy(data), 6),
        "blocks": {"block_size": args.block_size, "entries": block_summary(data, args.block_size)},
        "printable_ascii": {
            "minimum_length": args.ascii_min,
            "limit": args.ascii_limit,
            "runs": ascii_runs(data, args.ascii_min, args.ascii_limit),
        },
        "notes": [
            "No file format is inferred from filename alone.",
            "High-entropy or printable regions are observations, not automatic code/data classifications."
        ],
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
