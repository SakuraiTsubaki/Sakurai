# Pokémon Green path design — v3

## Verified source set

This game currently has two verified Japanese Game Boy source ROM identities:

| Release ID | Header version | Size | SHA-1 |
|---|---:|---:|---|
| `GB-JP-JA-REV-0` | 0 | 524288 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` |
| `GB-JP-JA-REV-A` | 1 | 524288 | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` |

Both report `POKEMON GREEN`, Japanese destination code, SGB flag `0x03`, 32 × 16 KiB banks, and 512 KiB ROM size. SGB enhancement is a release attribute and does not create another path branch.

## Canonical Green tree

```text
GAMES/GEN-01/GREEN/
├── RELEASES/
│   ├── GB-JP-JA-REV-0/
│   │   ├── MANIFESTS/
│   │   ├── ANALYSIS/
│   │   ├── DISASSEMBLY/
│   │   ├── DATA/
│   │   ├── TEXT/
│   │   ├── MAPS/
│   │   ├── SYMBOLS/
│   │   └── TESTS/
│   └── GB-JP-JA-REV-A/
│       └── ...
├── COMPARISONS/
│   └── GB-JP-JA-REV-0--GB-JP-JA-REV-A/
│       ├── ANALYSIS/
│       ├── DIFFS/
│       ├── REPORTS/
│       └── VERIFICATION/
├── PROJECTS/
│   └── MODERNIZATION/
│       ├── COMMON/
│       │   ├── ANALYSIS/
│       │   ├── DATA/
│       │   ├── LOCALIZATION/
│       │   ├── REPORTS/
│       │   └── TESTS/
│       └── TARGETS/
│           ├── GB-JP-JA-REV-0/
│           └── GB-JP-JA-REV-A/
└── SHARED/
    ├── STRUCTURE/
    ├── TOOLS/
    └── VERIFICATION/
```

Directories are created only when they contain real files; this tree documents allowed ownership, not mandatory empty folders.

## Legacy routing

```text
GENERATION-I/GREEN/JP-JA/REV-0/<WORK-TYPE>/...
  -> RELEASES/GB-JP-JA-REV-0/<WORK-TYPE>/...

GENERATION-I/GREEN/JP-JA/REV-A/<WORK-TYPE>/...
  -> RELEASES/GB-JP-JA-REV-A/<WORK-TYPE>/...

GENERATION-I/GREEN/JP-JA/REV-ALL/<WORK-TYPE>/...
  -> COMPARISONS/GB-JP-JA-REV-0--GB-JP-JA-REV-A/<WORK-TYPE>/...
```

`REV-ALL` is not a release. Every old file under that scope must be classified as a comparison, project artifact, or genuinely shared file before migration.

## Ownership rules

- Facts derived from exactly one ROM belong to that `RELEASES/<RELEASE-ID>`.
- A delta, equivalence audit, or result requiring both ROMs belongs to the explicit `COMPARISONS` pair.
- Modernized data, restored unused content, bug fixes, engine expansion, and derived builds belong to `PROJECTS`, even when based on one source release.
- Generic tooling or conventions that remain valid regardless of source revision belong to `SHARED`.
- Raw ROM bytes never enter GitHub; exact hashes and header identity are sufficient to bind local source files to repository work.

## Cross-repository identity

Tsubaki must reuse the same release IDs and project IDs when production assets or patches are generated. Do not rename `GB-JP-JA-REV-0` or `GB-JP-JA-REV-A` in the production repository.
