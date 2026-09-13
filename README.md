# Sakurai

Sakurai is the curated knowledge/research view of the Pokémon projects.

## Canonical architecture: v11

```text
GEN-XX/<GAME-ID>/
├── RELEASES/
├── PROJECTS/
├── COMPARES/
├── REFERENCES/
└── SHARED/

CROSS-GEN/
INFRA/
```

Sakurai stores selected identity/provenance records, observations, analysis, reverse engineering, schemas, mappings, specifications, reports, tools and verification evidence.

**Tsubaki is the complete non-ROM superset.** Every non-ROM artifact committed to Sakurai must also exist in Tsubaki at the same semantic v11 coordinate. Tsubaki may contain additional production/data artifacts. A Sakurai-only non-ROM artifact is a synchronization defect.

Complete original or modified/playable ROM images are never committed.

See `STRUCTURE.md`, `INFRA/ARCHITECTURE/V11.md`, `INFRA/ARCHITECTURE/MIGRATION-V11.md`, and `INFRA/POLICY/PAIR-SYNC.md`.
