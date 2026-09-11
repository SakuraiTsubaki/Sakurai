# Structure Migration

Repository migration is in progress from legacy ad-hoc paths to the canonical hierarchy documented in `STRUCTURE.md`.

## Completed

- Root-level legacy project folders have been moved into generation/game paths.
- Generation I and Generation II compatibility `MIGRATED` buckets have been unpacked into canonical GAME, LANGUAGE/REGION, REV, and WORK TYPE paths.
- Legacy bundle names no longer occupy GAME level.
- Old project-specific GitHub Actions are preserved under `.github/workflows-legacy/` and are inactive.

## Remaining

Generation III through Generation V legacy compatibility buckets are being normalized next. Generation VI through IX currently contain no project data requiring migration.

Migration preserves existing blobs/trees wherever possible and does not introduce ROM binaries.
