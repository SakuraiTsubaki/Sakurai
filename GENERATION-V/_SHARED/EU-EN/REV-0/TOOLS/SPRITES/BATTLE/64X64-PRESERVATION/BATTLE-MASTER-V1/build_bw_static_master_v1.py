#!/usr/bin/env python3
"""Build the Generation V BW ROM-primary 64x64 static battle-sprite master.

Input: project Pokémon Black/White .nds ROM(s).
Source archive: /a/0/0/4.
Static source members in each 20-member Pokémon/form block:
  +0 male front, +1 female front, +9 male back, +10 female back
Palettes:
  +18 normal, +19 shiny

The dedicated static NCGR canvas is converted directly to 64x64 with the shared
preservation-v2 palette-index kernel.  Multipart animated parts are intentionally
not frozen into the static master; they remain a separate preservation track.

No ROM bytes are written to the repository output.  Output consists of PNG
assets, manifests, hashes, atlas previews, and validation records only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import pathlib
import struct
import sys
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

import preservation_v2_generalized as pv2
import scan_bw_animation_union_bbox as core

POKEGRA_PATH = 'a/0/0/4'
STANDARD_BLOCKS = 712
BLOCK_SIZE = 20
STATIC_ROLES = {
    ('front', 'male'): 0,
    ('front', 'female'): 1,
    ('back', 'male'): 9,
    ('back', 'female'): 10,
}
PALETTES = {'normal': 18, 'shiny': 19}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def nds_files(data: bytes) -> dict[str, bytes]:
    """Return path -> raw file bytes for a Nintendo DS filesystem."""
    fnt_off, fnt_size, fat_off, fat_size = struct.unpack_from('<IIII', data, 0x40)
    fnt = data[fnt_off:fnt_off + fnt_size]
    fat = data[fat_off:fat_off + fat_size]
    _sub0, _first0, dir_count = struct.unpack_from('<IHH', fnt, 0)
    dirs = [struct.unpack_from('<IHH', fnt, i * 8) for i in range(dir_count)]
    names: dict[str, int] = {}

    def walk(did: int, prefix: str) -> None:
        sub, first, _parent = dirs[did - 0xF000]
        p = sub
        fid = first
        while True:
            n = fnt[p]
            p += 1
            if n == 0:
                break
            isdir = n & 0x80
            ln = n & 0x7F
            name = fnt[p:p + ln].decode('ascii', errors='replace')
            p += ln
            if isdir:
                child = struct.unpack_from('<H', fnt, p)[0]
                p += 2
                walk(child, prefix + name + '/')
            else:
                names[prefix + name] = fid
                fid += 1

    walk(0xF000, '')
    out = {}
    for name, fid in names.items():
        s, e = struct.unpack_from('<II', fat, fid * 8)
        out[name] = data[s:e]
    return out


class NarcBytes:
    def __init__(self, data: bytes):
        if data[:4] != b'NARC':
            raise ValueError('not a NARC archive')
        self.data = data
        pos = 0x10
        fat_size = struct.unpack_from('<I', data, pos + 4)[0]
        count = struct.unpack_from('<H', data, pos + 8)[0]
        self.fat = [struct.unpack_from('<II', data, pos + 12 + i * 8)
                    for i in range(count)]
        pos2 = pos + fat_size
        pos3 = pos2 + struct.unpack_from('<I', data, pos2 + 4)[0]
        self.gmif_base = pos3 + 8

    def __len__(self):
        return len(self.fat)

    def raw_member(self, i: int) -> bytes:
        s, e = self.fat[i]
        return self.data[self.gmif_base + s:self.gmif_base + e]

    def member(self, i: int) -> bytes:
        return core.lz11(self.raw_member(i))


def parse_nclr(d: bytes) -> list[tuple[int, int, int, int]]:
    _mg, _size, _bit, _unk, _pad, dsize, _doff = struct.unpack_from('<4sIHHIII', d, 16)
    raw = d[40:40 + dsize]
    if len(raw) < 32:
        raise ValueError('NCLR contains fewer than 16 colors')
    cols = []
    for i in range(16):
        c = struct.unpack_from('<H', raw, i * 2)[0]
        r, g, b = c & 31, (c >> 5) & 31, (c >> 10) & 31
        cv = lambda q: (q << 3) | (q >> 2)
        cols.append((cv(r), cv(g), cv(b), 0 if i == 0 else 255))
    return cols


def decode_static_ncgr(d: bytes) -> np.ndarray:
    g = core.parse_ncgr(d)
    w, h = int(g['w']), int(g['h'])
    pix = np.asarray(g['pix'], dtype=np.uint8)
    if pix.size != w * h:
        raise ValueError(f'NCGR pixel count mismatch {pix.size} != {w}x{h}')
    return pix.reshape(h, w)


def is_empty_indices(idx: np.ndarray) -> bool:
    return not bool(np.any(idx != 0))


def rgba_sha(im: Image.Image) -> str:
    return hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()


def save_unique_asset(im: Image.Image, asset_dir: pathlib.Path,
                      by_sha: dict[str, str]) -> tuple[str, str, bool]:
    h = rgba_sha(im)
    if h in by_sha:
        return h, by_sha[h], False
    rel = f'assets/{h[:24]}.png'
    p = asset_dir.parent / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, optimize=True)
    by_sha[h] = rel
    return h, rel, True


def make_atlas(rows: list[dict], out: pathlib.Path) -> None:
    """Build front/male/normal National Dex 001..649 contact sheet."""
    selected = {int(r['block']): r for r in rows
                if r['side'] == 'front' and r['gender'] == 'male'
                and r['palette'] == 'normal' and 1 <= int(r['block']) <= 649}
    cell = 72
    cols = 20
    count = 649
    rows_n = (count + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * cell, rows_n * cell), (255, 255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    root = out
    for dex in range(1, 650):
        r = selected.get(dex)
        if not r:
            continue
        im = Image.open(root / r['asset_path']).convert('RGBA')
        x = ((dex - 1) % cols) * cell + 4
        y = ((dex - 1) // cols) * cell + 2
        sheet.alpha_composite(im, (x, y))
        draw.text((x, y + 64), f'{dex:03}', fill=(0, 0, 0, 255))
    sheet.save(out / 'ATLAS_front_male_normal_001_649.png', optimize=True)


def build(rom_path: pathlib.Path, verify_rom: pathlib.Path | None,
          out: pathlib.Path, blocks: int) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    assets = out / 'assets'
    assets.mkdir(exist_ok=True)

    rom_data = rom_path.read_bytes()
    files = nds_files(rom_data)
    if POKEGRA_PATH not in files:
        raise KeyError(f'{POKEGRA_PATH} not found in {rom_path}')
    narc_blob = files[POKEGRA_PATH]
    narc = NarcBytes(narc_blob)

    verification = None
    if verify_rom:
        vdata = verify_rom.read_bytes()
        vfiles = nds_files(vdata)
        vnarc = vfiles[POKEGRA_PATH]
        verification = {
            'rom': str(verify_rom),
            'rom_sha256': sha256(vdata),
            'pokegra_sha256': sha256(vnarc),
            'pokegra_identical': vnarc == narc_blob,
        }

    if len(narc) < blocks * BLOCK_SIZE:
        raise ValueError(f'NARC has {len(narc)} members, cannot cover {blocks} blocks')

    source_cache: dict[tuple[int, str, str], np.ndarray] = {}
    source_member: dict[tuple[int, str, str], int] = {}
    source_status: dict[tuple[int, str, str], str] = {}
    errors = []

    # Decode canonical static slots first. Female empty slots become explicit
    # logical aliases to male, never invisible omissions.
    for block in range(blocks):
        base = block * BLOCK_SIZE
        for side in ('front', 'back'):
            male_rel = STATIC_ROLES[(side, 'male')]
            female_rel = STATIC_ROLES[(side, 'female')]
            try:
                male = decode_static_ncgr(narc.member(base + male_rel))
                source_cache[(block, side, 'male')] = male
                source_member[(block, side, 'male')] = base + male_rel
                source_status[(block, side, 'male')] = 'rom_static'
            except Exception as e:
                errors.append({'block': block, 'side': side, 'gender': 'male', 'error': repr(e)})
                continue
            try:
                female = decode_static_ncgr(narc.member(base + female_rel))
                source_member[(block, side, 'female')] = base + female_rel
                if is_empty_indices(female):
                    source_cache[(block, side, 'female')] = male
                    source_status[(block, side, 'female')] = 'empty_rom_slot_alias_to_male'
                else:
                    source_cache[(block, side, 'female')] = female
                    source_status[(block, side, 'female')] = 'rom_static_gender_difference'
            except Exception as e:
                source_cache[(block, side, 'female')] = male
                source_member[(block, side, 'female')] = base + female_rel
                source_status[(block, side, 'female')] = 'decode_error_alias_to_male'
                errors.append({'block': block, 'side': side, 'gender': 'female', 'error': repr(e)})

    unique: dict[str, str] = {}
    manifest: list[dict] = []
    source_index_cache: dict[tuple[int, str, str], np.ndarray] = {}

    for block in range(blocks):
        base = block * BLOCK_SIZE
        try:
            palettes = {
                pname: parse_nclr(narc.member(base + rel))
                for pname, rel in PALETTES.items()
            }
        except Exception as e:
            errors.append({'block': block, 'palette_error': repr(e)})
            continue

        for side in ('front', 'back'):
            for gender in ('male', 'female'):
                key = (block, side, gender)
                if key not in source_cache:
                    continue
                src = source_cache[key]
                try:
                    idx64 = pv2.resize_static_canvas(src)
                    pv2.validate_source_index_only(src, idx64)
                except Exception as e:
                    errors.append({'block': block, 'side': side, 'gender': gender,
                                   'conversion_error': repr(e)})
                    continue
                source_index_cache[key] = idx64
                src_used = sorted(map(int, np.unique(src[src != 0])))
                out_used = sorted(map(int, np.unique(idx64[idx64 != 0])))
                for pname, pal in palettes.items():
                    im = pv2.render_indices(idx64, pal)
                    ah, apath, created = save_unique_asset(im, assets, unique)
                    rec = {
                        'block': block,
                        'dex_if_standard': block if 1 <= block <= 649 else '',
                        'side': side,
                        'gender': gender,
                        'palette': pname,
                        'static_member': source_member[key],
                        'palette_member': base + PALETTES[pname],
                        'source_status': source_status[key],
                        'source_canvas': f'{src.shape[1]}x{src.shape[0]}',
                        'source_nonzero_indices': ' '.join(map(str, src_used)),
                        'output_nonzero_indices': ' '.join(map(str, out_used)),
                        'asset_sha256_rgba': ah,
                        'asset_path': apath,
                        'dedup_new_asset': int(created),
                    }
                    rec.update({f'out_{k}': v for k, v in pv2.describe(idx64).items()})
                    manifest.append(rec)

    # Inventory every member after the standard block region rather than dropping it.
    tail = []
    for i in range(blocks * BLOCK_SIZE, len(narc)):
        raw = narc.raw_member(i)
        dec = narc.member(i)
        tail.append({
            'member': i,
            'raw_size': len(raw),
            'decoded_size': len(dec),
            'raw_sha256': sha256(raw),
            'decoded_sha256': sha256(dec),
            'decoded_magic': dec[:4].decode('latin1', errors='replace'),
        })

    fieldnames = sorted({k for r in manifest for k in r})
    with (out / 'manifest.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(manifest)
    (out / 'tail_members.json').write_text(json.dumps(tail, indent=2), encoding='utf-8')
    (out / 'errors.json').write_text(json.dumps(errors, indent=2), encoding='utf-8')

    summary = {
        'source_rom': str(rom_path),
        'source_rom_sha256': sha256(rom_data),
        'pokegra_path': POKEGRA_PATH,
        'pokegra_size': len(narc_blob),
        'pokegra_sha256': sha256(narc_blob),
        'pokegra_members': len(narc),
        'standard_blocks_processed': blocks,
        'logical_render_records': len(manifest),
        'unique_rgba_assets': len(unique),
        'errors': len(errors),
        'tail_members': len(tail),
        'verify_rom': verification,
        'conversion': 'dedicated static NCGR full canvas -> 64x64 preservation-v2 index overlap',
        'normal_palette_rel': 18,
        'shiny_palette_rel': 19,
    }
    (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    make_atlas(manifest, out)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', type=pathlib.Path, required=True)
    ap.add_argument('--verify-rom', type=pathlib.Path)
    ap.add_argument('--out', type=pathlib.Path, required=True)
    ap.add_argument('--blocks', type=int, default=STANDARD_BLOCKS)
    args = ap.parse_args()
    summary = build(args.rom, args.verify_rom, args.out, args.blocks)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
