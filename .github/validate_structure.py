from pathlib import Path
import re
import sys

ROOT = Path('.')
LIBRARY = ROOT / 'LIBRARY'
PROJECTS = ROOT / 'PROJECTS'

GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^(?:_SHARED|[A-Z0-9][A-Z0-9.-]*)$')
PROJECT_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')

CANONICAL_ROOTS = {
    'LIBRARY', 'PROJECTS', 'INFRA', '.github', '.git',
    '.gitignore', '.gitattributes', 'README.md', 'STRUCTURE.md', 'MIGRATION.md'
}
LEGACY_ROOT_NAMES = {'GAMES', 'META'}
LIBRARY_BRANCHES = {'RELEASES', 'COMPARISONS', 'SHARED'}
PROJECT_SECTIONS = {
    'MANIFESTS', 'CROSSWALK', 'DESIGN', 'IMPLEMENTATION',
    'VERIFICATION', 'TOOLS', 'REPORTS'
}
BANNED_CANONICAL_PARTS = {'MULTI', 'REV-ALL', 'ALL-RELEASES', 'MULTI-REGION'}

errors = []
warnings = []


def children(path):
    if not path.exists():
        return []
    return [p for p in path.iterdir() if p.name not in {'.gitkeep', 'README.md'}]


def require_dirs(parent, label, matcher=None, allowed=None):
    out = []
    for p in children(parent):
        valid_name = (allowed is None or p.name in allowed) and (matcher is None or matcher.fullmatch(p.name))
        if not p.is_dir() or not valid_name:
            errors.append(f'invalid {label}: {p}')
            continue
        out.append(p)
    return out


def reject_pseudo_owners(root, label):
    if not root.exists():
        return
    for p in root.rglob('*'):
        if not p.is_dir():
            continue
        rel = p.relative_to(root)
        bad = BANNED_CANONICAL_PARTS.intersection(rel.parts)
        if bad:
            errors.append(f'forbidden pseudo-owner in canonical {label} path: {p} ({sorted(bad)})')


for p in ROOT.iterdir():
    if p.name in CANONICAL_ROOTS:
        continue
    if p.name in LEGACY_ROOT_NAMES or p.name.startswith('GENERATION-') or GEN_RE.fullmatch(p.name):
        warnings.append(f'legacy pre-v4 root pending migration: {p.name}')
        continue
    errors.append(f'non-canonical root entry: {p.name}')

reject_pseudo_owners(LIBRARY, 'library')
reject_pseudo_owners(PROJECTS, 'project')

# LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/{RELEASES,COMPARISONS,SHARED}
for gen in require_dirs(LIBRARY, 'library generation', matcher=GEN_RE):
    for platform in require_dirs(gen, 'platform', matcher=SLUG_RE):
        for game in require_dirs(platform, 'game id', matcher=SLUG_RE):
            branches = require_dirs(game, 'library ownership branch', allowed=LIBRARY_BRANCHES)
            for branch in branches:
                if game.name == '_SHARED' and branch.name == 'RELEASES':
                    errors.append(f'_SHARED cannot own official RELEASES: {branch}')
                    continue
                if branch.name in {'RELEASES', 'COMPARISONS'}:
                    require_dirs(branch, f'{branch.name.lower()} id', matcher=SLUG_RE)

# PROJECTS/<PROJECT-ID>/<canonical project section>/...
for project in require_dirs(PROJECTS, 'project id', matcher=PROJECT_RE):
    require_dirs(project, 'project section', allowed=PROJECT_SECTIONS)

if warnings:
    print('Repository v4.1 migration warnings:')
    for warning in warnings:
        print(f' - {warning}')

if errors:
    print('Repository structure v4.1 validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure v4.1 validation passed.')
