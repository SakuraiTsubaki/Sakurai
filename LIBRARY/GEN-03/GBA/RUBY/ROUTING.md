# Pokémon Ruby repository routing — v4.2

Canonical identity root: `LIBRARY/GEN-03/GBA/RUBY/`. ROM binaries remain outside GitHub.

The repository pair follows `INFRA/PATH-SPECS/ARTIFACT-OWNERSHIP-V4.2.md` and `INFRA/SCHEMAS/ARTIFACT-ROUTING-V4.2.json`. Ruby's concrete class-by-class routing is locked in `ROUTING-MATRIX.tsv`.

## Sakurai

Owns release/dump identity, hashes, headers, ROM layout, reverse engineering, text/data/maps/events interpretation, disassembly, symbols, factual cross-release comparisons, reproducible research tools, tests, and verification evidence.

Exact-file observations begin below `RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/`. Facts proven representative of the release may be promoted to the corresponding release-level research domain.

## Tsubaki

Owns production-facing extracted assets, graphics/audio/font/sprite/palette/icon/tileset/UI/title resources, asset deduplication, normalized/converted resources, build inputs, patches, implementation, and generated outputs.

Dump-specific extracted assets stay below `RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/<ASSET-DOMAIN>/` until verified as release-representative. Only then may they be promoted to `RELEASES/<RELEASE-ID>/<ASSET-DOMAIN>/`.

## Lifecycle

`OBSERVED -> EXTRACTED -> VERIFIED-RELEASE`

Relationships spanning releases belong to `COMPARISONS/<COMPARISON-ID>/`. Modernization, localization, expansion, ports, patches, and build outputs are `DERIVED` work and belong to top-level `PROJECTS/<PROJECT-ID>/`, never the original-release library.

## Release ID

GBA retail uses `<GAME-CODE>-R<HEADER-VERSION>`. A materially distinct non-retail build sharing the same native identity requires a stable qualifier, e.g. `AXVD-R0-DEBUG`. `build_kind` remains mandatory in release manifests.

## Current Ruby source set

The 13 observed ROMs are compared under `COMPARISONS/SOURCE-SET-2026-09-12/`. The source-set research tool now validates header/hash identity, coarse layout, 64 KiB bank fingerprints, GBA LZ10 blocks, and decompressed-output equality without writing ROM bytes.

Do not create `MULTI`, `REV-ALL`, `ALL`, `MISC`, or other pseudo-release owners.
