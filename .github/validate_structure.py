from pathlib import Path
import re
import sys

ROOT = Path('.')
INFRA = ROOT / 'INFRA'
QUARANTINE = INFRA / 'QUARANTINE'
CROSS_GEN = ROOT / 'CROSS-GEN'

GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')

STATIC_ROOTS = {
    'INFRA', 'CROSS-GEN', '.github', '.git', '.gitignore', '.gitattributes',
    'README.md', 'STRUCTURE.md', 'MIGRATION.md'
}
RETIRED_ROOTS = {'LIBRARY', 'PROJECTS', 'LEGACY'}
GEN_BRANCHES = {'TARGET', 'COMPARE', 'SHARED', 'REFERENCE'}
GAME_BRANCHES = {'SOURCE', 'COMPARE', 'SHARED', 'REFERENCE'}
CROSS_GEN_BRANCHES = {'TARGET', 'COMPARE', 'SHARED', 'REFERENCE'}
BANNED_CANONICAL_PARTS = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION',
    '_SHARED', 'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN', 'MIGRATED'
}
IGNORED_METADATA_FILES = {
    '.gitkeep', 'README.md', 'ROUTING.md', 'STRUCTURE.md',
    'PROJECT.yaml', 'project.yaml', 'MANIFEST.yaml', 'manifest.yaml'
}

errors = []


def children(path):
    if not path.exists():
        return []
    return [p for p in path.iterdir() if p.name not in IGNORED_METADATA_FILES]


def require_dirs(parent, label, matcher=SLUG_RE):
    out = []
    for p in children(parent):
        if not p.is_dir() or (matcher and not matcher.fullmatch(p.name)):
            errors.append(f'invalid {label}: {p}')
            continue
        out.append(p)
    return out


def in_quarantine(path):
    try:
        path.relative_to(QUARANTINE)
        return True
    except ValueError:
        return False


def reject_banned(root, label):
    if not root.exists():
        return
    for p in root.rglob('*'):
        if in_quarantine(p):
            continue
        rel = p.relative_to(root)
        bad = BANNED_CANONICAL_PARTS.intersection(rel.parts)
        if bad:
            errors.append(f'forbidden v7 label in {label}: {p} ({sorted(bad)})')


for p in ROOT.iterdir():
    if p.name in RETIRED_ROOTS:
        errors.append(f'retired pre-v7 root must not exist: {p.name}')
        continue
    if GEN_RE.fullmatch(p.name):
        if not p.is_dir():
            errors.append(f'generation root is not a directory: {p}')
        continue
    if p.name not in STATIC_ROOTS:
        errors.append(f'non-canonical v7 root entry: {p.name}')

for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    for node in children(gen):
        if not node.is_dir():
            errors.append(f'invalid generation child: {node}')
            continue

        if node.name in GEN_BRANCHES:
            if node.name in {'TARGET', 'COMPARE', 'REFERENCE'}:
                require_dirs(node, f'generation {node.name.lower()} id')
            reject_banned(node, f'generation {node.name.lower()}')
            continue

        if not SLUG_RE.fullmatch(node.name) or node.name in BANNED_CANONICAL_PARTS:
            errors.append(f'invalid v7 game id: {node}')
            continue

        game = node
        for branch in children(game):
            if not branch.is_dir() or branch.name not in GAME_BRANCHES:
                errors.append(f'invalid v7 game branch: {branch}')
                continue

            if branch.name == 'SOURCE':
                for platform in require_dirs(branch, 'source platform'):
                    for package in require_dirs(platform, 'package kind'):
                        for release in require_dirs(package, 'release id'):
                            reject_banned(release, 'source release')
            elif branch.name in {'COMPARE', 'REFERENCE'}:
                require_dirs(branch, f'{branch.name.lower()} id')
                reject_banned(branch, branch.name.lower())
            else:
                reject_banned(branch, 'shared')

if CROSS_GEN.exists():
    for branch in children(CROSS_GEN):
        if not branch.is_dir() or branch.name not in CROSS_GEN_BRANCHES:
            errors.append(f'invalid cross-generation branch: {branch}')
            continue
        if branch.name in {'TARGET', 'COMPARE', 'REFERENCE'}:
            require_dirs(branch, f'cross-generation {branch.name.lower()} id')
        reject_banned(branch, f'cross-generation {branch.name.lower()}')

for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    reject_banned(gen, gen.name)

if errors:
    print('Repository structure v7 validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure v7 validation passed.')
