#!/usr/bin/env python3
"""Build a Gen III-ready battle-sprite pack from the Tsubaki BW 64x64 cross-check set."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

SOURCE_ROOT = Path(
    "GENERATION-V/BW/EUR/REV-UNKNOWN/SPRITE_ASSETS/"
    "64x64_PRESERVATION_V2_EXTERNAL_CROSSCHECK"
)
ROLES = SOURCE_ROOT / "roles.csv"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def align4(buf: bytearray) -> None:
    while len(buf) & 3:
        buf.append(0)


def rgb8_to_bgr555(r: int, g: int, b: int) -> int:
    return ((r * 31 + 127) // 255) | (((g * 31 + 127) // 255) << 5) | (((b * 31 + 127) // 255) << 10)


def rgba_to_4bpp_and_palette(path: Path) -> tuple[bytes, bytes, int]:
    im = Image.open(path).convert("RGBA")
    if im.size != (64, 64):
        raise RuntimeError(f"expected 64x64 PNG, got {im.size}: {path}")

    colors: list[tuple[int, int, int]] = []
    cmap: dict[tuple[int, int, int], int] = {}
    idx = [0] * 4096
    for i, (r, g, b, a) in enumerate(im.getdata()):
        if a == 0:
            continue
        c = (r, g, b)
        n = cmap.get(c)
        if n is None:
            if len(colors) >= 15:
                raise RuntimeError(f">15 opaque colors: {path}")
            colors.append(c)
            n = len(colors)
            cmap[c] = n
        idx[i] = n

    raw = bytearray()
    for ty in range(8):
        for tx in range(8):
            for y in range(8):
                base = (ty * 8 + y) * 64 + tx * 8
                for x in range(0, 8, 2):
                    raw.append(idx[base + x] | (idx[base + x + 1] << 4))
    if len(raw) != 2048:
        raise AssertionError(len(raw))

    pal = bytearray(32)
    for slot, (r, g, b) in enumerate(colors, 1):
        v = rgb8_to_bgr555(r, g, b)
        pal[slot * 2] = v & 0xFF
        pal[slot * 2 + 1] = v >> 8
    return bytes(raw), bytes(pal), len(colors) + 1


def gba_lz77(data: bytes) -> bytes:
    n = len(data)
    out = bytearray((0x10, n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF))
    pos = 0
    chains: dict[bytes, deque[int]] = defaultdict(deque)

    def add(p: int) -> None:
        if p + 2 >= n:
            return
        q = chains[data[p:p + 3]]
        q.append(p)
        while len(q) > 128:
            q.popleft()

    while pos < n:
        flag_at = len(out)
        out.append(0)
        flags = 0
        payload = bytearray()
        for bit in range(8):
            if pos >= n:
                break
            best_len = 0
            best_pos = -1
            if pos + 2 < n:
                q = chains.get(data[pos:pos + 3])
                checked = 0
                if q:
                    for cand in reversed(q):
                        disp = pos - cand - 1
                        if disp > 0xFFF:
                            break
                        checked += 1
                        length = 3
                        limit = min(18, n - pos)
                        while length < limit and data[cand + length] == data[pos + length]:
                            length += 1
                        if length > best_len:
                            best_len = length
                            best_pos = cand
                            if length == 18:
                                break
                        if checked >= 64:
                            break
            if best_len >= 3:
                flags |= 1 << (7 - bit)
                disp = pos - best_pos - 1
                token = ((best_len - 3) << 12) | disp
                payload.extend(((token >> 8) & 0xFF, token & 0xFF))
                old = pos
                pos += best_len
                for p in range(old, pos):
                    add(p)
            else:
                payload.append(data[pos])
                add(pos)
                pos += 1
        out[flag_at] = flags
        out.extend(payload)

    align4(out)
    return bytes(out)


def gba_lz77_decompress(blob: bytes) -> bytes:
    if not blob or blob[0] != 0x10:
        raise ValueError("not type-0x10")
    target = blob[1] | (blob[2] << 8) | (blob[3] << 16)
    out = bytearray()
    p = 4
    while len(out) < target:
        flags = blob[p]
        p += 1
        for bit in range(8):
            if len(out) >= target:
                break
            if flags & (1 << (7 - bit)):
                a, b = blob[p], blob[p + 1]
                p += 2
                length = (a >> 4) + 3
                disp = ((a & 15) << 8) | b
                src = len(out) - disp - 1
                for _ in range(length):
                    out.append(out[src])
                    src += 1
            else:
                out.append(blob[p])
                p += 1
    return bytes(out[:target])


@dataclass(frozen=True)
class GfxRecord:
    id: int
    sha256: str
    raw_size: int
    offset: int
    compressed_size: int


@dataclass(frozen=True)
class PalRecord:
    id: int
    sha256: str
    offset: int
    size: int


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    repo = args.repo.resolve()
    source_root = repo / SOURCE_ROOT
    roles_path = repo / ROLES
    out = args.out if args.out.is_absolute() else repo / args.out
    out.mkdir(parents=True, exist_ok=True)

    if not roles_path.exists():
        raise FileNotFoundError(roles_path)

    logical: list[dict[str, object]] = []
    gfx_by_hash: dict[str, int] = {}
    pal_by_hash: dict[str, int] = {}
    gfx_raws: list[bytes] = []
    pal_raws: list[bytes] = []
    max_pal = 0

    with roles_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    expected = 649 * 4
    if len(rows) != expected:
        raise RuntimeError(f"expected {expected} BW logical roles, got {len(rows)}")

    seen_roles: set[tuple[int, str, str]] = set()
    per_dex: dict[int, set[tuple[str, str]]] = defaultdict(set)

    for row in rows:
        dex = int(row["dex"])
        side = row["side"]
        palette = row["palette"]
        role = (dex, side, palette)
        if role in seen_roles:
            raise RuntimeError(f"duplicate role: {role}")
        seen_roles.add(role)
        per_dex[dex].add((side, palette))

        rel_asset = Path(row["asset_path"])
        png = source_root / rel_asset
        if not png.exists():
            raise FileNotFoundError(png)

        raw, pal, pentries = rgba_to_4bpp_and_palette(png)
        max_pal = max(max_pal, pentries)
        gsha = sha256(raw)
        psha = sha256(pal)

        if gsha not in gfx_by_hash:
            gfx_by_hash[gsha] = len(gfx_raws)
            gfx_raws.append(raw)
        if psha not in pal_by_hash:
            pal_by_hash[psha] = len(pal_raws)
            pal_raws.append(pal)

        logical.append({
            "logical_id": len(logical),
            "dex": dex,
            "side": side,
            "palette": palette,
            "source_status": "BW_EXTERNAL_CROSSCHECK_NOT_ROM_PRIMARY",
            "source_path": png.relative_to(repo).as_posix(),
            "source_asset_sha256_rgba": row["asset_sha256_rgba"],
            "gfx_id": gfx_by_hash[gsha],
            "palette_id": pal_by_hash[psha],
            "gfx_sha256": gsha,
            "palette_sha256": psha,
            "palette_entries": pentries,
        })

    required_roles = {
        ("front", "normal"),
        ("front", "shiny"),
        ("back", "normal"),
        ("back", "shiny"),
    }
    if set(per_dex) != set(range(1, 650)):
        absent = sorted(set(range(1, 650)) - set(per_dex))
        raise RuntimeError(f"missing dex entries: {absent[:20]}")
    for dex, roles in per_dex.items():
        if roles != required_roles:
            raise RuntimeError(f"incomplete roles for dex {dex}: {sorted(roles)}")

    gfxpack = bytearray()
    gfxrecords: list[GfxRecord] = []
    total_raw = 0
    for i, raw in enumerate(gfx_raws):
        align4(gfxpack)
        off = len(gfxpack)
        comp = gba_lz77(raw)
        if gba_lz77_decompress(comp) != raw:
            raise RuntimeError(f"LZ77 round-trip failed: {i}")
        gfxpack.extend(comp)
        gfxrecords.append(GfxRecord(i, sha256(raw), len(raw), off, len(comp)))
        total_raw += len(raw)

    palpack = bytearray()
    palrecords: list[PalRecord] = []
    for i, pal in enumerate(pal_raws):
        off = len(palpack)
        palpack.extend(pal)
        palrecords.append(PalRecord(i, sha256(pal), off, len(pal)))

    (out / "gen5_bw_battle_gfx_lz.pack").write_bytes(gfxpack)
    (out / "gen5_bw_battle_palettes.gbapal").write_bytes(palpack)

    with (out / "logical_index.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(logical[0]))
        w.writeheader()
        w.writerows(logical)

    with (out / "gfx_index.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["id", "sha256", "raw_size", "offset", "compressed_size"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in gfxrecords:
            w.writerow(r.__dict__)

    with (out / "palette_index.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["id", "sha256", "offset", "size"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in palrecords:
            w.writerow(r.__dict__)

    summary = {
        "format": "GEN5_BW_BATTLE_TO_GEN3_PACK_V1",
        "source": SOURCE_ROOT.as_posix(),
        "source_status": "external cross-check only; not ROM-primary /a/0/0/4 master",
        "national_dex_species": 649,
        "logical_records": len(logical),
        "roles_per_species": 4,
        "role_set": ["front_normal", "front_shiny", "back_normal", "back_shiny"],
        "unique_4bpp_graphics": len(gfxrecords),
        "unique_palettes": len(palrecords),
        "raw_graphics_bytes_before_dedup": len(logical) * 2048,
        "unique_raw_graphics_bytes": total_raw,
        "gfx_lz_pack_bytes": len(gfxpack),
        "palette_pack_bytes": len(palpack),
        "gfx_compression_ratio_vs_unique_raw": len(gfxpack) / total_raw if total_raw else 0,
        "max_palette_entries_including_transparent": max_pal,
        "canvas": "64x64",
        "pixel_format": "GBA OBJ 4bpp tiled",
        "palette_format": "16-color little-endian BGR555; slot 0 transparent",
        "compression": "GBA BIOS LZ77 type 0x10; each unique 2048-byte frame independently compressed and 4-byte aligned",
        "dedup_policy": "identical GBA-ready graphics and palettes share IDs; all 2596 logical roles remain addressable",
        "integration_policy": "original Gen III sprites are preserved; this is an additive Gen V source pack for expanded species/variant tables",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (out / "README.md").write_text(
        "# Generation V BW battle sprites -> Generation III pack v1\n\n"
        "Generated from the existing Tsubaki BW 64x64 preservation-v2 external cross-check set. "
        "All National Dex 001-649 base species are retained as front/back normal/shiny logical records "
        "(2,596 roles total). Identical GBA-ready graphics and palettes are deduplicated internally; "
        "the original Generation III graphics are not overwritten.\n\n"
        "`gen5_bw_battle_gfx_lz.pack` contains concatenated GBA BIOS LZ77 type-0x10 64x64 4bpp frames. "
        "`gen5_bw_battle_palettes.gbapal` contains concatenated unique 32-byte BGR555 palettes. "
        "CSV indices preserve National Dex number, side, palette role, provenance, hashes and pack offsets.\n\n"
        "**Source status:** the current BW 64x64 set is an external cross-check, not the final ROM-primary "
        "`/a/0/0/4` master. This Gen III pack therefore preserves that status and is intended to be rebuilt "
        "against the authoritative ROM-primary master when it is published. No ROM binary is committed.\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
