#!/usr/bin/env python3
from __future__ import annotations
import argparse, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

def run(*args: str) -> None:
    print('+', ' '.join(args), flush=True)
    subprocess.run(args, check=True)

def main() -> None:
    ap = argparse.ArgumentParser(description='Run the deterministic Crystal ROM reproducibility pipeline.')
    ap.add_argument('--catalog', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--roundtrip-report', default=None)
    args = ap.parse_args()
    py = sys.executable
    report = args.roundtrip_report or str(pathlib.Path(args.output) / 'MULTI-REGION' / 'REV-MIXED' / 'ROM-REPRODUCIBILITY' / 'lossless_roundtrip_report.json')
    run(py, str(HERE/'crystal_rom_audit.py'), '--catalog', args.catalog, '--output', args.output)
    run(py, str(HERE/'scan_candidates.py'), '--catalog', args.catalog, '--output', args.output)
    run(py, str(HERE/'address_map.py'), '--catalog', args.catalog, '--output', args.output)
    run(py, str(HERE/'cross_version_equivalence.py'), '--catalog', args.catalog, '--output', args.output)
    run(py, str(HERE/'pointer_sweep_summary.py'), '--catalog', args.catalog, '--output', args.output)
    run(py, str(HERE/'seed_bank_ownership.py'), '--catalog', args.catalog, '--roles', str(ROOT/'upstream_bank_roles.csv'), '--output', args.output)
    run(py, str(HERE/'seed_page_ownership.py'), '--catalog', args.catalog, '--roles', str(ROOT/'upstream_bank_roles.csv'), '--output', args.output)
    run(py, str(HERE/'lossless_roundtrip.py'), '--catalog', args.catalog, '--report', report)
    run(py, str(HERE/'verify_outputs.py'), '--catalog', args.catalog, '--output', args.output)
    print('FULL PIPELINE: OK')

if __name__ == '__main__':
    main()
