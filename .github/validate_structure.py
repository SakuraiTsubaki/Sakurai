from pathlib import Path
import re
import sys

ROOT = Path('.')
LIBRARY = ROOT / 'LIBRARY'
PROJECTS = ROOT / 'PROJECTS'

GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')
CANONICAL_ROOTS = {
    'LIBRARY', 'PROJECTS', 'INFRA', '.github', '.git',
    '.gitignore', '.gitattributes', 'README.md', 'STRUCTURE.md', 'MIGRATION.md'
}
LEGACY_ROOT_NAMES = {'GAMES', 'META'}
GAME_BRANCHES = {'SOURCE', 'COMPARE', 'SHARED', 'REFERENCE'}
GEN_BRANCHES = {'COMPARE', 'SHARED', 'REFERENCE'}
PROJECT_SECTIONS = {
    'MANIFESTS', 'CROSSWALK', 'DESIGN', 'IMPLEMENTATION', 'PATCHES',
    'BUILD', 'TOOLS', 'REPORTS', 'VERIFICATION'
}
BANNED = {
    'MULTI', 'REV-ALL', 'ALL', 'MULTI-REGION', '_SHARED',
    'MISC', 'OTHER', 'GENERAL', 'REV-UNKNOWN'
}
IGNORED = {'.gitkeep', 'README.md', 'ROUTING.md', 'STRUCTURE.md'}

errors = []
warnings = []


def children(path):
    if not path.exists():
        return []
    return [p for p in path.iterdir() if p.name not in IGNORED]


def valid_slug(name):
    return bool(SLUG_RE.fullmatch(name)) and name not in BANNED


def require_slug_dirs(path, label):
    out = []
    for p in children(path):
        if not p.is_dir() or not valid_slug(p.name):
            errors.append(f'invalid {label}: {p}')
        else:
            out.append(p)
    return out


def reject_banned(path, label):
    if not path.exists():
        return
    for p in path.rglob('*'):
        if p.is_dir() and BANNED.intersection(p.relative_to(path).parts):
            errors.append(f'forbidden pseudo-owner in canonical {label}: {p}')


for p in ROOT.iterdir():
    if p.name in CANONICAL_ROOTS:
        continue
    if p.name in LEGACY_ROOT_NAMES or p.name.startswith('GENERATION-') or GEN_RE.fullmatch(p.name):
        warnings.append(f'legacy root pending v5 migration: {p.name}')
        continue
    if p.is_file() and p.suffix.lower() == '.md':
        warnings.append(f'top-level metadata document pending INFRA routing: {p.name}')
        continue
    errors.append(f'non-canonical root entry: {p.name}')

# v5: LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM>/<PACKAGE>/<RELEASE>/...
for gen in children(LIBRARY):
    if not gen.is_dir() or not GEN_RE.fullmatch(gen.name):
        errors.append(f'invalid library generation: {gen}')
        continue
    for node in children(gen):
        if node.name in GEN_BRANCHES:
            if node.name == 'COMPARE':
                require_slug_dirs(node, 'generation comparison id')
            continue
        if not node.is_dir() or not valid_slug(node.name):
            errors.append(f'invalid game id: {node}')
            continue
        branch_names = {p.name for p in children(node) if p.is_dir()}
        if not branch_names.intersection(GAME_BRANCHES):
            # old v4 platform-first subtree (for example GEN-01/GB/RED) remains migration input.
            warnings.append(f'legacy pre-v5 library subtree pending migration: {node}')
            continue
        for branch in children(node):
            if not branch.is_dir() or branch.name not in GAME_BRANCHES:
                warnings.append(f'non-v5 game child pending classification: {branch}')
                continue
            if branch.name == 'SOURCE':
                for platform in require_slug_dirs(branch, 'platform id'):
                    for package in require_slug_dirs(platform, 'package kind'):
                        require_slug_dirs(package, 'release id')
                reject_banned(branch, 'source path')
            elif branch.name == 'COMPARE':
                require_slug_dirs(branch, 'comparison id')
                reject_banned(branch, 'comparison path')

# PROJECTS/<PROJECT-ID>/<section>/...
for project in children(PROJECTS):
    if not project.is_dir() or not valid_slug(project.name):
        errors.append(f'invalid project id: {project}')
        continue
    for section in children(project):
        if not section.is_dir() or section.name not in PROJECT_SECTIONS:
            warnings.append(f'project child pending v5 classification: {section}')
    reject_banned(project, 'project path')

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
