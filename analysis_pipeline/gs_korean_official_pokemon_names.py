#!/usr/bin/env python3
"""Cross-check GS Korean's 256 fixed Pokémon-name slots against Pokémon Korea.

The official source is the current Pokémon Korea Pokédex.  Its AJAX response
contains alternate forms as additional records with the same National Pokédex
number; the first record for each number is the base-form display name used by
this comparison.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from gs_korean_codec import build_maps, encode_text


SOURCE_INDEX = "https://pokemonkorea.co.kr/pokedex"
SOURCE_AJAX = "https://pokemonkorea.co.kr/ajax/pokedex"
NAME_RE = re.compile(
    r"pokedex_detail\('(?P<page>\d+)',\s*'(?P<id>\d+)'\).*?"
    r"<h3><p>No\.(?P<dex>\d{4})</p>\s*(?P<name>[^<]+)</h3>",
    re.S,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_official_pages(paths: list[Path], accessed: str) -> tuple[list[dict], list[dict]]:
    by_dex: dict[int, dict] = {}
    pages: list[dict] = []
    for path in sorted(paths, key=lambda p: int(re.search(r"(\d+)", p.stem).group(1))):
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        matches = list(NAME_RE.finditer(text))
        pages.append(
            {
                "page_file": path.name,
                "sha256": sha256(raw),
                "records_in_response": len(matches),
            }
        )
        for match in matches:
            dex = int(match.group("dex"))
            if dex not in by_dex:
                detail_id = int(match.group("id"))
                by_dex[dex] = {
                    "national_dex_number": dex,
                    "latest_official_korean": match.group("name").strip(),
                    "official_detail_record_id": detail_id,
                    "official_source": f"https://pokemonkorea.co.kr/pokedex/view/{detail_id}",
                    "official_index_source": SOURCE_INDEX,
                    "source_accessed_date": accessed,
                    "selection_rule": "FIRST_RECORD_PER_DEX_NUMBER_BASE_FORM",
                }
    expected = set(range(1, 252))
    actual = set(by_dex)
    if actual != expected:
        raise ValueError(
            f"Official Pokédex coverage mismatch; missing={sorted(expected-actual)}, "
            f"extra={sorted(actual-expected)}"
        )
    return [by_dex[i] for i in range(1, 252)], pages


def slot_identity(index: int) -> tuple[str, str, str]:
    species_byte = (index + 1) & 0xFF
    if index < 251:
        return f"0x{species_byte:02X}", "NATIONAL_DEX_SPECIES", str(index + 1)
    labels = {
        251: "RESERVED_FC",
        252: "EGG_FD",
        253: "RESERVED_FE",
        254: "RESERVED_FF",
        255: "NO_MON_00_LOOKUP_UNDERFLOW",
    }
    return f"0x{species_byte:02X}", labels[index], ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("gold_rom", type=Path)
    parser.add_argument("phase2_csv", type=Path)
    parser.add_argument("official_html_dir", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--accessed", default=date.today().isoformat())
    args = parser.parse_args()

    html_paths = list(args.official_html_dir.glob("pokeajax_*.html"))
    if not html_paths:
        raise ValueError("No pokeajax_*.html official snapshots found")
    official, page_evidence = parse_official_pages(html_paths, args.accessed)
    official_by_dex = {row["national_dex_number"]: row for row in official}

    extracted = [
        row for row in read_csv(args.phase2_csv)
        if row["category"] == "POKEMON_NAME_SLOTS"
    ]
    if len(extracted) != 256:
        raise ValueError(f"Expected 256 ROM slots, got {len(extracted)}")

    maps = build_maps(args.gold_rom.read_bytes())
    rows: list[dict] = []
    for index, source in enumerate(extracted):
        species_hex, slot_kind, dex_text = slot_identity(index)
        original = source["decoded_text"]
        if dex_text:
            official_row = official_by_dex[int(dex_text)]
            latest = official_row["latest_official_korean"]
            encoded = encode_text(latest, maps)
            same = original == latest
            rows.append(
                {
                    "slot_index_zero_based": index,
                    "lookup_species_byte_hex": species_hex,
                    "slot_kind": slot_kind,
                    "national_dex_number": int(dex_text),
                    "original_gs_korean": original,
                    "latest_official_korean": latest,
                    "final_korean": latest,
                    "name_changed": not same,
                    "change_reason": "" if same else "LATEST_OFFICIAL_KOREAN_NAME",
                    "verification_status": "OFFICIAL_VERIFIED_CURRENT",
                    "official_source": official_row["official_source"],
                    "official_index_source": SOURCE_INDEX,
                    "source_accessed_date": args.accessed,
                    "encoded_length_bytes": len(encoded),
                    "encoded_hex": encoded.hex(" "),
                    "fixed_slot_capacity_bytes": 10,
                    "fits_fixed_slot": len(encoded) <= 10,
                    "bank_hex": source["bank_hex"],
                    "cpu_address_hex": source["cpu_address_hex"],
                    "file_offset_hex": source["file_offset_hex"],
                    "original_raw_hex": source["raw_hex"],
                }
            )
        else:
            rows.append(
                {
                    "slot_index_zero_based": index,
                    "lookup_species_byte_hex": species_hex,
                    "slot_kind": slot_kind,
                    "national_dex_number": "",
                    "original_gs_korean": original,
                    "latest_official_korean": "",
                    "final_korean": original,
                    "name_changed": False,
                    "change_reason": "INTERNAL_SLOT_PRESERVED_PENDING_ENGINE_AUDIT",
                    "verification_status": "INTERNAL_NON_POKEDEX_SLOT",
                    "official_source": "",
                    "official_index_source": "",
                    "source_accessed_date": "",
                    "encoded_length_bytes": int(source["raw_length"]),
                    "encoded_hex": source["raw_hex"],
                    "fixed_slot_capacity_bytes": 10,
                    "fits_fixed_slot": True,
                    "bank_hex": source["bank_hex"],
                    "cpu_address_hex": source["cpu_address_hex"],
                    "file_offset_hex": source["file_offset_hex"],
                    "original_raw_hex": source["raw_hex"],
                }
            )

    changed = [row for row in rows if row["name_changed"]]
    if [(r["national_dex_number"], r["original_gs_korean"], r["latest_official_korean"]) for r in changed] != [
        (61, "수륙챙이", "슈륙챙이"),
        (114, "덩구리", "덩쿠리"),
    ]:
        raise AssertionError("Unexpected official-name delta")
    if any(not row["fits_fixed_slot"] for row in rows):
        raise AssertionError("At least one final name exceeds its fixed slot")

    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "pokemon_name_official_comparison.csv", rows)
    (args.output / "pokemon_name_official_comparison.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(args.output / "official_pokemon_names_001_251.csv", official)
    (args.output / "official_pokemon_names_001_251.json").write_text(
        json.dumps(official, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    evidence = {
        "source_index": SOURCE_INDEX,
        "source_ajax": SOURCE_AJAX,
        "source_accessed_date": args.accessed,
        "request_filter": {
            "mode": "load_more",
            "snumber": 1,
            "snumber2": 251,
            "sortselval": "number asc,number_count asc",
        },
        "base_form_selection": "first returned record for each National Pokédex number",
        "pages": page_evidence,
    }
    (args.output / "official_source_evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "rom_slots": len(rows),
        "national_dex_species_slots": 251,
        "internal_slots": 5,
        "official_rows": len(official),
        "official_verified_rows": sum(r["verification_status"] == "OFFICIAL_VERIFIED_CURRENT" for r in rows),
        "changed_names": len(changed),
        "unchanged_official_names": 251 - len(changed),
        "changed_entries": [
            {
                "national_dex_number": r["national_dex_number"],
                "original": r["original_gs_korean"],
                "latest_official": r["latest_official_korean"],
                "encoded_length_bytes": r["encoded_length_bytes"],
            }
            for r in changed
        ],
        "all_final_names_fit_fixed_10_byte_slots": all(r["fits_fixed_slot"] for r in rows),
        "max_final_encoded_length_bytes": max(r["encoded_length_bytes"] for r in rows),
        "source": SOURCE_INDEX,
        "source_accessed_date": args.accessed,
    }
    (args.output / "phase6_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
