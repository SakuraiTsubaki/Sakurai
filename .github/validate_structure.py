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
INFRA = {'.github','.git','.gitignore','.gitattributes','README.md','STRUCTURE.md','MIGRATION.md','META','GAMES'}
errors = []

def children(p):
    return [x for x in p.iterdir() if x.name != '.gitkeep'] if p.exists() else []

def require_dirs(parent, label, matcher=None, allowed=None):
    out = []
    for p in children(parent):
        valid = (allowed is None or p.name in allowed) and (matcher is None or matcher.fullmatch(p.name))
        if not p.is_dir() or not valid:
            errors.append(f'invalid {label}: {p}')
        else:
            out.append(p)
    return out

def require_work_types(parent, label):
    require_dirs(parent, label, allowed=WORK_TYPES)

for p in ROOT.iterdir():
    if p.name in INFRA:
        continue
    if LEGACY_GEN_RE.fullmatch(p.name) or GEN_RE.fullmatch(p.name):
        errors.append(f'legacy pre-v3 generation root is forbidden: {p.name}')
    else:
        errors.append(f'non-canonical root entry: {p.name}')

for gen in require_dirs(GAMES, 'generation', matcher=GEN_RE):
    for game in require_dirs(gen, 'game id', matcher=GAME_RE):
        for branch in require_dirs(game, 'ownership branch', allowed=BRANCHES):
            if game.name == '_SHARED' and branch.name == 'RELEASES':
                errors.append(f'generation-wide _SHARED cannot own RELEASES: {branch}')
            elif branch.name == 'RELEASES':
                for release in require_dirs(branch, 'release id', matcher=ID_RE):
                    require_work_types(release, 'release work type')
            elif branch.name == 'COMPARISONS':
                for comparison in require_dirs(branch, 'comparison id', matcher=ID_RE):
                    require_work_types(comparison, 'comparison work type')
            elif branch.name == 'PROJECTS':
                for project in require_dirs(branch, 'project id', matcher=ID_RE):
                    for section in require_dirs(project, 'project section', allowed={'COMMON','TARGETS'}):
                        if section.name == 'COMMON':
                            require_work_types(section, 'project COMMON work type')
                        else:
                            for target in require_dirs(section, 'project target id', matcher=ID_RE):
                                require_work_types(target, 'project target work type')
            else:
                require_work_types(branch, 'shared work type')

if errors:
    print('Repository structure v3 validation failed:')
    for e in errors:
        print(f' - {e}')
    sys.exit(1)
print('Repository structure v3 validation passed.')
