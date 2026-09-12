from pathlib import Path
import re
import sys

ROOT = Path('.')
GEN_RE = re.compile(r'^GEN-\d{2}$')
LEGACY_GEN_RE = re.compile(r'^GENERATION-(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI)$')
GAME_RE = re.compile(r'^(?:_SHARED|[A-Z0-9][A-Z0-9-]*)$')
ID_RE = re.compile(r'^[A-Z0-9][A-Z0-9-]*$')
REV_RE = re.compile(r'^REV-(?:[A-Z]|\d+)$')
BRANCHES = {'SOURCE', 'TARGET', 'COMPARE', 'SHARED'}
WORK_TYPES = {
    'ANALYSIS','CENSUS','STRUCTURE','TEXT','DATA','DIFFS','TOOLS','TESTS',
    'VERIFICATION','REPORTS','LOCALIZATION','DISASSEMBLY','MANIFESTS','MAPS','SYMBOLS'
}
INFRA = {'.github','README.md','STRUCTURE.md','MIGRATION.md','META','.git'}

errors = []
warnings = []


def children(p):
    return [x for x in p.iterdir() if x.name != '.gitkeep']


def require_dirs(parent, label, matcher=None, allowed=None):
    out = []
    for p in children(parent):
        valid_name = (allowed is None or p.name in allowed) and (matcher is None or matcher.fullmatch(p.name))
        if not p.is_dir() or not valid_name:
            errors.append(f'invalid {label}: {p}')
            continue
        out.append(p)
    return out


for p in ROOT.iterdir():
    if p.name in INFRA or GEN_RE.fullmatch(p.name):
        continue
    if LEGACY_GEN_RE.fullmatch(p.name):
        warnings.append(f'legacy generation root pending migration: {p.name}')
        continue
    errors.append(f'non-canonical root entry: {p.name}')

for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    games = require_dirs(gen, 'GAME path', matcher=GAME_RE)
    for game in games:
        branches = require_dirs(game, 'ownership branch', allowed=BRANCHES)
        for branch in branches:
            if branch.name == 'SOURCE':
                releases = require_dirs(branch, 'SOURCE release id', matcher=ID_RE)
                for release in releases:
                    revs = require_dirs(release, 'SOURCE revision', matcher=REV_RE)
                    for rev in revs:
                        require_dirs(rev, 'SOURCE work type', allowed=WORK_TYPES)
            elif branch.name == 'TARGET':
                targets = require_dirs(branch, 'TARGET id', matcher=ID_RE)
                for target in targets:
                    bases = require_dirs(target, 'TARGET base id', matcher=ID_RE)
                    for base in bases:
                        require_dirs(base, 'TARGET work type', allowed=WORK_TYPES)
            else:  # COMPARE / SHARED
                scopes = require_dirs(branch, f'{branch.name} scope', matcher=ID_RE)
                for scope in scopes:
                    require_dirs(scope, f'{branch.name} work type', allowed=WORK_TYPES)

if warnings:
    print('Repository structure migration warnings:')
    for w in warnings:
        print(f' - {w}')

if errors:
    print('Repository structure validation failed:')
    for e in errors:
        print(f' - {e}')
    sys.exit(1)

print('Repository structure v2 validation passed.')
