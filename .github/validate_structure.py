from pathlib import Path
import re
import sys

ROOT = Path('.')
LIBRARY = ROOT / 'LIBRARY'
PROJECTS = ROOT / 'PROJECTS'
INFRA_ROOT = ROOT / 'INFRA'

GEN_RE = re.compile(r'^GEN-\d{2}$')
PLATFORM_RE = re.compile(r'^[A-Z0-9][A-Z0-9-]*$')
GAME_RE = re.compile(r'^(?:_SHARED|[A-Z0-9][A-Z0-9-]*)$')
ID_RE = re.compile(r'^[A-Z0-9][A-Z0-9._-]*$')
RELEASE_ID_RE = re.compile(r'^[A-Z0-9][A-Z0-9._-]*$')

LIBRARY_BRANCHES = {'RELEASES', 'COMPARISONS', 'SHARED'}
RELEASE_DOMAINS = {
    'MANIFESTS','DUMPS','ANALYSIS','CENSUS','STRUCTURE','DATA','TEXT','GRAPHICS',
    'AUDIO','MAPS','EVENTS','DISASSEMBLY','SYMBOLS','TOOLS','VERIFICATION','REPORTS',
    'LOCALIZATION','TESTS'
}
PROJECT_DOMAINS = {
    'MANIFESTS','CROSSWALK','DESIGN','IMPLEMENTATION','VERIFICATION','TOOLS','REPORTS'
}
INFRA_DOMAINS = {'REGISTRY','SCHEMAS','VALIDATORS','MIGRATION','TOOLS','CI'}
ROOT_CANONICAL = {
    '.github','.git','.gitignore','.gitattributes','README.md','STRUCTURE.md','MIGRATION.md',
    'LIBRARY','PROJECTS','INFRA'
}
ROOT_LEGACY = {'GAMES','META'}
LEGACY_GEN_RE = re.compile(r'^(?:GENERATION-(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI)|GEN-\d{2})$')

errors = []
warnings = []


def children(path):
    return [p for p in path.iterdir() if p.name != '.gitkeep'] if path.exists() else []


def require_dirs(parent, label, matcher=None, allowed=None):
    out = []
    for p in children(parent):
        valid = p.is_dir()
        if allowed is not None:
            valid = valid and p.name in allowed
        if matcher is not None:
            valid = valid and bool(matcher.fullmatch(p.name))
        if not valid:
            errors.append(f'invalid {label}: {p}')
        else:
            out.append(p)
    return out


for p in ROOT.iterdir():
    if p.name in ROOT_CANONICAL:
        continue
    if p.name in ROOT_LEGACY or LEGACY_GEN_RE.fullmatch(p.name):
        warnings.append(f'legacy pre-v4 root pending migration: {p.name}')
        continue
    errors.append(f'non-canonical root entry: {p.name}')

# LIBRARY: official release facts, dump observations, comparisons, shared game facts.
for gen in require_dirs(LIBRARY, 'library generation', matcher=GEN_RE):
    for platform in require_dirs(gen, 'platform', matcher=PLATFORM_RE):
        for game in require_dirs(platform, 'game id', matcher=GAME_RE):
            for branch in require_dirs(game, 'library ownership branch', allowed=LIBRARY_BRANCHES):
                if game.name == '_SHARED' and branch.name == 'RELEASES':
                    errors.append(f'generation/platform _SHARED cannot own RELEASES: {branch}')
                    continue
                if branch.name == 'RELEASES':
                    for release in require_dirs(branch, 'release id', matcher=RELEASE_ID_RE):
                        require_dirs(release, 'release domain', allowed=RELEASE_DOMAINS)
                elif branch.name == 'COMPARISONS':
                    for comparison in require_dirs(branch, 'comparison id', matcher=ID_RE):
                        require_dirs(comparison, 'comparison domain', allowed=RELEASE_DOMAINS - {'DUMPS'})
                else:  # SHARED
                    require_dirs(branch, 'shared library domain', allowed=RELEASE_DOMAINS - {'DUMPS'})

# PROJECTS: transformations may cross releases, games, platforms, and generations.
for project in require_dirs(PROJECTS, 'project id', matcher=ID_RE):
    require_dirs(project, 'project domain', allowed=PROJECT_DOMAINS)

# INFRA: repository-wide registries/schemas/validators/migration support.
require_dirs(INFRA_ROOT, 'infra domain', allowed=INFRA_DOMAINS)

if warnings:
    print('Repository structure v4 migration warnings:')
    for warning in warnings:
        print(f' - {warning}')

if errors:
    print('Repository structure v4 validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure v4 validation passed.')
