#!/usr/bin/env python3
"""Extract the fixed Game Freak ROM metadata header at 0x100-0x203."""
from __future__ import annotations
import argparse, csv, hashlib, json, struct
from pathlib import Path

GF_HEADER_OFFSET = 0x100
GF_HEADER_END = 0x204
ROM_BASE = 0x08000000
ROM_END = 0x09000000

PTR_FIELDS_1 = [
    'monFrontPics','monBackPics','monNormalPalettes','monShinyPalettes','monIcons',
    'monIconPaletteIds','monIconPalettes','monSpeciesNames','moveNames','decorations'
]
U32_FIELDS_1 = [
    'flagsOffset','varsOffset','pokedexOffset','seen1Offset','seen2Offset','pokedexVar',
    'pokedexFlag','mysteryEventFlag','pokedexCount'
]
U8_FIELDS_1 = [
    'playerNameLength','trainerNameLength','pokemonNameLength1','pokemonNameLength2',
    'unk5','unk6','unk7','unk8','unk9','unk10','unk11','unk12','unk13','unk14',
    'unk15','unk16','unk17'
]
U32_FIELDS_2 = [
    'saveBlock2Size','saveBlock1Size','partyCountOffset','partyOffset','warpFlagsOffset',
    'trainerIdOffset','playerNameOffset','playerGenderOffset','frontierStatusOffset',
    'frontierStatusOffset2','externalEventFlagsOffset','externalEventDataOffset','unk18'
]
PTR_FIELDS_2 = [
    'speciesInfo','abilityNames','abilityDescriptions','items','moves','ballGfx','ballPalettes'
]
U32_FIELDS_3 = ['gcnLinkFlagsOffset','gameClearFlag','ribbonFlag']
U8_FIELDS_2 = ['bagCountItems','bagCountKeyItems','bagCountPokeballs','bagCountTMHMs','bagCountBerries','pcItemsCount']
U32_FIELDS_4 = ['pcItemsOffset','giftRibbonsOffset','enigmaBerryOffset','enigmaBerrySize']
PTR_FIELDS_3 = ['moveDescriptions']


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from('<I', buf, off)[0]


def parse_header(buf: bytes) -> dict:
    if len(buf) < GF_HEADER_END:
        raise ValueError('ROM too small')
    d: dict[str, object] = {
        'gf_header_offset': GF_HEADER_OFFSET,
        'gf_header_end': GF_HEADER_END,
    }
    off = GF_HEADER_OFFSET
    d['version'] = u32(buf, off); off += 4
    d['language'] = u32(buf, off); off += 4
    d['gameName'] = buf[off:off+32].split(b'\0', 1)[0].decode('ascii', 'replace'); off += 32
    for name in PTR_FIELDS_1:
        d[name] = u32(buf, off); off += 4
    for name in U32_FIELDS_1:
        d[name] = u32(buf, off); off += 4
    for name in U8_FIELDS_1:
        d[name] = buf[off]; off += 1
    off = (off + 3) & ~3
    for name in U32_FIELDS_2:
        d[name] = u32(buf, off); off += 4
    for name in PTR_FIELDS_2:
        d[name] = u32(buf, off); off += 4
    for name in U32_FIELDS_3:
        d[name] = u32(buf, off); off += 4
    for name in U8_FIELDS_2:
        d[name] = buf[off]; off += 1
    off = (off + 3) & ~3
    for name in U32_FIELDS_4:
        d[name] = u32(buf, off); off += 4
    for name in PTR_FIELDS_3:
        d[name] = u32(buf, off); off += 4
    d['unk20'] = u32(buf, off); off += 4
    if off != GF_HEADER_END:
        raise AssertionError(f'parser ended at 0x{off:X}, expected 0x{GF_HEADER_END:X}')
    for name in PTR_FIELDS_1 + PTR_FIELDS_2 + PTR_FIELDS_3:
        value = int(d[name])
        d[name + '_rom_offset'] = value - ROM_BASE if ROM_BASE <= value < ROM_END else None
    return d


def choose_canonical(group: list[tuple[dict, Path, bytes]]) -> tuple[dict, Path, bytes]:
    for item in group:
        if item[0]['id'] == 'ENG_USA_EUR':
            return item
    return group[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('rom_dir', type=Path)
    ap.add_argument('--manifest', type=Path, default=Path('manifests/roms.json'))
    ap.add_argument('--json-out', type=Path, default=Path('analysis/gf_rom_headers.json'))
    ap.add_argument('--csv-out', type=Path, default=Path('analysis/gf_rom_headers.csv'))
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    groups: dict[str, list[tuple[dict, Path, bytes]]] = {}
    for ref in manifest['references']:
        path = args.rom_dir / ref['source_filename']
        if not path.exists():
            raise FileNotFoundError(path)
        buf = path.read_bytes()
        sha1 = hashlib.sha1(buf).hexdigest()
        if sha1 != ref['sha1']:
            raise ValueError(f"SHA-1 mismatch for {ref['id']}: {sha1}")
        groups.setdefault(sha1, []).append((ref, path, buf))

    rows = []
    for sha1, group in groups.items():
        ref, path, buf = choose_canonical(group)
        aliases = [x[0]['id'] for x in group if x[0]['id'] != ref['id']]
        rows.append({
            'id': ref['id'],
            'aliases': aliases,
            'source_filename': ref['source_filename'],
            'sha1': sha1,
            **parse_header(buf),
        })

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps({'schema_version': 1, 'records': rows}, indent=2) + '\n', encoding='utf-8')
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with args.csv_out.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row['aliases'] = ';'.join(row['aliases'])
            writer.writerow(row)

if __name__ == '__main__':
    main()
