#!/usr/bin/env python3
"""Pack the normalized Generation-III ledgers into a compact ROM-staging block.

The block is deliberately independent of Silver's one-byte species IDs. Canonical
species IDs are National Dex u16 values. Symbolic Gen-III constants (moves,
abilities, item names, etc.) are losslessly represented by deterministic local
registries embedded in the block; engine routing can later map those registries
to the cumulative runtime enums without changing canonical species identity.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import struct
import zlib
from collections import defaultdict
from pathlib import Path

MAGIC = b"S3PARM1\0"
VERSION = 1
HEADER_SIZE = 64
RECORD_SIZE = 48
CANON_MIN = 252
CANON_MAX = 386
SPECIES_COUNT = 135


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def u8(v: int) -> bytes:
    assert 0 <= v <= 0xFF, v
    return bytes((v,))


def u16(v: int) -> bytes:
    assert 0 <= v <= 0xFFFF, v
    return struct.pack("<H", v)


def registry(values) -> tuple[list[str], dict[str, int]]:
    vals = sorted({str(v) for v in values if str(v)})
    return vals, {v: i for i, v in enumerate(vals)}


def bool_value(v: str) -> int:
    return 1 if v.strip() in {"TRUE", "1", "true", "True"} else 0


def gender_value(v: str) -> int:
    v = v.strip()
    if v == "MON_MALE":
        return 0x00
    if v == "MON_FEMALE":
        return 0xFE
    if v == "MON_GENDERLESS":
        return 0xFF
    m = re.fullmatch(r"PERCENT_FEMALE\((\d+(?:\.\d+)?)\)", v)
    if not m:
        raise ValueError(f"Unsupported gender ratio: {v}")
    return min(254, int(float(m.group(1)) * 255 / 100))


def parse_int(v: str) -> int:
    return int(v.strip(), 0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode_dictionary(registries: list[tuple[str, list[str]]]) -> bytes:
    out = bytearray()
    out += u8(len(registries))
    for name, symbols in registries:
        nb = name.encode("ascii")
        out += u8(len(nb)) + nb + u16(len(symbols))
        for symbol in symbols:
            sb = symbol.encode("ascii")
            if len(sb) > 255:
                raise ValueError(symbol)
            out += u8(len(sb)) + sb
    return bytes(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("generated_dir", type=Path)
    ap.add_argument("output_bin", type=Path)
    ap.add_argument("output_layout", type=Path)
    args = ap.parse_args()
    gd = args.generated_dir

    species = rows(gd / "gen3_species_parameters.csv")
    evos = rows(gd / "gen3_evolutions.csv")
    level = rows(gd / "gen3_levelup_learnsets.csv")
    tmhm = rows(gd / "gen3_tmhm_learnsets.csv")
    tutor = rows(gd / "gen3_tutor_learnsets.csv")
    manifest = json.loads((gd / "gen3_manifest.json").read_text(encoding="utf-8"))

    assert len(species) == SPECIES_COUNT
    assert [int(r["national_id"]) for r in species] == list(range(CANON_MIN, CANON_MAX + 1))

    type_syms, type_id = registry([x for r in species for x in (r["type1"], r["type2"])])
    item_syms, item_id = registry([x for r in species for x in (r["item_common"], r["item_rare"])] + [r["parameter"] for r in evos if r["parameter"].startswith("ITEM_")])
    growth_syms, growth_id = registry(r["growth_rate"] for r in species)
    egg_syms, egg_id = registry([x for r in species for x in (r["egg_group1"], r["egg_group2"])])
    ability_syms, ability_id = registry([x for r in species for x in (r["ability1"], r["ability2"])])
    body_syms, body_id = registry(r["body_color"] for r in species)
    evo_method_syms, evo_method_id = registry(r["method"] for r in evos)
    move_syms, move_id = registry([r["move"] for r in level] + [r["machine_move"] for r in tmhm] + [r["tutor_move"] for r in tutor])

    for name, syms in (("types", type_syms), ("growth", growth_syms), ("egg", egg_syms), ("abilities", ability_syms), ("body", body_syms), ("evo methods", evo_method_syms)):
        if len(syms) > 256:
            raise ValueError(f"{name} registry exceeds u8: {len(syms)}")
    if len(move_syms) > 65536 or len(item_syms) > 65536:
        raise ValueError("u16 registry overflow")

    evo_by = defaultdict(list)
    lvl_by = defaultdict(list)
    tm_by = defaultdict(list)
    tut_by = defaultdict(list)
    for r in evos: evo_by[int(r["from_national_id"])].append(r)
    for r in level: lvl_by[int(r["national_id"])].append(r)
    for r in tmhm: tm_by[int(r["national_id"])].append(r)
    for r in tutor: tut_by[int(r["national_id"])].append(r)

    evo_flat: list[dict] = []
    lvl_flat: list[dict] = []
    tm_flat: list[dict] = []
    tut_flat: list[dict] = []
    records = bytearray()

    for s in species:
        nid = int(s["national_id"])
        e_index, l_index, tm_index, tu_index = len(evo_flat), len(lvl_flat), len(tm_flat), len(tut_flat)
        e_list, l_list, tm_list, tu_list = evo_by[nid], lvl_by[nid], tm_by[nid], tut_by[nid]
        evo_flat.extend(e_list); lvl_flat.extend(l_list); tm_flat.extend(tm_list); tut_flat.extend(tu_list)

        rec = bytearray()
        rec += u16(nid)
        rec += u16(int(s["pokeemerald_raw_species_id"]))
        rec += bytes(int(s[k]) for k in ("hp","attack","defense","speed","sp_attack","sp_defense"))
        rec += u8(type_id[s["type1"]]) + u8(type_id[s["type2"]])
        rec += u8(int(s["catch_rate"])) + u8(int(s["exp_yield"]))
        rec += bytes(int(s[k]) for k in ("ev_hp","ev_attack","ev_defense","ev_speed","ev_sp_attack","ev_sp_defense"))
        rec += u16(item_id[s["item_common"]]) + u16(item_id[s["item_rare"]])
        rec += u8(gender_value(s["gender_ratio"]))
        rec += u8(int(s["egg_cycles"])) + u8(int(s["friendship"]))
        rec += u8(growth_id[s["growth_rate"]])
        rec += u8(egg_id[s["egg_group1"]]) + u8(egg_id[s["egg_group2"]])
        rec += u8(ability_id[s["ability1"]]) + u8(ability_id[s["ability2"]])
        rec += u8(int(s["safari_flee_rate"])) + u8(body_id[s["body_color"]])
        rec += u8(bool_value(s["no_flip"]))
        rec += u8(len(e_list)) + u16(e_index)
        rec += u8(len(l_list)) + u16(l_index)
        rec += u8(len(tm_list)) + u16(tm_index)
        rec += u8(len(tu_list)) + u16(tu_index)
        rec += b"\0"
        assert len(rec) == RECORD_SIZE, (nid, len(rec))
        records += rec

    evo_data = bytearray()
    for r in evo_flat:
        param = r["parameter"].strip()
        if param.startswith("ITEM_"):
            param_kind, param_val = 1, item_id[param]
        else:
            param_kind, param_val = 0, parse_int(param)
        evo_data += u8(evo_method_id[r["method"]]) + u8(param_kind) + u16(param_val) + u16(int(r["to_national_id"]))

    level_data = bytearray()
    for r in lvl_flat:
        level_data += u8(int(r["level"])) + u16(move_id[r["move"]])

    tm_data = bytearray()
    for r in tm_flat:
        tm_data += u16(move_id[r["machine_move"]])

    tutor_data = bytearray()
    for r in tut_flat:
        tutor_data += u16(move_id[r["tutor_move"]])

    dict_data = encode_dictionary([
        ("type", type_syms),
        ("item", item_syms),
        ("growth", growth_syms),
        ("egg_group", egg_syms),
        ("ability", ability_syms),
        ("body_color", body_syms),
        ("evo_method", evo_method_syms),
        ("move", move_syms),
    ])

    records_off = HEADER_SIZE
    evo_off = records_off + len(records)
    level_off = evo_off + len(evo_data)
    tmhm_off = level_off + len(level_data)
    tutor_off = tmhm_off + len(tm_data)
    dict_off = tutor_off + len(tutor_data)
    end_off = dict_off + len(dict_data)

    payload = bytes(records + evo_data + level_data + tm_data + tutor_data + dict_data)
    payload_crc = zlib.crc32(payload) & 0xFFFFFFFF
    source_commit = bytes.fromhex(manifest["source_commit"][:16])

    header = bytearray()
    header += MAGIC
    header += struct.pack("<6H", VERSION, SPECIES_COUNT, CANON_MIN, CANON_MAX, RECORD_SIZE, 1)
    header += struct.pack("<7I", records_off, evo_off, level_off, tmhm_off, tutor_off, dict_off, end_off)
    header += source_commit
    header += struct.pack("<I", payload_crc)
    assert len(header) == 60
    header += struct.pack("<I", zlib.crc32(header) & 0xFFFFFFFF)
    assert len(header) == HEADER_SIZE

    block = bytes(header) + payload
    if len(block) > 0x8000:
        raise ValueError(f"Gen III block exceeds two 16-KiB banks: {len(block)}")

    args.output_bin.parent.mkdir(parents=True, exist_ok=True)
    args.output_bin.write_bytes(block)
    layout = {
        "magic": MAGIC.rstrip(b"\0").decode("ascii"),
        "version": VERSION,
        "canonical_range": [CANON_MIN, CANON_MAX],
        "species_count": SPECIES_COUNT,
        "record_size": RECORD_SIZE,
        "block_bytes": len(block),
        "block_sha256": sha256_bytes(block),
        "payload_crc32": f"{payload_crc:08x}",
        "source_repo": manifest["source_repo"],
        "source_commit": manifest["source_commit"],
        "sections": {
            "records": {"offset": records_off, "count": SPECIES_COUNT, "bytes": len(records)},
            "evolutions": {"offset": evo_off, "count": len(evo_flat), "entry_size": 6, "bytes": len(evo_data)},
            "level_up": {"offset": level_off, "count": len(lvl_flat), "entry_size": 3, "bytes": len(level_data)},
            "tm_hm": {"offset": tmhm_off, "count": len(tm_flat), "entry_size": 2, "bytes": len(tm_data)},
            "tutor": {"offset": tutor_off, "count": len(tut_flat), "entry_size": 2, "bytes": len(tutor_data)},
            "dictionary": {"offset": dict_off, "bytes": len(dict_data)},
            "end": end_off,
        },
        "registry_counts": {
            "type": len(type_syms), "item": len(item_syms), "growth": len(growth_syms),
            "egg_group": len(egg_syms), "ability": len(ability_syms), "body_color": len(body_syms),
            "evo_method": len(evo_method_syms), "move": len(move_syms),
        },
        "notes": [
            "Canonical species IDs are National Dex u16 values.",
            "Pokeemerald raw IDs are provenance only.",
            "Symbol registries are embedded so no Gen-III parameter names are discarded.",
            "The block is data-staging only until Silver runtime lookup/save/battle routines are routed to the cumulative engine.",
        ],
    }
    args.output_layout.write_text(json.dumps(layout, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(layout, indent=2))


if __name__ == "__main__":
    main()
