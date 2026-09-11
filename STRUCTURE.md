# Repository Structure

## Canonical path

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

This path model is mandatory for all project outputs.

## Root

Allowed project roots are `GENERATION-I` through `GENERATION-IX`. Repository infrastructure may also use `.github`, `README.md`, `STRUCTURE.md`, and `MIGRATION.md`. No ad-hoc project folders are allowed at repository root.

## GAME

GAME contains only a canonical single-game title or `_SHARED`.

- Generation I: `RED`, `GREEN`, `BLUE`, `YELLOW`
- Generation II: `GOLD`, `SILVER`, `CRYSTAL`
- Generation III: `RUBY`, `SAPPHIRE`, `EMERALD`, `FIRERED`, `LEAFGREEN`
- Generation IV: `DIAMOND`, `PEARL`, `PLATINUM`, `HEARTGOLD`, `SOULSILVER`
- Generation V: `BLACK`, `WHITE`, `BLACK2`, `WHITE2`
- Generation VI: `X`, `Y`, `OMEGARUBY`, `ALPHASAPPHIRE`
- Generation VII: `SUN`, `MOON`, `ULTRASUN`, `ULTRAMOON`, `LETSGO-PIKACHU`, `LETSGO-EEVEE`
- Generation VIII: `SWORD`, `SHIELD`, `BRILLIANTDIAMOND`, `SHININGPEARL`, `LEGENDS-ARCEUS`
- Generation IX: `SCARLET`, `VIOLET`, `LEGENDS-Z-A`

`_SHARED` is reserved for material that genuinely applies to multiple games in the same generation. Bundle labels such as `RGBY`, `GSC`, `RSE-FRLG`, `DPPt-HGSS`, `BW`, and `BW-B2W2` are not GAME names and must not be created at this level.

## LANGUAGE/REGION

Canonical values are `JP-JA`, `KR-KO`, `US-EN`, `EU-EN`, `EU-DE`, `EU-FR`, `EU-IT`, `EU-ES`, and `MULTI`.

Transformation directions such as `JAPAN-TO-KOREAN` are metadata, not locale folders. Source/target direction belongs inside localization manifests or documentation.

## REV

Use explicit revision folders such as `REV-0`, `REV-A`, `REV-1`, or `REV-ALL`. Legacy aliases such as `MULTI-REV`, `REV-COMMON`, `REV-MIXED`, and `REV-UNKNOWN` must not be introduced as canonical REV folders; when provenance requires those labels, keep them below WORK TYPE.

## WORK TYPE — Sakurai

Allowed research work types are:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, and `SYMBOLS`.

`MIGRATED` is no longer a valid WORK TYPE. All compatibility material has been promoted into canonical paths or preserved below a canonical WORK TYPE as provenance-labelled legacy subfolders.

Directories below WORK TYPE are free to describe the actual subject, phase, bank, table, map, component, provenance group, or legacy bundle.

## Legacy workflows

Old project-specific GitHub Actions are preserved under `.github/workflows-legacy/` and are intentionally inactive. The active repository-wide structural validator enforces the canonical path model.
