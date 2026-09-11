# Structure Migration

The repository has been migrated from mixed legacy naming to the canonical hierarchy defined in `STRUCTURE.md`.

## Migration rules

Legacy top-level game aliases are preserved byte-for-byte as Git trees under:

`GENERATION/GAME/MULTI/REV-ALL/MIGRATED/<legacy-source>/`

This keeps all existing files while removing duplicate or bundle names from the GAME level.

### Generation I

- `BLUE` → `BLUE`
- `GREEN` → `GREEN`
- `POKEMON-RED` → `RED`
- `POKEMON-YELLOW` → `YELLOW`
- `POCKET-MONSTERS-RGBY`, `RGBY` → `_SHARED`

### Generation II

- `GOLD`, `POCKET-MONSTERS-GOLD` → `GOLD`
- `SILVER`, `POCKET-MONSTERS-SILVER` → `SILVER`
- `CRYSTAL`, `POCKET-MONSTERS-CRYSTAL` → `CRYSTAL`
- `POCKET-MONSTERS-GOLD-SILVER`, `POCKET-MONSTERS-GSC` → `_SHARED`
- legacy root `GENERATION_II` title-screen structure → `GOLD/MULTI/REV-ALL/STRUCTURE/TITLE-SCREEN`
- legacy root `analysis_pipeline` → `_SHARED/KR-KO/REV-ALL/TOOLS`
- legacy root `deliverables/GENERATION-II/GOLD/KOREA-KO/REV-0/ANALYSIS` → `GOLD/KR-KO/REV-0/ANALYSIS`

### Generation III

- canonical single-game roots remain associated with their corresponding game
- `GEN3-SHARED`, `RSE-FRLG` → `_SHARED`

### Generation IV

- canonical single-game roots remain associated with their corresponding game
- `DIAMOND-PEARL`, `DPPt-HGSS`, `GENERATION-IV-TO-POCKET-MONSTERS` → `_SHARED`

### Generation V

- `BW`, `BW-B2W2` → `_SHARED` until their artifacts are safely separated among `BLACK`, `WHITE`, `BLACK2`, and `WHITE2`

## Workflows

Previously active project-specific workflows are preserved under `.github/workflows-legacy/` so the historical automation is not lost but cannot recreate legacy paths. `.github/workflows/validate-structure.yml` enforces the new hierarchy for future changes.

No ROM binaries are introduced by this migration, and existing Git object contents are reused rather than rewritten wherever possible.
