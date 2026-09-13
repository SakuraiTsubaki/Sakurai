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
    summary = {"font": font_path, "font_index": font_index, "glyph_count": len(chars),
               "sizes": args.sizes, "unicode_range": "U+AC00..U+D7A3",
               "oversample": args.oversample, "threshold": args.threshold, "margin": args.margin}
    meta_common = []
    for i, ch in enumerate(chars):
        dec = decompose_hangul(ch)
        rec = {"id": i, "char": ch, "codepoint": f"U+{ord(ch):04X}", "unicode": ord(ch),
               "is_modern_hangul": dec is not None}
        if dec:
            l, v, t = dec
            rec.update({"l_index": l, "l_jamo": L_TABLE[l], "v_index": v, "v_jamo": V_TABLE[v],
                        "t_index": t, "t_jamo": T_TABLE[t]})
        meta_common.append(rec)
    for cell in args.sizes:
        glyphs, raw1, raw2, records = [], bytearray(), bytearray(), []
        one_bytes = (cell * cell + 7) // 8
        tiles_per_glyph = (cell // 8) * (cell // 8)
        two_bytes = tiles_per_glyph * 16
        for i, ch in enumerate(chars):
            g = render_glyph(ch, cell, font_path, font_index, args.oversample, args.threshold, args.margin)
            ov = overrides.get(ch, {}).get(str(cell)) if ch in overrides else None
            g = apply_override(g, ov)
            glyphs.append(g)
            b1, b2 = pack_1bpp(g), pack_gb_2bpp_glyph(g, args.gb_ink_index)
            raw1 += b1; raw2 += b2
            r = dict(meta_common[i])
            r.update({"cell": cell, "1bpp_offset": i * one_bytes, "1bpp_length": len(b1),
                      "gb_2bpp_offset": i * two_bytes, "gb_2bpp_length": len(b2),
                      "tile_count": tiles_per_glyph})
            records.append(r)
        cols = args.cols8 if cell == 8 else args.cols16
        make_atlas(glyphs, cell, cols).save(outdir / f"atlas_{cell}x{cell}.png")
        (outdir / f"glyphs_{cell}x{cell}_1bpp.bin").write_bytes(raw1)
        (outdir / f"glyphs_{cell}x{cell}_gb2bpp.bin").write_bytes(raw2)
        (outdir / f"mapping_{cell}x{cell}.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        with (outdir / f"mapping_{cell}x{cell}.csv").open("w", encoding="utf-8-sig", newline="") as f:
            fields = list(records[0].keys()) if records else ["id", "char", "codepoint"]
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(records)
    (outdir / "charset.txt").write_text("".join(chars), encoding="utf-8")
    (outdir / "build_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
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
    return ap.parse_args()


if __name__ == "__main__":
    generate(parse_args())
