# Gen II GSC ← Generation V Extended Parameter Bridge

Status: **architecture fixed; ROM-revision-specific address binding remains to be generated from each uploaded ROM.**

Targets: Japanese Crystal, English Crystal Rev A, Korean Gold, Korean Silver, with version-specific layouts kept separate.

## Goal

Generation V parameters are not reduced to the subset Gen II already understands. Missing data receives a new structure and runtime behavior while original Gen II tables/routines remain preserved.

## 1. Static species layer

Add a canonical Gen V personal-data table indexed by a project-wide 16-bit species ID. The table contains the raw BW/B2W2 personal record plus version/form routing.

Gen II `GetBaseData`-style consumers are migrated behind an adapter that can return either:

- `GEN2_ORIGINAL`
- `GEN5_BW_ORIGINAL`
- `GEN5_B2W2_ORIGINAL`
- `PROJECT_APPLIED`

The native Gen II base-data table remains unchanged for original-profile access.

## 2. Species ID expansion

Native Gen II persistent species IDs are 8-bit. National Dex 001–649 requires 10 bits, so every path that treats species as one byte must be audited.

Affected classes include at minimum:

- party/box species fields and species lists,
- current/temp/battle species WRAM variables,
- daycare/egg data,
- wild/trainer encounter data,
- Pokédex indexing,
- evolution targets,
- Hall of Fame,
- naming/species-name lookup,
- PC and box UI,
- link/trade serialization,
- script commands that embed a species ID.

**Rule:** no hard-coded address is written until it is verified separately in each JP/EN/KR revision.

## 3. Move ID expansion

Native Gen II move slots are 8-bit. Generation V move IDs exceed 255.

Project working move IDs become at least 10-bit / represented as 16-bit in new code. The migration scope includes:

- four stored move slots,
- level-up/egg/TM/HM/tutor lists,
- PP lookup,
- move-name lookup,
- battle current/selected/last move,
- Disable/Encore-like state,
- AI move data,
- link/trade serialization.

The native move table remains as the Gen II original profile.

## 4. Ability layer

Gen II has no ability engine. Add:

- species ability slots 1/2/hidden,
- per-Pokémon resolved ability slot,
- battle-start hooks,
- switch-in/switch-out hooks,
- pre-move/post-move hooks,
- damage/type hooks,
- status/stat hooks,
- end-of-turn hooks,
- field/wild-encounter hooks where Generation V defines them.

Ability IDs are project IDs mapped from Gen V IDs; merely storing an ability number is not considered implementation.

## 5. Physical / Special / Status category

Gen II chooses physical/special behavior from move type. Generation V requires category per move.

Add an extended move metadata lookup and replace type-based category decisions in battle calculations with:

`GetMoveDamageCategory(move, profile)`

while retaining a Gen II original profile that returns the original type-based result.

## 6. EV / IV / nature state

Gen II stat experience and DVs are not equivalent to Generation V EVs, IVs and natures.

Do not silently reinterpret these fields without a save-format plan. The project must preserve original mode and add a project-applied modern-stat mode. Candidate strategies, in priority order:

1. confirmed-unused per-mon bits/bytes,
2. compact sidecar state tied to party/box slots,
3. deliberate reuse of stat-exp bytes only in a migrated modern-stat save profile,
4. save/SRAM layout expansion after mapper/RAM verification.

No option is finalized until JP/EN/KR SRAM layouts and mapper constraints are verified.

## 7. Per-species friendship and growth

Original Gen II mon creation uses a global base-happiness constant. Project-applied mode changes this to a personal-data lookup.

Gen II's six growth table indexes include two legacy formulas not used by species in the current Crystal source. They are candidates for Erratic/Fluctuating in project mode, but this optimization requires binary verification in every target ROM before use.

## 8. Items and held items

Generation V item integration requires an extended/mapped item namespace; raw Gen V item numbers must never be written into Gen II fields.

Required systems:

- item parameter table,
- held-item effects,
- third wild-held-item slot,
- bag/PC/mart indexing,
- field/battle use,
- evolution/form-change item hooks,
- Fling/Natural Gift-era metadata where relevant.

## 9. Evolutions, forms, breeding

Use Generation V canonical structures rather than squeezing them into Gen II's compact evolution stream.

- 7 evolution entries per species,
- 16-bit condition parameter and target species,
- new Gen V condition handlers,
- `(species, form)` personal routing,
- BW/B2W2 egg-move profiles,
- breeding child/base relationship table.

## 10. Save compatibility rule

Static ROM parameters can be added before save migration. Any feature that adds persistent per-Pokémon state (extended species/move IDs, hidden-ability selection, form, modern EV/IV/nature data) is not marked complete until save/load, box switching, daycare, Hall of Fame and link/trade serialization are all updated and regression-tested.

## 11. Implementation sequence

1. Static Gen V personal/move/evolution/item corpus resident in ROM.
2. 16-bit working species/move accessors in engine RAM/code paths.
3. Existing 001–251 species consume full Gen V static parameters through the new profile.
4. Persistent extended-ID encoding and save migration.
5. Enable species 252–649 and moves >255.
6. Ability engine and hidden-ability state.
7. Modern EV/IV/nature profile.
8. Gen V evolution/breeding/item/move effect handlers.
9. JP/EN/KR cross-revision tests.
