#!/usr/bin/env python3
"""Cross-check GS Korean move names 1-251 with current Korean data mirrors."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from gs_korean_codec import TERMINATOR, build_maps, encode_text


PKHEX_URL = "https://github.com/kwsch/PKHeX/blob/master/PKHeX.Core/Resources/text/other/ko/text_Moves_ko.txt"
POKEAPI_URL = "https://github.com/PokeAPI/pokeapi/blob/master/data/v2/csv/move_names.csv"
PKHEX_COMMIT = "556e2c142cdee41dbd092c2f9e7efc17e9456938"
POKEAPI_COMMIT = "8fe210b21c9abbe73de93670f3d5a346c80a3625"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("gold_rom", type=Path)
    ap.add_argument("phase2_names", type=Path)
    ap.add_argument("phase4_descriptions", type=Path)
    ap.add_argument("pkhex_moves", type=Path)
    ap.add_argument("pokeapi_move_names", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--accessed", required=True)
    args = ap.parse_args()

    source_rows = [r for r in read_csv(args.phase2_names) if r["category"] == "MOVE_NAMES"]
    if len(source_rows) != 251:
        raise ValueError(f"Expected 251 ROM move names, got {len(source_rows)}")

    descriptions = {int(r["move_id"]): r for r in read_csv(args.phase4_descriptions)}
    if set(descriptions) != set(range(1, 252)):
        raise ValueError("Phase 4 descriptions do not cover move IDs 1-251")

    pkhex_lines = args.pkhex_moves.read_text(encoding="utf-8-sig").splitlines()
    if len(pkhex_lines) < 252:
        raise ValueError("PKHeX move list is too short")
    pkhex = {i: pkhex_lines[i] for i in range(1, 252)}

    pokeapi = {
        int(r["move_id"]): r["name"]
        for r in read_csv(args.pokeapi_move_names)
        if r["local_language_id"] == "3" and 1 <= int(r["move_id"]) <= 251
    }
    if set(pokeapi) != set(range(1, 252)):
        raise ValueError("PokéAPI Korean move rows do not cover IDs 1-251")
    disagreements = [i for i in range(1, 252) if pkhex[i] != pokeapi[i]]
    if disagreements:
        raise AssertionError(f"Current-source disagreement at move IDs: {disagreements}")

    maps = build_maps(args.gold_rom.read_bytes())
    rows: list[dict] = []
    old_total = 0
    new_total = 0
    for move_id, source in enumerate(source_rows, 1):
        original = source["decoded_text"]
        latest = pkhex[move_id]
        encoded = encode_text(latest, maps)
        old_record_length = int(source["raw_length"]) + 1
        new_record_length = len(encoded) + 1
        old_total += old_record_length
        new_total += new_record_length
        same = original == latest
        spacing_only = not same and "".join(original.split()) == "".join(latest.split())
        category = "UNCHANGED" if same else ("SPACING_NORMALIZATION" if spacing_only else "RENAMED_OR_SPELLING")
        desc = descriptions[move_id]
        rows.append(
            {
                "move_id": move_id,
                "original_gs_korean": original,
                "latest_korean": latest,
                "final_korean": latest,
                "name_changed": not same,
                "change_category": category,
                "verification_status": "CURRENT_LOCALIZATION_DATA_CONSENSUS",
                "source_agreement": "PKHEX_EQUALS_POKEAPI",
                "pkhex_source": PKHEX_URL,
                "pkhex_commit": PKHEX_COMMIT,
                "pokeapi_source": POKEAPI_URL,
                "pokeapi_commit": POKEAPI_COMMIT,
                "source_accessed_date": args.accessed,
                "original_encoded_length_bytes": int(source["raw_length"]),
                "latest_encoded_length_bytes": len(encoded),
                "record_byte_delta_with_terminator": new_record_length - old_record_length,
                "latest_encoded_hex": encoded.hex(" "),
                "bank_hex": source["bank_hex"],
                "cpu_address_hex": source["cpu_address_hex"],
                "file_offset_hex": source["file_offset_hex"],
                "original_raw_hex": source["raw_hex"],
                "original_gs_korean_description": desc["description"],
                "description_cpu_address_hex": desc["cpu_address_hex"],
                "description_next_count": int(desc["next_count"]),
            }
        )

    changed = [r for r in rows if r["name_changed"]]
    if len(changed) != 50:
        raise AssertionError(f"Expected 50 current-name deltas, got {len(changed)}")
    if sum(r["change_category"] == "SPACING_NORMALIZATION" for r in rows) != 29:
        raise AssertionError("Unexpected spacing-only delta count")

    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "move_name_current_comparison.csv", rows)
    write_json(args.output / "move_name_current_comparison.json", rows)
    write_csv(
        args.output / "move_name_change_list.csv",
        [{k: r[k] for k in (
            "move_id", "original_gs_korean", "latest_korean", "change_category",
            "original_encoded_length_bytes", "latest_encoded_length_bytes",
            "record_byte_delta_with_terminator", "cpu_address_hex",
        )} for r in changed],
    )
    normalized = [
        {
            "move_id": i,
            "korean_name": pkhex[i],
            "pkhex_matches_pokeapi": pkhex[i] == pokeapi[i],
        }
        for i in range(1, 252)
    ]
    write_csv(args.output / "current_move_names_001_251.csv", normalized)
    write_json(args.output / "current_move_names_001_251.json", normalized)
    evidence = {
        "warning": "PKHeX and PokeAPI are secondary mirrors, not first-party Pokémon publications.",
        "verification_policy": "Consensus is sufficient for implementation planning; rows remain below DIRECT_OFFICIAL_SOURCE_VERIFIED until first-party corroboration is attached.",
        "source_accessed_date": args.accessed,
        "pkhex": {"url": PKHEX_URL, "commit": PKHEX_COMMIT, "sha256": digest(args.pkhex_moves)},
        "pokeapi": {"url": POKEAPI_URL, "commit": POKEAPI_COMMIT, "sha256": digest(args.pokeapi_move_names), "korean_language_id": 3},
        "rows_compared": 251,
        "source_disagreements": disagreements,
    }
    write_json(args.output / "current_move_name_source_evidence.json", evidence)
    summary = {
        "move_rows": 251,
        "unchanged": sum(not r["name_changed"] for r in rows),
        "changed_total": len(changed),
        "spacing_normalization": sum(r["change_category"] == "SPACING_NORMALIZATION" for r in rows),
        "renamed_or_spelling": sum(r["change_category"] == "RENAMED_OR_SPELLING" for r in rows),
        "pkhex_pokeapi_agreement": 251,
        "direct_official_source_verified": 0,
        "all_names_encodable_in_gs_korean": True,
        "old_table_bytes_with_terminators": old_total,
        "new_table_bytes_with_terminators": new_total,
        "table_byte_delta": new_total - old_total,
        "max_latest_name_encoded_bytes": max(r["latest_encoded_length_bytes"] for r in rows),
        "rom_output_written": False,
    }
    write_json(args.output / "phase7_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
