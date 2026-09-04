#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, hashlib, itertools, json, math

LANG_BY_CODE = {
    'BPGJ': 'Japanese',
    'BPGE': 'English',
    'BPGD': 'German',
    'BPGF': 'French',
    'BPGI': 'Italian',
    'BPGS': 'Spanish',
}


def parse_rom(path: Path):
    b = path.read_bytes()
    calc = (-sum(b[0xA0:0xBD]) - 0x19) & 0xFF
    sigs = []
    for pat in (b'FLASH1M_V', b'FLASH512_V', b'SRAM_V', b'EEPROM_V'):
        i = b.find(pat)
        if i >= 0:
            sigs.append(f"{b[i:i+20].split(bytes([0]))[0].decode('ascii','replace')}@0x{i:X}")
    return b, {
        'file': path.name,
        'size': len(b),
        'sha256': hashlib.sha256(b).hexdigest(),
        'sha1': hashlib.sha1(b).hexdigest(),
        'md5': hashlib.md5(b).hexdigest(),
        'title': b[0xA0:0xAC].split(bytes([0]))[0].decode('ascii','replace'),
        'game_code': b[0xAC:0xB0].decode('ascii','replace'),
        'maker_code': b[0xB0:0xB2].decode('ascii','replace'),
        'fixed_96': b[0xB2],
        'unit_code': b[0xB3],
        'device_type': b[0xB4],
        'software_version': b[0xBC],
        'header_checksum': b[0xBD],
        'header_checksum_calc': calc,
        'header_checksum_ok': b[0xBD] == calc,
        'save_signatures': '; '.join(sigs),
    }


def main():
    ap = argparse.ArgumentParser(description='Census Pokémon LeafGreen GBA ROM headers and pairwise byte differences.')
    ap.add_argument('rom_dir', type=Path)
    ap.add_argument('out_dir', type=Path)
    args = ap.parse_args()
    files = sorted(args.rom_dir.glob('*.gba'))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows, blobs = [], {}
    for p in files:
        b, row = parse_rom(p)
        blobs[p.name] = b
        rows.append(row)
    if not rows:
        raise SystemExit('No .gba files found')

    with (args.out_dir / 'rom_manifest.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    (args.out_dir / 'rom_manifest.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')

    pairs = []
    for (n1,b1),(n2,b2) in itertools.combinations(blobs.items(),2):
        if len(b1) != len(b2):
            continue
        diff = sum(x != y for x,y in zip(b1,b2))
        block = 0x10000
        pairs.append({
            'a': n1, 'b': n2,
            'different_bytes': diff,
            'different_pct': diff / len(b1) * 100,
            'same_64k_blocks': sum(b1[i:i+block] == b2[i:i+block] for i in range(0,len(b1),block)),
            'total_64k_blocks': math.ceil(len(b1)/block),
            'identical_prefix_bytes': next((i for i,(x,y) in enumerate(zip(b1,b2)) if x != y), len(b1)),
            'identical_suffix_bytes': next((i for i,(x,y) in enumerate(zip(reversed(b1),reversed(b2))) if x != y), len(b1)),
        })
    with (args.out_dir / 'pairwise_diff.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=pairs[0].keys())
        w.writeheader(); w.writerows(pairs)

    padding = []
    for name, b in blobs.items():
        val = b[-1]
        i = len(b) - 1
        while i >= 0 and b[i] == val:
            i -= 1
        padding.append({'file': name, 'trailing_byte': f'0x{val:02X}', 'run_start': i + 1, 'run_length': len(b) - 1 - i})
    with (args.out_dir / 'terminal_padding.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=padding[0].keys())
        w.writeheader(); w.writerows(padding)

if __name__ == '__main__':
    main()
