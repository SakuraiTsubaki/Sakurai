# Sakurai

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## Canonical architecture: v11

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
└── DUMPS/<DUMP-ID>/
```

Sakurai is the **curated knowledge/control subset**: release and exact-dump identity, provenance, hashes, headers/indexes, catalogs, research, reverse engineering, mappings, reports, specifications, analysis tools, and verification evidence.

Tsubaki uses the same semantic coordinates and is the **complete non-ROM superset**. Every eligible project artifact that is not an original or modified/playable ROM image is mirrored or retained there as appropriate.

For the current Gen V direct-ROM cutover, canonical coordinates begin at `GEN-05/BLACK/RELEASES/NDS-TWL/CART/IRBO-HV0/` and `GEN-05/WHITE/RELEASES/NDS-TWL/CART/IRAO-HV0/`.

See `STRUCTURE.md` and `INFRA/ARCHITECTURE/V11.md`.
