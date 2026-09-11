# Structure Migration Map

Current legacy paths are being normalized to the canonical rules in `STRUCTURE.md`.

## Generation I

- `BLUE` → `BLUE`
- `GREEN` → `GREEN`
- `POKEMON-RED` → `RED`
- `POKEMON-YELLOW` → `YELLOW`
- `POCKET-MONSTERS-RGBY` → `_SHARED`
- `RGBY` → `_SHARED`

## Generation II

- `GOLD` / `POCKET-MONSTERS-GOLD` → `GOLD`
- `SILVER` / `POCKET-MONSTERS-SILVER` → `SILVER`
- `CRYSTAL` / `POCKET-MONSTERS-CRYSTAL` → `CRYSTAL`
- `POCKET-MONSTERS-GOLD-SILVER` → `_SHARED`
- `POCKET-MONSTERS-GSC` → `_SHARED`

## Generation III

- `RUBY` → `RUBY`
- `SAPPHIRE` → `SAPPHIRE`
- `EMERALD` → `EMERALD`
- `FIRERED` → `FIRERED`
- `LEAFGREEN` → `LEAFGREEN`
- `GEN3-SHARED` → `_SHARED`
- `RSE-FRLG` → `_SHARED`

## Generation IV

- `DIAMOND` → `DIAMOND`
- `PEARL` → `PEARL`
- `PLATINUM` → `PLATINUM`
- `HEARTGOLD` → `HEARTGOLD`
- `SOULSILVER` → `SOULSILVER`
- `DIAMOND-PEARL` → `_SHARED`
- `DPPt-HGSS` → `_SHARED`
- `GENERATION-IV-TO-POCKET-MONSTERS` → `_SHARED` with provenance metadata

## Generation V

- `BW` → `_SHARED` until artifacts are separated into `BLACK` and `WHITE`
- `BW-B2W2` → `_SHARED` until artifacts are separated into `BLACK`, `WHITE`, `BLACK2`, and `WHITE2`

## Locale normalization

Examples:

- `JAPAN` → `JP-JA`
- `KOREA` / Korean target output → `KR-KO`
- `MULTI-REGION` → `MULTI`
- `JAPAN-TO-KOREAN` is not a locale; move to target locale and record source/target in `LOCALIZATION` metadata

## Revision normalization

- `MULTI-REV` → `REV-ALL`
- `REV-COMMON` → `REV-ALL` only when truly shared across all revisions; otherwise assign the actual revision

Migration should preserve file contents and Git history through normal commits. No ROM binaries are introduced during migration.
