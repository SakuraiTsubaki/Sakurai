#!/usr/bin/env python3
"""Map and fingerprint the symbolized main.c startup region in Pokémon Ruby.

The tool never writes ROM data. It verifies each local source ROM against
manifests/source_roms.json and then regenerates the compact Phase 2 manifest
and symbol-layout/target CSVs checked into the repository.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROM_BASE = 0x08000000

INTERNATIONAL_LAYOUT = [
    ("AgbMain", 0x000),
    ("UpdateLinkAndCallCallbacks", 0x0F4),
    ("InitMainCallbacks", 0x13C),
    ("CallCallbacks", 0x15C),
    ("SetMainCallback2", 0x180),
    ("SeedRngWithRtc", 0x198),
    ("InitKeys", 0x1B4),
    ("ReadKeys", 0x1DC),
    ("InitIntrHandlers", 0x278),
    ("SetVBlankCallback", 0x2F4),
    ("SetHBlankCallback", 0x300),
    ("SetVCountCallback", 0x30C),
    ("SetSerialCallback", 0x318),
    ("VBlankIntr", 0x324),
    ("InitFlashTimer", 0x3A0),
    ("HBlankIntr", 0x3B4),
    ("VCountIntr", 0x3E4),
    ("SerialIntr", 0x414),
    ("IntrDummy", 0x444),
    ("WaitForVBlank", 0x448),
    ("DoSoftReset", 0x468),
    ("ClearPokemonCrySongs", 0x4D8),
    ("__next_object_start", 0x4FC),
]

JAPAN_LAYOUT = [
    ("AgbMain", 0x000),
    ("UpdateLinkAndCallCallbacks", 0x0FC),
    ("InitMainCallbacks", 0x144),
    ("CallCallbacks", 0x164),
    ("SetMainCallback2", 0x188),
    ("SeedRngWithRtc", 0x19C),
    ("InitKeys", 0x1B8),
    ("ReadKeys", 0x1E0),
    ("InitIntrHandlers", 0x27C),
    ("SetVBlankCallback", 0x2F8),
    ("SetHBlankCallback", 0x304),
    ("SetVCountCallback", 0x310),
    ("SetSerialCallback", 0x31C),
    ("VBlankIntr", 0x328),
    ("InitFlashTimer", 0x3A4),
    ("HBlankIntr", 0x3B8),
    ("VCountIntr", 0x3E8),
    ("SerialIntr", 0x418),
    ("IntrDummy", 0x448),
    ("WaitForVBlank", 0x44C),
    ("DoSoftReset", 0x46C),
    ("ClearPokemonCrySongs", 0x4DC),
    ("__next_object_start", 0x500),
]

LAYOUTS = {
    "japan": JAPAN_LAYOUT,
    "international": INTERNATIONAL_LAYOUT,
}


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_hex(value: str) -> int:
    return int(value, 16)


def layout_records(layout):
    return [
        [name, hex(rel), next_rel - rel]
        for (name, rel), (_, next_rel) in zip(layout, layout[1:])
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom-dir", type=Path, required=True)
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("manifests/source_roms.json"),
    )
    parser.add_argument(
        "--startup-manifest",
        type=Path,
        default=Path("manifests/startup_phase2.json"),
    )
    parser.add_argument(
        "--out-manifest",
        type=Path,
        default=Path("manifests/main_phase2.json"),
    )
    parser.add_argument(
        "--out-layouts",
        type=Path,
        default=Path("symbols/main_layouts.csv"),
    )
    parser.add_argument(
        "--out-targets",
        type=Path,
        default=Path("symbols/main_targets.csv"),
    )
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    source = load_json(args.source_manifest)
    startup = load_json(args.startup_manifest)
    source_by_id = {row["id"]: row for row in source["roms"]}

    symbols = [name for name, _ in INTERNATIONAL_LAYOUT[:-1]]
    result = {
        "schema_version": 1,
        "scope": "main.c AgbMain through ClearPokemonCrySongs",
        "address_base": f"0x{ROM_BASE:08X}",
        "symbols": symbols,
        "layouts": {
            family: layout_records(layout)
            for family, layout in LAYOUTS.items()
        },
        "targets": {},
    }
    target_rows = []

    for target_id, start_info in startup["targets"].items():
        src = source_by_id[target_id]
        rom_path = args.rom_dir / src["file"]
        data = rom_path.read_bytes()

        actual_sha1 = sha1(data)
        if actual_sha1 != src["sha1"]:
            raise SystemExit(
                f"{target_id}: SHA-1 mismatch: expected {src['sha1']}, got {actual_sha1}"
            )

        family = "japan" if target_id == "japan_rev0" else "international"
        layout = LAYOUTS[family]
        agbmain = parse_hex(start_info["agbmain_offset"])
        region_end = agbmain + layout[-1][1]
        region = data[agbmain:region_end]

        function_hashes = []
        for (_, rel), (_, next_rel) in zip(layout, layout[1:]):
            function_hashes.append(sha1(data[agbmain + rel : agbmain + next_rel]))

        region_hash = sha1(region)
        result["targets"][target_id] = [
            family,
            f"0x{agbmain:X}",
            f"0x{region_end:X}",
            len(region),
            region_hash,
            function_hashes,
        ]
        target_rows.append(
            [
                target_id,
                family,
                f"0x{agbmain:X}",
                f"0x{region_end:X}",
                len(region),
                region_hash,
            ]
        )

    if args.verify_only:
        print(f"verified {len(result['targets'])} targets")
        return 0

    for path in (args.out_manifest, args.out_layouts, args.out_targets):
        path.parent.mkdir(parents=True, exist_ok=True)

    args.out_manifest.write_text(
        json.dumps(result, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with args.out_layouts.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        writer.writerow(["family", "symbol", "relative_offset", "size"])
        for family, layout in LAYOUTS.items():
            for symbol, relative_offset, size in layout_records(layout):
                writer.writerow([family, symbol, f"0x{int(relative_offset, 16):X}", size])

    with args.out_targets.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        writer.writerow(
            [
                "target",
                "family",
                "agbmain_offset",
                "main_region_end_offset",
                "main_region_size",
                "main_region_sha1",
            ]
        )
        writer.writerows(target_rows)

    print(f"wrote {args.out_manifest}")
    print(f"wrote {args.out_layouts}")
    print(f"wrote {args.out_targets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
