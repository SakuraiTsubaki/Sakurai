# Repository Structure

## Canonical path

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

This path model is mandatory for all new project outputs.

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

`_SHARED` is reserved for material that genuinely applies to multiple games in the same generation. Names such as `RGBY`, `GSC`, `RSE-FRLG`, `DPPt-HGSS`, `BW`, and `BW-B2W2` are not GAME names and must not be created at this level.

## LANGUAGE/REGION

Canonical values include `JP-JA`, `KR-KO`, `US-EN`, `EU-EN`, `EU-DE`, `EU-FR`, `EU-IT`, `EU-ES`, and `MULTI`.

A transformation direction such as `JAPAN-TO-KOREAN` is metadata, not a locale folder. Source/target direction belongs inside localization manifests or documentation.

## REV

Use explicit revision folders such as `REV-0`, `REV-A`, `REV-1`, or `REV-ALL`. `MULTI-REV` and `REV-COMMON` are legacy names and are forbidden for new paths.

## WORK TYPE — Sakurai

Allowed research work types are:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, `SYMBOLS`, and `MIGRATED`.

`MIGRATED` is a read-only compatibility/archive bucket created only during repository restructuring. New project output must never be written there.

Directories below WORK TYPE are free to describe the actual subject, phase, bank, table, map, or component.

## Legacy workflows

Old project-specific GitHub Actions are preserved under `.github/workflows-legacy/` and are intentionally inactive. The only active repository-wide workflow after migration is structural validation unless a new workflow is explicitly designed for the canonical paths.
