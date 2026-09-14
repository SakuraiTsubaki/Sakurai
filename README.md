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

A project has one live owner path. Project-specific analysis, comparisons, reports, tools, manifests, verification material, design, inputs, and other work products stay under that project root instead of being split across historical or version-specific trees.

Version updates modify the current tree directly. If a path changes, unique work is merged into the new canonical path and the old live path is removed in the same update. Git commits, tags, and pull requests are the history; no separate migration/history tree is required.

Sakurai is the curated research/control subset. It owns release/dump identity, provenance, hashes, analysis, reverse engineering, comparison, localization research, tables, schemas, reports, research tooling, citations, and verification evidence.

Tsubaki is the complete non-ROM superset and uses the same semantic IDs and coordinates.

**Only complete playable ROM image files are excluded from GitHub.**

See [STRUCTURE.md](STRUCTURE.md).
