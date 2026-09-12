from pathlib import Path
import re
import sys

ROOT = Path('.')
LIBRARY = ROOT / 'LIBRARY'
PROJECTS = ROOT / 'PROJECTS'
LEGACY = ROOT / 'LEGACY'

GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')

CANONICAL_ROOTS = {
    'LIBRARY', 'PROJECTS', 'INFRA', 'LEGACY', '.github', '.git',
    '.gitignore', '.gitattributes', 'README.md', 'STRUCTURE.md', 'MIGRATION.md'
}
GEN_BRANCHES = {'COMPARE', 'SHARED', 'REFERENCE'}
GAME_BRANCHES = {'SOURCE', 'COMPARE', 'SHARED', 'REFERENCE'}
LEGACY_PLATFORM_ROOTS = {
    'GB', 'GBC', 'GBA', 'NDS', 'NDS-NTR', 'NDS-TWL', '3DS',
    'GCN', 'WII', 'WIIU', 'SWITCH', 'SWITCH2'
}
BANNED_CANONICAL_PARTS = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION',
    '_SHARED', 'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN', 'MIGRATED'
}
IGNORED_METADATA_FILES = {
    '.gitkeep', 'README.md', 'ROUTING.md', 'STRUCTURE.md', 'PROJECT.yaml', 'project.yaml'
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


def reject_banned(root, label):
    if not root.exists():
        return
    for p in root.rglob('*'):
        if LEGACY in p.parents or p == LEGACY:
            continue
        rel = p.relative_to(root)
        bad = BANNED_CANONICAL_PARTS.intersection(rel.parts)
        if bad:
            errors.append(f'forbidden v6 label in {label}: {p} ({sorted(bad)})')


for p in ROOT.iterdir():
    if p.name not in CANONICAL_ROOTS:
        errors.append(f'non-canonical v6 root entry: {p.name}')

for gen in require_dirs(LIBRARY, 'library generation', matcher=GEN_RE):
    for node in children(gen):
        if not node.is_dir():
            errors.append(f'invalid generation child: {node}')
            continue
        if node.name in LEGACY_PLATFORM_ROOTS:
            errors.append(f'platform-first pre-v6 subtree must be under LEGACY: {node}')
            continue
        if node.name in GEN_BRANCHES:
            if node.name in {'COMPARE', 'REFERENCE'}:
                require_dirs(node, f'generation {node.name.lower()} id')
            reject_banned(node, f'generation {node.name.lower()}')
            continue
        if not SLUG_RE.fullmatch(node.name) or node.name in BANNED_CANONICAL_PARTS:
            errors.append(f'invalid v6 game id: {node}')
            continue

        game = node
        for branch in children(game):
            if not branch.is_dir() or branch.name not in GAME_BRANCHES:
                errors.append(f'invalid v6 game branch: {branch}')
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

if PROJECTS.exists():
    for scope in children(PROJECTS):
        if not scope.is_dir() or not (GEN_RE.fullmatch(scope.name) or scope.name == 'CROSS-GEN'):
            errors.append(f'invalid v6 project scope: {scope}')
            continue
        for project in require_dirs(scope, 'project id'):
            reject_banned(project, 'project')

reject_banned(LIBRARY, 'library')
reject_banned(PROJECTS, 'projects')
reject_banned(ROOT / 'INFRA', 'infra')

if errors:
    print('Repository structure v6 validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure v6 validation passed.')
