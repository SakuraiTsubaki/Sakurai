#!/usr/bin/env python3
"""Read-only Nintendo DS/TWL ROM baseline scanner used for the Generation V project.

It does not modify ROM data. It reports header identity, NitroFS/FAT structure,
and hashes suitable for reproducible comparison.
"""
from __future__ import annotations
import argparse, csv, hashlib, struct, zlib
from pathlib import Path


def u16(b: bytes, o: int) -> int:
    return struct.unpack_from('<H', b, o)[0]


def u32(b: bytes, o: int) -> int:
    return struct.unpack_from('<I', b, o)[0]


def sha1(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()


def parse_fnt(d: bytes):
    fnt_off, fnt_sz = u32(d, 0x40), u32(d, 0x44)
    fat_off, fat_sz = u32(d, 0x48), u32(d, 0x4C)
    fnt = d[fnt_off:fnt_off + fnt_sz]
    fat = d[fat_off:fat_off + fat_sz]
    n_dirs = u16(fnt, 6)
    dirs = [(u32(fnt, i*8), u16(fnt, i*8+4), u16(fnt, i*8+6)) for i in range(n_dirs)]
    files = []

    def walk(idx: int, prefix: list[str]):
        sub, first_id, _parent = dirs[idx]
        pos, fid = sub, first_id
        while True:
            n = fnt[pos]
            pos += 1
            if n == 0:
                break
            is_dir = bool(n & 0x80)
            ln = n & 0x7F
            name = fnt[pos:pos+ln].decode('ascii')
            pos += ln
            if is_dir:
                did = u16(fnt, pos)
                pos += 2
                walk(did - 0xF000, prefix + [name])
            else:
                start, end = struct.unpack_from('<II', fat, fid * 8)
                files.append((fid, '/'.join(prefix + [name]), start, end))
                fid += 1

    walk(0, [])
    return n_dirs, files


def scan(path: Path):
    d = path.read_bytes()
    fat_off, fat_sz = u32(d, 0x48), u32(d, 0x4C)
    ov9_off, ov9_sz = u32(d, 0x50), u32(d, 0x54)
    dirs, files = parse_fnt(d)
    fat = [struct.unpack_from('<II', d, fat_off+i*8) for i in range(fat_sz//8)]
    overlays = {}
    for i in range(ov9_sz // 32):
        vals = struct.unpack_from('<8I', d, ov9_off + i*32)
        overlays[vals[6] & 0x00FFFFFF] = vals[0]
    return d, {
        'file': path.name,
        'size': len(d),
        'title': d[:12].rstrip(b'\0').decode('ascii'),
        'game_code': d[0x0C:0x10].decode('ascii'),
        'maker_code': d[0x10:0x12].decode('ascii'),
        'unit_code': d[0x12],
        'device_capacity': d[0x14],
        'game_revision': u16(d, 0x1C),
        'rom_version': d[0x1E],
        'arm9_size': u32(d, 0x2C),
        'arm7_size': u32(d, 0x3C),
        'arm9i_size': u32(d, 0x1CC),
        'arm7i_size': u32(d, 0x1DC),
        'fnt_dirs': dirs,
        'named_files': len(files),
        'fat_entries': len(fat),
        'overlay9_count': ov9_sz // 32,
        'crc32': f'{zlib.crc32(d) & 0xFFFFFFFF:08X}',
        'md5': hashlib.md5(d).hexdigest(),
        'sha1': sha1(d),
        'sha256': hashlib.sha256(d).hexdigest(),
        'files': files,
        'fat': fat,
        'overlays': overlays,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom', nargs='+', type=Path)
    ap.add_argument('--manifest', type=Path)
    ns = ap.parse_args()
    scans = [scan(p) for p in ns.rom]
    for _d, r in scans:
        print(f"{r['file']}: {r['game_code']} CRC32={r['crc32']} SHA1={r['sha1']}")
        print(f"  title={r['title']!r} unit=0x{r['unit_code']:02X} revision=0x{r['game_revision']:04X} romver={r['rom_version']}")
        print(f"  overlays={r['overlay9_count']} named_files={r['named_files']} FAT={r['fat_entries']}")
    if ns.manifest:
        with ns.manifest.open('w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['rom', 'file_id', 'path', 'offset', 'size', 'sha1'])
            for d, r in scans:
                for fid, p, s, e in r['files']:
                    w.writerow([r['file'], fid, p, s, e-s, sha1(d[s:e])])

if __name__ == '__main__':
    main()
