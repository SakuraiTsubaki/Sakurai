#!/usr/bin/env python3
"""Create the deterministic localized-table analysis archive.

Expected inputs are the per-release full CSV outputs from extract_abilities.py
and extract_items.py. The archive contains no ROM bytes beyond the extracted
semantic text records and their reconstruction metadata.
"""
from __future__ import annotations
import argparse, io, lzma, tarfile
from pathlib import Path

RELEASES = ['JPN','ENG_USA_EUR','FRA','DEU','ITA','ESP']

def add_bytes(tf: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ''
    info.mode = 0o644
    tf.addfile(info, io.BytesIO(data))

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path, help='directory containing extracted CSV outputs')
    ap.add_argument('--out', type=Path, default=Path('analysis/localized_tables_full.tar.xz'))
    a = ap.parse_args()
    tar_buf = io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode='w') as tf:
        for release in RELEASES:
            low = release.lower()
            ability = a.root / f'{low}_abilities.csv'
            item_gz = a.root / f'{low}.full.csv.gz'
            add_bytes(tf, f'abilities/{release}.csv', ability.read_bytes())
            import gzip
            add_bytes(tf, f'items/{release}.csv', gzip.decompress(item_gz.read_bytes()))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_bytes(lzma.compress(tar_buf.getvalue(), preset=9))

if __name__ == '__main__':
    main()
