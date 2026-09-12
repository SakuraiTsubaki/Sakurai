from pathlib import Path
import re
import sys

ROOT = Path('.')
LIBRARY = ROOT / 'LIBRARY'
PROJECTS = ROOT / 'PROJECTS'

GEN_RE = re.compile(r'^GEN-\d{2}$')
SLUG_RE = re.compile(r'^[A-Z0-9][A-Z0-9.-]*$')
PROJECT_RE = SLUG_RE

CANONICAL_ROOTS = {'LIBRARY','PROJECTS','INFRA','.github','.git','.gitignore','.gitattributes','README.md','STRUCTURE.md','MIGRATION.md'}
LEGACY_ROOT_NAMES = {'GAMES','META'}
LEGACY_PLATFORM_NODES = {'GB','GBC','GBA','NDS','NDS-NTR','NDS-TWL','3DS','SWITCH','SWITCH2'}
GENERATION_BRANCHES = {'COMPARE','SHARED','REFERENCE'}
GAME_BRANCHES = {'SOURCE','COMPARE','SHARED','REFERENCE'}
PACKAGE_KINDS = {'CART','DIGITAL','DISC','UPDATE','DLC','DEMO','DISTRIBUTION'}
RELEASE_SECTIONS = {'IDENTITY','DUMPS','NATIVE','DOMAINS','TOOLS','REPORTS','VERIFICATION'}
DUMP_SECTIONS = {'IDENTITY','OBSERVATIONS','NATIVE','VERIFICATION'}
PROJECT_SECTIONS = {'MANIFESTS','CROSSWALK','DESIGN','SOURCE','NORMALIZED','CONVERTED','IMPLEMENTATION','PATCHES','BUILD','TOOLS','REPORTS','VERIFICATION','DIFFS'}
BANNED_V5_SEGMENTS = {'MULTI','REV-ALL','ALL','MULTI-REGION','_SHARED','MISC','OTHER','GENERAL','REV-UNKNOWN'}
IGNORED_METADATA_FILES = {'.gitkeep','README.md','ROUTING.md','STRUCTURE.md'}
errors=[]
warnings=[]

def children(path):
    if not path.exists(): return []
    return [p for p in path.iterdir() if p.name not in IGNORED_METADATA_FILES]

def dirs_only(parent,label,matcher=None,allowed=None,warn_unknown=False):
    out=[]
    for p in children(parent):
        if not p.is_dir():
            errors.append(f'invalid {label}: {p}')
            continue
        valid=(allowed is None or p.name in allowed) and (matcher is None or matcher.fullmatch(p.name))
        if not valid:
            (warnings if warn_unknown else errors).append(f'{"legacy/unmigrated" if warn_unknown else "invalid"} {label}: {p}')
            continue
        out.append(p)
    return out

def reject_banned(root,label):
    if not root.exists(): return
    for p in root.rglob('*'):
        if not p.is_dir(): continue
        bad=BANNED_V5_SEGMENTS.intersection(p.relative_to(root).parts)
        if bad: errors.append(f'forbidden v5 segment in {label}: {p} ({sorted(bad)})')

def validate_release(release):
    sections=dirs_only(release,'release section',allowed=RELEASE_SECTIONS)
    if 'IDENTITY' not in {p.name for p in sections}: errors.append(f'v5 source release missing IDENTITY: {release}')
    dumps=release/'DUMPS'
    if dumps.exists():
        for dump in dirs_only(dumps,'dump id',matcher=SLUG_RE):
            dirs_only(dump,'dump section',allowed=DUMP_SECTIONS)

def validate_source(source):
    for platform in dirs_only(source,'platform id',matcher=SLUG_RE):
        for package in dirs_only(platform,'package kind',allowed=PACKAGE_KINDS):
            for release in dirs_only(package,'release id',matcher=SLUG_RE): validate_release(release)

def validate_game(game):
    reject_banned(game,f'game {game.name}')
    for branch in dirs_only(game,'game branch',allowed=GAME_BRANCHES):
        if branch.name=='SOURCE': validate_source(branch)
        elif branch.name in {'COMPARE','REFERENCE'}: dirs_only(branch,f'{branch.name.lower()} id',matcher=SLUG_RE)

for p in ROOT.iterdir():
    if p.name in CANONICAL_ROOTS: continue
    if p.name in LEGACY_ROOT_NAMES or p.name.startswith('GENERATION-') or GEN_RE.fullmatch(p.name):
        warnings.append(f'legacy pre-v5 root pending migration: {p.name}'); continue
    if p.is_file() and p.suffix.lower()=='.md':
        warnings.append(f'top-level metadata document pending INFRA routing: {p.name}'); continue
    errors.append(f'non-canonical root entry: {p.name}')

for gen in dirs_only(LIBRARY,'library generation',matcher=GEN_RE):
    for node in children(gen):
        if not node.is_dir(): errors.append(f'invalid generation child: {node}'); continue
        if node.name in LEGACY_PLATFORM_NODES:
            warnings.append(f'legacy v4 platform-first library node pending migration: {node}'); continue
        if node.name in GENERATION_BRANCHES:
            if node.name in {'COMPARE','REFERENCE'}: dirs_only(node,f'generation {node.name.lower()} id',matcher=SLUG_RE)
            continue
        if not SLUG_RE.fullmatch(node.name): errors.append(f'invalid game id: {node}'); continue
        validate_game(node)

for project in dirs_only(PROJECTS,'project id',matcher=PROJECT_RE):
    dirs_only(project,'project section',allowed=PROJECT_SECTIONS,warn_unknown=True)

if warnings:
    print('Repository v5 migration warnings:')
    for warning in warnings: print(f' - {warning}')
if errors:
    print('Repository structure v5 validation failed:')
    for error in errors: print(f' - {error}')
    sys.exit(1)
print('Repository structure v5 validation passed.')
