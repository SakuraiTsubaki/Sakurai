#!/usr/bin/env python3
"""Inventory an unpacked Generation VI Pokémon-model archive deterministically.

Input is an already-unpacked directory containing archive members. This tool does
not require, read, or distribute a ROM/CCI/CIA image. It records member identity,
size, hashes, compression signatures, and conservative format hints without
pretending that a filename extension proves semantic role.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
from pathlib import Path


KNOWN_MAGICS = {
    b"BCH\x00": "BCH",
    b"CGFX": "CGFX",
    b"BCLIM": "BCLIM",
    b"CLIM": "BCLIM/CLIM",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def member_index(path: Path) -> int | None:
    # Prefer an all-decimal stem. Otherwise use the final decimal run.
    stem = path.stem
    if stem.isdecimal():
        return int(stem)
    matches = list(re.finditer(r"(\d+)", path.name))
    if matches:
        return int(matches[-1].group(1))
    return None


def read_prefix(path: Path, n: int = 64) -> bytes:
    with path.open("rb") as f:
        return f.read(n)


def detect_lz(prefix: bytes) -> str:
    if not prefix:
        return "empty"
    first = prefix[0]
    if first == 0x10:
        return "LZ10"
    if first == 0x11:
        return "LZ11"
    return "none-detected"


def detect_magic(prefix: bytes) -> str:
    for magic, name in KNOWN_MAGICS.items():
        if prefix.startswith(magic):
            return name
    # Game Freak containers often use tool-specific names/extensions; avoid
    # claiming a format from extension alone. Preserve printable prefix bytes.
    printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in prefix[:16])
    return f"unknown:{printable}"


def all_files(root: Path) -> list[Path]:
    return sorted(
        (p for p in root.rglob("*") if p.is_file()),
        key=lambda p: (
            member_index(p) is None,
            member_index(p) if member_index(p) is not None else 2**63,
            p.as_posix(),
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_dir", type=Path)
    parser.add_argument("--game", required=True, choices=["X", "Y", "OmegaRuby", "AlphaSapphire"])
    parser.add_argument("--archive-path", required=True, choices=["a/0/0/7", "a/0/0/8"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-label", default="unpacked-archive")
    args = parser.parse_args()

    root = args.archive_dir.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    expected = "a/0/0/7" if args.game in {"X", "Y"} else "a/0/0/8"
    if args.archive_path != expected:
        raise SystemExit(
            f"archive/game mismatch: {args.game} expects {expected}, got {args.archive_path}"
        )

    paths = all_files(root)
    rows = []
    for path in paths:
        prefix = read_prefix(path)
        rows.append({
            "game": args.game,
            "archive_path": args.archive_path,
            "member_index": "" if member_index(path) is None else member_index(path),
            "relative_path": path.relative_to(root).as_posix(),
            "filename_extension": path.suffix.lower(),
            "byte_size": path.stat().st_size,
            "sha256": sha256(path),
            "compression_hint": detect_lz(prefix),
            "signature_hint": detect_magic(prefix),
            "prefix_hex_16": prefix[:16].hex(),
            "source_label": args.source_label,
            "semantic_role": "unresolved",
            "verification": "observed-local-extraction",
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "game", "archive_path", "member_index", "relative_path",
        "filename_extension", "byte_size", "sha256", "compression_hint",
        "signature_hint", "prefix_hex_16", "source_label", "semantic_role",
        "verification",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    indexed = [r for r in rows if r["member_index"] != ""]
    indices = sorted(int(r["member_index"]) for r in indexed)
    duplicate_indices = sorted({i for i in indices if indices.count(i) > 1})

    print(f"PASS files={len(rows)} indexed_members={len(indexed)}")
    if indices:
        print(f"member_index_min={indices[0]} member_index_max={indices[-1]}")
    print(f"duplicate_member_indices={duplicate_indices}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
