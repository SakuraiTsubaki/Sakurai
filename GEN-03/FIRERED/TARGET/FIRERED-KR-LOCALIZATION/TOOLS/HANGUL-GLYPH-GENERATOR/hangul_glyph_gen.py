#!/usr/bin/env python3
"""Hangul 8x8 / 16x16 bitmap glyph generator.

Generates modern Hangul syllables (U+AC00..U+D7A3) or a text-derived subset
into PNG atlases, 1bpp raw glyph data, Game Boy-style 2bpp tile data, and
Unicode/ID mapping metadata.

No font file is bundled. Supply --font or let the script auto-detect a Korean
font installed on the current system.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Tuple

from PIL import Image, ImageDraw, ImageFont

HANGUL_START = 0xAC00
HANGUL_END = 0xD7A3
L_TABLE = list("ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ")
V_TABLE = list("ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ")
T_TABLE = [""] + list("ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")

DEFAULT_FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf",
]


def decompose_hangul(ch: str) -> Tuple[int, int, int] | None:
    cp = ord(ch)
    if not (HANGUL_START <= cp <= HANGUL_END):
        return None
    sindex = cp - HANGUL_START
    return sindex // 588, (sindex % 588) // 28, sindex % 28


def auto_font() -> str:
    for p in DEFAULT_FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("No Korean font auto-detected. Pass --font /path/to/font.ttf")


@lru_cache(maxsize=32)
def load_font(path: str, px: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, px, index=index)
    except TypeError:
        return ImageFont.truetype(path, px)


def crop_ink(im: Image.Image) -> Image.Image:
    bbox = im.getbbox()
    if bbox is None:
        return Image.new("L", (1, 1), 0)
    return im.crop(bbox)


def render_glyph(ch: str, cell: int, font_path: str, font_index: int,
                 oversample: int = 8, threshold: int = 120,
                 margin: int = 0) -> Image.Image:
    scale = oversample
    canvas_side = max(cell * scale * 3, 96)
    font = load_font(font_path, max(cell * scale * 2, 32), font_index)
    tmp = Image.new("L", (canvas_side, canvas_side), 0)
    dr = ImageDraw.Draw(tmp)
    try:
        dr.text((canvas_side // 2, canvas_side // 2), ch, fill=255, font=font, anchor="mm")
    except Exception:
        bbox = dr.textbbox((0, 0), ch, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        dr.text(((canvas_side - w) // 2 - bbox[0], (canvas_side - h) // 2 - bbox[1]), ch, fill=255, font=font)
    ink = crop_ink(tmp)
    usable = max(1, cell - 2 * margin)
    ratio = min((usable * scale) / max(1, ink.width), (usable * scale) / max(1, ink.height))
    new_size = (max(1, int(round(ink.width * ratio))), max(1, int(round(ink.height * ratio))))
    resized = ink.resize(new_size, Image.Resampling.LANCZOS)
    hi = Image.new("L", (cell * scale, cell * scale), 0)
    hi.paste(resized, ((hi.width - resized.width) // 2, (hi.height - resized.height) // 2))
    low = hi.resize((cell, cell), Image.Resampling.BOX)
    return low.point(lambda p: 255 if p >= threshold else 0, mode="L")



def decode_nds_tile_2bpp(tile: bytes) -> List[List[int]]:
    if len(tile) != 16:
        raise ValueError("NDS font tile must be 16 bytes")
    pixels = [[0] * 8 for _ in range(8)]
    for y in range(8):
        x = 0
        for value in (tile[2 * y + 1], tile[2 * y]):
            for shift in (6, 4, 2, 0):
                pixels[y][x] = (value >> shift) & 3
                x += 1
    return pixels


def decode_nds_glyph_2bpp(raw: bytes) -> List[List[int]]:
    if len(raw) != 64:
        raise ValueError("NDS 16x16 font glyph must be 64 bytes")
    pixels = [[0] * 16 for _ in range(16)]
    for tile_index, (ox, oy) in enumerate(((0, 0), (8, 0), (0, 8), (8, 8))):
        tile = decode_nds_tile_2bpp(raw[tile_index * 16:(tile_index + 1) * 16])
        for y in range(8):
            for x in range(8):
                pixels[oy + y][ox + x] = tile[y][x]
    return pixels


def nds_glyph_to_mask(raw: bytes) -> Image.Image:
    # Gen IV semantic indices: 0=zero/transparent, 1=foreground,
    # 2=shadow, 3=background. Legacy binary derivatives keep 1+2 as ink.
    pixels = decode_nds_glyph_2bpp(raw)
    out = Image.new("L", (16, 16), 0)
    px = out.load()
    for y, row in enumerate(pixels):
        for x, value in enumerate(row):
            px[x, y] = 255 if value in (1, 2) else 0
    return out


def pack_nds_tile_2bpp(pixels: List[List[int]]) -> bytes:
    out = bytearray()
    for y in range(8):
        halves = []
        for x0 in (0, 4):
            value = 0
            for i in range(4):
                value |= (pixels[y][x0 + i] & 3) << (6 - 2 * i)
            halves.append(value)
        # Gen IV DecompressGlyphTile reads the high byte of each little-endian
        # u16 before the low byte.
        out += bytes((halves[1], halves[0]))
    return bytes(out)


def pack_nds_glyph_2bpp_from_mask(im: Image.Image) -> bytes:
    if im.size != (16, 16):
        raise ValueError("Generation IV semantic source projection requires 16x16")
    px = im.load()
    out = bytearray()
    for ox, oy in ((0, 0), (8, 0), (0, 8), (8, 8)):
        tile = [
            [1 if px[ox + x, oy + y] >= 128 else 0 for x in range(8)]
            for y in range(8)
        ]
        out += pack_nds_tile_2bpp(tile)
    return bytes(out)


def build_gen4_korean_mapping() -> List[Dict]:
    mapping = []
    slot = 1024
    for lead in range(0xB0, 0xC9):
        for trail in range(0xA1, 0xFF):
            try:
                ch = bytes((lead, trail)).decode("euc_kr")
            except UnicodeDecodeError:
                continue
            if len(ch) == 1 and HANGUL_START <= ord(ch) <= HANGUL_END:
                mapping.append({
                    "char": ch,
                    "codepoint": f"U+{ord(ch):04X}",
                    "slot": slot,
                    "message_code": slot + 1,
                    "class": "ks_x_1001_wansung",
                })
                slot += 1
    if slot != 3374:
        raise ValueError(f"unexpected Wansung mapping end: {slot}")

    for i, trail in enumerate(range(0xA1, 0xD4)):
        ch = bytes((0xA4, trail)).decode("euc_kr")
        mapping.append({
            "char": ch,
            "codepoint": f"U+{ord(ch):04X}",
            "slot": 3376 + i,
            "message_code": 3377 + i,
            "class": "ks_x_1001_compatibility_jamo",
        })
    if len(mapping) != 2401:
        raise ValueError(f"unexpected Generation IV mapping size: {len(mapping)}")
    return mapping


def load_gen4_source_pack(path: str | None, member: int) -> Dict[str, Dict]:
    if not path:
        return {}
    root = Path(path)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    mapping_name = manifest.get("mapping_file")
    if mapping_name:
        mapping_path = root / mapping_name
        mapping_bytes = mapping_path.read_bytes()
        if manifest.get("mapping_file_encoding") == "gzip" or mapping_path.suffix == ".gz":
            mapping_bytes = gzip.decompress(mapping_bytes)
        mapping = json.loads(mapping_bytes.decode("utf-8"))
    elif manifest.get("mapping_scheme") == "ks_x_1001_wansung2350_plus_compat_jamo51":
        mapping = build_gen4_korean_mapping()
    else:
        raise ValueError("Generation IV source pack has no supported mapping definition")
    matches = [entry for entry in manifest["members"] if int(entry["member"]) == member]
    if len(matches) != 1:
        raise ValueError(f"Generation IV source member {member} not found")
    member_meta = matches[0]
    source_path = root / member_meta["source_file"]
    raw = source_path.read_bytes()
    if member_meta.get("source_file_encoding") == "gzip" or source_path.suffix == ".gz":
        raw = gzip.decompress(raw)
    bytes_per_glyph = int(member_meta["bytes_per_glyph"])
    if len(raw) != len(mapping) * bytes_per_glyph:
        raise ValueError("Generation IV source pack length mismatch")

    result = {}
    for i, rec in enumerate(mapping):
        entry = dict(rec)
        entry["raw"] = raw[i * bytes_per_glyph:(i + 1) * bytes_per_glyph]
        entry["member"] = member
        entry["source_file"] = member_meta["source_file"]
        result[rec["char"]] = entry
    return result


def apply_override(im: Image.Image, override: Dict | None) -> Image.Image:
    if not override:
        return im
    rows = override.get("rows")
    if rows:
        cell = im.width
        out = Image.new("L", (cell, cell), 0)
        px = out.load()
        for y, row in enumerate(rows[:cell]):
            bits = row.strip().replace(" ", "")
            for x, bit in enumerate(bits[:cell]):
                if bit in ("1", "#", "X", "x"):
                    px[x, y] = 255
        return out
    return im


def pack_1bpp(im: Image.Image) -> bytes:
    w, h = im.size
    out = bytearray()
    px = im.load()
    for y in range(h):
        for x0 in range(0, w, 8):
            b = 0
            for i in range(8):
                x = x0 + i
                if x < w and px[x, y] >= 128:
                    b |= 1 << (7 - i)
            out.append(b)
    return bytes(out)


def pack_gb_2bpp_tile(tile8: Image.Image, ink_index: int = 3) -> bytes:
    if tile8.size != (8, 8):
        raise ValueError("GB 2bpp packer requires 8x8 tile")
    px = tile8.load()
    out = bytearray()
    lo_bit = ink_index & 1
    hi_bit = (ink_index >> 1) & 1
    for y in range(8):
        lo = hi = 0
        for x in range(8):
            if px[x, y] >= 128:
                if lo_bit:
                    lo |= 1 << (7 - x)
                if hi_bit:
                    hi |= 1 << (7 - x)
        out += bytes([lo, hi])
    return bytes(out)


def pack_gb_2bpp_glyph(im: Image.Image, ink_index: int = 3) -> bytes:
    w, h = im.size
    if w % 8 or h % 8:
        raise ValueError("Glyph dimensions must be multiples of 8")
    out = bytearray()
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            out += pack_gb_2bpp_tile(im.crop((tx, ty, tx + 8, ty + 8)), ink_index)
    return bytes(out)


def make_atlas(glyphs: List[Image.Image], cell: int, cols: int) -> Image.Image:
    rows = math.ceil(len(glyphs) / cols)
    atlas = Image.new("L", (cols * cell, rows * cell), 0)
    for i, g in enumerate(glyphs):
        atlas.paste(g, ((i % cols) * cell, (i // cols) * cell))
    return atlas


def unique_chars_from_text(text: str, include_non_hangul: bool) -> List[str]:
    seen, out = set(), []
    for ch in text:
        if ch in "\r\n\t":
            continue
        if not include_non_hangul and decompose_hangul(ch) is None:
            continue
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return out


def load_chars(args) -> List[str]:
    if args.subset:
        text = Path(args.subset).read_text(encoding="utf-8")
        chars = unique_chars_from_text(text, args.include_non_hangul)
    else:
        chars = [chr(cp) for cp in range(HANGUL_START, HANGUL_END + 1)]
    if args.extras:
        for ch in args.extras:
            if ch not in chars and ch not in "\r\n\t":
                chars.append(ch)
    return chars


def load_overrides(path: str | None) -> Dict[str, Dict]:
    return {} if not path else json.loads(Path(path).read_text(encoding="utf-8"))


def generate(args) -> None:
    font_path = args.font or auto_font()
    font_index = args.font_index
    if font_index is None:
        font_index = 1 if font_path.endswith("NotoSansCJK-Bold.ttc") else 0
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    chars = load_chars(args)
    overrides = load_overrides(args.overrides)
    gen4_source = load_gen4_source_pack(args.gen4_source_dir, args.gen4_member)

    summary = {
        "font": font_path,
        "font_index": font_index,
        "glyph_count": len(chars),
        "sizes": args.sizes,
        "unicode_range": "U+AC00..U+D7A3",
        "oversample": args.oversample,
        "threshold": args.threshold,
        "margin": args.margin,
        "gen4_source_dir": args.gen4_source_dir,
        "gen4_member": args.gen4_member,
        "source_counts": {},
    }

    meta_common = []
    for i, ch in enumerate(chars):
        dec = decompose_hangul(ch)
        rec = {
            "id": i,
            "char": ch,
            "codepoint": f"U+{ord(ch):04X}",
            "unicode": ord(ch),
            "is_modern_hangul": dec is not None,
        }
        if dec:
            l, v, t = dec
            rec.update({
                "l_index": l,
                "l_jamo": L_TABLE[l],
                "v_index": v,
                "v_jamo": V_TABLE[v],
                "t_index": t,
                "t_jamo": T_TABLE[t],
            })
        meta_common.append(rec)

    for cell in args.sizes:
        glyphs = []
        raw1 = bytearray()
        raw2 = bytearray()
        raw_semantic2 = bytearray()
        records = []
        source_counts = {}
        one_bytes = (cell * cell + 7) // 8
        tiles_per_glyph = (cell // 8) * (cell // 8)
        two_bytes = tiles_per_glyph * 16

        for i, ch in enumerate(chars):
            official = gen4_source.get(ch) if cell == 16 else None
            if official:
                glyph = nds_glyph_to_mask(official["raw"])
                source_kind = "gen4_official"
                source_member = official["member"]
                source_slot = official["slot"]
                source_class = official["class"]
                semantic2 = official["raw"]
            else:
                glyph = render_glyph(
                    ch,
                    cell,
                    font_path,
                    font_index,
                    args.oversample,
                    args.threshold,
                    args.margin,
                )
                source_kind = "project_derived_vector"
                source_member = None
                source_slot = None
                source_class = None
                semantic2 = pack_nds_glyph_2bpp_from_mask(glyph) if cell == 16 else None

            ov = overrides.get(ch, {}).get(str(cell)) if ch in overrides else None
            if ov:
                glyph = apply_override(glyph, ov)
                source_kind = "project_override"
                source_member = None
                source_slot = None
                source_class = None
                semantic2 = pack_nds_glyph_2bpp_from_mask(glyph) if cell == 16 else None

            source_counts[source_kind] = source_counts.get(source_kind, 0) + 1
            glyphs.append(glyph)
            b1 = pack_1bpp(glyph)
            b2 = pack_gb_2bpp_glyph(glyph, args.gb_ink_index)
            raw1 += b1
            raw2 += b2
            if cell == 16:
                raw_semantic2 += semantic2

            rec = dict(meta_common[i])
            rec.update({
                "cell": cell,
                "source_kind": source_kind,
                "source_member": source_member,
                "source_slot": source_slot,
                "source_class": source_class,
                "1bpp_offset": i * one_bytes,
                "1bpp_length": len(b1),
                "gb_2bpp_offset": i * two_bytes,
                "gb_2bpp_length": len(b2),
                "tile_count": tiles_per_glyph,
            })
            if cell == 16:
                rec.update({
                    "semantic_2bpp_offset": i * 64,
                    "semantic_2bpp_length": 64,
                })
            records.append(rec)

        cols = args.cols8 if cell == 8 else args.cols16
        make_atlas(glyphs, cell, cols).save(outdir / f"atlas_{cell}x{cell}.png")
        (outdir / f"glyphs_{cell}x{cell}_1bpp.bin").write_bytes(raw1)
        (outdir / f"glyphs_{cell}x{cell}_gb2bpp.bin").write_bytes(raw2)
        if cell == 16:
            (outdir / "glyphs_16x16_semantic2bpp.bin").write_bytes(raw_semantic2)

        (outdir / f"mapping_{cell}x{cell}.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        with (outdir / f"mapping_{cell}x{cell}.csv").open(
            "w", encoding="utf-8-sig", newline=""
        ) as csv_file:
            fields = list(records[0].keys()) if records else ["id", "char", "codepoint"]
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
        summary["source_counts"][str(cell)] = source_counts

    (outdir / "charset.txt").write_text("".join(chars), encoding="utf-8")
    (outdir / "build_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", "-o", default="out")
    ap.add_argument("--font")
    ap.add_argument("--font-index", type=int, default=None)
    ap.add_argument("--sizes", type=int, nargs="+", default=[8, 16], choices=[8, 16])
    ap.add_argument("--subset")
    ap.add_argument("--include-non-hangul", action="store_true")
    ap.add_argument("--extras", default="")
    ap.add_argument("--oversample", type=int, default=8)
    ap.add_argument("--threshold", type=int, default=120)
    ap.add_argument("--margin", type=int, default=0)
    ap.add_argument("--cols8", type=int, default=128)
    ap.add_argument("--cols16", type=int, default=64)
    ap.add_argument("--gb-ink-index", type=int, default=3, choices=[1, 2, 3])
    ap.add_argument("--overrides")
    ap.add_argument(
        "--gen4-source-dir",
        help="source pack produced by extract-gen4-korean-font.py",
    )
    ap.add_argument(
        "--gen4-member",
        type=int,
        default=1,
        choices=[0, 1, 2, 4, 10],
        help="Generation IV source font member to use for exact 16x16 coverage",
    )
    return ap.parse_args()


if __name__ == "__main__":
    generate(parse_args())
