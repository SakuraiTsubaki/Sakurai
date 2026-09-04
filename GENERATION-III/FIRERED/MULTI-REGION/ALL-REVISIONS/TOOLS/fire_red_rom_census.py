#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, os, struct, zlib
from pathlib import Path
from itertools import combinations

NINTENDO_LOGO = bytes.fromhex('''
24 FF AE 51 69 9A A2 21 3D 84 82 0A 84 E4 09 AD
11 24 8B 98 C0 81 7F 21 A3 52 BE 19 93 09 CE 20
10 46 4A 4A F8 27 31 EC 58 C7 E8 33 82 E3 CE BF
85 F4 DF 94 CE 4B 09 C1 94 56 8A C0 13 72 A7 FC
9F 84 4D 73 A3 CA 9A 61 58 97 A3 27 FC 03 98 76
23 1D C7 61 03 04 AE 56 BF 38 84 00 40 A7 0E FD
FF 52 FE 03 6F 95 30 F1 97 FB C0 85 60 D6 80 25
A9 63 BE 03 01 4E 38 E2 F9 A2 34 FF BB 3E 03 44
78 00 90 CB 88 11 3A 94 65 C0 7C 63 87 F0 3C AF
D6 25 E4 8B 38 0A AC 72 21 D4 F8 07
''')

def digest(data: bytes, algo: str) -> str:
    h = hashlib.new(algo); h.update(data); return h.hexdigest()

def gba_header(data: bytes) -> dict:
    if len(data) < 0xC0:
        raise ValueError('File too small for GBA header')
    title_raw = data[0xA0:0xAC]
    game_code = data[0xAC:0xB0].decode('ascii', 'replace').rstrip('\x00')
    maker = data[0xB0:0xB2].decode('ascii', 'replace').rstrip('\x00')
    fixed = data[0xB2]
    unit = data[0xB3]
    device = data[0xB4]
    sw = data[0xBC]
    chk = data[0xBD]
    calc = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
    return {
        'title': title_raw.rstrip(b'\x00').decode('ascii', 'replace'),
        'game_code': game_code,
        'maker_code': maker,
        'fixed_value': f'0x{fixed:02X}',
        'unit_code': unit,
        'device_type': device,
        'software_version': sw,
        'header_checksum_stored': f'0x{chk:02X}',
        'header_checksum_calculated': f'0x{calc:02X}',
        'header_checksum_valid': chk == calc,
        'nintendo_logo_valid': data[0x04:0xA0] == NINTENDO_LOGO,
    }

def region_from_code(code: str) -> str:
    return {
        'J':'Japan', 'E':'USA/English', 'D':'Germany', 'F':'France',
        'I':'Italy', 'S':'Spain', 'P':'Europe', 'U':'Australia'
    }.get(code[-1:] if code else '', 'Unknown')

def scan_file(path: Path) -> tuple[dict, list[str]]:
    data = path.read_bytes()
    hdr = gba_header(data)
    bank_size = 0x10000
    bank_hashes = [hashlib.sha256(data[i:i+bank_size]).hexdigest() for i in range(0, len(data), bank_size)]
    row = {
        'filename': path.name,
        'size_bytes': len(data),
        'size_mib': round(len(data)/(1024*1024), 3),
        'crc32': f'{zlib.crc32(data) & 0xffffffff:08x}',
        'md5': digest(data, 'md5'),
        'sha1': digest(data, 'sha1'),
        'sha256': digest(data, 'sha256'),
        **hdr,
        'region_inferred': region_from_code(hdr['game_code']),
        'banks_64k': (len(data)+bank_size-1)//bank_size,
    }
    return row, bank_hashes

def diff_pair(a: Path, b: Path, ah: list[str], bh: list[str]) -> dict:
    da = a.read_bytes(); db = b.read_bytes()
    n = min(len(da), len(db))
    diff_count = sum(x != y for x,y in zip(da[:n], db[:n])) + abs(len(da)-len(db))
    first = None; last = None
    for i,(x,y) in enumerate(zip(da[:n], db[:n])):
        if x != y:
            first = i; break
    if diff_count:
        for i in range(n-1, -1, -1):
            if da[i] != db[i]:
                last = i; break
        if len(da) != len(db):
            last = max(len(da), len(db)) - 1
    changed_banks = [i for i,(x,y) in enumerate(zip(ah,bh)) if x != y]
    if len(ah) != len(bh):
        changed_banks.extend(range(min(len(ah),len(bh)), max(len(ah),len(bh))))
    return {
        'a': a.name, 'b': b.name,
        'byte_differences': diff_count,
        'difference_percent': round((diff_count/max(len(da),len(db)))*100, 6) if max(len(da),len(db)) else 0,
        'first_difference_offset': None if first is None else f'0x{first:08X}',
        'last_difference_offset': None if last is None else f'0x{last:08X}',
        'changed_64k_banks_count': len(changed_banks),
        'changed_64k_banks': changed_banks,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom_dir', nargs='?', default='/mnt/data')
    ap.add_argument('-o','--out', default='/mnt/data/fire_red_census')
    args=ap.parse_args()
    roms=sorted(Path(args.rom_dir).glob('*.gba'))
    out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rows=[]; bankmap={}
    for p in roms:
        row,bh=scan_file(p); rows.append(row); bankmap[p.name]=bh
    cols=list(rows[0].keys()) if rows else []
    with (out/'rom_census.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
    (out/'rom_census.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'bank_sha256.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['filename','bank_index','offset_start','offset_end','sha256'])
        for name,banks in bankmap.items():
            for i,h in enumerate(banks): w.writerow([name,i,f'0x{i*0x10000:08X}',f'0x{(i+1)*0x10000-1:08X}',h])
    pairs=[]
    pmap={p.name:p for p in roms}
    for a,b in combinations(roms,2):
        pairs.append(diff_pair(a,b,bankmap[a.name],bankmap[b.name]))
    (out/'pairwise_diff_summary.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'pairwise_diff_summary.csv').open('w',newline='',encoding='utf-8') as f:
        cols2=['a','b','byte_differences','difference_percent','first_difference_offset','last_difference_offset','changed_64k_banks_count','changed_64k_banks']
        w=csv.DictWriter(f,fieldnames=cols2); w.writeheader()
        for r in pairs:
            rr=dict(r); rr['changed_64k_banks']=' '.join(f'{x:02X}' for x in r['changed_64k_banks']); w.writerow(rr)
    targets=[
        ('Pocket Monsters - Fire Red (Japan).gba','Pocket Monsters - Fire Red (Japan) (Rev 1).gba'),
        ('Pokemon - Fire Red Version (USA).gba','Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba')
    ]
    trows=[]
    for a,b in targets:
        if a in pmap and b in pmap:
            trows.append(diff_pair(pmap[a],pmap[b],bankmap[a],bankmap[b]))
    lines=['# Pokémon FireRed ROM Census','',f'- ROM count: **{len(rows)}**',f'- All ROMs are **{rows[0]["size_mib"]:.0f} MiB**' if rows else '', '- Original ROM binaries are intentionally excluded from GitHub.', '', '## Identity and header validation','', '| File | Game code | Region | Rev | CRC32 | SHA-1 | Header | Logo |','|---|---|---|---:|---|---|---|---|']
    for r in rows:
        lines.append(f'| {r["filename"]} | `{r["game_code"]}` | {r["region_inferred"]} | {r["software_version"]} | `{r["crc32"]}` | `{r["sha1"]}` | {"OK" if r["header_checksum_valid"] else "FAIL"} | {"OK" if r["nintendo_logo_valid"] else "FAIL"} |')
    lines += ['', '## Revision-pair binary deltas','']
    for r in trows:
        lines += [f'### {r["a"]} → {r["b"]}', f'- Differing bytes: **{r["byte_differences"]:,}** ({r["difference_percent"]:.6f}%)', f'- First/last difference: `{r["first_difference_offset"]}` / `{r["last_difference_offset"]}`', f'- Changed 64 KiB banks: **{r["changed_64k_banks_count"]} / 256**', f'- Bank indices: `{", ".join(f"{x:02X}" for x in r["changed_64k_banks"])}`', '']
    lines += ['## Generated files','', '- `rom_census.csv` / `rom_census.json`: ROM identity ledger', '- `bank_sha256.csv`: per-64 KiB bank hashes', '- `pairwise_diff_summary.csv` / `.json`: all 28 pairwise binary-difference summaries', '- `fire_red_rom_census.py`: reproducible census tool', '']
    (out/'ROM_CENSUS.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'rows':rows,'target_pairs':trows},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
