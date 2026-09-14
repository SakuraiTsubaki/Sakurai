from pathlib import Path
import re
import sys

ROOT = Path('.')
GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9._-]*$')
DUMP_RE = re.compile(r'^DUMP-SHA256-[0-9A-F]{16}$')

ROOT_ALLOWED = {
    '.github', '.git', '.gitignore', '.gitattributes',
    'README.md', 'STRUCTURE.md',
    'INFRA', 'CROSS-GEN',
}
GEN_BRANCHES = {'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED', 'KNOWLEDGE', 'VERIFY'}
GAME_BRANCHES = {
    'RELEASES', 'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED',
    'KNOWLEDGE', 'VERIFY', 'CATALOGS', 'REPORTS', 'TABLES', 'ANALYSIS', 'TOOLS',
}
CROSS_BRANCHES = {'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED', 'KNOWLEDGE', 'VERIFY'}
RETIRED_ROOTS = {'LIBRARY', 'projects', 'workspaces', 'PROJECTS', 'LEGACY', 'STRUCTURE-V2.md', 'MIGRATION.md'}
RETIRED_BRANCHES = {'SOURCE', 'TARGET', 'COMPARE', 'REFERENCE'}
BANNED_IDS = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION', '_SHARED',
    'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN', 'MIGRATED'
}
ROM_SUFFIXES = {'.gb', '.gbc', '.gba', '.nds', '.3ds', '.cia', '.xci', '.nsp'}
errors = []


def dirs(path):
    if not path.exists():
        return []
    return [p for p in path.iterdir() if p.is_dir()]


def valid_slug(name):
    return bool(SLUG_RE.fullmatch(name)) and name not in BANNED_IDS


def check_id_dirs(path, label):
    for p in dirs(path):
        if not valid_slug(p.name):
            errors.append(f'invalid {label}: {p}')


def check_releases(path):
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
                        if dump.name.startswith('DUMP-SHA256-') and not DUMP_RE.fullmatch(dump.name):
                            errors.append(f'malformed dump id: {dump}')


for entry in ROOT.iterdir():
    if GEN_RE.fullmatch(entry.name):
        if not entry.is_dir():
            errors.append(f'generation root is not a directory: {entry}')
        continue
    if entry.name in RETIRED_ROOTS:
        errors.append(f'retired root exists: {entry.name}')
    elif entry.name not in ROOT_ALLOWED:
        errors.append(f'non-canonical root entry: {entry.name}')

if (ROOT / 'INFRA' / 'MIGRATION').exists():
    errors.append('retired migration tree exists: INFRA/MIGRATION')

for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    for node in dirs(gen):
        if node.name in RETIRED_BRANCHES:
            errors.append(f'retired generation branch exists: {node}')
            continue
        if node.name in GEN_BRANCHES:
            if node.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(node, f'generation {node.name.lower()} id')
            continue
        if not valid_slug(node.name):
            errors.append(f'invalid game id: {node}')
            continue
        for branch in dirs(node):
            if branch.name in RETIRED_BRANCHES:
                errors.append(f'retired game branch exists: {branch}')
            elif branch.name == 'RELEASES':
                check_releases(branch)
            elif branch.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(branch, f'{branch.name.lower()} id')
            elif branch.name not in GAME_BRANCHES:
                errors.append(f'invalid game branch: {branch}')

cross = ROOT / 'CROSS-GEN'
if cross.exists():
    for branch in dirs(cross):
        if branch.name in RETIRED_BRANCHES:
            errors.append(f'retired CROSS-GEN branch exists: {branch}')
        elif branch.name in CROSS_BRANCHES:
            if branch.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(branch, f'cross-generation {branch.name.lower()} id')
        else:
            errors.append(f'invalid CROSS-GEN branch: {branch}')

for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in ROM_SUFFIXES:
        errors.append(f'ROM image extension is forbidden: {p}')

if errors:
    print('Repository structure validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure validation passed.')
