#!/usr/bin/env python3
"""Audit and dry-run rebuild the Korean Gold/Silver move-name table.

No ROM is written.  The script verifies the shipped lookup routines, rebuilds
Bank 6C in memory with the Phase 7 names, and records hashes and UI-length risk.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from gs_korean_codec import BANK_SIZE, TERMINATOR, build_maps, decode_text, encode_text


BANK = 0x6C
TABLE_CPU = 0x564A
TABLE_OFFSET = TABLE_CPU - 0x4000
MOVE_COUNT = 251
NAMES_POINTERS_OFFSET = 0x35C3
GET_NAME_OFFSET = 0x35DB
GET_NTH_STRING_OFFSET = 0x3629
GET_MOVE_NAME_OFFSET = 0x3726

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
GET_MOVE_NAME = bytes.fromhex(
    "e5 3e 02 ea fa c1 fa 0e d2 ea f9 c1 cd db 35 11 36 d0 e1 c9"
)


def sha(data: bytes, algo: str = "sha256") -> str:
    return hashlib.new(algo, data).hexdigest()


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


def extract_original_table(rom: bytes, maps) -> tuple[list[str], int, bytes]:
    bank = rom[BANK * BANK_SIZE : (BANK + 1) * BANK_SIZE]
    cursor = TABLE_OFFSET
    names: list[str] = []
    for _ in range(MOVE_COUNT):
        end = bank.find(bytes([TERMINATOR]), cursor)
        if end < 0:
            raise ValueError("Missing move-name terminator")
        decoded, unknown = decode_text(bank[cursor:end], maps)
        if unknown:
            raise ValueError(f"Undefined move-name code: {unknown}")
        names.append(decoded)
        cursor = end + 1
    return names, cursor, bank[TABLE_OFFSET:cursor]


def verify_routines(label: str, rom: bytes) -> dict:
    checks = [
        ("NamesPointers", NAMES_POINTERS_OFFSET, NAMES_POINTERS),
        ("GetName", GET_NAME_OFFSET, GET_NAME),
        ("GetNthString", GET_NTH_STRING_OFFSET, GET_NTH_STRING),
        ("GetMoveName", GET_MOVE_NAME_OFFSET, GET_MOVE_NAME),
    ]
    rows = []
    for name, offset, expected in checks:
        actual = rom[offset : offset + len(expected)]
        if actual != expected:
            raise AssertionError(f"{label}: {name} routine mismatch")
        rows.append(
            {
                "version": label,
                "symbol": name,
                "bank_hex": "0x00",
                "cpu_address_hex": f"0x{offset:04X}",
                "file_offset_hex": f"0x{offset:06X}",
                "length_bytes": len(expected),
                "sha256": sha(expected),
                "verified": True,
            }
        )
    return {"rows": rows, "raw": {name: expected.hex(" ") for name, _, expected in checks}}


def audit_version(label: str, rom: bytes, phase7: list[dict]) -> tuple[dict, list[dict], bytes]:
    maps = build_maps(rom)
    original_names, original_end, original_table = extract_original_table(rom, maps)
    expected_original = [r["original_gs_korean"] for r in phase7]
    if original_names != expected_original:
        raise AssertionError(f"{label}: Phase 7 original-name mismatch")

    rebuilt = bytearray()
    ui_rows: list[dict] = []
    for row in phase7:
        move_id = int(row["move_id"])
        original = row["original_gs_korean"]
        latest = row["latest_korean"]
        encoded = encode_text(latest, maps)
        rebuilt.extend(encoded)
        rebuilt.append(TERMINATOR)
        ui_rows.append(
            {
                "version": label,
                "move_id": move_id,
                "original_name": original,
                "latest_name": latest,
                "original_display_tiles": len(original),
                "latest_display_tiles": len(latest),
                "display_tile_delta": len(latest) - len(original),
                "latest_encoded_bytes": len(encoded),
                "name_buffer_copy_capacity_bytes": 21,
                "buffer_safe_with_terminator": len(encoded) + 1 <= 21,
                "exceeds_shipped_global_max_display_tiles": len(latest) > max(map(len, original_names)),
                "ui_risk_status": "NO_WORSE_THAN_SHIPPED_GLOBAL_MAX" if len(latest) <= max(map(len, original_names)) else "SCREEN_AUDIT_REQUIRED",
            }
        )

    bank_start = BANK * BANK_SIZE
    original_bank = rom[bank_start : bank_start + BANK_SIZE]
    new_end = TABLE_OFFSET + len(rebuilt)
    if any(original_bank[original_end:]):
        raise AssertionError(f"{label}: expected zero-filled tail after move-name table")
    dry_bank = original_bank[:TABLE_OFFSET] + bytes(rebuilt) + bytes(BANK_SIZE - new_end)
    if len(dry_bank) != BANK_SIZE:
        raise AssertionError("Dry-run bank length changed")
    dry_rom = rom[:bank_start] + dry_bank + rom[bank_start + BANK_SIZE :]
    decoded_new, decoded_end, _ = extract_original_table(dry_rom, maps)
    if decoded_new != [r["latest_korean"] for r in phase7] or decoded_end != new_end:
        raise AssertionError(f"{label}: rebuilt move-name lookup mismatch")

    routine = verify_routines(label, rom)
    result = {
        "version": label,
        "source_rom_sha1": sha(rom, "sha1"),
        "bank_6c_original_sha256": sha(original_bank),
        "bank_6c_dry_run_sha256": sha(dry_bank),
        "original_table_cpu_start_hex": f"0x{TABLE_CPU:04X}",
        "original_table_cpu_end_exclusive_hex": f"0x{0x4000 + original_end:04X}",
        "dry_run_table_cpu_end_exclusive_hex": f"0x{0x4000 + new_end:04X}",
        "original_table_bytes": len(original_table),
        "dry_run_table_bytes": len(rebuilt),
        "byte_delta": len(rebuilt) - len(original_table),
        "original_zero_tail_bytes": BANK_SIZE - original_end,
        "dry_run_zero_tail_bytes": BANK_SIZE - new_end,
        "names_pointer_entry": {"bank_hex": "0x6C", "cpu_address_hex": "0x564A"},
        "lookup_model": "TERMINATOR_SCANNED_NTH_STRING_NO_PER_MOVE_POINTERS",
        "name_buffer_copy_capacity_bytes": 21,
        "max_original_display_tiles": max(map(len, original_names)),
        "max_latest_display_tiles": max(len(r["latest_korean"]) for r in phase7),
        "max_latest_encoded_bytes_with_terminator": max(int(r["latest_encoded_length_bytes"]) + 1 for r in phase7),
        "all_names_buffer_safe": all(r["buffer_safe_with_terminator"] for r in ui_rows),
        "all_names_no_worse_than_shipped_global_display_max": not any(r["exceeds_shipped_global_max_display_tiles"] for r in ui_rows),
        "dry_run_full_rom_sha1": sha(dry_rom, "sha1"),
        "rom_output_written": False,
        "routine_checks": routine["rows"],
    }
    return result, ui_rows, dry_bank


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("gold_rom", type=Path)
    ap.add_argument("silver_rom", type=Path)
    ap.add_argument("phase7_comparison", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    phase7 = read_csv(args.phase7_comparison)
    if len(phase7) != MOVE_COUNT:
        raise ValueError("Phase 7 comparison must contain 251 rows")
    gold_result, gold_ui, gold_dry = audit_version("KOREAN_GOLD", args.gold_rom.read_bytes(), phase7)
    silver_result, silver_ui, silver_dry = audit_version("KOREAN_SILVER", args.silver_rom.read_bytes(), phase7)
    if gold_dry != silver_dry:
        raise AssertionError("Gold/Silver dry-run Bank 6C results differ")
    if [{k: v for k, v in r.items() if k != "version"} for r in gold_ui] != [
        {k: v for k, v in r.items() if k != "version"} for r in silver_ui
    ]:
        raise AssertionError("Gold/Silver UI audits differ")

    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "move_name_ui_length_audit.csv", gold_ui)
    write_json(args.output / "move_name_ui_length_audit.json", gold_ui)
    routine_rows = gold_result.pop("routine_checks") + silver_result.pop("routine_checks")
    write_csv(args.output / "move_name_lookup_routine_evidence.csv", routine_rows)
    write_json(args.output / "move_name_lookup_routine_evidence.json", routine_rows)
    patch_plan = {
        "operation": "DEFERRED_INTEGRATED_INSERTION",
        "write_binary_now": False,
        "target_bank_hex": "0x6C",
        "target_cpu_start_hex": "0x564A",
        "method": "re-encode 251 names in ID order, append 0x50 to each, replace table, zero-fill remaining bank tail",
        "pointer_edits_required": False,
        "reason": "NamesPointers retains Bank 0x6C / CPU 0x564A and GetNthString scans terminators dynamically.",
        "integration_prerequisites": [
            "finish official terminology masters",
            "finish text/UI/pointer audits",
            "apply all approved edits to separate Gold/Silver working copies",
            "recompute cartridge header/global checksums",
            "run emulator and event regression suite",
        ],
    }
    write_json(args.output / "move_name_deferred_patch_plan.json", patch_plan)
    gold_routines = [{k: v for k, v in row.items() if k != "version"} for row in routine_rows[:4]]
    silver_routines = [{k: v for k, v in row.items() if k != "version"} for row in routine_rows[4:]]
    summary = {
        "gold": gold_result,
        "silver": silver_result,
        "gold_silver_dry_run_bank_identical": gold_dry == silver_dry,
        "lookup_routines_identical_and_verified": gold_routines == silver_routines
        and all(r["verified"] for r in routine_rows),
        "ui_rows": len(gold_ui),
        "names_with_positive_display_tile_delta": sum(r["display_tile_delta"] > 0 for r in gold_ui),
        "names_exceeding_shipped_global_max": sum(r["exceeds_shipped_global_max_display_tiles"] for r in gold_ui),
        "dry_run_only": True,
        "rom_output_written": False,
    }
    write_json(args.output / "phase8_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
