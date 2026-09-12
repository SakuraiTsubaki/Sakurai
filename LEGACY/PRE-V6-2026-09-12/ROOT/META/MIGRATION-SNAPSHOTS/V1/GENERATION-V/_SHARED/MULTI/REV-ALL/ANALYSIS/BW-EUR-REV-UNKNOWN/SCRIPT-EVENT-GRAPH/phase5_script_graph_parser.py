#!/usr/bin/env python3
"""Pokémon Black/White (BW1) Phase 5 field-script/event graph extractor.

Primary input: an original BW1 NDS ROM kept locally/read-only.
Command schema input: FrostsGen5Editor ScriptNARC.cs at pinned commit
334344270b82b47c40bdbcfbcad2aac2d003a8b5. The program extracts ONLY the
`bw1CommandList` block; it never substitutes the BW2 table.

This file was written while the project execution container was unavailable;
run/validation status must remain UNVERIFIED until executed against the uploaded
Black/White ROMs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import struct
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

FROST_COMMIT = "334344270b82b47c40bdbcfbcad2aac2d003a8b5"
FROST_RAW = (
    "https://raw.githubusercontent.com/FrostFalcon/FrostsGen5Editor/"
    + FROST_COMMIT + "/Data/NARCTypes/ScriptNARC.cs"
)


def u16(b: bytes, o: int) -> int:
    return struct.unpack_from("<H", b, o)[0]


def s16(b: bytes, o: int) -> int:
    return struct.unpack_from("<h", b, o)[0]


def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]


def s32(b: bytes, o: int) -> int:
    return struct.unpack_from("<i", b, o)[0]


def sha1(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()


def write_csv(path: Path, rows: Iterable[dict], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


class NDS:
    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        self.fnt_off = u32(self.data, 0x40)
        self.fnt_size = u32(self.data, 0x44)
        self.fat_off = u32(self.data, 0x48)
        self.fat_size = u32(self.data, 0x4C)
        self.files = self._parse_fnt()

    def _parse_fnt(self) -> Dict[str, int]:
        fnt = self.data[self.fnt_off:self.fnt_off + self.fnt_size]
        if len(fnt) < 8:
            raise ValueError("FNT too small")
        dir_count = u16(fnt, 6)
        dirs = []
        for i in range(dir_count):
            o = i * 8
            dirs.append((u32(fnt, o), u16(fnt, o + 4), u16(fnt, o + 6)))
        children: Dict[int, List[Tuple[str, bool, int]]] = {}
        for i, (suboff, first_file_id, _parent) in enumerate(dirs):
            did = 0xF000 + i
            pos = suboff
            file_id = first_file_id
            ent = []
            while pos < len(fnt):
                n = fnt[pos]
                pos += 1
                if n == 0:
                    break
                is_dir = bool(n & 0x80)
                ln = n & 0x7F
                name = fnt[pos:pos + ln].decode("ascii", "replace")
                pos += ln
                if is_dir:
                    child = u16(fnt, pos)
                    pos += 2
                    ent.append((name, True, child))
                else:
                    ent.append((name, False, file_id))
                    file_id += 1
            children[did] = ent

        out: Dict[str, int] = {}
        def walk(did: int, prefix: str) -> None:
            for name, is_dir, ident in children.get(did, []):
                p = f"{prefix}/{name}" if prefix else name
                if is_dir:
                    walk(ident, p)
                else:
                    out[p] = ident
        walk(0xF000, "")
        return out

    def get_file(self, path: str) -> bytes:
        key = path.lstrip("/")
        fid = self.files[key]
        o = self.fat_off + fid * 8
        start, end = u32(self.data, o), u32(self.data, o + 4)
        return self.data[start:end]


class NARC:
    def __init__(self, data: bytes):
        if data[:4] != b"NARC":
            raise ValueError("not NARC")
        fat = data.find(b"BTAF")
        img = data.find(b"GMIF")
        if fat < 0 or img < 0:
            raise ValueError("missing BTAF/GMIF")
        count = u16(data, fat + 8)
        image_base = img + 8
        self.members = []
        for i in range(count):
            s = u32(data, fat + 0x0C + i * 8)
            e = u32(data, fat + 0x10 + i * 8)
            self.members.append(data[image_base + s:image_base + e])


@dataclass(frozen=True)
class CommandDef:
    opcode: int
    name: str
    widths: Tuple[int, ...]


def load_bw1_command_defs(source: str) -> Dict[int, CommandDef]:
    m = re.search(
        r"bw1CommandList\s*=\s*new\s+Dictionary<int,\s*CommandType>\s*\(\)\s*\{(.*?)\n\s*\};",
        source, re.S,
    )
    if not m:
        raise ValueError("bw1CommandList block not found")
    body = m.group(1)
    rx = re.compile(
        r"\{\s*0x([0-9A-Fa-f]+)\s*,\s*new\s+CommandType\(\"([^\"]+)\"\s*,\s*(\d+)(.*?)\)\s*\}"
    )
    out: Dict[int, CommandDef] = {}
    for mm in rx.finditer(body):
        op = int(mm.group(1), 16)
        count = int(mm.group(3))
        tail = [int(x) for x in re.findall(r"\d+", mm.group(4))]
        widths = tuple(tail[:count])
        if len(widths) != count:
            raise ValueError(f"command 0x{op:X} {mm.group(2)} width mismatch")
        out[op] = CommandDef(op, mm.group(2), widths)
    if not out or 0x23 not in out or out[0x23].name != "FlagSet":
        raise ValueError("BW1 command sanity check failed")
    return out


def obtain_command_source(path: Optional[Path], allow_fetch: bool) -> str:
    if path:
        return path.read_text(encoding="utf-8-sig")
    if not allow_fetch:
        raise SystemExit("Provide --command-source or --fetch-command-source")
    with urllib.request.urlopen(FROST_RAW, timeout=30) as r:
        return r.read().decode("utf-8-sig")


def script_entry_points(data: bytes) -> Tuple[List[int], Optional[str]]:
    p = 0
    ptrs = []
    while p + 2 <= len(data):
        if u16(data, p) == 0xFD13:
            return ptrs, None
        if p + 4 > len(data):
            break
        rel = s32(data, p)
        target = p + 4 + rel
        if target < 0 or target >= len(data):
            return ptrs, f"bad pointer at 0x{p:X} -> 0x{target:X}"
        ptrs.append(target)
        p += 4
    return ptrs, "no 0xFD13 pointer terminator"


def read_param(data: bytes, pos: int, width: int) -> int:
    if width == 1:
        return data[pos]
    if width == 2:
        return u16(data, pos)
    if width == 4:
        return s32(data, pos)
    raise ValueError(width)


def decode_sequence(data: bytes, start: int, defs: Dict[int, CommandDef], hard_end: int) -> Tuple[List[dict], str]:
    rows = []
    pos = start
    max_target = start
    status = "ok"
    guard = 0
    while pos + 2 <= min(len(data), hard_end) and guard < 10000:
        guard += 1
        at = pos
        op = u16(data, pos)
        pos += 2
        d = defs.get(op)
        if d is None:
            status = f"unknown opcode 0x{op:04X} @0x{at:X}"
            rows.append({"offset": at, "opcode": op, "name": "UNKNOWN", "parameters": "", "size": 2})
            break
        params = []
        ok = True
        for width in d.widths:
            if pos + width > len(data):
                ok = False
                break
            params.append(read_param(data, pos, width))
            pos += width
        if not ok:
            status = f"truncated {d.name} @0x{at:X}"
            break
        size = pos - at
        resolved = ""
        if op == 0x04 and params:
            resolved = str(pos + params[0])
            max_target = max(max_target, pos + params[0])
        elif op == 0x1E and params:
            resolved = str(pos + params[0])
            max_target = max(max_target, pos + params[0])
        elif op in (0x1F, 0x20) and len(params) > 1:
            resolved = str(pos + params[1])
            max_target = max(max_target, pos + params[1])
        elif op == 0x64 and len(params) > 1:
            resolved = str(pos + params[1])
        rows.append({
            "offset": at, "opcode": op, "name": d.name,
            "parameters": ";".join(str(x) for x in params),
            "size": size, "resolved_target": resolved,
        })
        if op in (0x02, 0x05, 0x1D) and pos >= max_target:
            break
    if guard >= 10000:
        status = "guard limit"
    return rows, status


def parse_zone_headers(rom: NDS) -> List[dict]:
    narc = NARC(rom.get_file("a/0/1/2"))
    raw = narc.members[0]
    if len(raw) % 0x30:
        raise ValueError("zone header table not 0x30-aligned")
    rows = []
    for i in range(len(raw) // 0x30):
        b = raw[i*0x30:(i+1)*0x30]
        enc = u16(b, 20)
        rows.append({
            "zone_index": i,
            "map_script_member": u16(b, 6),
            "init_script_member": u16(b, 8),
            "text_member": u16(b, 10),
            "encounter_member": enc & 0x1FFF,
            "encounter_upper": (enc >> 13) & 7,
            "zone_entities_member": u16(b, 22),
            "parent_zone": u16(b, 24),
            "name_index": u16(b, 26) & 0x3FF,
        })
    return rows


def parse_entity_bindings(rom: NDS, zones: List[dict]) -> List[dict]:
    members = NARC(rom.get_file("a/1/2/5")).members
    out = []
    for z in zones:
        zid = z["zone_index"]
        mid = z["zone_entities_member"]
        if mid >= len(members):
            continue
        b = members[mid]
        if len(b) < 8:
            continue
        interact_n, npc_n, warp_n, trig_n = b[4], b[5], b[6], b[7]
        pos = 8
        for i in range(interact_n):
            if pos + 0x14 > len(b): break
            out.append({"zone_index": zid, "kind": "interactable", "entity_index": i,
                        "script_id": u16(b, pos), "condition": u16(b, pos+2)})
            pos += 0x14
        for i in range(npc_n):
            if pos + 0x24 > len(b): break
            out.append({"zone_index": zid, "kind": "npc", "entity_index": i,
                        "entity_id": u16(b, pos), "script_id": u16(b, pos+10),
                        "spawn_flag": u16(b, pos+8)})
            pos += 0x24
        pos += warp_n * 0x14
        for i in range(trig_n):
            if pos + 0x16 > len(b): break
            out.append({"zone_index": zid, "kind": "trigger", "entity_index": i,
                        "script_id": u16(b, pos), "variable": u16(b, pos+4),
                        "required_value": u16(b, pos+2)})
            pos += 0x16
        init_idx = 0
        while pos + 2 <= len(b) and u16(b, pos) != 0:
            if pos + 6 > len(b): break
            out.append({"zone_index": zid, "kind": "entity_init", "entity_index": init_idx,
                        "script_id": u16(b, pos+2), "init_type": u16(b, pos),
                        "unknown": u16(b, pos+4)})
            pos += 6
            init_idx += 1
    return out


def semantic_edges(member: int, entry: int, cmd: dict) -> List[dict]:
    name = cmd["name"]
    pars = [int(x) for x in cmd["parameters"].split(";") if x != ""]
    base = {"script_member": member, "entry_index": entry, "command_offset": cmd["offset"], "command": name}
    edges = []
    def add(kind: str, value: int, role: str):
        edges.append({**base, "edge_type": kind, "value": value, "role": role})
    if name in ("FlagSet", "FlagReset") and pars: add("flag", pars[0], name)
    elif name == "FlagGet" and pars: add("flag", pars[0], "read")
    if name.startswith("Work"):
        for i, v in enumerate(pars):
            if v >= 0x4000: add("variable", v, f"param{i}")
    msg_positions = {
        "MsgSystem":[0], "MsgSystemAsync":[0], "MsgInfo":[0], "MsgMulti":[0],
        "MsgActorEx":[1], "MsgActor":[1], "MsgPlaceSign":[0], "MsgCheckerBG":[0],
        "MsgActorGendered":[1,2], "MsgActorVersioned":[1,2], "MsgScream":[0],
    }
    for i in msg_positions.get(name, []):
        if i < len(pars): add("text_message", pars[i], f"param{i}")
    if name in ("RTCallGlobalAsync", "RTCallGlobal", "RTReserveScript") and pars:
        add("global_script", pars[0], name)
    if name in ("CallTrainerBattle",) and pars:
        add("trainer", pars[0], "trainer1")
        if len(pars) > 1 and pars[1]: add("trainer", pars[1], "trainer2")
    if name == "CallTrainerMultiBattle" and len(pars) >= 3:
        add("trainer", pars[0], "ally")
        add("trainer", pars[1], "trainer1")
        add("trainer", pars[2], "trainer2")
    if name.startswith("TrainerFlag") and pars: add("trainer", pars[0], name)
    if name.startswith("Item") and pars and name not in ("ItemGetTMCount",): add("item", pars[0], name)
    species_param1 = {"PokePartyAdd", "PokePartyAddEx", "PokePartyAddEgg", "BoxAdd", "BoxAddEx"}
    if name in species_param1 and len(pars) > 1: add("species", pars[1], name)
    if name == "CallWildBattle" and pars: add("species", pars[0], "wild_battle")
    if name == "FieldSetNextZone" and pars: add("zone", pars[0], "transition")
    return edges


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--command-source", type=Path)
    ap.add_argument("--fetch-command-source", action="store_true")
    args = ap.parse_args()

    source = obtain_command_source(args.command_source, args.fetch_command_source)
    defs = load_bw1_command_defs(source)
    rom = NDS(args.rom)
    scripts = NARC(rom.get_file("a/0/5/7")).members
    zones = parse_zone_headers(rom)
    bindings = parse_entity_bindings(rom, zones)

    member_rows, entry_rows, command_rows, edge_rows = [], [], [], []
    for mid, data in enumerate(scripts):
        entries, err = script_entry_points(data)
        member_rows.append({"member": mid, "size": len(data), "sha1": sha1(data),
                            "entry_count": len(entries), "pointer_error": err or ""})
        sorted_entries = sorted(set(entries))
        for ei, start in enumerate(entries):
            nexts = [x for x in sorted_entries if x > start]
            hard_end = nexts[0] if nexts else len(data)
            cmds, status = decode_sequence(data, start, defs, hard_end)
            entry_rows.append({"member": mid, "entry_index": ei, "start": start,
                               "hard_end": hard_end, "status": status, "command_count": len(cmds)})
            for ci, c in enumerate(cmds):
                row = {"member": mid, "entry_index": ei, "command_index": ci, **c}
                command_rows.append(row)
                edge_rows.extend(semantic_edges(mid, ei, c))

    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out/"script_members.csv", member_rows,
              ["member","size","sha1","entry_count","pointer_error"])
    write_csv(args.out/"script_entries.csv", entry_rows,
              ["member","entry_index","start","hard_end","status","command_count"])
    write_csv(args.out/"script_commands.csv", command_rows,
              ["member","entry_index","command_index","offset","opcode","name","parameters","size","resolved_target"])
    write_csv(args.out/"script_edges.csv", edge_rows,
              ["script_member","entry_index","command_offset","command","edge_type","value","role"])
    write_csv(args.out/"zone_script_bindings.csv", bindings,
              ["zone_index","kind","entity_index","entity_id","script_id","condition","spawn_flag","variable","required_value","init_type","unknown"])
    print(f"ROM={args.rom.name} scripts={len(scripts)} defs={len(defs)} zones={len(zones)}")
    print(f"entries={len(entry_rows)} commands={len(command_rows)} edges={len(edge_rows)} bindings={len(bindings)}")

if __name__ == "__main__":
    main()
