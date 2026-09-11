# Repository Structure

This repository uses one canonical path model:

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

## 1. Generation

Allowed roots are `GENERATION-I` through `GENERATION-IX`.

## 2. Game

The GAME level contains only one canonical game title or the reserved `_SHARED` folder.

Canonical game names currently in scope:

- Generation I: `RED`, `GREEN`, `BLUE`, `YELLOW`
- Generation II: `GOLD`, `SILVER`, `CRYSTAL`
- Generation III: `RUBY`, `SAPPHIRE`, `EMERALD`, `FIRERED`, `LEAFGREEN`
- Generation IV: `DIAMOND`, `PEARL`, `PLATINUM`, `HEARTGOLD`, `SOULSILVER`
- Generation V: `BLACK`, `WHITE`, `BLACK2`, `WHITE2`
- Generation VI: `X`, `Y`, `OMEGA-RUBY`, `ALPHA-SAPPHIRE`
- Generation VII: `SUN`, `MOON`, `ULTRA-SUN`, `ULTRA-MOON`, `LETS-GO-PIKACHU`, `LETS-GO-EEVEE`
- Generation VIII: `SWORD`, `SHIELD`, `BRILLIANT-DIAMOND`, `SHINING-PEARL`, `LEGENDS-ARCEUS`
- Generation IX: `SCARLET`, `VIOLET`, `LEGENDS-Z-A`

Pair/group aliases such as `RGBY`, `GSC`, `GOLD-SILVER`, `DIAMOND-PEARL`, `DPPt-HGSS`, `BW`, `BW-B2W2`, `RSE-FRLG`, or `GEN3-SHARED` are not valid GAME folders. Truly shared material goes under `_SHARED`.

## 3. Language / Region

Use normalized locale tokens only:

- `JP-JA`
- `US-EN`
- `EU-EN`
- `EU-DE`
- `EU-FR`
- `EU-IT`
- `EU-ES`
- `KR-KO`
- `MULTI` only for artifacts that intentionally compare multiple locale variants
- `COMMON` only for language-independent data

Translation directions such as `JAPAN-TO-KOREAN` are not locale folders. Put that information in the work type and provenance metadata.

## 4. Revision

Use revision identifiers only:

- `REV-0`, `REV-A`, `REV-B`, `REV-1`, etc. for one real revision
- `REV-ALL` only for intentional cross-revision comparison

`MULTI-REV` and `REV-COMMON` are not valid revision names.

## 5. Work Type — Sakurai

Allowed top-level work types:

- `META`
- `ROM-IDENTITY`
- `STRUCTURE`
- `TEXT`
- `GAME-DATA`
- `EVENTS`
- `GRAPHICS-ANALYSIS`
- `DIFFS`
- `UNUSED`
- `LOCALIZATION`
- `TOOLS`
- `TESTS`
- `REPORTS`

Subfolders may exist below a work type when they describe real technical subdivisions, but they must not repeat generation/game/locale/revision concepts.

## 6. Shared and cross-generation work

`_SHARED` is reserved for genuinely generation-wide material that cannot belong to one game.

For cross-generation asset application:

- Source asset provenance stays with the original source game in Tsubaki.
- Target implementation analysis stays with the target game in Sakurai.
- Record source generation/game in a manifest instead of creating a synthetic GAME folder.

## 7. Naming rules

- Folder names are uppercase ASCII with hyphens where needed.
- No date folders. Dates belong in filenames or metadata.
- No `TEMP`, `MISC`, `ETC`, `FINAL`, `FINAL2`, or ad-hoc project aliases.
- Do not create a second alias for an existing game.
- Do not place workflows, translation directions, or project nicknames at the GAME level.

## Examples

```text
GENERATION-II/
└─ SILVER/
   └─ KR-KO/
      └─ REV-0/
         ├─ STRUCTURE/
         ├─ TEXT/
         └─ TESTS/
```

```text
GENERATION-IV/
└─ _SHARED/
   └─ COMMON/
      └─ REV-ALL/
         └─ REPORTS/
```

This document is the canonical path policy for all future automatic GitHub reflection.