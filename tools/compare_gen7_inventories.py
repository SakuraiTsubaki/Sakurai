#!/usr/bin/env python3
"""Compare two Generation VII decompilation inventory JSON files.

Designed for Sun/Moon, Ultra Sun/Ultra Moon, and Let's Go Pikachu/Eevee pairs.
The output is metadata-only: added/removed/changed/same paths plus hashes that
appear under different paths in the two targets.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def load(path: Path) -> dict[str, dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("files") or payload.get("entries")
    if rows is None:
        raise ValueError(f"unsupported inventory schema: {path}")
    result = {}
    for row in rows:
        if "path" not in row or "sha256" not in row:
            continue
        result[row["path"]] = row
    return result


def hash_paths(rows: dict[str, dict]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = collections.defaultdict(list)
    for path, row in rows.items():
        out[row["sha256"]].append(path)
    return {h: sorted(paths) for h, paths in out.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("inventory_diff.json"))
    parser.add_argument("--left-label", default="left")
    parser.add_argument("--right-label", default="right")
    args = parser.parse_args()

    left = load(args.left)
    right = load(args.right)
    lpaths = set(left)
    rpaths = set(right)

    same = []
    changed = []
    for path in sorted(lpaths & rpaths):
        lrow, rrow = left[path], right[path]
        if lrow["sha256"] == rrow["sha256"]:
            same.append(path)
        else:
            changed.append({
                "path": path,
                "left_size": lrow.get("size"),
                "right_size": rrow.get("size"),
                "left_sha256": lrow["sha256"],
                "right_sha256": rrow["sha256"],
            })

    lh = hash_paths(left)
    rh = hash_paths(right)
    moved_or_aliased = []
    for digest in sorted(set(lh) & set(rh)):
        if lh[digest] != rh[digest]:
            moved_or_aliased.append({
                "sha256": digest,
                "left_paths": lh[digest],
                "right_paths": rh[digest],
            })

    payload = {
        "schema": "sakurai.generation-vii.inventory-diff.v1",
        "left_label": args.left_label,
        "right_label": args.right_label,
        "counts": {
            "left_files": len(left),
            "right_files": len(right),
            "same_path_same_content": len(same),
            "same_path_changed_content": len(changed),
            "left_only": len(lpaths - rpaths),
            "right_only": len(rpaths - lpaths),
            "same_content_different_path_groups": len(moved_or_aliased),
        },
        "left_only": sorted(lpaths - rpaths),
        "right_only": sorted(rpaths - lpaths),
        "same_path_same_content": same,
        "same_path_changed_content": changed,
        "same_content_different_path": moved_or_aliased,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote comparison -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
