#!/usr/bin/env python3
"""Audit and modernize all 67 GS Korean trainer-class name records.

The Korean Gold and Silver ROMs are read-only technical sources.  This script
verifies their shared table bytes and emits review/insertion data only; it never
writes a ROM.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from gs_korean_codec import build_maps, encode_text


BANK = 0x6C
BANK_SIZE = 0x4000
CPU_START = 0x49A1
CPU_END_EXCLUSIVE = 0x4C4A
FILE_START = BANK * BANK_SIZE + (CPU_START - 0x4000)
FILE_END_EXCLUSIVE = BANK * BANK_SIZE + (CPU_END_EXCLUSIVE - 0x4000)
TERMINATOR = 0x50

POKEGOLD_CONSTANTS_URL = (
    "https://github.com/pret/pokegold/blob/"
    "656583c939d30f920a316177311a502dd222b57c/"
    "constants/trainer_constants.asm"
)
POKECRYSTAL_CONSTANTS_URL = (
    "https://github.com/pret/pokecrystal/blob/"
    "7a7881d0d62e0ddbd82dcf10e7116807487ac651/"
    "constants/trainer_constants.asm"
)
OFFICIAL_CORPUS_URL = (
    "https://github.com/torresflo/Pokemon-Obsidian/blob/"
    "9b08cdd4d6b62fa80763a58a690c476aed2c1ea8/"
    "Obsidian/Data/Text/Dialogs/100029.csv"
)
PKHEX_CONTEXT_URL = (
    "https://github.com/kwsch/PKHeX/blob/"
    "77dcd3a7895bceaafbbff12d25bdf77c1acd8ca5/"
    "PKHeX.Core/Resources/text/script/gen2/const_gs_ko.txt"
)
LGPE_CORPUS_URL = (
    "https://github.com/tanripj/pokemon_text_dumps/blob/"
    "d67e1c3cbcf56571b84b1951a4d2dfc6619dc468/"
    "lgpe/storytext/lgpe_storytext_korean.txt"
)
HGSS_CLASS_REFERENCE_URL = (
    "https://github.com/forkwikiman/enha_monimarkup/blob/"
    "4f42347f38d7bc190acc1517637bc4d57b172ed3/"
    "%ED%8F%AC%EC%BC%93%EB%AA%AC%EC%8A%A4%ED%84%B0/"
    "%EB%93%B1%EC%9E%A5%EC%9D%B8%EB%AC%BC/"
    "%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%84%88.wiki"
)


CLASS_IDS = [
    "FALKNER", "WHITNEY", "BUGSY", "MORTY", "PRYCE", "JASMINE", "CHUCK", "CLAIR",
    "RIVAL1", "POKEMON_PROF", "WILL", "CAL", "BRUNO", "KAREN", "KOGA", "CHAMPION",
    "BROCK", "MISTY", "LT_SURGE", "SCIENTIST", "ERIKA", "YOUNGSTER", "SCHOOLBOY",
    "BIRD_KEEPER", "LASS", "JANINE", "COOLTRAINERM", "COOLTRAINERF", "BEAUTY",
    "POKEMANIAC", "GRUNTM", "GENTLEMAN", "SKIER", "TEACHER", "SABRINA",
    "BUG_CATCHER", "FISHER", "SWIMMERM", "SWIMMERF", "SAILOR", "SUPER_NERD",
    "RIVAL2", "GUITARIST", "HIKER", "BIKER", "BLAINE", "BURGLAR", "FIREBREATHER",
    "JUGGLER", "BLACKBELT_T", "EXECUTIVEM", "PSYCHIC_T", "PICNICKER", "CAMPER",
    "EXECUTIVEF", "SAGE", "MEDIUM", "BOARDER", "POKEFANM", "KIMONO_GIRL", "TWINS",
    "POKEFANF", "RED", "BLUE", "OFFICER", "GRUNTF", "MYSTICALMAN_COMPAT_SLOT",
]


# Project decisions.  Unlisted rows retain the official GS Korean string.
# Each changed row records whether the basis is a later localization corpus,
# later official terminology seen through a secondary source, or an editorial
# modernization made transparently by this project.
OVERRIDES = {
    10: ("포켓몬 박사", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_AND_CURRENT_NAME"),
    20: ("연구원", "CURRENT_LOCALIZATION_CORPUS", "CURRENT_OFFICIAL_CLASS_NAME"),
    23: ("학원 끝난 아이", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    25: ("짧은 치마", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    27: ("엘리트 트레이너", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    28: ("엘리트 트레이너", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    31: ("로켓단 조무래기", "CURRENT_OFFICIAL_TERMINOLOGY_SECONDARY_REFERENCE", "ROLE_RESTORATION"),
    33: ("스키어", "LATER_OFFICIAL_NAME_SECONDARY_REFERENCE", "LATER_OFFICIAL_CLASS_NAME"),
    36: ("곤충채집소년", "CURRENT_LOCALIZATION_CORPUS", "CURRENT_OFFICIAL_CLASS_NAME"),
    38: ("수영팬티소년", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    49: ("저글러", "PROJECT_EDITORIAL_MODERNIZATION", "OUTDATED_EXONYM_REMOVAL"),
    51: ("로켓단 간부", "CURRENT_OFFICIAL_TERMINOLOGY_SECONDARY_REFERENCE", "ROLE_RESTORATION"),
    53: ("피크닉걸", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    55: ("로켓단 간부", "CURRENT_OFFICIAL_TERMINOLOGY_SECONDARY_REFERENCE", "ROLE_RESTORATION"),
    56: ("수행자", "LATER_OFFICIAL_NAME_SECONDARY_REFERENCE", "LATER_OFFICIAL_CLASS_NAME"),
    59: ("애호가클럽", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    62: ("애호가클럽", "CURRENT_LOCALIZATION_CORPUS", "ORTHOGRAPHY_NORMALIZATION"),
    66: ("로켓단 조무래기", "CURRENT_OFFICIAL_TERMINOLOGY_SECONDARY_REFERENCE", "ROLE_RESTORATION"),
}

CORPUS_CONFIRMED = {
    "POKEMON_PROF", "SCIENTIST", "YOUNGSTER", "SCHOOLBOY", "BIRD_KEEPER", "LASS",
    "COOLTRAINERM", "COOLTRAINERF", "BEAUTY", "POKEMANIAC", "GENTLEMAN",
    "BUG_CATCHER", "FISHER", "SWIMMERM", "SWIMMERF", "SAILOR", "GUITARIST",
    "HIKER", "BLACKBELT_T", "PSYCHIC_T", "PICNICKER", "CAMPER", "POKEFANM",
    "TWINS", "POKEFANF", "CHAMPION",
}


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


def visible_tiles(text: str) -> int:
    # In GS Korean each displayed Korean syllable, Latin glyph, or space takes
    # one tile even though Korean syllables use two encoded bytes.
    return len(text)


def reconstructed_original(rows: list[dict[str, str]]) -> bytes:
    out = bytearray()
    for row in rows:
        out.extend(bytes.fromhex(row["raw_hex"]))
        out.append(TERMINATOR)
    return bytes(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("gold_rom", type=Path)
    ap.add_argument("silver_rom", type=Path)
    ap.add_argument("phase2_names", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--accessed", required=True)
    ap.add_argument("--pokegold-commit", required=True)
    args = ap.parse_args()

    source = [r for r in read_csv(args.phase2_names) if r["category"] == "TRAINER_CLASS_NAMES"]
    if len(source) != 67 or len(CLASS_IDS) != 67:
        raise ValueError("Expected exactly 67 trainer-class records and IDs")

    gold = args.gold_rom.read_bytes()
    silver = args.silver_rom.read_bytes()
    gold_region = gold[FILE_START:FILE_END_EXCLUSIVE]
    silver_region = silver[FILE_START:FILE_END_EXCLUSIVE]
    rebuilt_original = reconstructed_original(source)
    if gold_region != silver_region:
        raise AssertionError("Korean Gold/Silver trainer-class regions differ")
    if gold_region != rebuilt_original:
        raise AssertionError("Phase 2 rows do not exactly reconstruct the ROM region")

    maps = build_maps(gold)
    rows: list[dict] = []
    for index, (src, class_id) in enumerate(zip(source, CLASS_IDS), start=1):
        original = src["decoded_text"]
        if index in OVERRIDES:
            final, status, change = OVERRIDES[index]
        else:
            final = original
            change = "UNCHANGED"
            if class_id in CORPUS_CONFIRMED or original in {
                "체육관 관장", "사천왕", "포켓몬 트레이너"
            }:
                status = "CURRENT_LOCALIZATION_CORPUS"
            elif class_id == "BURGLAR":
                status = "LATER_OFFICIAL_SCRIPT_CORPUS"
            elif class_id == "MYSTICALMAN_COMPAT_SLOT":
                status = "UNUSED_SLOT_LEGACY_OFFICIAL_RETAINED"
            else:
                status = "LEGACY_OFFICIAL_RETAINED_NO_NEWER_GAME_TEXT"

        encoded = encode_text(final, maps)
        original_len = int(src["raw_length"])
        rows.append({
            "class_id_decimal": index,
            "class_id_hex": f"0x{index:02X}",
            "internal_class_id": class_id,
            "original_gs_korean": original,
            "final_korean": final,
            "name_changed": original != final,
            "change_category": change,
            "verification_status": status,
            "direct_first_party_source_verified": False,
            "original_encoded_length_bytes": original_len,
            "final_encoded_length_bytes": len(encoded),
            "record_byte_delta_with_terminator": len(encoded) - original_len,
            "original_display_tiles": visible_tiles(original),
            "final_display_tiles": visible_tiles(final),
            "final_encoded_hex": encoded.hex(" "),
            "bank_hex": src["bank_hex"],
            "cpu_address_hex": src["cpu_address_hex"],
            "file_offset_hex": src["file_offset_hex"],
            "original_raw_hex": src["raw_hex"],
            "usage_note": (
                "TRAILING_COMPATIBILITY_STRING_NOT_A_GS_CLASS_ID"
                if class_id == "MYSTICALMAN_COMPAT_SLOT" else "ACTIVE_CLASS_SLOT"
            ),
        })

    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "trainer_class_current_comparison.csv", rows)
    write_json(args.output / "trainer_class_current_comparison.json", rows)
    changed = [r for r in rows if r["name_changed"]]
    write_csv(args.output / "trainer_class_change_list.csv", changed)

    old_size = len(gold_region)
    new_size = sum(r["final_encoded_length_bytes"] + 1 for r in rows)
    max_old_tiles = max(r["original_display_tiles"] for r in rows)
    max_new_tiles = max(r["final_display_tiles"] for r in rows)
    ui_rows = [{
        "class_id_decimal": r["class_id_decimal"],
        "internal_class_id": r["internal_class_id"],
        "final_korean": r["final_korean"],
        "display_tiles": r["final_display_tiles"],
        "encoded_bytes": r["final_encoded_length_bytes"],
        "within_observed_original_tile_max": r["final_display_tiles"] <= max_old_tiles,
        "within_observed_original_byte_max": r["final_encoded_length_bytes"] <= max(
            x["original_encoded_length_bytes"] for x in rows
        ),
    } for r in rows]
    write_csv(args.output / "trainer_class_ui_length_audit.csv", ui_rows)
    write_json(args.output / "trainer_class_ui_length_audit.json", ui_rows)

    evidence = {
        "source_accessed_date": args.accessed,
        "warning": (
            "Contemporary name evidence is preserved from secondary extraction/mirror sources. "
            "No row is falsely marked as direct first-party verification."
        ),
        "sources": [
            {
                "role": "GEN2_INTERNAL_CLASS_ID_ORDER",
                "url": POKEGOLD_CONSTANTS_URL,
                "commit": args.pokegold_commit,
                "authority_note": "Disassembly semantics only; Korean ROM bytes remain primary.",
            },
            {
                "role": "CRYSTAL_MYSTICALMAN_CLASS_ID_CONTEXT",
                "url": POKECRYSTAL_CONSTANTS_URL,
                "commit": "7a7881d0d62e0ddbd82dcf10e7116807487ac651",
                "authority_note": (
                    "Gold/Silver define only IDs 1-66; Crystal adds MYSTICALMAN as ID 67. "
                    "The Korean GS bank nevertheless contains the corresponding trailing string."
                ),
            },
            {
                "role": "CURRENT_MULTILINGUAL_LOCALIZATION_CORPUS",
                "url": OFFICIAL_CORPUS_URL,
                "commit": "9b08cdd4d6b62fa80763a58a690c476aed2c1ea8",
                "matched_examples": [
                    "포켓몬 박사", "연구원", "학원 끝난 아이", "짧은 치마",
                    "엘리트 트레이너", "곤충채집소년", "수영팬티소년",
                    "피크닉걸", "애호가클럽",
                ],
            },
            {
                "role": "GEN2_ROCKET_ROLE_CONTEXT",
                "url": PKHEX_CONTEXT_URL,
                "commit": "77dcd3a7895bceaafbbff12d25bdf77c1acd8ca5",
                "matched_examples": ["로켓단 조무래기", "로켓단 간부"],
            },
            {
                "role": "LATER_OFFICIAL_SCRIPT_CORPUS",
                "url": LGPE_CORPUS_URL,
                "commit": "d67e1c3cbcf56571b84b1951a4d2dfc6619dc468",
                "matched_examples": ["불난집 전문털이범"],
            },
            {
                "role": "HGSS_CLASS_NAME_SECONDARY_REFERENCE",
                "url": HGSS_CLASS_REFERENCE_URL,
                "commit": "4f42347f38d7bc190acc1517637bc4d57b172ed3",
                "matched_examples": ["스키어", "수행자"],
            },
        ],
        "project_editorial_decisions": [
            {
                "class_id": 49,
                "internal_class_id": "JUGGLER",
                "original": "집시저글러",
                "final": "저글러",
                "reason": "Remove an outdated ethnic exonym while preserving the Juggler class function.",
            }
        ],
    }
    write_json(args.output / "trainer_class_source_evidence.json", evidence)

    structure = {
        "bank_hex": "0x6C",
        "cpu_start": f"0x{CPU_START:04X}",
        "cpu_end_exclusive": f"0x{CPU_END_EXCLUSIVE:04X}",
        "file_start": f"0x{FILE_START:06X}",
        "file_end_exclusive": f"0x{FILE_END_EXCLUSIVE:06X}",
        "record_count": 67,
        "terminator_hex": f"0x{TERMINATOR:02X}",
        "original_region_bytes": old_size,
        "original_region_sha256": hashlib.sha256(gold_region).hexdigest(),
        "gold_silver_region_identical": True,
        "phase2_roundtrip_exact": True,
        "next_table_cpu_address": "0x4C4A",
        "next_table_preserved": True,
        "new_logical_table_bytes": new_size,
        "new_table_byte_delta": new_size - old_size,
        "fits_original_region_without_relocation": new_size <= old_size,
        "rom_written": False,
        "gold_rom_sha256": sha256(args.gold_rom),
        "silver_rom_sha256": sha256(args.silver_rom),
    }
    write_json(args.output / "trainer_class_structure_evidence.json", structure)

    summary = {
        "trainer_class_slots": 67,
        "gold_silver_class_ids": 66,
        "trailing_crystal_compatibility_strings": 1,
        "changed_total": len(changed),
        "unchanged_total": len(rows) - len(changed),
        "orthography_or_current_name_changes": sum(
            r["change_category"] in {
                "ORTHOGRAPHY_AND_CURRENT_NAME", "ORTHOGRAPHY_NORMALIZATION",
                "CURRENT_OFFICIAL_CLASS_NAME", "LATER_OFFICIAL_CLASS_NAME"
            } for r in rows
        ),
        "role_restorations": sum(r["change_category"] == "ROLE_RESTORATION" for r in rows),
        "editorial_modernizations": sum(
            r["change_category"] == "OUTDATED_EXONYM_REMOVAL" for r in rows
        ),
        "all_final_names_encodable": True,
        "max_original_display_tiles": max_old_tiles,
        "max_final_display_tiles": max_new_tiles,
        "all_within_observed_original_tile_max": all(
            r["within_observed_original_tile_max"] for r in ui_rows
        ),
        "original_table_bytes": old_size,
        "final_logical_table_bytes": new_size,
        "table_byte_delta": new_size - old_size,
        "fits_original_region_without_relocation": new_size <= old_size,
        "gold_silver_original_table_identical": True,
        "direct_first_party_source_verified_rows": 0,
        "rom_output_written": False,
        "next_phase": "Build relocated/fixed-region candidate and verify lookup/UI behavior.",
    }
    write_json(args.output / "phase11_summary.json", summary)

    changed_lines = "\n".join(
        f"| {r['class_id_decimal']} | `{r['internal_class_id']}` | {r['original_gs_korean']} | "
        f"{r['final_korean']} | {r['change_category']} |"
        for r in changed
    )
    report = f"""# GS Korean 구현 분석 11단계 — 트레이너 분류 67개 현대화

## 결론

- 한국판 표는 금·은 클래스 ID 1–66과 Crystal의 67번 `MYSTICALMAN`용 후행 문자열 1개로 구성된다.
- 한국판 금·은의 원본 표 영역은 완전히 동일하며 Phase 2 추출 데이터로 바이트 단위 재구성된다.
- 67개 중 {len(changed)}개를 수정 후보로 확정하고 {len(rows) - len(changed)}개는 유지한다.
- 모든 최종 문자열은 기존 GS Korean 문자표로 인코딩된다.
- 최장 표시 폭은 원본 {max_old_tiles}타일, 수정안 {max_new_tiles}타일이다.
- 논리 테이블은 {old_size}바이트에서 {new_size}바이트로 {new_size - old_size:+d}바이트 변한다.
- ROM은 쓰지 않았다. 다음 단계에서 배치·참조 방식을 검증한 뒤 후보 데이터를 만든다.

## 변경 목록

| ID | 내부 클래스 | 기존 한국어 | 최종 후보 | 분류 |
|---:|---|---|---|---|
{changed_lines}

## 중요한 판정

- `GRUNTM/GRUNTF`와 `EXECUTIVEM/EXECUTIVEF`는 기존 한국판에서 모두 ‘로켓단’으로 합쳐졌으나,
  내부 역할을 보존해 각각 ‘로켓단 조무래기’와 ‘로켓단 간부’로 분리한다.
- `MYSTICALMAN`용 ‘수수께끼의 청년’은 금·은의 유효 클래스 ID가 아니라 후행 호환 문자열이다.
  Crystal 이식 자료로 가치가 있으므로 삭제하지 않고 보존한다.
- `JUGGLER`의 ‘저글러’는 최신 공식 명칭이라고 단정하지 않는 프로젝트 편집 판정이다.
- 현대 명칭 자료는 추출·미러 자료이므로 모든 행의 직접 1차 공식 검증 표시는 `false`로 유지한다.

## 구조 경계

- 뱅크: `0x6C`
- 시작: CPU `0x49A1` / 파일 `0x{FILE_START:06X}`
- 다음 표: CPU `0x4C4A` / 파일 `0x{FILE_END_EXCLUSIVE:06X}`
- 종료 바이트: `0x50`
- 한국판 금·은 원본 표 일치: 예
- ROM 출력: 없음
"""
    (args.output / "GS_KOREAN_IMPLEMENTATION_PHASE11_KO.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
