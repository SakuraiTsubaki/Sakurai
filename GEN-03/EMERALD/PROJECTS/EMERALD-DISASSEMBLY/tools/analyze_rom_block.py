#!/usr/bin/env python3
"""Compare one same-offset ROM block across the reference releases."""
from __future__ import annotations
import argparse, csv, hashlib, itertools, json, math, struct
from collections import Counter
from pathlib import Path

ROM_BASE = 0x08000000
ROM_END = 0x09000000


def entropy(buf: bytes) -> float:
    counts = Counter(buf)
    n = len(buf)
    return -sum((c / n) * math.log2(c / n) for c in counts.values()) if n else 0.0


def choose_canonical(group):
    for item in group:
        if item[0]['id'] == 'ENG_USA_EUR':
            return item
    return group[0]


def load_unique_refs(manifest_path: Path, rom_dir: Path):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    groups = {}
    for ref in manifest['references']:
        path = rom_dir / ref['source_filename']
        buf = path.read_bytes()
        sha1 = hashlib.sha1(buf).hexdigest()
        if sha1 != ref['sha1']:
            raise ValueError(f"SHA-1 mismatch for {ref['id']}: {sha1}")
        groups.setdefault(sha1, []).append((ref, path, buf))
    out = []
    for group in groups.values():
        ref, path, buf = choose_canonical(group)
        out.append((ref['id'], buf))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('rom_dir', type=Path)
    ap.add_argument('--manifest', type=Path, default=Path('manifests/roms.json'))
    ap.add_argument('--block-index', type=lambda x: int(x, 0), default=0)
    ap.add_argument('--block-size', type=lambda x: int(x, 0), default=0x10000)
    ap.add_argument('--page-size', type=lambda x: int(x, 0), default=0x1000)
    ap.add_argument('--baseline', default='ENG_USA_EUR')
    ap.add_argument('--out-prefix', type=Path, default=Path('analysis/block_00'))
    args = ap.parse_args()

    refs = load_unique_refs(args.manifest, args.rom_dir)
    by_id = dict(refs)
    start = args.block_index * args.block_size
    end = start + args.block_size
    if args.baseline not in by_id:
        raise ValueError(f'baseline {args.baseline!r} not found')

    pair_rows = []
    for (id_a, buf_a), (id_b, buf_b) in itertools.combinations(refs, 2):
        a = buf_a[start:end]
        b = buf_b[start:end]
        same = sum(x == y for x, y in zip(a, b))
        pair_rows.append({
            'release_a': id_a,
            'release_b': id_b,
            'same_bytes': same,
            'different_bytes': len(a) - same,
            'same_pct': f'{same / len(a):.6%}',
        })

    page_rows = []
    for page_start in range(start, end, args.page_size):
        page_end = min(page_start + args.page_size, end)
        same = sum(
            1 for pos in range(page_start, page_end)
            if len({buf[pos] for _, buf in refs}) == 1
        )
        for release_id, buf in refs:
            page = buf[page_start:page_end]
            ptr_count = sum(
                1 for off in range(0, len(page) - 3, 4)
                if ROM_BASE <= struct.unpack_from('<I', page, off)[0] < ROM_END
            )
            page_rows.append({
                'start': f'0x{page_start:08X}',
                'end': f'0x{page_end - 1:08X}',
                'release': release_id,
                'all_release_same_bytes': same,
                'all_release_same_pct': f'{same / len(page):.6%}',
                'aligned_rom_pointer_words': ptr_count,
                'zero_bytes': page.count(0),
                'ff_bytes': page.count(0xFF),
                'entropy_bits_per_byte': f'{entropy(page):.6f}',
            })

    delta_rows = []
    baseline = by_id[args.baseline]
    for release_id, buf in refs:
        if release_id == args.baseline:
            continue
        deltas = Counter()
        word_diffs = both_ptr = one_ptr = 0
        for off in range(start, end, 4):
            x = struct.unpack_from('<I', baseline, off)[0]
            y = struct.unpack_from('<I', buf, off)[0]
            if x == y:
                continue
            word_diffs += 1
            xp = ROM_BASE <= x < ROM_END
            yp = ROM_BASE <= y < ROM_END
            if xp and yp:
                both_ptr += 1
                deltas[y - x] += 1
            elif xp or yp:
                one_ptr += 1
        for delta, count in deltas.most_common():
            delta_rows.append({
                'release': release_id,
                'word_differences': word_diffs,
                'both_rom_pointer_differences': both_ptr,
                'one_sided_rom_pointer_differences': one_ptr,
                'pointer_delta_decimal': delta,
                'pointer_delta_hex': ('+' if delta >= 0 else '-') + f'0x{abs(delta):X}',
                'count': count,
            })

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    outputs = [
        (args.out_prefix.with_name(args.out_prefix.name + '_pairwise_similarity.csv'), pair_rows),
        (args.out_prefix.with_name(args.out_prefix.name + '_4k_pages.csv'), page_rows),
        (args.out_prefix.with_name(args.out_prefix.name + '_pointer_deltas.csv'), delta_rows),
    ]
    for path, rows in outputs:
        with path.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

if __name__ == '__main__':
    main()
