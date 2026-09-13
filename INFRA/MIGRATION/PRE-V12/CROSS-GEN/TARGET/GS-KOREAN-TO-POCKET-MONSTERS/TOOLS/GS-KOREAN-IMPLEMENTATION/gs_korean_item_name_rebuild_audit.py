#!/usr/bin/env python3
"""Audit and dry-run rebuild the GS Korean item-name region.

The official Korean Gold/Silver ROMs are read only.  The only binary output is
the derived replacement payload for Bank 6C:4000-49A1; no ROM or ROM bank is
written.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from gs_korean_codec import BANK_SIZE, TERMINATOR, build_maps, decode_text, encode_text


BANK = 0x6C
TABLE_CPU_START = 0x4000
REGION_CPU_END = 0x49A1
TABLE_OFFSET = 0
REGION_SIZE = REGION_CPU_END - TABLE_CPU_START
ITEM_SLOT_COUNT = 256
NAME_BUFFER_CAPACITY = 21
PACK_COLUMNS = 8
MART_COLUMNS = 8

NAMES_POINTERS_OFFSET = 0x35C3
GET_NAME_OFFSET = 0x35DB
GET_NTH_STRING_OFFSET = 0x3629
GET_ITEM_NAME_OFFSET = 0x368A

NAMES_POINTERS = bytes.fromhex(
    "6c 4a 4c 6c 4a 56 00 00 00 6c 00 40 00 47 dc 00 7a df 6c a1 49 04 00 40"
)
GET_NAME = bytes.fromhex(
    "f0 9f f5 e5 c5 d5 fa fa c1 fe 01 20 11 fa f9 c1 ea 0e d2 cd 5b 36 "
    "21 0b 00 19 5d 54 18 22 fa fa c1 3d 5f 16 00 21 c3 35 19 19 19 "
    "2a d7 2a 66 6f fa f9 c1 3d cd 29 36 11 36 d0 01 15 00 cd c2 31 "
    "7b ea ba d0 7a ea bb d0 d1 c1 e1 f1 d7 c9"
)
GET_NTH_STRING = bytes.fromhex("a7 c8 c5 47 0e 50 2a b9 20 fc 05 20 f9 c1 c9")
GET_ITEM_NAME = bytes.fromhex(
    "e5 c5 fa 0e d2 fe bf 30 0d ea f9 c1 3e 04 ea fa c1 cd db 35 "
    "18 03 cd a9 36 11 36 d0 c1 e1 c9"
)


def sha(data: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, data).hexdigest()


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


def extract_names(bank: bytes, maps) -> tuple[list[str], int, bytes]:
    cursor = TABLE_OFFSET
    names = []
    for _ in range(ITEM_SLOT_COUNT):
        end = bank.find(bytes([TERMINATOR]), cursor)
        if end < 0 or end >= REGION_SIZE:
            raise ValueError("Missing item-name terminator inside the item-name region")
        decoded, unknown = decode_text(bank[cursor:end], maps)
        if unknown:
            raise ValueError(f"Undefined item-name code: {unknown}")
        names.append(decoded)
        cursor = end + 1
    return names, cursor, bank[:cursor]


def verify_routines(label: str, rom: bytes) -> list[dict]:
    checks = [
        ("NamesPointers", NAMES_POINTERS_OFFSET, NAMES_POINTERS),
        ("GetName", GET_NAME_OFFSET, GET_NAME),
        ("GetNthString", GET_NTH_STRING_OFFSET, GET_NTH_STRING),
        ("GetItemName", GET_ITEM_NAME_OFFSET, GET_ITEM_NAME),
    ]
    rows = []
    for symbol, offset, expected in checks:
        actual = rom[offset : offset + len(expected)]
        if actual != expected:
            raise AssertionError(f"{label}: {symbol} mismatch")
        rows.append({
            "version": label,
            "symbol": symbol,
            "bank_hex": "0x00",
            "cpu_address_hex": f"0x{offset:04X}",
            "file_offset_hex": f"0x{offset:06X}",
            "length_bytes": len(expected),
            "sha256": sha(expected),
            "verified": True,
        })
    return rows


def build_payload(rows: list[dict[str, str]], maps) -> tuple[bytes, list[dict], int]:
    table = bytearray()
    ui_rows = []
    original_max = max(len(r["original_gs_korean"]) for r in rows)
    for row in rows:
        original = row["original_gs_korean"]
        latest = row["final_korean"]
        encoded = encode_text(latest, maps)
        table.extend(encoded)
        table.append(TERMINATOR)
        latest_tiles = len(latest)
        ui_rows.append({
            "item_id_decimal": int(row["item_id_decimal"]),
            "item_id_hex": row["item_id_hex"],
            "slot_kind": row["slot_kind"],
            "original_name": original,
            "latest_name": latest,
            "original_display_tiles": len(original),
            "latest_display_tiles": latest_tiles,
            "display_tile_delta": latest_tiles - len(original),
            "latest_encoded_bytes": len(encoded),
            "encoded_bytes_with_terminator": len(encoded) + 1,
            "name_buffer_copy_capacity_bytes": NAME_BUFFER_CAPACITY,
            "buffer_safe_with_terminator": len(encoded) + 1 <= NAME_BUFFER_CAPACITY,
            "pack_list_columns": PACK_COLUMNS,
            "mart_list_columns": MART_COLUMNS,
            "pack_list_width_safe": latest_tiles <= PACK_COLUMNS,
            "mart_list_width_safe": latest_tiles <= MART_COLUMNS,
            "exceeds_shipped_global_max_display_tiles": latest_tiles > original_max,
            "ui_risk_status": (
                "STATIC_WIDTH_SAFE_RUNTIME_TEST_PENDING"
                if latest_tiles <= min(PACK_COLUMNS, MART_COLUMNS)
                and len(encoded) + 1 <= NAME_BUFFER_CAPACITY
                else "UI_REDESIGN_REQUIRED"
            ),
        })
    if len(table) > REGION_SIZE:
        raise ValueError("Rebuilt item-name table exceeds its fixed region")
    table_length = len(table)
    return bytes(table) + bytes(REGION_SIZE - table_length), ui_rows, table_length


def audit_version(label: str, rom: bytes, comparison: list[dict[str, str]], payload: bytes) -> dict:
    maps = build_maps(rom)
    bank_start = BANK * BANK_SIZE
    original_bank = rom[bank_start : bank_start + BANK_SIZE]
    original_names, original_end, original_table = extract_names(original_bank, maps)
    if original_names != [r["original_gs_korean"] for r in comparison]:
        raise AssertionError(f"{label}: Phase 9 originals do not match the ROM")
    if original_end != REGION_SIZE:
        raise AssertionError(f"{label}: original item table does not end at 0x49A1")

    dry_bank = payload + original_bank[REGION_SIZE:]
    dry_names, dry_end, dry_table = extract_names(dry_bank, maps)
    expected = [r["final_korean"] for r in comparison]
    if dry_names != expected:
        raise AssertionError(f"{label}: dry-run item names do not round-trip")
    if any(dry_bank[dry_end:REGION_SIZE]):
        raise AssertionError(f"{label}: fixed-region padding is not zero")
    if dry_bank[REGION_SIZE:] != original_bank[REGION_SIZE:]:
        raise AssertionError(f"{label}: data after the item-name region changed")
    dry_rom = rom[:bank_start] + dry_bank + rom[bank_start + BANK_SIZE :]
    return {
        "version": label,
        "source_rom_sha1": sha(rom, "sha1"),
        "bank_6c_original_sha256": sha(original_bank),
        "bank_6c_dry_run_sha256": sha(dry_bank),
        "original_table_cpu_start_hex": "0x4000",
        "original_table_cpu_end_exclusive_hex": f"0x{TABLE_CPU_START + original_end:04X}",
        "dry_run_table_cpu_end_exclusive_hex": f"0x{TABLE_CPU_START + dry_end:04X}",
        "fixed_region_cpu_end_exclusive_hex": "0x49A1",
        "original_table_bytes": len(original_table),
        "dry_run_table_bytes": len(dry_table),
        "byte_delta": len(dry_table) - len(original_table),
        "dry_run_zero_padding_bytes": REGION_SIZE - dry_end,
        "names_pointer_entry": {"bank_hex": "0x6C", "cpu_address_hex": "0x4000"},
        "next_table_pointer_entry": {"role": "TRAINER_CLASS_NAMES", "bank_hex": "0x6C", "cpu_address_hex": "0x49A1"},
        "pointer_edits_required": False,
        "dry_run_full_rom_sha1": sha(dry_rom, "sha1"),
        "rom_output_written": False,
        "routine_checks": verify_routines(label, rom),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("gold_rom", type=Path)
    ap.add_argument("silver_rom", type=Path)
    ap.add_argument("phase9_comparison", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    comparison = read_csv(args.phase9_comparison)
    if len(comparison) != ITEM_SLOT_COUNT:
        raise ValueError("Phase 9 comparison must contain 256 rows")
    gold_rom = args.gold_rom.read_bytes()
    silver_rom = args.silver_rom.read_bytes()
    gold_maps = build_maps(gold_rom)
    payload, ui_rows, encoded_table_bytes = build_payload(comparison, gold_maps)
    gold = audit_version("KOREAN_GOLD", gold_rom, comparison, payload)
    silver = audit_version("KOREAN_SILVER", silver_rom, comparison, payload)

    gold_checks = gold.pop("routine_checks")
    silver_checks = silver.pop("routine_checks")
    normalized_gold = [{k: v for k, v in r.items() if k != "version"} for r in gold_checks]
    normalized_silver = [{k: v for k, v in r.items() if k != "version"} for r in silver_checks]
    if normalized_gold != normalized_silver:
        raise AssertionError("Gold/Silver item-name lookup routines differ")
    if gold["bank_6c_dry_run_sha256"] != silver["bank_6c_dry_run_sha256"]:
        raise AssertionError("Gold/Silver dry-run Bank 6C differs")

    args.output.mkdir(parents=True, exist_ok=True)
    payload_path = args.output / "item_name_region_candidate.bin"
    payload_path.write_bytes(payload)
    (args.output / "item_name_region_candidate.sha256").write_text(
        f"{sha(payload)}  {payload_path.name}\n", encoding="ascii"
    )
    write_csv(args.output / "item_name_ui_length_audit.csv", ui_rows)
    write_json(args.output / "item_name_ui_length_audit.json", ui_rows)
    routine_rows = gold_checks + silver_checks
    write_csv(args.output / "item_name_lookup_routine_evidence.csv", routine_rows)
    write_json(args.output / "item_name_lookup_routine_evidence.json", routine_rows)

    production_manifest = {
        "schema": "tsubaki.gs-korean-item-name-region.v1",
        "status": "CANDIDATE_NOT_FINAL",
        "payload": payload_path.name,
        "payload_sha256": sha(payload),
        "payload_size_bytes": len(payload),
        "target_bank_hex": "0x6C",
        "target_cpu_range": ["0x4000", "0x49A1"],
        "target_bank_offset_range": ["0x0000", "0x09A1"],
        "replacement_method": "replace complete fixed item-name region",
        "encoded_table_bytes": encoded_table_bytes,
        "zero_padding_bytes": len(payload) - encoded_table_bytes,
        "pointer_edits_required": False,
        "source_rom_sha1_allowlist": [gold["source_rom_sha1"], silver["source_rom_sha1"]],
        "prohibitions": ["do not distribute a ROM", "do not apply before terminology approval"],
    }
    write_json(args.output / "item_name_insertion_manifest.json", production_manifest)
    patch_plan = {
        "operation": "DEFERRED_INTEGRATED_INSERTION",
        "write_rom_now": False,
        "payload": payload_path.name,
        "method": "replace Bank 0x6C:0x4000-0x49A1 with the fixed-size candidate payload",
        "pointer_edits_required": False,
        "reason": "The item table becomes 125 bytes shorter, and the fixed region is zero-padded so the trainer table remains at 0x49A1.",
        "runtime_tests_required": [
            "pack item, ball and key-item pockets",
            "mart buy and sell lists",
            "battle item messages",
            "held-item and party/status displays",
            "TM/HM dynamic name branch",
        ],
    }
    write_json(args.output / "item_name_deferred_patch_plan.json", patch_plan)
    summary = {
        "gold": gold,
        "silver": silver,
        "gold_silver_dry_run_bank_identical": True,
        "lookup_routines_identical_and_verified": all(r["verified"] for r in routine_rows),
        "ui_rows": len(ui_rows),
        "max_original_display_tiles": max(r["original_display_tiles"] for r in ui_rows),
        "max_latest_display_tiles": max(r["latest_display_tiles"] for r in ui_rows),
        "names_with_positive_display_tile_delta": sum(r["display_tile_delta"] > 0 for r in ui_rows),
        "names_exceeding_eight_column_lists": sum(
            not r["pack_list_width_safe"] or not r["mart_list_width_safe"] for r in ui_rows
        ),
        "names_exceeding_name_buffer": sum(not r["buffer_safe_with_terminator"] for r in ui_rows),
        "candidate_payload_sha256": sha(payload),
        "candidate_payload_size_bytes": len(payload),
        "candidate_status": "CANDIDATE_NOT_FINAL",
        "dry_run_only": True,
        "rom_output_written": False,
    }
    write_json(args.output / "phase10_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
