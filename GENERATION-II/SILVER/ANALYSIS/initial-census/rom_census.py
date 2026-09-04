#!/usr/bin/env python3
"""Forensic census for Pokémon Silver multi-region Game Boy Color ROMs.

This tool never modifies ROMs. It emits text-only manifests suitable for version control.
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv, hashlib, itertools, json

CART_TYPES = {
    0x00:'ROM ONLY',0x01:'MBC1',0x02:'MBC1+RAM',0x03:'MBC1+RAM+BATTERY',
    0x05:'MBC2',0x06:'MBC2+BATTERY',0x08:'ROM+RAM',0x09:'ROM+RAM+BATTERY',
    0x0F:'MBC3+TIMER+BATTERY',0x10:'MBC3+TIMER+RAM+BATTERY',0x11:'MBC3',
    0x12:'MBC3+RAM',0x13:'MBC3+RAM+BATTERY',0x19:'MBC5',0x1A:'MBC5+RAM',
    0x1B:'MBC5+RAM+BATTERY',0x1C:'MBC5+RUMBLE',0x1D:'MBC5+RUMBLE+RAM',
    0x1E:'MBC5+RUMBLE+RAM+BATTERY',
}
ROM_SIZES={0x00:32768,0x01:65536,0x02:131072,0x03:262144,0x04:524288,
           0x05:1048576,0x06:2097152,0x07:4194304,0x08:8388608,
           0x52:1179648,0x53:1310720,0x54:1572864}
RAM_SIZES={0x00:0,0x01:2048,0x02:8192,0x03:32768,0x04:131072,0x05:65536}
NINTENDO_LOGO=bytes.fromhex('CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D 00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99 BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E')

def header_checksum(d: bytes) -> int:
    x=0
    for i in range(0x134,0x14D):
        x=(x-d[i]-1)&0xFF
    return x

def global_checksum(d: bytes) -> int:
    return (sum(d[:0x14E])+sum(d[0x150:]))&0xFFFF

def census(path: Path) -> dict:
    d=path.read_bytes()
    return {
        'file': path.name,
        'bytes': len(d),
        'md5': hashlib.md5(d).hexdigest(),
        'sha1': hashlib.sha1(d).hexdigest(),
        'sha256': hashlib.sha256(d).hexdigest(),
        'entry_point': d[0x100:0x104].hex().upper(),
        'nintendo_logo_valid': d[0x104:0x134] == NINTENDO_LOGO,
        'title': d[0x134:0x143].rstrip(b'\0').decode('ascii','replace'),
        'title_raw': d[0x134:0x144].hex().upper(),
        'cgb_flag': f'0x{d[0x143]:02X}',
        'new_licensee_raw': d[0x144:0x146].decode('ascii','replace'),
        'sgb_flag': f'0x{d[0x146]:02X}',
        'cartridge_type_code': f'0x{d[0x147]:02X}',
        'cartridge_type': CART_TYPES.get(d[0x147], 'UNKNOWN'),
        'rom_size_code': f'0x{d[0x148]:02X}',
        'declared_rom_bytes': ROM_SIZES.get(d[0x148]),
        'ram_size_code': f'0x{d[0x149]:02X}',
        'declared_ram_bytes': RAM_SIZES.get(d[0x149]),
        'destination_code': f'0x{d[0x14A]:02X}',
        'old_licensee_code': f'0x{d[0x14B]:02X}',
        'version': d[0x14C],
        'header_checksum_stored': f'0x{d[0x14D]:02X}',
        'header_checksum_calc': f'0x{header_checksum(d):02X}',
        'header_checksum_valid': header_checksum(d)==d[0x14D],
        'global_checksum_stored': f'0x{int.from_bytes(d[0x14E:0x150],"big"):04X}',
        'global_checksum_calc': f'0x{global_checksum(d):04X}',
        'global_checksum_valid': global_checksum(d)==int.from_bytes(d[0x14E:0x150],'big'),
        'bank_count': len(d)//0x4000,
    }

def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('rom_dir', type=Path)
    ap.add_argument('-o','--out', type=Path, default=Path('silver_analysis'))
    args=ap.parse_args()
    paths=sorted(args.rom_dir.glob('*.gbc'))
    if not paths: raise SystemExit('No .gbc files found')
    args.out.mkdir(parents=True, exist_ok=True)
    data={p.name:p.read_bytes() for p in paths}
    rows=[census(p) for p in paths]
    write_csv(args.out/'rom_manifest.csv', rows)
    (args.out/'rom_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    banks=[]
    for p in paths:
        d=data[p.name]
        for off in range(0,len(d),0x4000):
            bank=d[off:off+0x4000]
            banks.append({'file':p.name,'bank':off//0x4000,'offset_start':f'0x{off:06X}',
                          'offset_end':f'0x{off+len(bank)-1:06X}','sha1':hashlib.sha1(bank).hexdigest(),
                          'md5':hashlib.md5(bank).hexdigest(),'all_ff':all(x==0xFF for x in bank),
                          'all_00':all(x==0 for x in bank)})
    write_csv(args.out/'bank_manifest.csv',banks)
    pairs=[]
    for a,b in itertools.combinations(paths,2):
        da,db=data[a.name],data[b.name]; n=min(len(da),len(db))
        diffs=[i for i,(x,y) in enumerate(zip(da[:n],db[:n])) if x!=y]
        identical=[]
        for bank in range(n//0x4000):
            s=bank*0x4000; e=s+0x4000
            if da[s:e]==db[s:e]: identical.append(bank)
        pairs.append({'a':a.name,'b':b.name,'size_a':len(da),'size_b':len(db),'shared_bytes':n,
                      'diff_bytes_shared':len(diffs),'diff_pct_shared':round(100*len(diffs)/n,6),
                      'first_diff':f'0x{diffs[0]:06X}' if diffs else '',
                      'last_diff':f'0x{diffs[-1]:06X}' if diffs else '',
                      'shared_bank_count':n//0x4000,'identical_aligned_bank_count':len(identical),
                      'identical_aligned_banks':','.join(f'{x:02X}' for x in identical)})
    write_csv(args.out/'pairwise_comparison.csv',pairs)

if __name__ == '__main__':
    main()
