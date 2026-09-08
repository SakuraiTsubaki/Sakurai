#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib, subprocess, sys

EXPECTED = {
    'pokecrystal.gbc': {'target_label': 'USA-EUROPE_REV0', 'sha1': 'f4cd194bdee0d04ca4eac29e09b8e4e9d818c133'},
    'pokecrystal11.gbc': {'target_label': 'USA-EUROPE_REV1', 'sha1': 'f2f52230b536214ef7c9924f483392993e226cfb'},
}
PINNED_COMMIT = '7a7881d0d62e0ddbd82dcf10e7116807487ac651'
RGBDS_RECOMMENDED = '1.0.3'

def sha1(path: pathlib.Path) -> str:
    h = hashlib.sha1()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main() -> None:
    ap = argparse.ArgumentParser(description='Verify pret/pokecrystal source builds against the supplied English Crystal ROM identities.')
    ap.add_argument('--pokecrystal-dir', required=True)
    ap.add_argument('--build', action='store_true', help='Run make and make crystal11 before verifying.')
    ap.add_argument('--report', default=None)
    args = ap.parse_args()
    root = pathlib.Path(args.pokecrystal_dir).resolve()
    if args.build:
        subprocess.run(['make'], cwd=root, check=True)
        subprocess.run(['make', 'crystal11'], cwd=root, check=True)

    git_head = None
    if (root / '.git').exists():
        try:
            git_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        except Exception:
            pass

    results = []
    for filename, spec in EXPECTED.items():
        p = root / filename
        exists = p.is_file()
        actual = sha1(p) if exists else None
        results.append({'filename': filename, 'target_label': spec['target_label'], 'exists': exists, 'expected_sha1': spec['sha1'], 'actual_sha1': actual, 'match': exists and actual == spec['sha1']})
    report = {'schema_version': 1, 'upstream': 'pret/pokecrystal', 'pinned_reference_commit': PINNED_COMMIT, 'detected_git_head': git_head, 'pinned_commit_match': git_head == PINNED_COMMIT if git_head else None, 'recommended_rgbds': RGBDS_RECOMMENDED, 'results': results, 'success': all(r['match'] for r in results)}
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        pathlib.Path(args.report).write_text(text, encoding='utf-8')
    print(text, end='')
    sys.exit(0 if report['success'] else 1)

if __name__ == '__main__':
    main()
