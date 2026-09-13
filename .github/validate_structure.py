from pathlib import Path
import re
import sys

ROOT = Path('.')
GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')
ID_RE = re.compile(r'^[A-Z0-9][A-Z0-9._-]*$')
DUMP_RE = re.compile(r'^DUMP-SHA256-[0-9A-F]{16}$')
LOWER_ID_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')

STATIC_ROOTS = {
    'INFRA', 'CROSS-GEN', 'projects', '.github', '.git', '.gitignore',
    '.gitattributes', 'README.md', 'STRUCTURE.md', 'STRUCTURE-V2.md', 'MIGRATION.md'
}
# These pre-v11 roots are existing migration inputs only.
MIGRATION_ROOTS = {'LIBRARY', 'GENERATION-IV'}
RETIRED_ROOTS = {'PROJECTS', 'LEGACY'}

CANONICAL_GAME_BRANCHES = {'RELEASES', 'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED'}
CANONICAL_GEN_BRANCHES = {'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED'}
CANONICAL_CROSS_BRANCHES = {'PROJECTS', 'COMPARES', 'REFERENCES', 'SHARED'}
LEGACY_GAME_BRANCHES = {'SOURCE', 'TARGET', 'COMPARE', 'REFERENCE', 'KNOWLEDGE', 'VERIFY'}
LEGACY_GEN_BRANCHES = {'TARGET', 'COMPARE', 'REFERENCE'}
LEGACY_CROSS_BRANCHES = {'TARGET', 'COMPARE', 'REFERENCE'}

BANNED_IDS = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION', '_SHARED',
    'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN', 'MIGRATED'
}
IGNORE = {
    '.gitkeep', 'README.md', 'ROUTING.md', 'STRUCTURE.md', 'MANIFEST.yaml',
    'manifest.yaml', 'PROJECT.yaml', 'project.yaml'
}

errors = []
warnings = []


def children(path):
    return [] if not path.exists() else [p for p in path.iterdir() if p.name not in IGNORE]


def valid_slug(name):
    return bool(SLUG_RE.fullmatch(name)) and name not in BANNED_IDS


def valid_id(name):
    return bool(ID_RE.fullmatch(name)) and name not in BANNED_IDS


def check_id_dirs(path, label):
    for p in children(path):
        if p.is_file() and p.name.endswith('.json'):
            continue
        if not p.is_dir() or not valid_id(p.name):
            errors.append(f'invalid {label}: {p}')


def check_releases(path):
    for platform in children(path):
        if platform.is_file() and platform.name.endswith('.json'):
            continue
        if not platform.is_dir() or not valid_slug(platform.name):
            errors.append(f'invalid platform id: {platform}')
            continue
        for package in children(platform):
            if package.is_file() and package.name.endswith('.json'):
                continue
            if not package.is_dir() or not valid_slug(package.name):
                errors.append(f'invalid package kind: {package}')
                continue
            for release in children(package):
                if release.is_file() and release.suffix.lower() in {'.json', '.yaml', '.yml', '.md'}:
                    continue
                if not release.is_dir() or not valid_slug(release.name):
                    errors.append(f'invalid release id: {release}')
                    continue
                dumps = release / 'DUMPS'
                if dumps.exists():
                    for dump in children(dumps):
                        if dump.is_file() and dump.name.endswith('.json'):
                            continue
                        if not dump.is_dir() or not DUMP_RE.fullmatch(dump.name):
                            errors.append(f'invalid dump id: {dump}')


def note_legacy(path):
    warnings.append(f'legacy migration path remains: {path}')


for entry in ROOT.iterdir():
    if entry.name in MIGRATION_ROOTS:
        note_legacy(entry)
    elif entry.name in RETIRED_ROOTS:
        errors.append(f'retired top-level root exists: {entry.name}')
    elif GEN_RE.fullmatch(entry.name):
        if not entry.is_dir():
            errors.append(f'generation root is not a directory: {entry}')
    elif entry.name not in STATIC_ROOTS:
        errors.append(f'non-canonical v11 root entry: {entry.name}')

projects = ROOT / 'projects'
if projects.exists():
    if not projects.is_dir():
        errors.append('projects root is not a directory')
    else:
        for project in children(projects):
            if not project.is_dir() or not LOWER_ID_RE.fullmatch(project.name):
                errors.append(f'invalid legacy project id: {project}')

for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    for node in children(gen):
        if not node.is_dir():
            errors.append(f'invalid generation child: {node}')
            continue

        if node.name in CANONICAL_GEN_BRANCHES:
            if node.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(node, f'generation {node.name.lower()} id')
            continue
        if node.name in LEGACY_GEN_BRANCHES:
            note_legacy(node)
            continue
        if not valid_slug(node.name):
            errors.append(f'invalid game id: {node}')
            continue

        for branch in children(node):
            if branch.is_file() and branch.name.startswith('MIGRATION') and branch.suffix.lower() == '.md':
                continue
            if not branch.is_dir():
                errors.append(f'invalid game branch: {branch}')
                continue
            if branch.name in CANONICAL_GAME_BRANCHES:
                if branch.name == 'RELEASES':
                    check_releases(branch)
                elif branch.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                    check_id_dirs(branch, f'{branch.name.lower()} id')
                continue
            if branch.name in LEGACY_GAME_BRANCHES:
                note_legacy(branch)
                continue
            errors.append(f'invalid game branch: {branch}')

cross = ROOT / 'CROSS-GEN'
if cross.exists():
    for branch in children(cross):
        if not branch.is_dir():
            errors.append(f'invalid CROSS-GEN branch: {branch}')
            continue
        if branch.name in CANONICAL_CROSS_BRANCHES:
            if branch.name in {'PROJECTS', 'COMPARES', 'REFERENCES'}:
                check_id_dirs(branch, f'cross-generation {branch.name.lower()} id')
            continue
        if branch.name in LEGACY_CROSS_BRANCHES:
            note_legacy(branch)
            continue
        errors.append(f'invalid CROSS-GEN branch: {branch}')

if warnings:
    print('Repository structure v11 migration warnings:')
    for warning in warnings:
        print(f' - {warning}')

if errors:
    print('Repository structure v11 validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure v11 validation passed.')
