# Repository Structure v5

Status: **canonical**. v5 replaces the v4 `LIBRARY/GEN-XX/<PLATFORM>/<GAME>/RELEASES/...` layout.

The redesign is based on the actual supplied source ROMs, not on filename conventions alone. The two current Generation V sources expose a hybrid NTR/TWL cartridge layout, exact dump provenance, a large ARM9 overlay set, NitroFS/NARC containers, embedded child ROMs, and substantial Black/White byte-level sharing. The repository therefore separates **identity**, **exact dump observation**, **platform-native physical structure**, and **semantic game domains**.

Original ROM/executable binaries are never committed.

## 0. Canonical roots

```text
LIBRARY/
PROJECTS/
INFRA/
.github/
README.md
STRUCTURE.md
MIGRATION.md
```

- `LIBRARY` = facts and permissible release-owned research.
- `PROJECTS` = transformations, modernization, ports, integration, localization, patches, and target implementation.
- `INFRA` = repository-wide schemas, registries, validators, migration maps, and generic tooling.

Legacy roots such as `GENERATION-*`, standalone `GEN-*`, `GAMES/`, old v4 `LIBRARY/GEN-XX/<PLATFORM>/...`, `MULTI`, `REV-ALL`, `_SHARED`, `MISC`, `OTHER`, and `GENERAL` are migration inputs only.

# 1. Canonical source path

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

This order is intentional:

1. generation,
2. game,
3. source ownership,
4. native platform/execution profile,
5. package kind,
6. concrete release identity.

Human market/language labels are manifest fields and are not allowed to replace native build identity.

## 1.1 Platform IDs

Use the actual execution/package profile, not a vague console family when the distinction matters.

Examples:

```text
GB
GBC
GBA
NDS-NTR
NDS-TWL
3DS
SWITCH
SWITCH2
```

For the supplied Pokémon Black/White files, header unit code `0x02` identifies an NDS+DSi/TWL-enhanced cartridge, so the canonical platform is `NDS-TWL`, not plain `NDS`.

## 1.2 Package kinds

Examples:

```text
CART
DIGITAL
DISC
UPDATE
DLC
DEMO
DISTRIBUTION
```

Generation V Black/White retail sources use `CART`.

## 1.3 Release IDs

Use the strongest platform-native identity that is actually supported by the release.

For GBA/NDS/TWL:

```text
<GAME-CODE>-HV<ROM-VERSION>
```

Examples:

```text
IRBO-HV0
IRAO-HV0
AXVE-HV2
BPRJ-HV1
```

`HV` means the ROM/header version byte. It is deliberately not named `R` or `REV`, because preservation-set revision labels and official software revisions are separate metadata and must not be silently conflated with one header byte.

For GB/GBC, where there is no equivalent four-character game-code model, use a platform-appropriate stable release key such as:

```text
<MARKET>-<LANGUAGE>-HV<n>
```

For later platforms, use the strongest native title/build identifier plus the software/update version. Do not invent pseudo cartridge codes for platforms that do not have them.

# 2. Release leaf structure

```text
.../<RELEASE-ID>/
├── IDENTITY/
├── DUMPS/
├── NATIVE/
├── DOMAINS/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

## IDENTITY

Release-level identity only. Typical files:

```text
release.yaml
locales.yaml
serials.yaml
versions.yaml
provenance-policy.yaml
```

A release represents the official software/build identity. It is not the same thing as one observed ROM filename.

## DUMPS

Exact supplied or observed files are children of the release:

```text
DUMPS/<DUMP-ID>/
├── IDENTITY/
├── OBSERVATIONS/
├── NATIVE/
└── VERIFICATION/
```

Recommended dump ID:

```text
<PROVENANCE>-<SHA1-PREFIX>
```

Examples:

```text
SWEETNDS-a68b3bed
SWEETNDS-f94d4578
```

Dump paths record the exact observed bytes, hashes, source filename, provenance, dump quality, and which conclusions are safe to promote. A bad, incomplete, trimmed, overdumped, patched, or otherwise non-canonical image never becomes a fake official release.

## NATIVE

`NATIVE` mirrors the platform's physical/software structure without pretending that raw ROM paths are semantic game categories.

Recommended NDS/TWL structure:

```text
NATIVE/
├── HEADER/
│   ├── NTR/
│   └── TWL/
├── EXECUTABLE/
│   ├── NTR/
│   │   ├── ARM9/
│   │   ├── ARM7/
│   │   └── OVERLAY9/
│   └── TWL/
│       ├── ARM9I/
│       ├── ARM7I/
│       ├── MODCRYPT/
│       └── DIGESTS/
├── FILESYSTEM/
│   ├── FNT/
│   ├── FAT/
│   └── NITROFS/
├── CONTAINERS/
│   └── NARC/
├── EMBEDDED/
│   └── CHILD-ROM/
├── MEDIA/
│   ├── BANNER/
│   └── AUDIO/
├── NETWORK/
└── INDEXES/
```

In Sakurai these directories contain maps, indexes, schemas, decoded metadata, hashes, offsets, symbol research, cross-references, and reproducible extraction descriptions — not copyrighted whole-ROM binaries.

Raw paths such as `a/0/2/6` remain native identifiers. Their proposed meanings are recorded separately in a path map and linked to semantic domains only after verification. A community label must never silently replace the original path.

## DOMAINS

`DOMAINS` is the normalized semantic research layer. It may cite one or many native files/overlays.

```text
DOMAINS/
├── POKEMON/
├── FORMS/
├── TYPES/
├── ABILITIES/
├── MOVES/
├── ITEMS/
├── EVOLUTION/
├── BATTLE/
├── ENCOUNTERS/
├── TRAINERS/
├── NPC/
├── MAPS/
├── EVENTS/
├── TEXT/
├── GRAPHICS/
├── ANIMATION/
├── AUDIO/
├── UI/
├── SAVE/
├── COMMUNICATION/
├── ONLINE/
├── DISTRIBUTION/
├── TIME-DATE-SEASONS/
├── UNUSED/
└── BUGS/
```

This separation is mandatory. Physical location and game meaning are different axes.

# 3. Comparisons, shared material, and references

## Same-game comparisons

```text
LIBRARY/GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
```

Use for revisions, languages, regions, or dump-vs-clean validation within one game.

## Cross-game comparisons

```text
LIBRARY/GEN-XX/COMPARE/<COMPARISON-ID>/
```

Generation V example:

```text
LIBRARY/GEN-05/COMPARE/BLACK-IRBO-HV0--WHITE-IRAO-HV0/
```

No `_SHARED` pseudo-game is required.

## SHARED

```text
LIBRARY/GEN-XX/<GAME-ID>/SHARED/...
LIBRARY/GEN-XX/SHARED/...
```

`SHARED` is only for material that is genuinely identity-independent: a schema, generic parser, terminology map, or format description. **Byte-identical release files are not moved to SHARED merely because they match.** Their release ownership remains intact; equivalence is recorded by hash in `COMPARE`. Git itself already deduplicates identical blobs internally.

## REFERENCE

```text
LIBRARY/GEN-XX/<GAME-ID>/REFERENCE/<REFERENCE-ID>/...
LIBRARY/GEN-XX/REFERENCE/<REFERENCE-ID>/...
```

External disassemblies, research databases, official manuals, community NARC maps, and other secondary materials live here or are referenced from here. They never overwrite source-ROM facts.

# 4. Current Generation V bindings from the supplied ROMs

The actual supplied files bind to:

```text
LIBRARY/GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/
LIBRARY/GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/
```

Observed dumps:

```text
.../IRBO-HV0/DUMPS/SWEETNDS-a68b3bed/
.../IRAO-HV0/DUMPS/SWEETNDS-f94d4578/
```

Source-ROM observations supporting this design:

```text
Black: game code IRBO, unit 0x02, ROM version 0, 256 MiB
White: game code IRAO, unit 0x02, ROM version 0, 256 MiB
FAT entries: 484 each
ARM9 overlays: 237 each
NitroFS files: 247 each
```

Black/White comparison of the supplied images:

```text
FAT entries byte-identical: 299 / 484
FAT entries different:      185 / 484
ARM9 overlays identical:      57 / 237
ARM9 overlays different:     180 / 237
NitroFS files identical:     242 / 247
NitroFS files different:       5 / 247
```

This is why v5 keeps release ownership while storing equality/delta information in `COMPARE`; a single physical `SHARED` asset tree would destroy provenance, while fully duplicated semantic research would waste effort and obscure the real relationship.

The supplied SweeTnDs images are retained as dump-specific observations with the existing bad/incomplete external preservation classification. TWL/DSi-specific conclusions stay dump-scoped until revalidated against a verified full clean dump. NTR/NitroFS observations may be retained with explicit provenance.

# 5. Projects

Derived work does not belong in the release tree.

```text
PROJECTS/<PROJECT-ID>/
├── MANIFESTS/
├── CROSSWALK/
├── DESIGN/
├── IMPLEMENTATION/
├── PATCHES/
├── BUILD/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

For the current integration project:

```text
PROJECTS/GEN5-TO-POCKET-MONSTERS/
```

Project manifests lock canonical library sources/targets by path and hash. `TARGET` is a project concern, not a fake source-release branch inside `LIBRARY`.

# 6. Sakurai ownership

Sakurai is authoritative for:

- release/dump identity,
- ROM maps and native structure,
- reverse engineering,
- data/text/script research,
- semantic domain catalogs,
- cross-release comparisons,
- unused/bug research,
- source citations,
- extraction/rebuild specifications,
- verification evidence.

Tsubaki may use the same release IDs and project IDs, but production assets and build outputs are owned there.

# 7. Repository-pair invariant

Sakurai and Tsubaki must share exactly the same:

- `GEN-XX`,
- `GAME-ID`,
- `PLATFORM-ID`,
- `PACKAGE-KIND`,
- `RELEASE-ID`,
- `DUMP-ID`,
- `PROJECT-ID`,
- project target IDs.

Leaf responsibilities may differ. Identity never does.

# 8. Path rules

New canonical paths must not use:

```text
MULTI
REV-ALL
ALL
MULTI-REGION
_SHARED
MISC
OTHER
GENERAL
REV-UNKNOWN
```

Unknown facts stay unknown in manifests; they do not become directory names that look like identities.

Every tracked artifact must answer exactly one ownership question:

- official source-release fact -> `LIBRARY/.../SOURCE/.../<RELEASE-ID>/`
- exact observed file/dump fact -> `.../DUMPS/<DUMP-ID>/`
- same-game relationship -> `<GAME-ID>/COMPARE/`
- cross-game relationship -> `GEN-XX/COMPARE/`
- genuinely identity-independent material -> `SHARED/`
- external source/reference -> `REFERENCE/`
- derived transformation -> `PROJECTS/`
- repository-wide schema/tool/registry -> `INFRA/`

Git history is the archive; duplicate live trees are not.