# RBY GitHub restructure — Sakurai — 2026-09-13

## Role

Sakurai is the authoritative evidence/research repository for RBY ENGLISH → ポケットモンスター.

It owns source-release identity and hashes, ROM header observations, bank/text censuses, comparisons, translation research/specification, routing design, audit records and verification. Full ROM binaries are excluded.

## Canonical source identity

```text
GEN-01/<GAME>/SOURCE/<PLATFORM>/CART/<RELEASE-ID>/
```

For this 12-ROM working set, Japanese R/G/B/Y and English R/B are under `GB`; English Yellow US-EU-EN-HV0 is under `GBC` because the inspected ROM has CGB flag `0x80`.

## Canonical multi-game target

```text
GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/
```

Active project evidence now uses this path. `LIBRARY/` and `PROJECTS/` are retired prefixes and are not used for new/touched project data.

## Material recorded in Sakurai

- `MANIFESTS/source-set.json`: exact 12-source set, sizes, SHA-1/SHA-256, platform IDs and checksum status.
- `MANIFESTS/release-lock.json`: nine Japanese-base English target locks.
- `MANIFESTS/text-engine-research.json`: canonical text-engine research linkage.
- `VERIFICATION/source-rom-verification-2026-09-13.md`: direct verification of all 12 supplied ROMs.
- `DESIGN/GITHUB-PATH-ROUTING-v9.md`: project-specific routing contract.
- `GEN-01/COMPARE/RBY-ROM-CENSUS-2026-09-12/`: 608-bank ROM comparison evidence.
- `GEN-01/COMPARE/RBY-TEXT-ENGINE-CENSUS-2026-09-12/`: text-system discovery evidence.

## Translation authority

Japanese Pocket Monsters Red/Green/Blue/Pikachu are translation originals. English Red/Blue/Yellow are technical implementation references only. Japanese Green remains an independent translation source; English Red/Blue may be consulted for implementation structure but never replace Green's Japanese source text.
