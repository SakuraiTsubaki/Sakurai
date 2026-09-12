# Pokémon Sapphire repository routing

Canonical source identity root: `LIBRARY/GEN-03/GBA/SAPPHIRE/`.

## Sakurai
Release/dump identity, hashes, GBA header audit, ROM extent/layout research, reverse engineering, text/data maps, disassembly, cross-release diffs, reproducible research tools, reports and verification.

## Tsubaki
Production-facing source locks, asset fingerprints, extraction/deduplication maps, graphics/audio/font/sprite inventories, converted resources, build inputs, patches and implementation outputs.

## Rules
- GBA retail release ID: `<GAME-CODE>-R<HEADER-VERSION>` unless a truthful build qualifier is required.
- Exact observed file ID: `PROJECT-<SHA1-8>`.
- Cross-release owner for this set: `COMPARISONS/SOURCE-SET-2026-09-12/`.
- Never create `MULTI`, `REV-ALL`, `MISC`, or `ALL` as fake release identities.
- Original ROM binaries remain outside GitHub.
