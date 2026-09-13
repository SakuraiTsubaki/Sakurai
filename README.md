# Sakurai

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## Canonical architecture: v12

Current work lives only under:

```text
GEN-XX/<GAME-ID>/RELEASES|PROJECTS|COMPARES|REFERENCES|SHARED
GEN-XX/PROJECTS|COMPARES|REFERENCES|SHARED
CROSS-GEN/PROJECTS|COMPARES|REFERENCES|SHARED
INFRA/
```

Transitional `LIBRARY`, lowercase `projects`, `workspaces`, `SOURCE`, `TARGET`, `COMPARE`, and `REFERENCE` paths are not valid live coordinates. Historical trees are preserved only under `INFRA/MIGRATION/` and in Git history.

Sakurai is the curated research/control subset. It owns release/dump identity, provenance, hashes, analysis, reverse engineering, comparison, localization research, tables, schemas, reports, research tooling, citations, and verification evidence.

Tsubaki is the complete non-ROM superset and uses the same semantic IDs and coordinates.

**Only complete playable ROM image files are excluded from GitHub.**

See [STRUCTURE.md](STRUCTURE.md) and [MIGRATION.md](MIGRATION.md).
