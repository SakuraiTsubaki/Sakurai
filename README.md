# Sakurai

Pokémon source identity, reverse engineering, comparison, localization research, technical design, and verification repository.

## Canonical architecture: v11

New work uses `GEN-XX/<GAME-ID>/RELEASES|PROJECTS|COMPARES|REFERENCES|SHARED`, plus generation-level and `CROSS-GEN` coordinates when ownership is genuinely broader than one game. Exact observed ROM images are registered by content-addressed dump IDs under `RELEASES/.../DUMPS/`; ROM bytes are never committed.

Sakurai is the research/control subset. It contains identity, provenance, hashes, analysis, reverse engineering, tables, reports, schemas, research tools, citations, and verification evidence.

Tsubaki is the complete non-ROM superset. Every new Sakurai project artifact is also committed to Tsubaki at the same semantic coordinate whenever practical. Production-only assets and build products can remain Tsubaki-only.

See [STRUCTURE.md](STRUCTURE.md), [INFRA/ARCHITECTURE/V11.md](INFRA/ARCHITECTURE/V11.md), and [MIGRATION.md](MIGRATION.md).
