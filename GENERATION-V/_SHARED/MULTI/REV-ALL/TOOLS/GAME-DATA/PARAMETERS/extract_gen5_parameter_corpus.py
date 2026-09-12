#!/usr/bin/env python3
"""Extract Generation V game-parameter corpora from BW/B2W2 NDS ROMs.

The extractor intentionally preserves raw records in addition to decoded fields.
Unknown/partially-known bytes are never discarded or assigned invented semantics.

Outputs JSON files for:
- personal data
- move data
- level-up learnsets
- evolutions
- item data (partially decoded + raw)
- breeding child/base table
- egg moves (version-family path aware)

This file is an analysis/extraction tool. It does not redistribute ROM data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


def u16(data: bytes, off: int) -> int:
    return struct.unpack_from("<H", data, off)[0]


def s8(v: int) -> int:
    return v - 0x100 if v & 0x80 else v


def u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


@dataclass
class NdsFile:
    path: str
    file_id: int
    start: int
    end: int


class NdsRom:
    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        self.fnt_off = u32(self.data, 0x40)
        self.fnt_size = u32(self.data, 0x44)
        self.fat_off = u32(self.data, 0x48)
        self.fat_size = u32(self.data, 0x4C)
        self.fnt = self.data[self.fnt_off : self.fnt_off + self.fnt_size]
        self.files: Dict[str, int] = {}
        self._walk_dir(0xF000, "")

    def _walk_dir(self, dir_id: int, prefix: str) -> None:
        idx = dir_id - 0xF000
        subtable_off = u32(self.fnt, idx * 8)
        file_id = u16(self.fnt, idx * 8 + 4)
        pos = subtable_off
        while True:
            n = self.fnt[pos]
            pos += 1
            if n == 0:
                break
            is_dir = bool(n & 0x80)
            name_len = n & 0x7F
            name = self.fnt[pos : pos + name_len].decode("ascii")
            pos += name_len
            if is_dir:
                child = u16(self.fnt, pos)
                pos += 2
                self._walk_dir(child, prefix + name + "/")
            else:
                self.files[prefix + name] = file_id
                file_id += 1

    def file_range(self, path: str) -> NdsFile:
        file_id = self.files[path]
        start = u32(self.data, self.fat_off + file_id * 8)
        end = u32(self.data, self.fat_off + file_id * 8 + 4)
        return NdsFile(path, file_id, start, end)

    def read_file(self, path: str) -> bytes:
        f = self.file_range(path)
        return self.data[f.start : f.end]


class Narc:
    def __init__(self, data: bytes):
        if data[:4] != b"NARC":
            raise ValueError("Not a NARC")
        self.data = data
        self.chunks: Dict[bytes, int] = {}
        pos = 0x10
        while pos + 8 <= len(data):
            magic = data[pos : pos + 4]
            size = u32(data, pos + 4)
            if size < 8 or pos + size > len(data):
                raise ValueError("Malformed NARC chunk")
            self.chunks[magic] = pos
            pos += size
        self.btaf = self.chunks[b"BTAF"]
        self.gmif = self.chunks[b"GMIF"]
        self.count = u16(data, self.btaf + 8)
        self.gmif_data = self.gmif + 8

    def member(self, i: int) -> bytes:
        rs = u32(self.data, self.btaf + 0x0C + i * 8)
        re = u32(self.data, self.btaf + 0x10 + i * 8)
        return self.data[self.gmif_data + rs : self.gmif_data + re]

    def members(self) -> List[bytes]:
        return [self.member(i) for i in range(self.count)]


def raw_hex(b: bytes) -> str:
    return b.hex()


def decode_personal(rec: bytes, index: int) -> dict:
    out = {"index": index, "size": len(rec), "raw": raw_hex(rec)}
    if len(rec) < 0x3C:
        out["status"] = "short_record"
        return out
    ev = u16(rec, 0x0A)
    out.update(
        {
            "base_stats": {
                "hp": rec[0], "attack": rec[1], "defense": rec[2],
                "speed": rec[3], "sp_attack": rec[4], "sp_defense": rec[5],
            },
            "types": [rec[6], rec[7]],
            "catch_rate": rec[8],
            "stage_aux": rec[9],
            "ev_yield": {
                "hp": (ev >> 0) & 3,
                "attack": (ev >> 2) & 3,
                "defense": (ev >> 4) & 3,
                "speed": (ev >> 6) & 3,
                "sp_attack": (ev >> 8) & 3,
                "sp_defense": (ev >> 10) & 3,
            },
            "held_items": [u16(rec, 0x0C), u16(rec, 0x0E), u16(rec, 0x10)],
            "gender_ratio": rec[0x12],
            "hatch_counter": rec[0x13],
            "base_friendship": rec[0x14],
            "growth_rate": rec[0x15],
            "egg_groups": [rec[0x16], rec[0x17]],
            "abilities": [rec[0x18], rec[0x19], rec[0x1A]],
            "escape_rate": rec[0x1B],
            "form_stats_start": u16(rec, 0x1C),
            "form_sprites_start": u16(rec, 0x1E),
            "form_count": rec[0x20],
            "body_color": rec[0x21],
            "base_exp": u16(rec, 0x22),
            "height": u16(rec, 0x24),
            "weight": u16(rec, 0x26),
            "tm_hm_bits": raw_hex(rec[0x28:0x38]),
            "trailing_compatibility_bits": raw_hex(rec[0x38:0x3C]),
        }
    )
    if len(rec) > 0x3C:
        out["version_extension_raw"] = raw_hex(rec[0x3C:])
    return out


def decode_move(rec: bytes, index: int) -> dict:
    out = {"index": index, "size": len(rec), "raw": raw_hex(rec)}
    if len(rec) < 0x24:
        out["status"] = "short_record"
        return out
    out.update(
        {
            "type": rec[0x00],
            "effect_category": rec[0x01],
            "damage_category": rec[0x02],
            "power": rec[0x03],
            "accuracy": rec[0x04],
            "pp": rec[0x05],
            "priority": s8(rec[0x06]),
            "hits_raw": rec[0x07],
            "result_effect": u16(rec, 0x08),
            "effect_chance": rec[0x0A],
            "status_aux": rec[0x0B],
            "min_turns": rec[0x0C],
            "max_turns": rec[0x0D],
            "crit_stage": rec[0x0E],
            "flinch": rec[0x0F],
            "effect_id": u16(rec, 0x10),
            "recoil_or_target_hp": s8(rec[0x12]),
            "healing_or_user_hp": s8(rec[0x13]),
            "target": rec[0x14],
            "stats": list(rec[0x15:0x18]),
            "stat_magnitudes": [s8(x) for x in rec[0x18:0x1B]],
            "stat_chances": list(rec[0x1B:0x1E]),
            "flags_tail_raw": raw_hex(rec[0x1E:0x24]),
        }
    )
    return out


def decode_level_moves(rec: bytes, index: int) -> dict:
    entries = []
    pos = 0
    while pos + 4 <= len(rec):
        block = rec[pos : pos + 4]
        if block == b"\xFF\xFF\xFF\xFF":
            break
        entries.append(
            {
                "move": u16(block, 0),
                "level": block[2],
                "aux": block[3],
                "raw": raw_hex(block),
            }
        )
        pos += 4
    return {"index": index, "size": len(rec), "entries": entries, "raw": raw_hex(rec)}


def decode_evolution(rec: bytes, index: int) -> dict:
    entries = []
    for pos in range(0, min(len(rec), 42), 6):
        if pos + 6 > len(rec):
            break
        method, param, target = u16(rec, pos), u16(rec, pos + 2), u16(rec, pos + 4)
        entries.append({"method": method, "parameter": param, "target": target})
    return {"index": index, "size": len(rec), "entries": entries, "raw": raw_hex(rec)}


def decode_item(rec: bytes, index: int, family: str) -> dict:
    # Historical BW/B2W2 documentation leaves several bytes unresolved.
    # Decode only fields with established ordering and retain the full raw record.
    out = {"index": index, "size": len(rec), "raw": raw_hex(rec)}
    if len(rec) < 8:
        out["status"] = "short_record"
        return out
    out.update(
        {
            "stored_price": u16(rec, 0),
            "shop_buy_price_bw": u16(rec, 0) * 10 if family == "BW" else None,
            "battle_use_or_effect": rec[2],
            "gain_or_effect_param": rec[3],
            "berry_aux": rec[4],
            "fling_effect": rec[5],
            "fling_power": rec[6],
            "natural_gift_power_or_aux": rec[7],
        }
    )
    if len(rec) >= 12:
        out.update(
            {
                "access_flags": rec[8],
                "pocket": rec[9],
                "item_type": rec[10],
                "item_category": rec[11],
            }
        )
    # Preserve all remaining bytes. More semantic decoding is added only after verification.
    if len(rec) > 12:
        out["remaining_raw"] = raw_hex(rec[12:])
    return out


def decode_child(rec: bytes, index: int) -> dict:
    # Do not infer structure beyond recording common small integer payloads.
    return {"index": index, "size": len(rec), "raw": raw_hex(rec)}


def decode_egg_moves(rec: bytes, index: int) -> dict:
    out = {"index": index, "size": len(rec), "raw": raw_hex(rec), "moves": []}
    if len(rec) < 2:
        return out
    count = u16(rec, 0)
    out["declared_count"] = count
    max_count = (len(rec) - 2) // 2
    safe_count = min(count, max_count)
    out["moves"] = [u16(rec, 2 + i * 2) for i in range(safe_count)]
    if count > max_count:
        out["status"] = "declared_count_exceeds_member_size"
    return out


def family_paths(family: str) -> dict:
    if family == "BW":
        return {
            "personal": "a/0/1/6",
            "level_moves": "a/0/1/8",
            "evolutions": "a/0/1/9",
            "child": "a/0/2/0",
            "moves": "a/0/2/1",
            "items": "a/0/2/4",
            "egg_moves": "a/1/2/3",
            "encounters": "a/1/2/6",
        }
    if family == "B2W2":
        return {
            "personal": "a/0/1/6",
            "level_moves": "a/0/1/8",
            "evolutions": "a/0/1/9",
            "child": "a/0/2/0",
            "moves": "a/0/2/1",
            "items": "a/0/2/4",
            "egg_moves": "a/1/2/4",
            "encounters": "a/1/2/7",
        }
    raise ValueError(f"Unsupported family: {family}")


def dump_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--family", choices=["BW", "B2W2"], required=True)
    ap.add_argument("--version", required=True, help="e.g. Black-EUR or White2-JPN")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rom = NdsRom(args.rom)
    paths = family_paths(args.family)

    metadata = {
        "rom_filename": args.rom.name,
        "sha1": hashlib.sha1(rom.data).hexdigest(),
        "family": args.family,
        "version": args.version,
        "paths": paths,
    }
    dump_json(args.out / "metadata.json", metadata)

    jobs = [
        ("personal", decode_personal),
        ("moves", decode_move),
        ("level_moves", decode_level_moves),
        ("evolutions", decode_evolution),
        ("items", lambda r, i: decode_item(r, i, args.family)),
        ("child", decode_child),
        ("egg_moves", decode_egg_moves),
    ]

    for name, decoder in jobs:
        narc_data = rom.read_file(paths[name])
        narc = Narc(narc_data)
        records = [decoder(rec, i) for i, rec in enumerate(narc.members())]
        dump_json(
            args.out / f"{name}.json",
            {
                "source_path": paths[name],
                "member_count": narc.count,
                "records": records,
            },
        )

    print(f"Extracted Generation V parameter corpus to: {args.out}")


if __name__ == "__main__":
    main()
