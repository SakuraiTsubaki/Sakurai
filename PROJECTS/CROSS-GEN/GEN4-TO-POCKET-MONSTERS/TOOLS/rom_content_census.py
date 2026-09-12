#!/usr/bin/env python3
"""Generate reproducible metadata catalogs from project ROM baselines.

The tool never modifies a ROM. It writes only metadata/CSV observations:
- NDS: header, FNT/FAT file index, SHA-1, NARC member counts.
- GBA: header verification, long 00/FF run candidates with aligned ROM-pointer
  reference counts, and structurally valid 0x10 LZ77 stream candidates.

Candidate output is not semantic identification or safe-space certification.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import csv
import hashlib
import json
import struct
from pathlib import Path


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def narc_members(blob: bytes) -> int | None:
    if len(blob) < 0x1C or blob[:4] != b"NARC":
        return None
    try:
        header_size = struct.unpack_from("<H", blob, 0x0C)[0]
        if blob[header_size:header_size + 4] not in (b"BTAF", b"FATB"):
            return None
        return struct.unpack_from("<H", blob, header_size + 8)[0]
    except (IndexError, struct.error):
        return None


def parse_nds(data: bytes) -> tuple[dict, list[dict]]:
    u32 = lambda o: struct.unpack_from("<I", data, o)[0]
    header = {
        "title": data[:12].split(b"\0", 1)[0].decode("ascii", "replace"),
        "game_code": data[12:16].decode("ascii", "replace"),
        "maker_code": data[16:18].decode("ascii", "replace"),
        "unit_code": data[0x12],
        "rom_version": data[0x1E],
        "fnt_offset": u32(0x40), "fnt_size": u32(0x44),
        "fat_offset": u32(0x48), "fat_size": u32(0x4C),
        "rom_size_header": u32(0x80), "header_size": u32(0x84),
    }
    fat = [struct.unpack_from("<II", data, header["fat_offset"] + i * 8)
           for i in range(header["fat_size"] // 8)]
    fnt = data[header["fnt_offset"]:header["fnt_offset"] + header["fnt_size"]]
    if len(fnt) < 8:
        raise ValueError("invalid/empty NDS FNT")
    dir_count = struct.unpack_from("<H", fnt, 6)[0]
    dirs = [struct.unpack_from("<IHH", fnt, i * 8) for i in range(dir_count)]
    rows: list[dict] = []
    visited: set[int] = set()

    def walk(dir_id: int, prefix: str) -> None:
        idx = dir_id - 0xF000
        if idx < 0 or idx >= len(dirs) or dir_id in visited:
            return
        visited.add(dir_id)
        pos, file_id, _ = dirs[idx]
        while pos < len(fnt):
            n = fnt[pos]; pos += 1
            if n == 0:
                break
            is_dir = bool(n & 0x80); ln = n & 0x7F
            name = fnt[pos:pos + ln].decode("ascii", "replace"); pos += ln
            if is_dir:
                sub = struct.unpack_from("<H", fnt, pos)[0]; pos += 2
                walk(sub, prefix + name + "/")
            else:
                if file_id >= len(fat):
                    raise ValueError(f"FNT file id {file_id} exceeds FAT")
                start, end = fat[file_id]
                blob = data[start:end]
                magic = blob[:4]
                magic4 = (magic.decode("ascii", "replace")
                          if len(magic) == 4 and all(32 <= b < 127 for b in magic)
                          else magic.hex())
                count = narc_members(blob)
                rows.append({
                    "file_id": file_id, "path": prefix + name,
                    "rom_start": f"0x{start:08X}", "rom_end": f"0x{end:08X}",
                    "size": end - start, "magic4": magic4,
                    "narc_members": "" if count is None else count,
                    "sha1": sha1(blob),
                })
                file_id += 1

    walk(0xF000, "")
    rows.sort(key=lambda r: r["file_id"])
    header.update({
        "fat_entry_count": len(fat),
        "fnt_directory_count": dir_count,
        "named_file_count": len(rows),
        "named_narc_count": sum(r["magic4"] == "NARC" for r in rows),
    })
    return header, rows


def gba_header(data: bytes) -> dict:
    if len(data) < 0xC0:
        raise ValueError("file too small for GBA header")
    stored = data[0xBD]
    calculated = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
    return {
        "title": data[0xA0:0xAC].split(b"\0", 1)[0].decode("ascii", "replace"),
        "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
        "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
        "software_version": data[0xBC],
        "header_complement": stored,
        "header_complement_calculated": calculated,
        "header_checksum_valid": stored == calculated,
    }


def padding_runs(data: bytes, minimum: int = 4096) -> list[dict]:
    targets = collections.Counter()
    for off in range(0, len(data) - 3, 4):
        value = struct.unpack_from("<I", data, off)[0]
        if 0x08000000 <= value < 0x08000000 + len(data):
            targets[value - 0x08000000] += 1
    ordered = sorted(targets)
    out: list[dict] = []
    i = 0
    while i < len(data):
        fill = data[i]
        if fill not in (0x00, 0xFF):
            i += 1; continue
        j = i + 1
        while j < len(data) and data[j] == fill:
            j += 1
        if j - i >= minimum:
            lo, hi = bisect.bisect_left(ordered, i), bisect.bisect_left(ordered, j)
            refs = sum(targets[x] for x in ordered[lo:hi])
            out.append({
                "start": f"0x{i:08X}", "end_exclusive": f"0x{j:08X}",
                "length": j - i, "fill_byte": f"{fill:02X}",
                "aligned_rom_pointer_refs_into_range": refs,
                "status": "candidate-only; requires code/data/runtime verification",
            })
        i = j
    return out


def validate_lz77(data: bytes, off: int, max_output: int = 0x200000) -> dict | None:
    if off + 4 > len(data) or data[off] != 0x10:
        return None
    output_size = data[off + 1] | data[off + 2] << 8 | data[off + 3] << 16
    if output_size <= 0 or output_size > max_output:
        return None
    src, produced = off + 4, 0
    try:
        while produced < output_size:
            flags = data[src]; src += 1
            for bit in range(8):
                if produced >= output_size:
                    break
                if flags & (0x80 >> bit):
                    a, b = data[src], data[src + 1]; src += 2
                    length = (a >> 4) + 3
                    distance = (((a & 0x0F) << 8) | b) + 1
                    if distance > produced:
                        return None
                    produced += min(length, output_size - produced)
                else:
                    src += 1; produced += 1
                if src > len(data):
                    return None
    except IndexError:
        return None
    return {
        "offset": f"0x{off:08X}", "decompressed_size": output_size,
        "compressed_size": src - off, "compressed_end_exclusive": f"0x{src:08X}",
    }


def lz77_candidates(data: bytes) -> list[dict]:
    out = []
    for off in range(0, len(data) - 4, 4):
        if data[off] == 0x10:
            row = validate_lz77(data, off)
            if row:
                out.append(row)
    return out


def run_entry(entry: dict, out_root: Path) -> dict:
    rom = Path(entry["path"])
    data = rom.read_bytes()
    base = out_root / entry["release_id"]
    base.mkdir(parents=True, exist_ok=True)
    observation = {
        "release_id": entry["release_id"], "dump_id": entry.get("dump_id"),
        "source_filename": rom.name, "size": len(data), "sha1": sha1(data),
        "rom_binary_committed": False,
    }
    (base / "rom-observation.json").write_text(json.dumps(observation, indent=2) + "\n")
    if entry["platform"].startswith("NDS"):
        header, files = parse_nds(data)
        narcs = [r for r in files if r["magic4"] == "NARC"]
        (base / "header.json").write_text(json.dumps(header, indent=2) + "\n")
        write_csv(base / "nitrofs-files.csv", files)
        write_csv(base / "narc-catalog.csv", narcs)
        return {"release_id": entry["release_id"], "files": len(files), "narcs": len(narcs)}
    header = gba_header(data)
    pads = padding_runs(data)
    lz = lz77_candidates(data)
    (base / "header.json").write_text(json.dumps(header, indent=2) + "\n")
    write_csv(base / "padding-candidates.csv", pads)
    write_csv(base / "lz77-candidates.csv", lz)
    return {"release_id": entry["release_id"], "padding_candidates": len(pads), "lz77_candidates": len(lz)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path, help="JSON array: path/platform/release_id/dump_id")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    entries = json.loads(args.manifest.read_text(encoding="utf-8"))
    results = [run_entry(e, args.out) for e in entries]
    (args.out / "summary.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
