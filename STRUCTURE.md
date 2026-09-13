# Repository Structure v11

Status: **canonical** — 2026-09-13.

The detailed specification is [`INFRA/ARCHITECTURE/V11.md`](INFRA/ARCHITECTURE/V11.md).

The canonical coordinate is:

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/DUMPS/<DUMP-ID>/
```

**Sakurai** is the curated knowledge/control subset. **Tsubaki is the complete non-ROM superset**: every project-produced artifact that is not an original/modified playable ROM image belongs in Tsubaki, including analysis tables/reports as well as extracted/normalized assets, implementation data, patches, tools, and build metadata.

Legacy `SOURCE`, `TARGET`, `LIBRARY`, `projects`, and `workspaces` paths receive no new canonical work. See [`INFRA/ARCHITECTURE/MIGRATION-V11.md`](INFRA/ARCHITECTURE/MIGRATION-V11.md).
