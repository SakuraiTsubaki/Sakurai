# Sakurai / Tsubaki ROM artifact routing contract — v6

Canonical repository architecture: v6.

## Sakurai: original/source truth

Sakurai owns facts that answer what an original release is, where data lives, how it behaves, and how official releases differ.

Canonical release root:
`LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/`

Release-owned sections include `IDENTITY`, `DUMPS`, `NATIVE`, `DOMAINS`, `TOOLS`, `REPORTS`, and `VERIFICATION`. Exact supplied-file observations remain dump-scoped until promoted by verification.

Same-game comparisons belong under `LIBRARY/GEN-XX/<GAME-ID>/COMPARE/`; cross-game factual comparisons belong under `LIBRARY/GEN-XX/COMPARE/`.

Generation-scoped project research belongs under `PROJECTS/GEN-XX/<PROJECT-ID>/`. Projects whose source and implementation targets span generations belong under `PROJECTS/CROSS-GEN/<PROJECT-ID>/`.

For Generation V → ポケットモンスター the canonical Sakurai project root is:
`PROJECTS/CROSS-GEN/GEN5-TO-POCKET-MONSTERS/`.

## Tsubaki: production/build truth

Tsubaki owns transformed/generated insertion resources, production converters, target-local data, patches, build layouts and build manifests. It mirrors Sakurai release/dump IDs but does not duplicate research ownership.

For Generation V → ポケットモンスター the canonical Tsubaki root is also:
`PROJECTS/CROSS-GEN/GEN5-TO-POCKET-MONSTERS/`.

Cross-target production resources use `IMPLEMENTATION/COMMON/`; target-specific resources use `IMPLEMENTATION/<TARGET-ID>/`.

## Identity and payload rules

Use the strongest verified native technical release identifier, with header/software version represented independently. A release identity and an observed dump identity are never interchangeable. Filename region tags are metadata, not ownership keys.

Original ROM binaries are never committed. Bulk unmodified copyrighted ROM extractions are not the default Git payload; reproduce them locally from locked inputs and commit fingerprints, indexes, converters, transformed project assets, patches and manifests.

## Decision test

- Original byte/table/archive/function/release fact → Sakurai `LIBRARY`.
- Relationship among original releases → Sakurai `COMPARE`.
- Source-to-target semantics or integration design → Sakurai project `CROSSWALK` / `DESIGN`.
- Converted sprite/table/patch/build input → Tsubaki.
- Tool whose primary purpose is producing insertion/build artifacts → Tsubaki `TOOLS`, referencing Sakurai identities.

Do not create new canonical work in `GENERATION-*`, old flat project roots, `_SHARED`, `MULTI`, `REV-ALL`, `REV-UNKNOWN`, `MISC`, `OTHER`, `GENERAL`, or obsolete `R0/R1/R2` compatibility target aliases. Historical records remain in `LEGACY` or Git history.
