from pathlib import Path
import re
import sys

ROOT = Path('.')
GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9._-]*$')
DUMP_RE = re.compile(r'^DUMP-SHA256-[0-9A-F]{16}$')

STATIC_ROOTS = {
    'INFRA', 'CROSS-GEN', '.github', '.git', '.gitignore', '.gitattributes',
    'README.md', 'STRUCTURE.md', 'STRUCTURE-V2.md', 'MIGRATION.md',
    'projects', 'workspaces',
}
MIGRATION_ROOTS = {'LIBRARY', 'GENERATION-IV'}
RETIRED_ROOTS = {'PROJECTS', 'LEGACY'}
V11_GAME_BRANCHES = {
    'RELEASES', 'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED',
    'KNOWLEDGE', 'VERIFY',
}
V11_GEN_BRANCHES = {
    'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED', 'KNOWLEDGE', 'VERIFY',
}
V11_CROSS_BRANCHES = {
    'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED', 'KNOWLEDGE', 'VERIFY',
}
LEGACY_GAME_BRANCHES = {'SOURCE', 'TARGET', 'COMPARE', 'REFERENCE'}
LEGACY_GEN_BRANCHES = {'TARGET', 'COMPARE', 'REFERENCE'}
LEGACY_CROSS_BRANCHES = {'TARGET', 'COMPARE', 'REFERENCE'}
BANNED_IDS = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION', '_SHARED',
    'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN', 'MIGRATED'
}
ROM_SUFFIXES = {'.gb', '.gbc', '.gba', '.nds', '.3ds', '.cia', '.xci', '.nsp'}
errors = []


def visible_children(path):
    if not path.exists():
        return []
    return list(path.iterdir())


def dirs(path):
    return [p for p in visible_children(path) if p.is_dir()]


def valid_slug(name):
    return bool(SLUG_RE.fullmatch(name)) and name not in BANNED_IDS


def check_id_dirs(path, label):
    for p in dirs(path):
        if not valid_slug(p.name):
            errors.append(f'invalid {label}: {p}')


def check_releases(path):
    # Metadata files such as INDEX.json are legal alongside coordinate directories.
    for platform in dirs(path):
        if not valid_slug(platform.name):
            errors.append(f'invalid platform id: {platform}')
            continue
        for package in dirs(platform):
            if not valid_slug(package.name):
                errors.append(f'invalid package kind: {package}')
                continue
            for release in dirs(package):
                if not valid_slug(release.name):
                    errors.append(f'invalid release id: {release}')
                    continue
                dumps = release / 'DUMPS'
                if dumps.exists():
                    for dump in dirs(dumps):
                        if not DUMP_RE.fullmatch(dump.name):
                            errors.append(f'invalid v11 dump id: {dump}')


for entry in ROOT.iterdir():
    if entry.name in MIGRATION_ROOTS:
        continue
    if entry.name in RETIRED_ROOTS:
        errors.append(f'retired root exists: {entry.name}')
    elif GEN_RE.fullmatch(entry.name):
        if not entry.is_dir():
            errors.append(f'generation root is not a directory: {entry}')
    elif entry.name not in STATIC_ROOTS:
        errors.append(f'non-canonical v11 root entry: {entry.name}')


for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    # Generation-level metadata files are legal; validate semantic directories only.
    for node in dirs(gen):
        if node.name in V11_GEN_BRANCHES:
            if node.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(node, f'generation {node.name.lower()} id')
            continue
        if node.name in LEGACY_GEN_BRANCHES:
            continue
        if not valid_slug(node.name):
            errors.append(f'invalid game id: {node}')
            continue

        for branch in dirs(node):
            if branch.name == 'RELEASES':
                check_releases(branch)
            elif branch.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(branch, f'{branch.name.lower()} id')
            elif branch.name in {'SHARED', 'KNOWLEDGE', 'VERIFY'}:
                pass
            elif branch.name in LEGACY_GAME_BRANCHES:
                pass
            else:
                errors.append(f'invalid v11 game branch: {branch}')


cross = ROOT / 'CROSS-GEN'
if cross.exists():
    for branch in dirs(cross):
        if branch.name in V11_CROSS_BRANCHES:
            if branch.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(branch, f'cross-generation {branch.name.lower()} id')
        elif branch.name in LEGACY_CROSS_BRANCHES:
            pass
        else:
            errors.append(f'invalid v11 CROSS-GEN branch: {branch}')


# Full playable ROM images are prohibited. Generic/discrete binary assets are allowed.
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in ROM_SUFFIXES:
        errors.append(f'ROM image extension is forbidden: {p}')


if errors:
    print('Repository structure v11 validation failed:')
    for e in errors:
        print(f' - {e}')
    sys.exit(1)

print('Repository structure v11 validation passed.')
