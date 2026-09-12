# GS Korean → Pocket Monsters — v4.1 path routing

This project follows the repository-wide v4 identity model. Original ROM binaries are never committed.

## 1. Platform identity is not a header compatibility flag

`<PLATFORM>` in a canonical path is the title/platform family used by the repository. A ROM filename extension, CGB flag, or SGB flag is compatibility metadata and must not silently move a release to a different platform tree.

For this 23-ROM source set:

```text
Generation I titles -> LIBRARY/GEN-01/GB/...
Generation II titles -> LIBRARY/GEN-02/GBC/...
```

Therefore English Yellow remains:

```text
LIBRARY/GEN-01/GB/YELLOW/RELEASES/US-EU-EN-HV0
```

even though the supplied file is named `.gbc` and has CGB flag `0x80`. Its compatibility profile is `DMG_CGB_DUAL`; that is metadata, not a path selector.

Compatibility profiles used by this project:

- `DMG_ONLY`: CGB flag `0x00`.
- `DMG_CGB_DUAL`: CGB flag `0x80`.
- `CGB_ONLY`: CGB flag `0xC0`.
- SGB support is recorded separately from the SGB flag.

## 2. Original-release facts

Facts describing one official ROM/build belong to `LIBRARY`, not the project tree.

```text
LIBRARY/GEN-01/GB/<GAME>/RELEASES/<RELEASE-ID>/...
LIBRARY/GEN-02/GBC/<GAME>/RELEASES/<RELEASE-ID>/...
```

Examples: header metadata, per-release pointer maps, bank ownership, text-engine addresses, revision-only differences, checksums, and provenance.

## 3. Exact supplied-file observations

A specific uploaded/dumped file is a `DUMP`, not a new release:

```text
LIBRARY/.../RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/...
```

The project `source-matrix.yaml` references those canonical release/dump identities; it does not duplicate ownership of the same ROM in a project-specific library tree.

## 4. Cross-release research

Version/revision comparisons belong to:

```text
LIBRARY/.../COMPARISONS/<COMPARISON-ID>/...
```

Generation/platform-wide comparisons may use `_SHARED` as the game scope. `MULTI`, `REV-ALL`, `ALL`, or fabricated locale release owners are forbidden.

## 5. Project-owned research and design

```text
PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/
├── MANIFESTS/
├── CROSSWALK/
├── DESIGN/
├── IMPLEMENTATION/
├── VERIFICATION/
├── TOOLS/
└── REPORTS/
```

- `MANIFESTS`: source/target release locks, the authoritative 23-ROM source matrix, and routing policy.
- `CROSSWALK`: Japanese/English source → modern Korean terminology mappings. JP and EN remain independently sourced.
- `DESIGN`: Hangul engine, pointer relocation, text allocation, UI, SRAM/name handling specifications.
- `IMPLEMENTATION`: research-side target maps/specifications; production-ready insertion assets remain in Tsubaki.
- `VERIFICATION`: round-trip, checksum, event, text, pointer, and UI verification evidence.
- `TOOLS`: extractors, decoders, diff tools, validators.
- `REPORTS`: source census, bank audits, translation audits.

## 6. GS Korean implementation-reference routing

Korean Gold/Silver are official source releases and implementation references.

- Banks `0x68–0x69`: Gold/Silver differ; keep version-owned source/text research separate.
- Bank `0x6C`: byte-identical; decoded names/terminology and semantic crosswalk belong in Sakurai.
- Banks `0x78–0x7A`: byte-identical Hangul font source; reusable production representation belongs in Tsubaki `LIBRARY/GEN-02/GBC/_SHARED/SHARED/FONTS/GS-KOREAN-HANGUL-8X16`.

## 7. Repository ownership contract

Sakurai owns ROM identity, analysis, reverse engineering, manifests, source maps, decoded research tables, specifications, research tools, crosswalks, and verification evidence.

Tsubaki owns reusable fonts/graphics/assets, converted resources, generated insertion data, build inputs, patches, and final production artifacts.

Release IDs, dump IDs, project IDs, and target IDs must mean exactly the same thing in both repositories.
