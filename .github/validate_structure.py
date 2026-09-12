from pathlib import Path
import re
import sys

ROOT = Path('.')
GENERATIONS = {
    'GENERATION-I': {'RED','GREEN','BLUE','YELLOW'},
    'GENERATION-II': {'GOLD','SILVER','CRYSTAL'},
    'GENERATION-III': {'RUBY','SAPPHIRE','EMERALD','FIRERED','LEAFGREEN'},
    'GENERATION-IV': {'DIAMOND','PEARL','PLATINUM','HEARTGOLD','SOULSILVER'},
    'GENERATION-V': {'BLACK','WHITE','BLACK2','WHITE2'},
    'GENERATION-VI': {'X','Y','OMEGARUBY','ALPHASAPPHIRE'},
    'GENERATION-VII': {'SUN','MOON','ULTRASUN','ULTRAMOON','LETSGO-PIKACHU','LETSGO-EEVEE'},
    'GENERATION-VIII': {'SWORD','SHIELD','BRILLIANTDIAMOND','SHININGPEARL','LEGENDS-ARCEUS'},
    'GENERATION-IX': {'SCARLET','VIOLET','LEGENDS-Z-A'},
}
LOCALES = {'JP-JA','KR-KO','US-EN','EU-EN','EU-DE','EU-FR','EU-IT','EU-ES','MULTI'}
WORK_TYPES = {'ANALYSIS','CENSUS','STRUCTURE','TEXT','DATA','DIFFS','TOOLS','TESTS','VERIFICATION','REPORTS','LOCALIZATION','DISASSEMBLY','MANIFESTS','MAPS','SYMBOLS'}
ROOT_ALLOWED = set(GENERATIONS) | {'.github','README.md','STRUCTURE.md','MIGRATION.md','.git'}
REV_RE = re.compile(r'^REV-(?:ALL|[A-Z]|\d+)$')

# Generation IV has completed the second-stage semantic normalization.  Other
# generations can be added here as their old below-WORK-TYPE replicas are
# dismantled.
STRICT_SEMANTIC_GENERATIONS = {'GENERATION-IV'}
LEGACY_ROLE_DIRS = {
    'USA', 'KOREA', 'KO-KR', 'MULTI-REGION', 'MULTI-REV', 'REV-MIXED',
    'REV-UNKNOWN', 'REV-COMMON', 'ALL-REVISIONS', 'ALL', 'MIGRATED',
}
ALL_GAME_NAMES = set().union(*GENERATIONS.values()) | {'_SHARED'}

errors = []
for p in ROOT.iterdir():
    if p.name not in ROOT_ALLOWED:
        errors.append(f'non-canonical root entry: {p.name}')

for gen, games in GENERATIONS.items():
    gp = ROOT / gen
    if not gp.exists():
        errors.append(f'missing generation root: {gen}')
        continue
    for game in gp.iterdir():
        if game.name == '.gitkeep':
            continue
        if not game.is_dir() or game.name not in games | {'_SHARED'}:
            errors.append(f'invalid GAME path: {game}')
            continue
        for locale in game.iterdir():
            if locale.name == '.gitkeep':
                continue
            if not locale.is_dir() or locale.name not in LOCALES:
                errors.append(f'invalid LANGUAGE/REGION path: {locale}')
                continue
            for rev in locale.iterdir():
                if rev.name == '.gitkeep':
                    continue
                if not rev.is_dir() or not REV_RE.fullmatch(rev.name):
                    errors.append(f'invalid REV path: {rev}')
                    continue
                for work in rev.iterdir():
                    if work.name == '.gitkeep':
                        continue
                    if not work.is_dir() or work.name not in WORK_TYPES:
                        errors.append(f'invalid WORK TYPE path: {work}')
                        continue
                    if gen not in STRICT_SEMANTIC_GENERATIONS:
                        continue
                    for nested in work.rglob('*'):
                        if not nested.is_dir():
                            continue
                        name = nested.name
                        if name in WORK_TYPES:
                            errors.append(f'repeated WORK TYPE below canonical WORK TYPE: {nested}')
                        if name in LOCALES or name in ALL_GAME_NAMES or REV_RE.fullmatch(name):
                            errors.append(f'repeated structural role below WORK TYPE: {nested}')
                        if name in LEGACY_ROLE_DIRS or name.startswith('LEGACY-'):
                            errors.append(f'legacy structural replica below WORK TYPE: {nested}')

if errors:
    print('Repository structure validation failed:')
    for e in errors:
        print(f' - {e}')
    sys.exit(1)
print('Repository structure validation passed.')
