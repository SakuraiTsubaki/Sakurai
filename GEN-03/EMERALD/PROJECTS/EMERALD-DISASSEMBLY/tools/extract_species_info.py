#!/usr/bin/env python3
"""Extract the shared Emerald SpeciesInfo table from verified reference ROMs."""
from __future__ import annotations
import argparse, csv, hashlib, json, struct
from pathlib import Path

RECORD_COUNT = 412
RECORD_STRIDE = 0x1C
SEMANTIC_SIZE = 0x1A
SEGMENTS = [(0, 102), (103, 205), (206, 308), (309, 411)]


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def parse_record(index: int, raw: bytes) -> dict[str, object]:
    if len(raw) != RECORD_STRIDE:
        raise ValueError(f'bad SpeciesInfo record size at {index}: {len(raw)}')
    ev = struct.unpack_from('<H', raw, 0x0A)[0]
    return {
        'internal_id': index,
        'base_hp': raw[0x00],
        'base_attack': raw[0x01],
        'base_defense': raw[0x02],
        'base_speed': raw[0x03],
        'base_sp_attack': raw[0x04],
        'base_sp_defense': raw[0x05],
        'bst': sum(raw[0x00:0x06]),
        'type1': raw[0x06],
        'type2': raw[0x07],
        'catch_rate': raw[0x08],
        'exp_yield': raw[0x09],
        'ev_hp': (ev >> 0) & 3,
        'ev_attack': (ev >> 2) & 3,
        'ev_defense': (ev >> 4) & 3,
        'ev_speed': (ev >> 6) & 3,
        'ev_sp_attack': (ev >> 8) & 3,
        'ev_sp_defense': (ev >> 10) & 3,
        'ev_reserved': (ev >> 12) & 0xF,
        'item_common': struct.unpack_from('<H', raw, 0x0C)[0],
        'item_rare': struct.unpack_from('<H', raw, 0x0E)[0],
        'gender_ratio': raw[0x10],
        'egg_cycles': raw[0x11],
        'base_friendship': raw[0x12],
        'growth_rate': raw[0x13],
        'egg_group1': raw[0x14],
        'egg_group2': raw[0x15],
        'ability1': raw[0x16],
        'ability2': raw[0x17],
        'safari_zone_flee_rate': raw[0x18],
        'body_color': raw[0x19] & 0x7F,
        'no_flip': (raw[0x19] >> 7) & 1,
        'padding_hex': raw[0x1A:0x1C].hex().upper(),
        'raw_hex': raw.hex().upper(),
    }


def load_verified_rom(ref: dict, rom_dir: Path) -> bytes:
    path = rom_dir / ref['source_filename']
    data = path.read_bytes()
    got = sha1(data)
    if got != ref['sha1']:
        raise ValueError(f"SHA-1 mismatch for {ref['id']}: {got}")
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('rom_dir', type=Path)
    ap.add_argument('--manifest', type=Path, default=Path('manifests/roms.json'))
    ap.add_argument('--headers', type=Path, default=Path('analysis/gf_rom_headers.json'))
    ap.add_argument('--out-dir', type=Path, default=Path('data/species_info'))
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    refs = {r['id']: r for r in manifest['references']}
    headers = json.loads(args.headers.read_text(encoding='utf-8'))['records']
    args.out_dir.mkdir(parents=True, exist_ok=True)

    releases = []
    shared_table = None
    for header in headers:
        rid = header['id']
        rom = load_verified_rom(refs[rid], args.rom_dir)
        root = int(header['speciesInfo_rom_offset'])
        table = rom[root:root + RECORD_COUNT * RECORD_STRIDE]
        if len(table) != RECORD_COUNT * RECORD_STRIDE:
            raise ValueError(f'{rid}: truncated SpeciesInfo table')
        if shared_table is None:
            shared_table = table
        elif table != shared_table:
            raise ValueError(f'{rid}: SpeciesInfo differs from the canonical table')
        releases.append({
            'release': rid,
            'root_rom_offset': f'0x{root:08X}',
            'byte_length': len(table),
            'sha1': sha1(table),
        })

    assert shared_table is not None
    rows = [parse_record(i, shared_table[i * RECORD_STRIDE:(i + 1) * RECORD_STRIDE]) for i in range(RECORD_COUNT)]
    if any(row['ev_reserved'] != 0 for row in rows):
        raise ValueError('nonzero reserved EV-yield bits found')
    if any(row['padding_hex'] != '0000' for row in rows):
        raise ValueError('nonzero SpeciesInfo record padding found')

    for start, end in SEGMENTS:
        with (args.out_dir / f'species_info_{start:03d}_{end:03d}.csv').open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows[start:end + 1])

    meta = {
        'schema_version': 1,
        'record_count': RECORD_COUNT,
        'record_stride': RECORD_STRIDE,
        'semantic_size': SEMANTIC_SIZE,
        'byte_length': len(shared_table),
        'shared_table_sha1': sha1(shared_table),
        'all_unique_releases_byte_identical': True,
        'segments': [f'{a:03d}-{b:03d}' for a, b in SEGMENTS],
        'release_roots': releases,
    }
    (args.out_dir / 'manifest.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
