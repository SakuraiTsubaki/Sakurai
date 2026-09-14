from pathlib import Path
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
}
REQUIRED_DOCS = {
    'README.md',
    'PROJECT_STATUS.md',
    'ROADMAP.md',
    'VERSIONS.md',
    'RESEARCH_GUIDE.md',
    'VERIFICATION.md',
    'REPOSITORY_STRUCTURE.md',
    'PROJECT_STANDARDS.md',
    'ASSET_WORKFLOW.md',
}
errors = []

for name in sorted(REQUIRED_ROOT):
    if not (ROOT / name).exists():
        errors.append(f'missing required root entry: {name}')

for name in sorted(REQUIRED_DOCS):
    if not (ROOT / 'docs' / name).is_file():
        errors.append(f'missing required documentation file: docs/{name}')

if not (ROOT / 'manifests' / 'README.md').is_file():
    errors.append('missing manifest guide: manifests/README.md')

if (ROOT / 'INFRA' / 'DOCS').exists():
    errors.append('legacy path must not be recreated: INFRA/DOCS')

if (ROOT / 'INFRA' / 'MANIFESTS').exists():
    errors.append('legacy path must not be recreated: INFRA/MANIFESTS')

for path in ROOT.rglob('*'):
    if path.is_file() and path.suffix.lower() in ROM_SUFFIXES:
        errors.append(f'ROM image extension is forbidden: {path}')

if errors:
    print('Repository structure validation failed:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('Repository structure validation passed.')
