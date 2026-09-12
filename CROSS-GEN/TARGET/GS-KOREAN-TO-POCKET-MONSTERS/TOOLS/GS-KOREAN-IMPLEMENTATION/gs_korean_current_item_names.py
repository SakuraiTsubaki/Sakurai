#!/usr/bin/env python3
"""Cross-check all 256 GS Korean item-name slots with current Korean data.

The script preserves unused/internal slots and Gen II's TM/HM numbering model.
It does not write a ROM.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from gs_korean_codec import build_maps, encode_text


PKHEX_URL = "https://github.com/kwsch/PKHeX/tree/master/PKHeX.Core/Resources/text/items"
POKEAPI_URL = "https://github.com/PokeAPI/pokeapi/tree/master/data/v2/csv"
POKEGOLD_URL = "https://github.com/pret/pokegold/blob/master/data/items/names.asm"

PKHEX_ENGLISH_OVERRIDES = {
    "bicycle": "Bike",
    "secret-potion": "Secret Medicine",
    "silver-wing": "Silver Feather",
    "rainbow-wing": "Rainbow Feather",
}

# Generation II names whose later canonical item identity cannot be recovered by
# comparing the old English display label literally.
POKEAPI_IDENTIFIER_OVERRIDES = {
    0x05: "poke-ball",
    0x0D: "paralyze-heal",
    0x15: "max-elixir",
    0x25: "poke-doll",
    0x33: "x-defense",
    0x35: "x-sp-atk",
    0x37: "dowsing-machine",
    0x41: "elixir",
    0x46: "clear-bell",
    0x4A: "pecha-berry",
    0x4E: "cheri-berry",
    0x4F: "aspear-berry",
    0x50: "rawst-berry",
    0x53: "persim-berry",
    0x54: "chesto-berry",
    0x59: "blue-apricorn",
    0x5C: "yellow-apricorn",
    0x5D: "green-apricorn",
    0x61: "white-apricorn",
    0x63: "black-apricorn",
    0x65: "pink-apricorn",
    0x69: "stick",
    0x6D: "lum-berry",
    0x73: None,  # GS Ball has no current Korean row in the selected mirrors.
    0x74: "blue-card",
    0x96: "leppa-berry",
    0x9D: "heavy-ball",
    0xAD: "oran-berry",
    0xAE: "sitrus-berry",
}

# Official GS Korean is the last Korean publication for these discontinued
# objects.  Spelling is retained unless a new translation is explicitly noted.
LEGACY_FINAL = {
    0x68: ("핑크빛 리본", "LEGACY_OFFICIAL_GS_KOREAN_RETAINED"),
    0x73: ("GS볼", "LEGACY_OFFICIAL_GS_KOREAN_RETAINED"),
    0x98: ("파괴의 유전자", "LEGACY_OFFICIAL_GS_KOREAN_RETAINED"),
    0x9E: ("꽃무늬메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xA7: ("나무상자", "LEGACY_OFFICIAL_GS_KOREAN_RETAINED"),
    0xA8: ("오동나무상자", "LEGACY_OFFICIAL_GS_KOREAN_RETAINED"),
    0xAA: ("물방울무늬 리본", "NEW_TRANSLATION_NO_CURRENT_OFFICIAL_ROW"),
    0xB4: ("기와조각", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xB5: ("파도타기메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xB6: ("옥빛메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xB7: ("초상화메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xB8: ("러브리메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xB9: ("브이브이메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xBA: ("변신메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xBB: ("푸른하늘메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xBC: ("음표메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
    0xBD: ("환상의메일", "PROJECT_ORTHOGRAPHY_NORMALIZATION"),
}


def norm_english(value: str) -> str:
    value = value.lower().replace("é", "e").replace("#", "poke")
    return re.sub(r"[^a-z0-9]", "", value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_pokegold_names(path: Path) -> list[str]:
    result = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.search(r'\bli\s+"(.*)"', line)
        if match:
            result.append(match.group(1))
    if len(result) != 256:
        raise ValueError(f"Expected 256 pret item labels, got {len(result)}")
    return result


def build_pokeapi(items_path: Path, names_path: Path):
    identifiers = {int(r["id"]): r["identifier"] for r in read_csv(items_path)}
    by_identifier = {identifier: item_id for item_id, identifier in identifiers.items()}
    english = {
        int(r["item_id"]): r["name"]
        for r in read_csv(names_path)
        if r["local_language_id"] == "9"
    }
    korean = {
        int(r["item_id"]): r["name"]
        for r in read_csv(names_path)
        if r["local_language_id"] == "3"
    }
    by_english: dict[str, list[int]] = {}
    for item_id, name in english.items():
        if item_id in korean:
            by_english.setdefault(norm_english(name), []).append(item_id)
    return identifiers, by_identifier, english, korean, by_english


def build_pkhex(english_path: Path, korean_path: Path):
    english = english_path.read_text(encoding="utf-8-sig").splitlines()
    korean = korean_path.read_text(encoding="utf-8-sig").splitlines()
    if len(english) != len(korean):
        raise ValueError("PKHeX English/Korean item list length differs")
    result: dict[str, list[tuple[int, str]]] = {}
    for index, (en, ko) in enumerate(zip(english, korean)):
        result.setdefault(norm_english(en), []).append((index, ko))
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("gold_rom", type=Path)
    ap.add_argument("phase2_names", type=Path)
    ap.add_argument("phase5_master", type=Path)
    ap.add_argument("pokegold_names", type=Path)
    ap.add_argument("pkhex_english", type=Path)
    ap.add_argument("pkhex_korean", type=Path)
    ap.add_argument("pokeapi_items", type=Path)
    ap.add_argument("pokeapi_names", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--accessed", required=True)
    ap.add_argument("--pkhex-commit", required=True)
    ap.add_argument("--pokeapi-commit", required=True)
    ap.add_argument("--pokegold-commit", required=True)
    args = ap.parse_args()

    source = [r for r in read_csv(args.phase2_names) if r["category"] == "ITEM_NAMES"]
    phase5 = read_csv(args.phase5_master)
    if len(source) != 256 or len(phase5) != 256:
        raise ValueError("Expected 256 item-name and description-master rows")
    pret_names = parse_pokegold_names(args.pokegold_names)
    identifiers, by_identifier, pa_en, pa_ko, pa_by_en = build_pokeapi(
        args.pokeapi_items, args.pokeapi_names
    )
    pkhex = build_pkhex(args.pkhex_english, args.pkhex_korean)
    maps = build_maps(args.gold_rom.read_bytes())

    rows = []
    for slot, (src, desc, pret_name) in enumerate(zip(source, phase5, pret_names)):
        item_id = (slot + 1) & 0xFF
        original = src["decoded_text"]
        placeholder = original in {"?", "<?>"}
        machine = 0xBF <= item_id <= 0xF9 and not placeholder
        canonical_identifier = ""
        canonical_english = ""
        pokeapi_name = ""
        pkhex_name = ""
        pkhex_index = ""
        agreement = "NOT_APPLICABLE"

        if placeholder:
            latest = original
            status = "UNUSED_OR_INTERNAL_SLOT_PRESERVED"
            slot_kind = "UNUSED_OR_INTERNAL"
        elif machine:
            latest = original
            status = "GEN2_MACHINE_LABEL_PRESERVED"
            slot_kind = "TM_OR_HM"
        else:
            slot_kind = "NAMED_ITEM"
            override = POKEAPI_IDENTIFIER_OVERRIDES.get(item_id, "__NO_OVERRIDE__")
            candidate_ids: list[int] = []
            if override != "__NO_OVERRIDE__" and override is not None:
                if override not in by_identifier:
                    raise KeyError(f"Unknown PokeAPI identifier override: {override}")
                candidate_ids = [by_identifier[override]]
            elif override == "__NO_OVERRIDE__":
                candidate_ids = pa_by_en.get(norm_english(pret_name), [])
            if candidate_ids:
                # Duplicate regional objects have the same Korean label; prefer
                # the lowest stable PokeAPI ID.
                candidate_ids.sort()
                pa_id = candidate_ids[0]
                canonical_identifier = identifiers[pa_id]
                canonical_english = pa_en[pa_id]
                pokeapi_name = pa_ko[pa_id]
                latest = pokeapi_name
                pkhex_lookup = PKHEX_ENGLISH_OVERRIDES.get(canonical_identifier, canonical_english)
                matches = [(index, ko) for index, ko in pkhex.get(norm_english(pkhex_lookup), []) if ko]
                matched_korean = {ko for _, ko in matches}
                if pokeapi_name in matched_korean:
                    pkhex_index, pkhex_name = min((index, ko) for index, ko in matches if ko == pokeapi_name)
                    agreement = "PKHEX_EQUALS_POKEAPI" if pkhex_name == pokeapi_name else "SOURCE_DISAGREEMENT"
                    status = "CURRENT_LOCALIZATION_DATA_CONSENSUS" if agreement == "PKHEX_EQUALS_POKEAPI" else "REVIEW_REQUIRED_SOURCE_DISAGREEMENT"
                else:
                    agreement = "POKEAPI_ONLY_FOR_SELECTED_LEGACY_OBJECT"
                    status = "CURRENT_LOCALIZATION_DATA_SINGLE_MIRROR"
            elif item_id in LEGACY_FINAL:
                latest, status = LEGACY_FINAL[item_id]
                agreement = "NO_CURRENT_MIRROR_ROW"
            else:
                raise AssertionError(f"No mapping for named item ID 0x{item_id:02X}: {original} / {pret_name}")

        encoded = encode_text(latest, maps)
        original_len = int(src["raw_length"])
        same = original == latest
        spacing_only = not same and "".join(original.split()) == "".join(latest.split())
        if same:
            change_category = "UNCHANGED"
        elif spacing_only:
            change_category = "SPACING_NORMALIZATION"
        elif item_id in {0x4A, 0x4E, 0x4F, 0x50, 0x53, 0x54, 0x6D, 0x96, 0xAD, 0xAE}:
            change_category = "GENERATION_SUCCESSOR_NAME"
        elif status == "NEW_TRANSLATION_NO_CURRENT_OFFICIAL_ROW":
            change_category = "NEW_TRANSLATION"
        else:
            change_category = "RENAMED_OR_SPELLING"
        rows.append({
            "slot_index_zero_based": slot,
            "item_id_decimal": item_id,
            "item_id_hex": f"0x{item_id:02X}",
            "slot_kind": slot_kind,
            "pret_gen2_english_label": pret_name,
            "original_gs_korean": original,
            "latest_korean": latest,
            "final_korean": latest,
            "name_changed": not same,
            "change_category": change_category,
            "verification_status": status,
            "source_agreement": agreement,
            "canonical_identifier": canonical_identifier,
            "canonical_english": canonical_english,
            "pokeapi_korean": pokeapi_name,
            "pkhex_korean": pkhex_name,
            "pkhex_item_index": pkhex_index,
            "original_encoded_length_bytes": original_len,
            "latest_encoded_length_bytes": len(encoded),
            "record_byte_delta_with_terminator": len(encoded) - original_len,
            "latest_encoded_hex": encoded.hex(" "),
            "bank_hex": src["bank_hex"],
            "cpu_address_hex": src["cpu_address_hex"],
            "file_offset_hex": src["file_offset_hex"],
            "original_raw_hex": src["raw_hex"],
            "original_gs_korean_description": desc["original_gs_korean_description"],
            "description_cpu_address_hex": desc["description_cpu_address_hex"],
        })

    disagreements = [r for r in rows if r["source_agreement"] == "SOURCE_DISAGREEMENT"]
    if disagreements:
        raise AssertionError(f"Current-source disagreement: {[r['item_id_hex'] for r in disagreements]}")
    changed = [r for r in rows if r["name_changed"]]
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "item_name_current_comparison.csv", rows)
    write_json(args.output / "item_name_current_comparison.json", rows)
    master_fields = [
        "slot_index_zero_based", "item_id_decimal", "item_id_hex", "slot_kind",
        "original_gs_korean", "latest_korean", "final_korean",
        "original_gs_korean_description", "description_cpu_address_hex",
        "canonical_identifier", "canonical_english", "change_category",
        "verification_status", "source_agreement",
    ]
    master_rows = [{k: r[k] for k in master_fields} for r in rows]
    write_csv(args.output / "item_name_description_master_phase9.csv", master_rows)
    write_json(args.output / "item_name_description_master_phase9.json", master_rows)
    change_fields = [
        "item_id_decimal", "item_id_hex", "original_gs_korean", "latest_korean",
        "change_category", "verification_status", "source_agreement",
        "original_encoded_length_bytes", "latest_encoded_length_bytes",
        "record_byte_delta_with_terminator", "cpu_address_hex",
    ]
    write_csv(args.output / "item_name_change_list.csv", [{k: r[k] for k in change_fields} for r in changed])
    evidence = {
        "warning": "PKHeX and PokeAPI are secondary localization-data mirrors, not first-party Pokémon publications.",
        "policy": "Consensus supports implementation planning. Direct first-party verification remains a separate status.",
        "source_accessed_date": args.accessed,
        "pkhex": {
            "url": PKHEX_URL, "commit": args.pkhex_commit,
            "english_sha256": sha256(args.pkhex_english),
            "korean_sha256": sha256(args.pkhex_korean),
        },
        "pokeapi": {
            "url": POKEAPI_URL, "commit": args.pokeapi_commit,
            "items_sha256": sha256(args.pokeapi_items),
            "item_names_sha256": sha256(args.pokeapi_names),
            "korean_language_id": 3, "english_language_id": 9,
        },
        "gen2_semantics": {
            "url": POKEGOLD_URL, "commit": args.pokegold_commit,
            "names_asm_sha256": sha256(args.pokegold_names),
            "authority_note": "Used only to identify Gen II slot semantics; Korean ROM bytes remain primary.",
        },
    }
    write_json(args.output / "current_item_name_source_evidence.json", evidence)
    summary = {
        "item_name_slots": 256,
        "named_item_slots": sum(r["slot_kind"] == "NAMED_ITEM" for r in rows),
        "tm_hm_slots": sum(r["slot_kind"] == "TM_OR_HM" for r in rows),
        "unused_or_internal_slots": sum(r["slot_kind"] == "UNUSED_OR_INTERNAL" for r in rows),
        "unchanged": sum(not r["name_changed"] for r in rows),
        "changed_total": len(changed),
        "spacing_normalization": sum(r["change_category"] == "SPACING_NORMALIZATION" for r in rows),
        "generation_successor_name": sum(r["change_category"] == "GENERATION_SUCCESSOR_NAME" for r in rows),
        "renamed_or_spelling": sum(r["change_category"] == "RENAMED_OR_SPELLING" for r in rows),
        "new_translation": sum(r["change_category"] == "NEW_TRANSLATION" for r in rows),
        "current_data_consensus": sum(r["verification_status"] == "CURRENT_LOCALIZATION_DATA_CONSENSUS" for r in rows),
        "current_data_single_mirror": sum(r["verification_status"] == "CURRENT_LOCALIZATION_DATA_SINGLE_MIRROR" for r in rows),
        "legacy_or_editorial_without_current_mirror": sum(r["source_agreement"] == "NO_CURRENT_MIRROR_ROW" for r in rows),
        "direct_official_source_verified": 0,
        "all_final_names_encodable": True,
        "old_table_bytes_with_terminators": sum(int(r["original_encoded_length_bytes"]) + 1 for r in rows),
        "new_table_bytes_with_terminators": sum(int(r["latest_encoded_length_bytes"]) + 1 for r in rows),
        "table_byte_delta": sum(int(r["record_byte_delta_with_terminator"]) for r in rows),
        "max_latest_name_encoded_bytes": max(int(r["latest_encoded_length_bytes"]) for r in rows),
        "source_disagreements": 0,
        "rom_output_written": False,
    }
    write_json(args.output / "phase9_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
