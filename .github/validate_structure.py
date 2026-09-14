from pathlib import Path
import json
import sys

ROOT = Path('.')
ROM_SUFFIXES = {'.gb', '.gbc', '.gba', '.nds', '.3ds', '.cia', '.cci', '.cxi', '.xci', '.nsp', '.nca', '.iso', '.gcm', '.rvz', '.wbfs'}
REQUIRED_ROOT = {
    'README.md',
    'CONTRIBUTING.md',
    '.gitignore',
    '.gitattributes',
    '.editorconfig',
    '.github',
    'docs',
    'manifests',
    'projects',
    'shared',
    'derived',
}
REQUIRED_DOCS = {
    'README.md',
    'AGGREGATION_MODEL.md',
    'PROJECT_STATUS.md',
    'ROADMAP.md',
    'VERSIONS.md',
    'RESEARCH_GUIDE.md',
    'VERIFICATION.md',
    'REPOSITORY_STRUCTURE.md',
    'PROJECT_STANDARDS.md',
    'ASSET_WORKFLOW.md',
}
EXPECTED_COUNTS = {'disassembly': 12, 'decompilation': 34, 'total': 46}
errors = []

for name in sorted(REQUIRED_ROOT):
    if not (ROOT / name).exists():
        errors.append(f'missing required root entry: {name}')

for name in sorted(REQUIRED_DOCS):
    if not (ROOT / 'docs' / name).is_file():
        errors.append(f'missing required documentation file: docs/{name}')

for family in ('disassembly', 'decompilation'):
    if not (ROOT / 'projects' / family / 'README.md').is_file():
        errors.append(f'missing aggregate namespace: projects/{family}/README.md')

for namespace in ('shared', 'derived'):
    if not (ROOT / namespace / 'README.md').is_file():
        errors.append(f'missing aggregate namespace: {namespace}/README.md')

manifest_path = ROOT / 'manifests' / 'upstream-repositories.json'
if not (ROOT / 'manifests' / 'README.md').is_file():
    errors.append('missing manifest guide: manifests/README.md')
if not manifest_path.is_file():
    errors.append('missing upstream registry: manifests/upstream-repositories.json')
else:
    try:
        registry = json.loads(manifest_path.read_text(encoding='utf-8'))
        counts = registry.get('counts', {})
        for key, expected in EXPECTED_COUNTS.items():
            if counts.get(key) != expected:
                errors.append(f'upstream count mismatch for {key}: expected {expected}, got {counts.get(key)!r}')

        families = registry.get('families', {})
        names = []
        for family, expected in (('disassembly', 12), ('decompilation', 34)):
            generations = families.get(family, {}).get('generations', {})
            family_names = [name for repos in generations.values() for name in repos]
            if len(family_names) != expected:
                errors.append(f'{family} registry must contain {expected} repositories, found {len(family_names)}')
            names.extend(family_names)
        if len(names) != len(set(names)):
            errors.append('duplicate upstream repository name in registry')
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f'invalid upstream registry: {exc}')

if (ROOT / 'INFRA' / 'DOCS').exists():
    errors.append('legacy path must not be recreated: INFRA/DOCS')
if (ROOT / 'INFRA' / 'MANIFESTS').exists():
    errors.append('legacy path must not be recreated: INFRA/MANIFESTS')
if (ROOT / 'INFRA' / 'ARCHITECTURE').exists():
    errors.append('superseded versioned architecture tree must not be recreated: INFRA/ARCHITECTURE')

for path in ROOT.rglob('*'):
    if path.is_file() and path.suffix.lower() in ROM_SUFFIXES:
        errors.append(f'ROM image extension is forbidden: {path}')

if errors:
    print('Repository structure validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure validation passed.')
