from pathlib import Path
import re
import sys

ROOT = Path('.')
QUARANTINE = ROOT / 'INFRA' / 'QUARANTINE'
GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')
PROJECT_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')

STATIC_ROOTS = {
    'INFRA', 'CROSS-GEN', 'projects', '.github', '.git', '.gitignore', '.gitattributes',
    'README.md', 'STRUCTURE.md', 'MIGRATION.md'
}
RETIRED_ROOTS = {'LIBRARY', 'PROJECTS', 'LEGACY'}
GAME_BRANCHES = {'SOURCE', 'TARGET', 'COMPARE', 'SHARED', 'REFERENCE'}
GEN_BRANCHES = {'TARGET', 'COMPARE', 'SHARED', 'REFERENCE'}
CROSS_BRANCHES = {'TARGET', 'COMPARE', 'SHARED', 'REFERENCE'}
BANNED = {
    'MULTI', 'REV-ALL', 'ALL', 'ALL-RELEASES', 'MULTI-REGION', '_SHARED',
    'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN', 'MIGRATED'
}
IGNORE = {'.gitkeep', 'README.md', 'ROUTING.md', 'STRUCTURE.md', 'MANIFEST.yaml', 'manifest.yaml', 'PROJECT.yaml', 'project.yaml'}
errors = []


def children(path):
    if not path.exists():
        return []
    return [p for p in path.iterdir() if p.name not in IGNORE]


def is_quarantine(path):
    try:
        path.relative_to(QUARANTINE)
        return True
    except ValueError:
        return False


def check_slug_dirs(path, label):
    for p in children(path):
        if not p.is_dir() or not SLUG_RE.fullmatch(p.name) or p.name in BANNED:
            errors.append(f'invalid {label}: {p}')


def reject_banned(path, label):
    if not path.exists():
        return
    for p in path.rglob('*'):
        if is_quarantine(p):
            continue
        bad = BANNED.intersection(p.relative_to(path).parts)
        if bad:
            errors.append(f'forbidden label in {label}: {p} ({sorted(bad)})')


for entry in ROOT.iterdir():
    if entry.name in RETIRED_ROOTS:
        errors.append(f'retired pre-v9 root exists: {entry.name}')
    elif GEN_RE.fullmatch(entry.name):
        if not entry.is_dir():
            errors.append(f'generation root is not a directory: {entry}')
    elif entry.name not in STATIC_ROOTS:
        errors.append(f'non-canonical v9 root entry: {entry.name}')

projects = ROOT / 'projects'
if projects.exists():
    if not projects.is_dir():
        errors.append('projects root is not a directory')
    else:
        for project in children(projects):
            if not project.is_dir() or not PROJECT_RE.fullmatch(project.name):
                errors.append(f'invalid project id: {project}')

for gen in [p for p in ROOT.iterdir() if p.is_dir() and GEN_RE.fullmatch(p.name)]:
    for node in children(gen):
        if not node.is_dir():
            errors.append(f'invalid generation child: {node}')
            continue

        if node.name in GEN_BRANCHES:
            if node.name in {'TARGET', 'COMPARE', 'REFERENCE'}:
                check_slug_dirs(node, f'generation {node.name.lower()} id')
            reject_banned(node, f'{gen.name}/{node.name}')
            continue

        if not SLUG_RE.fullmatch(node.name) or node.name in BANNED:
            errors.append(f'invalid game id: {node}')
            continue

        for branch in children(node):
            if not branch.is_dir() or branch.name not in GAME_BRANCHES:
                errors.append(f'invalid game branch: {branch}')
                continue

            if branch.name == 'SOURCE':
                for platform in children(branch):
                    if not platform.is_dir() or not SLUG_RE.fullmatch(platform.name):
                        errors.append(f'invalid platform id: {platform}')
                        continue
                    for package in children(platform):
                        if not package.is_dir() or not SLUG_RE.fullmatch(package.name):
                            errors.append(f'invalid package kind: {package}')
                            continue
                        check_slug_dirs(package, 'release id')
            elif branch.name in {'TARGET', 'COMPARE', 'REFERENCE'}:
                check_slug_dirs(branch, f'{branch.name.lower()} id')

            reject_banned(branch, str(branch))

cross = ROOT / 'CROSS-GEN'
if cross.exists():
    for branch in children(cross):
        if not branch.is_dir() or branch.name not in CROSS_BRANCHES:
            errors.append(f'invalid CROSS-GEN branch: {branch}')
            continue
        if branch.name in {'TARGET', 'COMPARE', 'REFERENCE'}:
            check_slug_dirs(branch, f'cross-generation {branch.name.lower()} id')
        reject_banned(branch, str(branch))

if errors:
    print('Repository structure v9 validation failed:')
    for e in errors:
        print(f' - {e}')
    sys.exit(1)

print('Repository structure v9 validation passed.')
