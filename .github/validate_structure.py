from pathlib import Path
import re
import sys

ROOT = Path('.')
GAMES = ROOT / 'GAMES'
GEN_RE = re.compile(r'^GEN-\d{2}$')
LEGACY_GEN_RE = re.compile(r'^GENERATION-(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI)$')
GAME_RE = re.compile(r'^(?:_SHARED|[A-Z0-9][A-Z0-9-]*)$')
ID_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')
BRANCHES = {'RELEASES', 'COMPARISONS', 'PROJECTS', 'SHARED'}
WORK_TYPES = {
    'ANALYSIS','CENSUS','STRUCTURE','TEXT','DATA','DIFFS','TOOLS','TESTS',
    'VERIFICATION','REPORTS','LOCALIZATION','DISASSEMBLY','MANIFESTS','MAPS','SYMBOLS'
}
INFRA = {
    '.github','.git','.gitignore','.gitattributes','README.md','STRUCTURE.md',
    'MIGRATION.md','META','GAMES'
}

errors = []
warnings = []


def children(p):
    return [x for x in p.iterdir() if x.name != '.gitkeep'] if p.exists() else []


def require_dirs(parent, label, matcher=None, allowed=None):
    out = []
    for p in children(parent):
        valid_name = (allowed is None or p.name in allowed) and (matcher is None or matcher.fullmatch(p.name))
        if not p.is_dir() or not valid_name:
            errors.append(f'invalid {label}: {p}')
            continue
        out.append(p)
    return out


def require_work_types(parent, label):
    require_dirs(parent, label, allowed=WORK_TYPES)


for p in ROOT.iterdir():
    if p.name in INFRA:
        continue
    if LEGACY_GEN_RE.fullmatch(p.name) or GEN_RE.fullmatch(p.name):
        warnings.append(f'legacy pre-v3 generation root pending migration: {p.name}')
        continue
    errors.append(f'non-canonical root entry: {p.name}')

for gen in require_dirs(GAMES, 'generation', matcher=GEN_RE):
    for game in require_dirs(gen, 'game id', matcher=GAME_RE):
        branches = require_dirs(game, 'ownership branch', allowed=BRANCHES)
        for branch in branches:
            if game.name == '_SHARED' and branch.name == 'RELEASES':
                errors.append(f'generation-wide _SHARED cannot own RELEASES: {branch}')
                continue

            if branch.name == 'RELEASES':
                releases = require_dirs(branch, 'release id', matcher=ID_RE)
                for release in releases:
                    require_work_types(release, 'release work type')

            elif branch.name == 'COMPARISONS':
                comparisons = require_dirs(branch, 'comparison id', matcher=ID_RE)
                for comparison in comparisons:
                    require_work_types(comparison, 'comparison work type')

            elif branch.name == 'PROJECTS':
                projects = require_dirs(branch, 'project id', matcher=ID_RE)
                for project in projects:
                    sections = require_dirs(project, 'project section', allowed={'COMMON', 'TARGETS'})
                    for section in sections:
                        if section.name == 'COMMON':
                            require_work_types(section, 'project COMMON work type')
                        else:
                            targets = require_dirs(section, 'project target id', matcher=ID_RE)
                            for target in targets:
                                require_work_types(target, 'project target work type')

            else:  # SHARED
                require_work_types(branch, 'shared work type')

if warnings:
    print('Repository structure migration warnings:')
    for w in warnings:
        print(f' - {w}')

if errors:
    print('Repository structure validation failed:')
    for e in errors:
        print(f' - {e}')
    sys.exit(1)

print('Repository structure v3 validation passed.')
