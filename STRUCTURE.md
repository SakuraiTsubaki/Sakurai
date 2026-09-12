# Repository Structure

## Canonical path

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

This five-level ownership path is mandatory. It is not a wrapper around an older project path; it is the semantic home of the artifact.

## Root

Allowed project roots are `GENERATION-I` through `GENERATION-IX`. Repository infrastructure may also use `.github`, `README.md`, `STRUCTURE.md`, `MIGRATION.md`, and `.git`.

## GAME

GAME contains only one canonical single-game title or `_SHARED`.

- Generation I: `RED`, `GREEN`, `BLUE`, `YELLOW`
- Generation II: `GOLD`, `SILVER`, `CRYSTAL`
- Generation III: `RUBY`, `SAPPHIRE`, `EMERALD`, `FIRERED`, `LEAFGREEN`
- Generation IV: `DIAMOND`, `PEARL`, `PLATINUM`, `HEARTGOLD`, `SOULSILVER`
- Generation V: `BLACK`, `WHITE`, `BLACK2`, `WHITE2`
- Generation VI: `X`, `Y`, `OMEGARUBY`, `ALPHASAPPHIRE`
- Generation VII: `SUN`, `MOON`, `ULTRASUN`, `ULTRAMOON`, `LETSGO-PIKACHU`, `LETSGO-EEVEE`
- Generation VIII: `SWORD`, `SHIELD`, `BRILLIANTDIAMOND`, `SHININGPEARL`, `LEGENDS-ARCEUS`
- Generation IX: `SCARLET`, `VIOLET`, `LEGENDS-Z-A`

`_SHARED` is used only when an artifact genuinely belongs to multiple games in the same generation. Synthetic bundle labels such as `RGBY`, `GSC`, `RSE-FRLG`, `DIAMOND-PEARL`, `DPPt-HGSS`, `BW`, and `BW-B2W2` are not GAME-level folders.

## LANGUAGE / REGION

Canonical values are `JP-JA`, `KR-KO`, `US-EN`, `EU-EN`, `EU-DE`, `EU-FR`, `EU-IT`, `EU-ES`, and `MULTI`.

Use `MULTI` only when the artifact intentionally spans more than one locale. Translation direction and old labels such as `USA`, `KOREA`, `KO-KR`, `MULTI-REGION`, or `JAPAN-TO-KOREAN` are provenance metadata, not structural folders.

## REV

Use explicit revision folders such as `REV-0`, `REV-A`, `REV-1`, `REV-5`, or `REV-ALL`. `REV-ALL` means an intentional cross-revision artifact; it must not be used merely because the original revision was unknown.

Legacy labels such as `MULTI-REV`, `REV-COMMON`, `REV-MIXED`, and `REV-UNKNOWN` are not canonical revision folders.

## WORK TYPE — Sakurai

Allowed research work types are:

`ANALYSIS`, `CENSUS`, `STRUCTURE`, `TEXT`, `DATA`, `DIFFS`, `TOOLS`, `TESTS`, `VERIFICATION`, `REPORTS`, `LOCALIZATION`, `DISASSEMBLY`, `MANIFESTS`, `MAPS`, and `SYMBOLS`.

Choose the work type from what the artifact is now, not where it came from. Examples:

- ROM identity / hashes / source identity → `MANIFESTS`
- filesystem, archive layouts, limits → `STRUCTURE`
- decoded tables and normalized records → `DATA`
- version/game comparisons → `DIFFS`
- unused/dummy/bug census → `CENSUS`
- phase summaries and narrative results → `REPORTS`
- reproducibility/audit results → `VERIFICATION`
- scripts used to inspect data → `TOOLS`

## No path replicas below WORK TYPE

Subfolders below WORK TYPE may describe a real subject, component, table, map, system, source relationship, or historical phase. They must **not recreate structural roles** already expressed by the canonical five levels.

Forbidden below WORK TYPE:

- another locale/region layer (`USA`, `KOREA`, `KR-KO`, `MULTI-REGION`, etc.);
- another revision layer (`REV-MIXED`, `MULTI-REV`, `REV-UNKNOWN`, etc.);
- another work-type layer such as `.../ANALYSIS/.../ANALYSIS/...`;
- an old complete project route such as `DPPt-HGSS/MULTI-REGION/REV-MIXED/ANALYSIS`;
- `LEGACY-*` wrappers whose only purpose is to preserve an old pathname.

Historical provenance belongs in `MANIFESTS` or in file metadata/text. Git history is the authoritative record of old paths.

A bundle name may appear below WORK TYPE only when it is a genuine subject name rather than a surrogate GAME layer; prefer explicit semantic names such as `HEARTGOLD-SOULSILVER`, `DIAMOND-PEARL`, `CROSS-GENERATION`, `MOVE-ENGINE`, or `FORM-SYSTEM`.

## Phase naming

`PHASE-*` may be retained as a secondary historical subdivision when it helps trace an existing workflow, but artifacts must first be placed under their semantic WORK TYPE. Do not create a top-level phase tree that mixes reports, data, diffs, tools, and unused findings together.

## Cross-generation work

Keep source provenance in a manifest. Analysis of a relationship may live under `ANALYSIS/CROSS-GENERATION/<SUBJECT>`. Target implementation artifacts should otherwise be owned by their actual target game/generation rather than by a synthetic source bundle.

## Migration rule

Migration must move the current tree into semantic canonical homes and remove the obsolete current paths. Do not preserve duplicate live copies solely to keep the old pathname. Old locations remain recoverable from Git history.

## Legacy workflows

Old project-specific GitHub Actions may remain under `.github/workflows-legacy/` and are intentionally inactive. Active validation enforces the canonical five-level path; generations that complete semantic normalization may additionally enable strict below-WORK-TYPE validation.
