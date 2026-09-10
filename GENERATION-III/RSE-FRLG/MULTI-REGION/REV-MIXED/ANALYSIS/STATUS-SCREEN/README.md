# Generation III Pokémon status / summary screen audit — RSE / FRLG

## Scope

This pass compares the Generation III summary-screen families as distinct products rather than treating the generation as one UI:

- Pokémon Ruby / Sapphire
- Pokémon Emerald
- Pokémon FireRed / LeafGreen

Primary implementation references are `pret/pokeruby`, `pret/pokeemerald`, and `pret/pokefirered`. Existing Sakurai Emerald cross-language disassembly work remains the ROM-side anchor; exact per-build JP/EN summary-function offsets are a follow-up binary mapping task.

ROM binaries are not stored in GitHub.

## Ruby / Sapphire — confirmed four-page model

`pret/pokeruby/include/pokemon_summary_screen.h` defines four visible summary pages:

1. `PSS_PAGE_INFO`
2. `PSS_PAGE_SKILLS`
3. `PSS_PAGE_BATTLE_MOVES`
4. `PSS_PAGE_CONTEST_MOVES`

The screen also has explicit operating modes for normal view, moves-only view, move selection, move deletion, move-order-edit lockout, PC normal view, and PC moves-only view.

The Ruby/Sapphire source confirms the page header family `PokeInfo / PokeSkills / BattleMoves / ContestMoves` and dedicated input handlers for Left/Right page changes, Up/Down Pokémon changes, A-button move-page entry, and move-order editing.

### R/S Info page

The information page is responsible for the individual Pokémon identity/memo layer introduced in Generation III, including Trainer Memo logic and the information necessary to describe the Pokémon's origin/meeting circumstances. The summary system also handles the Pokémon front sprite, caught-ball sprite, gender, Pokédex identity, type display, status/Pokérus state, and related identity markers.

### R/S Skills page

Confirmed fields include:

- held item
- ribbon count
- HP and the five non-HP battle stats
- total experience
- experience to next level
- experience progress bar

The code explicitly calls `PrintHeldItemName`, `PrintNumRibbons`, and the stat/experience printers from this page.

### R/S Battle Moves page

Generation III expands the move list into a detailed inspection UI. The battle-move path supports:

- four move slots
- current / maximum PP
- move type
- power
- accuracy
- move description
- move selection and order swapping

This is the first handheld-generation summary family in which the normal summary screen itself carries the richer move-detail workflow rather than relying on the Generation II party-menu `usable moves` screen.

### R/S Contest Moves page

R/S preserves a completely separate Contest interpretation of the same four moves. The source contains Contest category/type sprites, Contest move/effect tables, Contest-effect strings, and dedicated Contest move rendering.

Generation III Contest move records are separate game data, not merely cosmetic labels. Their data drive Contest category, effect, appeal/jam behavior, combo identifiers, and summary descriptions.

## Emerald — four pages preserved, screen engine reorganized

`pret/pokeemerald/src/pokemon_summary_screen.c` explicitly defines:

1. `PSS_PAGE_INFO`
2. `PSS_PAGE_SKILLS`
3. `PSS_PAGE_BATTLE_MOVES`
4. `PSS_PAGE_CONTEST_MOVES`
5. `PSS_PAGE_COUNT`

Thus Emerald preserves the R/S four-page visible content model rather than replacing it.

### Emerald Info page

The dynamic Info-page window set explicitly contains:

- Original Trainer
- Trainer ID
- Ability
- Trainer Memo

The extracted summary buffer also stores species, level, ribbon count, ailment, ability selector, met location, met level, met game, personality ID, experience, moves, PP, all six stats, held item, friendship, OT gender, nature, PP bonuses, OT name, and OT ID.

Ability name and description are printed as part of the Info page in Emerald.

### Emerald Skills page

The dynamic Skills-page fields explicitly contain:

- held item
- ribbon count
- HP / Attack / Defense
- Special Attack / Special Defense / Speed
- EXP / next-level EXP

The page calls `PrintHeldItemName`, `PrintRibbonCount`, the two stat-column printers, and `PrintExpPointsNextLevel`.

RSE does not provide a dedicated ribbon-list page: the summary shows only the number of Ribbons; the detailed ribbon view belongs to the PokéNav.

### Emerald Battle Moves page

The implementation contains dedicated move-name/PP windows, move descriptions, type icons, and a sliding Power/Accuracy panel. It also contains explicit move-selection and move-position-switch state machines plus separate party- and Box-Pokémon swapping functions.

### Emerald Contest Moves page

The implementation has a distinct sliding Appeal/Jam panel, Contest move type/category icons, Contest descriptions, and explicit heart tiles:

- empty appeal heart
- filled appeal heart
- filled jam heart
- empty jam heart

This page is therefore a real functional branch of the summary engine and must be preserved when Generation V UI/features are integrated into an RSE-derived target.

### Emerald page-transition architecture

Emerald allocates two 0x400 tilemap buffers for each of the four pages and contains explicit `ChangePage`, `PssScrollRight`, `PssScrollLeft`, pagination, and sliding-window routines. Page-specific panels can therefore animate independently of the persistent Pokémon portrait/identity layer.

The screen also handles:

- party and Box Pokémon sources
- Multi Battle ordering
- new-move selection
- move-order lockouts
- egg-specific page limitation
- Pokémon markings
- caught-ball icon
- status icon
- Pokérus-cured symbol
- Deoxys-specific display handling

## FireRed / LeafGreen — a different three-page family

FRLG must not be treated as `RSE minus one decorative tab`. `pret/pokefirered` implements a separately reorganized summary engine.

The page enum includes:

- `PSS_PAGE_INFO`
- `PSS_PAGE_SKILLS`
- `PSS_PAGE_MOVES`
- `PSS_PAGE_MOVES_INFO`
- additional special/internal move-related page states

Normal browsing is the three-page Info → Skills → Moves family. `PSS_PAGE_MOVES_INFO` is a move-detail/selection state rather than a fourth normal Contest page.

### FRLG Info page

The normal information page contains the Pokémon identity and Trainer Memo presentation. FRLG has dedicated Kanto/Sevii-region memo logic and separate memo handling for eggs and Pokémon not held by their Original Trainer.

### FRLG Skills page

A significant layout change from Emerald is confirmed in code: `PokeSum_PrintAbilityNameAndDesc()` is dispatched on `PSS_PAGE_SKILLS`, not the Info page.

The skills page also owns the battle-stat / EXP presentation. FRLG uses sprite-based HP and EXP bar objects in addition to its text/window layer.

### FRLG Moves page

FRLG keeps the Generation III battle-move detail feature:

- move names
- current/max PP
- type icons
- power
- accuracy
- description
- move selection
- move-position swapping

It has a dedicated `PSS_PAGE_MOVES_INFO` detailed state and separate move-selection cursor sprites.

### No Contest page / no Contest data

FRLG has no Pokémon Contests. Generation III Contest move data used by RSE is not included for FRLG, and the normal FRLG summary has no Contest Moves page.

This is a structural content difference, not merely a hidden UI flag.

### Ribbons in FRLG

Ribbon data on a transferred Pokémon are retained, but FRLG provides no way to view the Pokémon's ribbons. In contrast, RSE summary shows the ribbon count and the PokéNav can show the actual ribbons.

This distinction must be preserved in source documentation even if the final integrated project later chooses to expose ribbon data through an expanded page.

### FRLG portrait behavior

FRLG gives its summary portrait a unique bounce response associated with the Pokémon cry. The implementation has a dedicated `MonPicBounceState`; documented game behavior varies the number of jumps according to the Pokémon's current condition/HP and suppresses the bounce in incapacitated/status cases.

### FRLG graphics/state architecture

The FRLG summary structure owns three 0x800 BG tilemap buffers and explicit page-flip state, background-horizontal-offset animation, window sets, and sprite objects for:

- front Pokémon picture
- small Pokémon icon
- caught-ball icon
- HP bar
- EXP bar
- status icon
- Pokérus icon
- shiny star
- markings
- move-selection cursors

Thus FRLG should receive its own implementation mapping rather than reusing Emerald offsets/layout assumptions.

## Generation III comparison matrix

| Feature | Ruby/Sapphire | Emerald | FireRed/LeafGreen |
|---|---|---|---|
| Normal visible pages | 4 | 4 | 3 |
| Info | yes | yes | yes |
| Skills | yes | yes | yes |
| Battle/Known Moves | yes | yes | yes |
| Contest Moves | yes | yes | no |
| Move type/power/accuracy/description | yes | yes | yes |
| Move order editing in summary | yes | yes | yes |
| Ability displayed | yes | Info page | Skills page |
| Held item | yes | Skills page | yes |
| Ribbon count in summary | yes | yes | no |
| Detailed ribbons in summary | no | no | no |
| Detailed ribbons elsewhere | PokéNav | PokéNav | unavailable |
| Markings displayed | yes | yes | yes |
| Markings editable directly in summary | no | no | no |
| Contest move data present | yes | yes | no |
| Dedicated reduced in-battle summary | no Gen-IV-style variant | no Gen-IV-style variant | no Gen-IV-style variant |
| Egg-specific handling | yes | yes | yes |

## Generation II → III transition

The important architectural change is not merely higher-color graphics. Generation III turns the status screen into a general-purpose Pokémon inspection subsystem:

`identity / Trainer Memo + stats / EXP + detailed battle moves + optional game-family content`

Compared with Generation II, the screen gains Nature/Ability-era individual metadata, meeting/origin presentation, detailed move statistics and description, summary-level move reordering, caught-ball/marking presentation, and—on Hoenn games—a second interpretation of the move list for Contests.

## Implication for Generation V → Pocket Monsters

The integration target should use capabilities rather than replacing whole pages blindly.

Recommended preserved capability set:

- `SUMMARY_INFO`
- `SUMMARY_TRAINER_MEMO`
- `SUMMARY_SKILLS`
- `SUMMARY_BATTLE_MOVES`
- `SUMMARY_MOVE_REORDER`
- `SUMMARY_CONTEST_MOVES` (RSE only as original content)
- `SUMMARY_RIBBON_COUNT` (RSE original behavior)
- `SUMMARY_RIBBON_LIST` (later-generation integration capability, not falsely attributed to Gen III)
- `SUMMARY_MARKINGS`
- `SUMMARY_EGG`
- `SUMMARY_GAME_SPECIFIC`

When Generation V functionality is brought backward, RSE's Contest page must not be deleted to make room for BW-style pages. FRLG likewise should retain its original three-page Kanto family and gain additional pages/capabilities through expansion rather than being forcibly converted into the Emerald layout.

## Verification state

### Confirmed

- R/S four-page enum and summary modes: `pret/pokeruby`.
- R/S Contest-page code/data presence: `pret/pokeruby`.
- Emerald four-page enum and dynamic field ownership: `pret/pokeemerald`.
- Emerald Ability on Info and ribbon count on Skills: `pret/pokeemerald`.
- Emerald Power/Accuracy and Appeal/Jam sliding panels: `pret/pokeemerald`.
- Emerald move-reorder routines and page scrolling: `pret/pokeemerald`.
- FRLG three-page normal browsing family plus Moves Info substate: `pret/pokefirered`.
- FRLG Ability rendered on Skills page: `pret/pokefirered`.
- FRLG dedicated portrait/HP/EXP/status/Pokérus/shiny/marking/move-cursor objects: `pret/pokefirered`.
- FRLG lack of Contest move data: Generation III Contest data documentation plus FRLG source structure.
- RSE ribbon-count vs PokéNav ribbon-list behavior, and FRLG inability to view ribbons: documented cross-game behavior.

### Pending direct ROM mapping

- exact JP and western ROM offsets for every summary-screen function
- compressed graphics/palette/tilemap byte ranges per revision/language
- Japanese official page-label string extraction and pointer locations
- R/S vs Emerald binary-level routine correspondence
- FR vs LG binary equality/differences for summary assets and code
- revision-specific differences in the supplied JP/EN builds

No guessed ROM addresses are recorded as facts.

## Technical references

- pret/pokeruby — `include/pokemon_summary_screen.h`, `src/pokemon_summary_screen.c`
- pret/pokeemerald — `include/pokemon_summary_screen.h`, `src/pokemon_summary_screen.c`
- pret/pokefirered — `include/pokemon_summary_screen.h`, `src/pokemon_summary_screen.c`
- Bulbapedia — Summary / Generation III gallery and feature comparison
- Bulbapedia — Contest move data structure (Generation III)
- Bulbapedia — Ribbon checking behavior by game
- Sakurai existing Emerald cross-language disassembly work — `GENERATION-III/EMERALD/MULTI/ALL/DISASSEMBLY/`
