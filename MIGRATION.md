# Repository Migration — v9

Status: **staged cutover design**, 2026-09-13.

v9 is a path/ownership migration. Do not rewrite content merely to move it. Reuse existing Git trees/blobs where possible and migrate in reviewable batches.

## Root mapping

```text
GEN-XX/...                → GAMES/GEN-XX/...
CROSS-GEN/TARGET/...      → SCOPES/CROSS-GEN/TARGETS/...
CROSS-GEN/COMPARE/...     → SCOPES/CROSS-GEN/COMPARES/...
CROSS-GEN/REFERENCE/...   → SCOPES/CROSS-GEN/REFERENCES/...
CROSS-GEN/SHARED/...      → SCOPES/CROSS-GEN/SHARED/...
INFRA/...                 → INFRA/...
LIBRARY/...               → semantic owner under GAMES/ or ARCHIVE/PRE-V9/
GENERATION-IV/...         → semantic owner under GAMES/GEN-04/ or ARCHIVE/PRE-V9/
quarantine/legacy         → ARCHIVE/PRE-V9/...
```

## Game path mapping

```text
GEN-XX/<GAME>/SOURCE/<PLATFORM>/<PACKAGE>/<RELEASE>/...
→ GAMES/GEN-XX/<GAME>/RELEASES/<RELEASE>/...

GEN-XX/<GAME>/TARGET/<TARGET>/...
→ GAMES/GEN-XX/<GAME>/TARGETS/<TARGET>/...

GEN-XX/<GAME>/COMPARE/<COMPARE>/...
→ GAMES/GEN-XX/<GAME>/COMPARES/<COMPARE>/...

GEN-XX/<GAME>/REFERENCE/<REF>/...
→ GAMES/GEN-XX/<GAME>/REFERENCES/<REF>/...
```

`PLATFORM`, `PACKAGE`, language, region, revision, build/product/title codes move to the release identity manifest. They remain searchable facts but stop being ownership directories.

## Same-generation multi-game mapping

```text
GEN-XX/TARGET/<TARGET>/...     → SCOPES/GEN-XX/TARGETS/<TARGET>/...
GEN-XX/COMPARE/<COMPARE>/...   → SCOPES/GEN-XX/COMPARES/<COMPARE>/...
GEN-XX/REFERENCE/<REF>/...     → SCOPES/GEN-XX/REFERENCES/<REF>/...
GEN-XX/SHARED/<RESOURCE>/...   → SCOPES/GEN-XX/SHARED/<RESOURCE>/...
```

## ROM/disassembly role split

For dedicated implementation repositories such as `SakuraiTsubaki/pokegold-kr`:

```text
ROM identity, hashes, offsets, bank maps, architecture research, comparisons, specs
→ Sakurai

reusable extracted assets, converters, insertion-ready data, patches, build tools
→ Tsubaki

engine source
→ dedicated implementation repository; lock exact commit in both role repositories as needed
```

Full original or modified ROMs remain excluded.

## Initial v9 seed in this branch

```text
GAMES/GEN-02/GOLD/TARGETS/GOLD-KR-NATDEX/RESEARCH/ROM-LIMITS-AND-ARCHITECTURE.md
GAMES/GEN-02/SILVER/TARGETS/SILVER-KR-NATDEX/RESEARCH/ROM-LIMITS-AND-ARCHITECTURE.md
```

These files establish the role split before bulk path migration.

## Cutover order

1. Land v9 schema and validators.
2. Register stable game/release/target IDs in `REGISTRY/`.
3. Move one generation at a time with path-only tree reuse.
4. Rewrite internal path references mechanically.
5. Move unresolved unique material to `ARCHIVE/PRE-V9/` only when no semantic owner can be proven.
6. Remove retired live roots only after validation reaches zero references.

## Invariants

1. No full commercial ROM/executable binaries.
2. No force update of `main`.
3. Preserve blob bytes for path-only migration.
4. One live semantic owner per artifact.
5. Same IDs in Sakurai and Tsubaki.
6. Dedicated implementation repositories remain canonical for their source.
7. Archive is read-only and receives no new normal work.
