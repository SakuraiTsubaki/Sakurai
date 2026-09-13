# Repository Structure v11

Status: **canonical** — 2026-09-13.

v11 keeps the v10 release-centric semantic grammar and fixes the repository split.

```text
GEN-XX/<GAME-ID>/
├── RELEASES/
├── PROJECTS/
├── COMPARES/
├── REFERENCES/
└── SHARED/
```

Release coordinates remain:

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
└── DUMPS/<DUMP-ID>/
```

**Tsubaki is the complete non-ROM superset.** Only complete original or modified/playable ROM images are excluded. Analysis, documentation, metadata, hashes, observations, source, scripts, tables, manifests, catalogs, extracted/normalized/converted assets, implementation, patches, build metadata/logs, tests, reports, tools and verification all belong in Tsubaki.

**Sakurai is a curated knowledge/research subset.** Every non-ROM artifact present in Sakurai must also exist in Tsubaki at the same semantic coordinate. Tsubaki may contain additional production/data artifacts.

A Tsubaki-only artifact is valid. A Sakurai-only non-ROM artifact is a synchronization defect.

See `INFRA/ARCHITECTURE/V11.md` and `INFRA/POLICY/PAIR-SYNC.md`.
