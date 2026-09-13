# Repository Migration — v11

Status: **active cutover** — 2026-09-13.

v11 retains the v10 semantic coordinates and changes repository ownership semantics.

- `RELEASES`, `PROJECTS`, `COMPARES`, `REFERENCES`, `SHARED` remain canonical.
- Tsubaki becomes the complete non-ROM superset.
- Sakurai remains a curated research/control subset.
- Existing Sakurai-only non-ROM files must be mirrored into Tsubaki at the same v11 coordinate.
- Existing Tsubaki production data stays in place.
- v9 and older `SOURCE/TARGET/COMPARE/REFERENCE` paths are migration inputs only.
- Complete original or modified/playable ROM images remain excluded.

See `INFRA/ARCHITECTURE/MIGRATION-V11.md`.
