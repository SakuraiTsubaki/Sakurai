#!/usr/bin/env python3
"""Extract Pokémon graphics rooted by Emerald's Game Freak ROM header.

The tool verifies reference ROM SHA-1 values, follows per-release header roots,
decodes GBA LZ77/4bpp/BGR555 assets, and exports editable PNGs plus exact raw
payloads. Icon palette descriptors 3-5 are deliberately ignored because only
0-2 are real palettes in Emerald.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, struct
from pathlib import Path
from PIL import Image

ROM_BASE = 0x08000000
SLOT_COUNT = 440
VALID_ICON_PALETTES = 3


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def gba_lz77(data: bytes, offset: int) -> tuple[bytes, bytes]:
    if data[offset] != 0x10:
        raise ValueError(f"not GBA LZ77 at 0x{offset:X}")
    size = data[offset+1] | data[offset+2] << 8 | data[offset+3] << 16
    src = offset + 4
    out = bytearray()
    while len(out) < size:
        flags = data[src]
        src += 1
        for bit in range(7, -1, -1):
            if len(out) >= size:
                break
            if flags & (1 << bit):
                a, b = data[src], data[src+1]
                src += 2
                length = (a >> 4) + 3
                disp = ((a & 0xF) << 8 | b) + 1
                if disp > len(out):
                    raise ValueError("invalid LZ77 displacement")
                for _ in range(length):
                    out.append(out[-disp])
            else:
                out.append(data[src])
                src += 1
    return bytes(out), data[offset:src]


def bgr555_palette(raw: bytes) -> list[tuple[int, int, int, int]]:
    if len(raw) != 32:
        raise ValueError(f"palette bank must be 32 bytes, got {len(raw)}")
    colors = []
    for i in range(0, 32, 2):
        v = raw[i] | raw[i+1] << 8
        colors.append(((v & 31) * 255 // 31,
                       ((v >> 5) & 31) * 255 // 31,
                       ((v >> 10) & 31) * 255 // 31,
                       0 if i == 0 else 255))
    return colors


def render_4bpp(raw: bytes, width: int, height: int, palette) -> Image.Image:
    if len(raw) != width * height // 2:
        raise ValueError((len(raw), width, height))
    image = Image.new("RGBA", (width, height))
    px = image.load()
    tiles_x = width // 8
    for tile_i in range(len(raw) // 32):
        tile = raw[tile_i*32:(tile_i+1)*32]
        tx = (tile_i % tiles_x) * 8
        ty = (tile_i // tiles_x) * 8
        for y in range(8):
            for x in range(8):
                b = tile[y*4 + x//2]
                index = (b >> (4 * (x & 1))) & 0xF
                px[tx+x, ty+y] = palette[index]
    return image


def render_mon(raw: bytes, palette_raw: bytes) -> Image.Image:
    banks = len(palette_raw) // 32
    if banks == 1:
        return render_4bpp(raw, 64, len(raw) * 2 // 64,
                           bgr555_palette(palette_raw))
    if len(raw) == banks * 2048:
        image = Image.new("RGBA", (64, 64 * banks))
        for bank in range(banks):
            frame = render_4bpp(raw[bank*2048:(bank+1)*2048], 64, 64,
                                bgr555_palette(palette_raw[bank*32:(bank+1)*32]))
            image.alpha_composite(frame, (0, bank * 64))
        return image
    raise ValueError(f"unsupported packed mon graphic: gfx={len(raw)} pal={len(palette_raw)}")


def load_verified(ref: dict, rom_dir: Path) -> bytes:
    data = (rom_dir / ref["source_filename"]).read_bytes()
    got = sha1(data)
    if got != ref["sha1"]:
        raise ValueError(f"{ref['id']}: SHA-1 mismatch {got}")
    return data


def safe_name(index: int) -> str:
    if index == 412:
        return "egg"
    if 413 <= index <= 437:
        return f"unown_{chr(ord('b') + index - 413)}"
    if index == 438:
        return "unown_emark"
    if index == 439:
        return "unown_qmark"
    return f"slot_{index:03d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom_dir", type=Path)
    ap.add_argument("--release", default="JPN")
    ap.add_argument("--manifest", type=Path, default=Path("manifests/roms.json"))
    ap.add_argument("--headers", type=Path, default=Path("analysis/gf_rom_headers.json"))
    ap.add_argument("--out-dir", type=Path, default=Path("graphics/pokemon/extracted"))
    args = ap.parse_args()

    refs = {r["id"]: r for r in json.loads(args.manifest.read_text(encoding="utf-8"))["references"]}
    headers = {r["id"]: r for r in json.loads(args.headers.read_text(encoding="utf-8"))["records"]}
    ref = refs[args.release]
    h = headers[args.release]
    rom = load_verified(ref, args.rom_dir)
    out = args.out_dir / args.release.lower()
    out.mkdir(parents=True, exist_ok=True)

    icon_palettes = []
    for pal_id in range(VALID_ICON_PALETTES):
        ptr, tag, pad = struct.unpack_from("<IHH", rom, h["monIconPalettes_rom_offset"] + pal_id * 8)
        off = ptr - ROM_BASE
        icon_palettes.append(rom[off:off+32])

    rows = []
    for i in range(SLOT_COUNT):
        name = safe_name(i)
        slot_dir = out / f"{i:03d}_{name}"
        slot_dir.mkdir(parents=True, exist_ok=True)

        front_ptr, front_size, front_tag = struct.unpack_from("<IHH", rom, h["monFrontPics_rom_offset"] + i*8)
        back_ptr, back_size, back_tag = struct.unpack_from("<IHH", rom, h["monBackPics_rom_offset"] + i*8)
        normal_ptr, normal_tag, _ = struct.unpack_from("<IHH", rom, h["monNormalPalettes_rom_offset"] + i*8)
        shiny_ptr, shiny_tag, _ = struct.unpack_from("<IHH", rom, h["monShinyPalettes_rom_offset"] + i*8)
        icon_ptr = struct.unpack_from("<I", rom, h["monIcons_rom_offset"] + i*4)[0]
        icon_pal_id = rom[h["monIconPaletteIds_rom_offset"] + i]
        if icon_pal_id >= VALID_ICON_PALETTES:
            raise ValueError(f"slot {i}: invalid used icon palette {icon_pal_id}")

        front, front_lz = gba_lz77(rom, front_ptr - ROM_BASE)
        back, back_lz = gba_lz77(rom, back_ptr - ROM_BASE)
        normal, normal_lz = gba_lz77(rom, normal_ptr - ROM_BASE)
        shiny, shiny_lz = gba_lz77(rom, shiny_ptr - ROM_BASE)
        icon = rom[icon_ptr - ROM_BASE:icon_ptr - ROM_BASE + 1024]

        render_mon(front, normal).save(slot_dir / "front_normal.png")
        render_mon(front, shiny).save(slot_dir / "front_shiny.png")
        render_mon(back, normal).save(slot_dir / "back_normal.png")
        render_mon(back, shiny).save(slot_dir / "back_shiny.png")
        render_4bpp(icon, 32, 64, bgr555_palette(icon_palettes[icon_pal_id])).save(slot_dir / "icon.png")

        (slot_dir / "front.4bpp.lz").write_bytes(front_lz)
        (slot_dir / "back.4bpp.lz").write_bytes(back_lz)
        (slot_dir / "normal.gbapal.lz").write_bytes(normal_lz)
        (slot_dir / "shiny.gbapal.lz").write_bytes(shiny_lz)
        (slot_dir / "icon.4bpp").write_bytes(icon)
        (slot_dir / "normal.gbapal").write_bytes(normal)
        (slot_dir / "shiny.gbapal").write_bytes(shiny)

        rows.append({
            "slot": i, "name": name,
            "front_size_field": front_size, "front_tag": front_tag,
            "back_size_field": back_size, "back_tag": back_tag,
            "normal_tag": normal_tag, "shiny_tag": shiny_tag,
            "icon_palette_id": icon_pal_id,
            "front_sha1": sha1(front), "back_sha1": sha1(back),
            "normal_palette_sha1": sha1(normal), "shiny_palette_sha1": sha1(shiny),
            "icon_sha1": sha1(icon),
        })

    with (out / "metadata.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
