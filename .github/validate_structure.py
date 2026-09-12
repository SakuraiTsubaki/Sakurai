from pathlib import Path
import re
import sys

ROOT = Path('.')
LIBRARY = ROOT / 'LIBRARY'
PROJECTS = ROOT / 'PROJECTS'

GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')
PROJECT_RE = SLUG_RE

CANONICAL_ROOTS = {
    'LIBRARY', 'PROJECTS', 'INFRA', '.github', '.git',
    '.gitignore', '.gitattributes', 'README.md', 'STRUCTURE.md', 'MIGRATION.md'
}
LEGACY_ROOT_NAMES = {'GAMES', 'META'}
LEGACY_V4_PLATFORM_ROOTS = {
    'GB', 'GBC', 'GBA', 'NDS', 'NDS-NTR', 'NDS-TWL', '3DS',
    'GCN', 'WII', 'WIIU', 'SWITCH', 'SWITCH2'
}
GEN_BRANCHES = {'COMPARE', 'SHARED', 'REFERENCE'}
GAME_BRANCHES = {'SOURCE', 'COMPARE', 'SHARED', 'REFERENCE'}
PROJECT_SECTIONS = {
    'MANIFESTS', 'CROSSWALK', 'DESIGN', 'IMPLEMENTATION', 'DIFFS',
    'PATCHES', 'BUILD', 'VERIFICATION', 'TOOLS', 'REPORTS'
}
BANNED_CANONICAL_PARTS = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION',
    '_SHARED', 'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN'
}
IGNORED_METADATA_FILES = {'.gitkeep', 'README.md', 'ROUTING.md', 'STRUCTURE.md'}

errors = []
warnings = []


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
        warnings.append(f'legacy pre-v5 root pending migration: {p.name}')
        continue
    if p.is_file() and p.suffix.lower() == '.md':
        warnings.append(f'top-level metadata document pending INFRA routing: {p.name}')
        continue
    errors.append(f'non-canonical root entry: {p.name}')

for gen in require_dirs(LIBRARY, 'library generation', matcher=GEN_RE):
    for node in children(gen):
        if not node.is_dir():
            errors.append(f'invalid generation child: {node}')
            continue
        if node.name in LEGACY_V4_PLATFORM_ROOTS:
            warnings.append(f'legacy v4 platform-first subtree pending migration: {node}')
            continue
        if node.name in GEN_BRANCHES:
            if node.name in {'COMPARE', 'REFERENCE'}:
                require_dirs(node, f'generation {node.name.lower()} id')
            reject_banned(node, f'generation {node.name.lower()}')
            continue
        if not SLUG_RE.fullmatch(node.name) or node.name in BANNED_CANONICAL_PARTS:
            errors.append(f'invalid v5 game id: {node}')
            continue

        game = node
        for branch in children(game):
            if not branch.is_dir() or branch.name not in GAME_BRANCHES:
                errors.append(f'invalid v5 game branch: {branch}')
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

for project in require_dirs(PROJECTS, 'project id', matcher=PROJECT_RE):
    for section in children(project):
        if not section.is_dir() or section.name not in PROJECT_SECTIONS:
            errors.append(f'invalid project section: {section}')
            continue
        reject_banned(section, 'project')

if warnings:
    print('Repository v5 migration warnings:')
    for warning in warnings:
        print(f' - {warning}')

if errors:
    print('Repository structure v5 validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure v5 validation passed.')
