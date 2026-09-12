# Repository Path Architecture V2

Status: proposed canonical replacement for the legacy `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE` layout.

## Why V2 is required

The existing five-level tree works for single-ROM research, but it cannot represent cross-generation, many-source-to-many-target projects without hiding the source/target relationship inside filenames or prose.

`Generation IV → ポケットモンスター` is the concrete counterexample: five Nintendo DS Generation IV releases are source baselines and five Japanese GBA Generation III releases are target baselines. Source research, target research, crosswalks, conversion design, target-specific implementation, and verification are different ownership roles and must not be collapsed into one GAME path.

V2 therefore separates immutable per-release knowledge from project-specific integration work.

---

## Top-level model

Both `Sakurai` and `Tsubaki` use the same logical top-level namespaces:

```text
LIBRARY/
PROJECTS/
INFRA/
```

- `LIBRARY`: canonical facts/assets that belong to one original release or an explicit cross-release comparison.
- `PROJECTS`: transformations, ports, integrations, patches, target-specific design, and project verification.
- `INFRA`: repository-wide schema, validators, migration tools, CI, naming rules, indexes.

ROM binaries are never committed.

---

# 1. LIBRARY

Canonical release path:

```text
LIBRARY/<GENERATION>/<PLATFORM>/<GAME>/<RELEASE-ID>/<REVISION>/<DOMAIN>/...
```

Canonical `RELEASE-ID`:

```text
<GAMECODE>-<LOCALE>
```

Examples:

```text
LIBRARY/GEN-IV/NDS/DIAMOND/ADAE-US-EN/REV-5/MANIFESTS/ROM-IDENTITY.md
LIBRARY/GEN-IV/NDS/PLATINUM/CPUK-KR-KO/REV-0/STRUCTURE/NITROFS/...
LIBRARY/GEN-IV/NDS/HEARTGOLD/IPKK-KR-KO/REV-0/DATA/...
LIBRARY/GEN-III/GBA/RUBY/AXVJ-JP-JA/REV-0/MANIFESTS/ROM-IDENTITY.md
LIBRARY/GEN-III/GBA/FIRERED/BPRJ-JP-JA/REV-1/STRUCTURE/...
```

The Game Code is structural because it is a direct cartridge/release identity key. Locale remains visible because Game Code alone is not a human-readable localization label and should not be overloaded with every regional/language rule.

### Cross-release library work

A comparison that is genuinely not owned by one ROM lives at the nearest common scope:

```text
LIBRARY/GEN-IV/NDS/_CROSS-RELEASE/<SUBJECT>/...
LIBRARY/GEN-III/GBA/_CROSS-RELEASE/<SUBJECT>/...
LIBRARY/GEN-III/_CROSS-PLATFORM/<SUBJECT>/...
```

Do not duplicate one-ROM data into `_CROSS-RELEASE`; store only comparison results, normalized matrices, and shared interpretations there.

---

# 2. PROJECTS

Cross-ROM work is not stored under a source generation or a target generation. It gets a project root.

```text
PROJECTS/<PROJECT-ID>/
```

For this project:

```text
PROJECTS/GEN4-TO-POCKET-MONSTERS/
```

Canonical project layout:

```text
PROJECTS/GEN4-TO-POCKET-MONSTERS/
├── MANIFESTS/
│   ├── source-roms.yaml
│   ├── target-roms.yaml
│   ├── release-aliases.yaml
│   └── provenance.yaml
├── CROSSWALK/
│   ├── POKEMON/
│   ├── FORMS/
│   ├── TYPES/
│   ├── ABILITIES/
│   ├── MOVES/
│   ├── ITEMS/
│   ├── EVOLUTION/
│   ├── BATTLE/
│   ├── ENCOUNTERS/
│   ├── TRAINERS/
│   ├── NPC/
│   ├── MAPS/
│   ├── EVENTS/
│   ├── TEXT/
│   ├── GRAPHICS/
│   ├── AUDIO/
│   ├── UI/
│   ├── SAVE/
│   ├── COMMUNICATION/
│   └── UNUSED/
├── DESIGN/
│   ├── ENGINE/
│   ├── DATA-EXPANSION/
│   ├── POINTERS/
│   ├── ROM-EXPANSION/
│   ├── SAVE-EXPANSION/
│   ├── GRAPHICS-CONVERSION/
│   └── COMPATIBILITY/
├── IMPLEMENTATION/
│   ├── _SHARED/
│   ├── AXVJ-JP-JA-REV-0/
│   ├── AXPJ-JP-JA-REV-0/
│   ├── BPEJ-JP-JA-REV-0/
│   ├── BPRJ-JP-JA-REV-1/
│   └── BPGJ-JP-JA-REV-0/
├── VERIFICATION/
│   ├── SOURCE-PARITY/
│   ├── TARGET-REGRESSION/
│   ├── CROSS-VERSION/
│   ├── SAVE-LOAD/
│   └── INTEGRATION/
├── TOOLS/
└── REPORTS/
```

`CROSSWALK` answers “what does Gen IV do and how does it map to the target architecture?”

`DESIGN` answers “how will the missing structure be added safely?”

`IMPLEMENTATION` owns actual target-facing tables, code, converted resources, patches, pointer maps, and insertion layouts.

`VERIFICATION` owns reproducibility and behavioral tests.

---

# 3. Current source ROM matrix

The currently attached Generation IV source baselines are:

| Role | Game | Platform | Locale | Game Code | Header revision | Size | SHA-1 |
|---|---|---|---|---|---:|---:|---|
| SOURCE | Diamond | NDS | US-EN | ADAE | 5 | 64 MiB | `a46233d8b79a69ea87aa295a0efad5237d02841e` |
| SOURCE | Pearl | NDS | US-EN | APAE | 5 | 64 MiB | `99083bf15ec7c6b81b4ba241ee10abd9e80999ac` |
| SOURCE | Platinum | NDS | KR-KO | CPUK | 0 | 128 MiB | `f811d9c7ab5262f593012da794c2fa81dbcdbcc1` |
| SOURCE | HeartGold | NDS | KR-KO | IPKK | 0 | 128 MiB | `5834fb3a2d751c48501d47d6a56898d7af6ccf9e` |
| SOURCE | SoulSilver | NDS | KR-KO | IPGK | 0 | 128 MiB | `0330e6449306606114a92bdbb3f9d3d51d392b96` |

`REV-5` above is the actual Nintendo DS header ROM-version byte for the attached Diamond/Pearl baselines. It must be recorded as a header identity fact; external dump-set naming is separate verification metadata.

# 4. Current target ROM matrix

The currently attached Japanese Generation III target baselines are:

| Role | Game | Platform | Locale | Game Code | Header revision | Size | SHA-1 |
|---|---|---|---|---|---:|---:|---|
| TARGET | Ruby | GBA | JP-JA | AXVJ | 0 | 8 MiB | `5c5e546720300b99ae45d2aa35c646c8b8ff5c56` |
| TARGET | Sapphire | GBA | JP-JA | AXPJ | 0 | 8 MiB | `3233342c2f3087e6ffe6c1791cd5867db07df842` |
| TARGET | Emerald | GBA | JP-JA | BPEJ | 0 | 16 MiB | `d7cf8f156ba9c455d164e1ea780a6bf1945465c2` |
| TARGET | FireRed | GBA | JP-JA | BPRJ | 1 | 16 MiB | `7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857` |
| TARGET | LeafGreen | GBA | JP-JA | BPGJ | 0 | 16 MiB | `5946f1b59e8d71cc61249661464d864185c92a5f` |

---

# 5. Repository responsibility split

## Sakurai

Stores research and reproducibility artifacts:

- ROM identity manifests and hashes
- extraction maps and filesystem structure
- normalized data tables
- disassembly/decompilation notes
- source/target diffs
- crosswalk tables
- design documents
- pointer maps and symbol maps
- scripts/tools
- tests and verification logs
- migration manifests
- reports

## Tsubaki

Stores implementation assets:

- extracted reusable graphics/audio resources where redistribution is appropriate
- converted sprites, tiles, palettes, UI resources
- insertion-ready binary data fragments that are not ROM images
- patches
- build resources
- generated tables used by builds
- target-specific converted assets

The logical `LIBRARY/...` and `PROJECTS/...` identities should mirror each other across both repositories, while the domains/files differ by repository responsibility.

---

# 6. Rules replacing the legacy five-level path

1. A ROM-intrinsic artifact belongs under `LIBRARY`, never under a project merely because a project first discovered it.
2. A cross-ROM transformation belongs under `PROJECTS`, never under one source game's folder.
3. Every release-specific library path contains PLATFORM and GAMECODE identity.
4. Source and target ROM binaries remain external/read-only; GitHub stores only identity metadata, analysis, patches, tools, and permissible assets.
5. Project implementation is target-owned. One source artifact can feed multiple target implementations without duplication.
6. Cross-version comparison uses `_CROSS-RELEASE` only for derived comparison artifacts, not as a dumping ground for copied files.
7. Old `MULTI`, `REV-ALL`, `LEGACY-*`, and source-bundle wrapper paths are migrated into either canonical LIBRARY ownership or PROJECTS ownership.
8. Git history preserves old locations; live duplicate trees are not retained solely for compatibility.

---

# 7. Migration order

1. Create `LIBRARY`, `PROJECTS`, and `INFRA` namespaces in both repositories.
2. Migrate immutable ROM identity manifests first.
3. Migrate one-ROM research/assets into release-specific `LIBRARY` paths.
4. Migrate DP/Pt/HGSS comparisons into `LIBRARY/GEN-IV/NDS/_CROSS-RELEASE` when they are pure research.
5. Migrate Gen IV → Gen III mapping/design/converted work into `PROJECTS/GEN4-TO-POCKET-MONSTERS`.
6. Split implementation by the five concrete Japanese target release IDs.
7. Remove obsolete live paths after verification; rely on Git history for provenance.
8. Update CI/path validators only after the new tree is populated and path-equivalence checks pass.

---

# 8. Immediate consequence for current repositories

The current `GENERATION-IV/<GAME>/<LOCALE>/<REV>/...` and `GENERATION-III/<GAME>/<LOCALE>/<REV>/...` roots should no longer be the final canonical ownership model.

Example migration:

```text
OLD:
GENERATION-IV/DIAMOND/US-EN/REV-5/MANIFESTS/ROM-IDENTITY.md

NEW:
LIBRARY/GEN-IV/NDS/DIAMOND/ADAE-US-EN/REV-5/MANIFESTS/ROM-IDENTITY.md
```

```text
OLD:
GENERATION-III/_SHARED/MULTI/REV-ALL/ANALYSIS/.../GEN4_IMPORT_V1/...

NEW, depending on content:
PROJECTS/GEN4-TO-POCKET-MONSTERS/CROSSWALK/GRAPHICS/...
PROJECTS/GEN4-TO-POCKET-MONSTERS/DESIGN/GRAPHICS-CONVERSION/...
PROJECTS/GEN4-TO-POCKET-MONSTERS/IMPLEMENTATION/_SHARED/GRAPHICS/...
```

This removes the central ambiguity of the old tree: whether an artifact belongs to the ROM being studied, the ROM receiving the port, or the relationship between them.
