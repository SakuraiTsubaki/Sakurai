# Repository Structure v4

Status: **canonical**. This replaces the v3 `GAMES/...` model before large-scale migration begins.

## Core rule

The repository has two different kinds of identity and they must never be collapsed:

1. **RELEASE** — the official software/build identity being studied.
2. **DUMP** — the exact ROM/executable image actually supplied or observed, with its own hash, provenance, and quality status.

A project is a third concern: it consumes one or more releases and produces derived work. Cross-generation projects therefore live outside any one game's tree.

Original ROM/executable binaries are never committed.

## Why v4 is required

The currently supplied project ROMs expose three weaknesses in v3:

- Generation V Black/White are supplied as SweeTnDs-era images whose internal game codes identify real BW releases, while the exact supplied dumps are separately classified as non-canonical/bad or incomplete. Release identity and dump identity are therefore not the same thing.
- `Generation V -> Pocket Monsters` consumes Generation V sources and targets multiple Generation II/III builds. A cross-generation many-to-many project cannot truthfully be owned by one `GAMES/GEN-XX/<GAME>/PROJECTS` path.
- Platform-native identity differs. GBA/NDS have useful game codes; GB/GBC do not provide the same universal four-character game-code model. One release-ID grammar must allow platform-specific native identity rather than inventing pseudo-codes.

## Canonical roots

```text
LIBRARY/
PROJECTS/
INFRA/
.github/
README.md
STRUCTURE.md
MIGRATION.md
```

- `LIBRARY` = facts and permissible assets owned by original official releases.
- `PROJECTS` = transformations, ports, integrations, modernization, patches, and project-specific verification.
- `INFRA` = repository-wide release registries, schemas, validators, migration maps, shared tooling, and CI support.

Legacy roots such as `GENERATION-*`, standalone `GEN-*`, `GAMES/`, `MULTI`, and `REV-ALL` are migration sources only.

# 1. LIBRARY

Canonical game root:

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/
├── RELEASES/
├── COMPARISONS/
└── SHARED/
```

Example:

```text
LIBRARY/GEN-03/GBA/RUBY/
LIBRARY/GEN-05/NDS/BLACK/
LIBRARY/GEN-02/GBC/CRYSTAL/
```

## RELEASES

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/RELEASES/<RELEASE-ID>/
├── MANIFESTS/
├── DUMPS/
├── ANALYSIS/
├── STRUCTURE/
├── DATA/
├── TEXT/
├── GRAPHICS/
├── AUDIO/
├── MAPS/
├── EVENTS/
├── DISASSEMBLY/
├── SYMBOLS/
├── TOOLS/
└── VERIFICATION/
```

A release path represents one official software build, not one filename from a dump set.

### Release-ID grammar

Release IDs are unique **within one game root** and use the strongest platform-native identity available.

For GBA and NDS/TWL:

```text
<GAME-CODE>-R<HEADER-VERSION>
```

Examples:

```text
AXVJ-R0   # Ruby Japan
AXVE-R2   # Ruby English USA/Europe Rev 2
BPRJ-R1   # FireRed Japan Rev 1
IRBO-R0   # Black English O-code USA/Europe
IRAO-R0   # White English O-code USA/Europe
```

For GB/GBC, where the same four-character game-code scheme does not exist:

```text
<MARKET>-<LANGUAGE>-HV<HEADER-VERSION>
```

Examples:

```text
KR-KO-HV0       # Gold/Silver Korean build within the corresponding game root
JP-JA-HV0       # Crystal Japan
US-EU-EN-HV1    # Crystal English USA/Europe header version 1 / Rev A
```

If a future platform provides a stronger native title/build identifier, use that native identifier plus the official software/update version. Do not force cartridge-style `REV-*` onto platforms that do not use it.

Locale, language set, product code, title ID, cartridge flags, revision labels used by preservation sets, and all hashes remain explicit manifest fields even when some are also encoded in the human-readable release ID.

## DUMPS

Exact observed files are children of a release:

```text
.../RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/
```

Recommended dump ID:

```text
<PROVENANCE>-<SHA1-PREFIX>
```

Example:

```text
LIBRARY/GEN-05/NDS/BLACK/RELEASES/IRBO-R0/DUMPS/SWEETNDS-a68b3bed/
LIBRARY/GEN-05/NDS/WHITE/RELEASES/IRAO-R0/DUMPS/SWEETNDS-f94d4578/
```

`DUMPS/<DUMP-ID>/MANIFESTS/dump.yaml` records the original supplied filename, complete hashes, source/provenance, preservation classification, header observations, and whether conclusions may be promoted to release-level facts.

A bad, trimmed, incomplete, overdumped, or otherwise non-canonical image never creates a fake official release. It remains a dump observation attached to the real release identity when that binding is supportable.

## COMPARISONS

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/COMPARISONS/<COMPARISON-ID>/...
```

Use this for relationships between two or more releases of the same game. Generation-wide comparisons use the reserved game scope `_SHARED`:

```text
LIBRARY/GEN-05/NDS/_SHARED/COMPARISONS/BLACK-IRBO-R0--WHITE-IRAO-R0/...
LIBRARY/GEN-02/GBC/_SHARED/COMPARISONS/GSC-JP-EN-KR/...
```

`MULTI`, `REV-ALL`, `ALL`, `MULTI-REGION`, and similar pseudo-release owners are forbidden in new canonical paths.

## SHARED

```text
LIBRARY/GEN-XX/<PLATFORM>/<GAME-ID>/SHARED/...
```

Use only for material that is genuinely independent of one exact release, such as a game-wide schema, generic parser, or terminology map. Release-specific facts must stay with their release.

# 2. PROJECTS

Cross-release and cross-generation transformations live here:

```text
PROJECTS/<PROJECT-ID>/
├── MANIFESTS/
├── CROSSWALK/
├── DESIGN/
├── IMPLEMENTATION/
├── VERIFICATION/
├── TOOLS/
└── REPORTS/
```

For the current project:

```text
PROJECTS/GEN5-TO-POCKET-MONSTERS/
```

### MANIFESTS

Project manifests reference canonical library releases; they do not duplicate the original research tree.

```text
MANIFESTS/
├── source-set.yaml
├── target-set.yaml
├── release-lock.yaml
├── provenance.yaml
└── status.yaml
```

### CROSSWALK

Domain-by-domain Generation V -> target mapping:

```text
POKEMON/
FORMS/
TYPES/
ABILITIES/
MOVES/
ITEMS/
EVOLUTION/
BATTLE/
ENCOUNTERS/
TRAINERS/
NPC/
MAPS/
EVENTS/
TEXT/
GRAPHICS/
ANIMATION/
AUDIO/
UI/
SAVE/
COMMUNICATION/
TIME-DATE-SEASONS/
UNUSED/
```

### DESIGN

```text
ENGINE/
DATA-MODEL/
ROM-EXPANSION/
POINTERS/
SAVE-EXPANSION/
GRAPHICS-CONVERSION/
AUDIO-CONVERSION/
SCRIPTING/
COMPATIBILITY/
```

### IMPLEMENTATION

```text
IMPLEMENTATION/
├── _SHARED/
└── <TARGET-ID>/
```

`TARGET-ID` is project-local but must resolve unambiguously to one canonical release in `MANIFESTS/release-lock.yaml`.

# 3. Current release bindings

The currently supplied Generation V sources bind to:

```text
LIBRARY/GEN-05/NDS/BLACK/RELEASES/IRBO-R0/
LIBRARY/GEN-05/NDS/WHITE/RELEASES/IRAO-R0/
```

The supplied SweeTnDs files are dump observations under those releases, not the canonical releases themselves.

The currently supplied target baseline set spans:

```text
GEN-02/GBC: GOLD, SILVER, CRYSTAL
GEN-03/GBA: RUBY, SAPPHIRE, EMERALD, FIRERED, LEAFGREEN
```

Exact release IDs and hashes are locked in `INFRA/REGISTRY/ROM-SETS/` and in the project release lock.

Black 2 / White 2 remain required by the Generation V project scope, but no release path is fabricated until an actual official-build identity is bound to a supplied/verified source. Missing required inputs are tracked in project status metadata rather than represented by fake ROM folders.

# 4. Sakurai ownership

Sakurai is the research, reverse-engineering, documentation, and verification source of truth. Typical domains include:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `DATA`, `TEXT`, `DISASSEMBLY`, `SYMBOLS`, `MAPS`, `EVENTS`, `LOCALIZATION`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `MANIFESTS`.

# 5. Repository pair contract

Sakurai and Tsubaki use identical `LIBRARY` release IDs, project IDs, and target IDs.

- Sakurai owns identity manifests, research, crosswalks, design specifications, scripts, and verification evidence.
- Tsubaki owns production assets, converted resources, build inputs, patches, and generated implementation artifacts.

A file's repository is determined by artifact responsibility; its release/project identity must not change between repositories.

# 6. Migration invariant

Every migrated artifact must have exactly one truthful owner:

- original-release fact -> `LIBRARY/.../RELEASES`
- exact supplied-file observation -> `LIBRARY/.../RELEASES/.../DUMPS`
- release relationship -> `LIBRARY/.../COMPARISONS`
- derived port/integration/modernization -> `PROJECTS/...`
- repository-wide schema/registry/migration tool -> `INFRA/...`

Do not keep duplicate live copies solely to preserve old paths. Git history is the archive.