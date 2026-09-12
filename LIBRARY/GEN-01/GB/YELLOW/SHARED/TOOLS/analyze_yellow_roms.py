#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, hashlib, json, zlib

CART = {0x13: 'MBC3+RAM+BATTERY', 0x1B: 'MBC5+RAM+BATTERY'}

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def parse_header(data):
    hchk = 0
    for b in data[0x134:0x14D]:
        hchk = (hchk - b - 1) & 0xFF
    gcalc = (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF
    gstored = int.from_bytes(data[0x14E:0x150], 'big')
    cgb = data[0x143]
    title_raw = data[0x134:0x143] if cgb in (0x80, 0xC0) else data[0x134:0x144]
    return {
        'title': title_raw.split(b'\0')[0].decode('ascii', 'replace'),
        'cgb_flag': f'0x{cgb:02X}',
        'sgb_flag': f'0x{data[0x146]:02X}',
        'cartridge_type': f'0x{data[0x147]:02X} {CART.get(data[0x147], "UNKNOWN")}',
        'rom_size_code': f'0x{data[0x148]:02X}',
        'ram_size_code': f'0x{data[0x149]:02X}',
        'destination_code': f'0x{data[0x14A]:02X}',
        'version': data[0x14C],
        'header_checksum_ok': hchk == data[0x14D],
        'global_checksum_ok': gcalc == gstored,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('directory', type=Path)
    ap.add_argument('--out', type=Path, default=Path('yellow-audit'))
    args = ap.parse_args()
    files = sorted(list(args.directory.glob('*.gb')) + list(args.directory.glob('*.gbc')))
    args.out.mkdir(parents=True, exist_ok=True)

    rows = []
    bank_hashes = {}
    for p in files:
        data = p.read_bytes()
        rows.append({
            'file': p.name,
            'size': len(data),
            'banks_16KiB': len(data) // 0x4000,
            'crc32': f'{zlib.crc32(data) & 0xffffffff:08x}',
            'md5': hashlib.md5(data).hexdigest(),
            'sha1': sha1(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            **parse_header(data),
        })
        bank_hashes[p.name] = [sha1(data[i:i+0x4000]) for i in range(0, len(data), 0x4000)]

    with (args.out / 'rom_inventory.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    (args.out / 'bank_sha1.json').write_text(json.dumps(bank_hashes, indent=2), encoding='utf-8')

    groups = {}
    for row in rows:
        groups.setdefault(row['sha1'], []).append(row['file'])
    (args.out / 'duplicate_groups.json').write_text(json.dumps(groups, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
