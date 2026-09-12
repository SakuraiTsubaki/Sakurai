# Pokémon Ruby repository routing

Canonical identity root: `LIBRARY/GEN-03/GBA/RUBY/`. ROM binaries remain outside GitHub.

## Sakurai
Owns release/dump identity, hashes, headers, ROM layout, reverse engineering, text/data maps, disassembly, comparisons, reproducible research tools, and verification evidence.

## Tsubaki
Owns production-facing asset inventories, graphics/audio/font/sprite extraction maps, deduplication/fingerprint tables, converted assets, build inputs, patches, and implementation outputs. Dump-specific extracted assets stay below `RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/` until verified as release-representative.

## Release ID
GBA retail: `<GAME-CODE>-R<HEADER-VERSION>`. Non-retail builds sharing the same native identity require a build qualifier, e.g. `AXVD-R0-DEBUG`. The manifest field `build_kind` is mandatory.

## Cross-release work
The current 13-ROM observed set is `COMPARISONS/SOURCE-SET-2026-09-12/`. Do not create `MULTI`, `REV-ALL`, `ALL`, or `MISC` pseudo-release owners.
