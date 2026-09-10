# Generation I–V Status / Summary Screen Integration Specification

## Purpose

This document synthesizes the completed Generation I–IV status/summary audits with the verified Generation V behavioral model and defines a preservation-first integration architecture for **Generation V → ポケットモンスター**.

The goal is not to replace earlier status screens with Pokémon Black/White. The goal is to preserve original game-specific presentation and behavior, then add Generation V capabilities through a common extensible summary subsystem.

Priority remains:

`preserve -> coexist -> integrate -> expand -> conditional branch`

No ROM offset, overlay number, NARC member, or function address is promoted to fact unless directly verified.

---

## 1. Generation lineage

### Generation I — Japanese Red / Green / Blue / Pikachu

Architecture:

`StatusScreen -> StatusScreen2`

Two independent render routines are invoked in sequence. There is no persistent page index and no left/right page dispatcher.

Screen 1 preserves:

- front sprite
- Pokédex number
- nickname/species identity
- level
- HP bar and HP fraction
- status condition
- Attack / Defense / Speed / Special
- Type 1 / Type 2
- OT / Trainer ID
- cry

Screen 2 preserves:

- total EXP
- EXP to next level
- target next level
- four moves
- current / maximum PP

Japanese Pikachu adds a status-screen-specific special starter Pikachu voice branch.

### Generation II — Gold / Silver / Crystal

Architecture:

`persistent identity/sprite region + 3-page dispatcher + page-specific renderer`

Pages:

1. PINK — HP/status/type/EXP
2. GREEN — held item/moves/PP
3. BLUE — OT/ID/battle stats

New interaction model:

- Left/Right: page change
- Up/Down: party Pokémon change
- A: advance/exit
- B: exit

Crystal retains the three-page model while adding a more explicit jumptable/state-machine driver and animated status-screen Pokémon portrait handling.

### Generation III — RSE / FRLG

RSE normal pages:

1. Info
2. Skills
3. Battle Moves
4. Contest Moves

FRLG normal pages:

1. Info
2. Skills
3. Moves

Generation III turns the status screen into a broader inspection subsystem and adds/expands:

- Nature-era individual metadata
- Ability
- meeting/origin presentation
- held item
- ribbon count in RSE
- caught-ball marker
- Pokémon markings
- detailed move type/power/accuracy/description
- move-order editing
- Contest interpretation of moves in RSE

FRLG must remain a distinct family: no Contest page/data, Ability placement differs, and the portrait has its own bounce response behavior.

### Generation IV — D/P/Pt / HGSS

D/P/Pt primary categories:

1. Pokémon Info
2. Trainer Memo
3. Pokémon Skills
4. Battle Moves
5. Condition
6. Contest Moves
7. Ribbons

Generation IV adds/formalizes:

- meeting date in summary
- Physical / Special / Status move category
- Characteristic
- dedicated Ribbon view
- touch navigation
- reduced in-battle summary family

HGSS reorganizes the larger Sinnoh set into three paired dual-screen groups:

1. Trainer Memo / Info
2. Skills / Battle Moves
3. Performance / Ribbons

HGSS-specific preserved content includes:

- Pokéathlon Performance: Speed / Power / Skill / Stamina / Jump
- Shiny Leaf display
- nature-stat increase/decrease visual emphasis

### Generation V — BW / B2W2

Verified behavioral model:

- dual-screen summary presentation
- primary Status / Stats-oriented browsing with move-detail subview
- conditional Ribbon page: absent when the Pokémon has no Ribbons
- six markings are displayed
- BW: markings cannot be edited from the summary
- B2W2: markings can be edited from the summary
- move order remains editable
- in-battle reduced family: Summary / Check Moves / move description
- animated Pokémon sprite presentation
- touching the Pokémon can show its back sprite
- additional stylus gestures can trigger sprite motion

Exact BW/B2W2 overlay/NARC/member mapping remains **UNRESOLVED** until direct ROM member-level tracing succeeds.

---

## 2. Unified capability registry

The final subsystem must not hard-code one fixed page count. It should register capabilities and construct the visible page set from the active game profile, source Pokémon, battle state, and feature availability.

Recommended capability IDs:

| Capability | Meaning | Earliest source |
|---|---|---|
| `SUMMARY_IDENTITY` | nickname/species/Dex No./level/gender | Gen I core, gender Gen II |
| `SUMMARY_PORTRAIT` | Pokémon front image and cry | Gen I |
| `SUMMARY_PORTRAIT_INTERACTION` | bounce/animation/back-view/touch response | FRLG/Crystal/Gen V variants |
| `SUMMARY_HP_STATUS` | HP/status display | Gen I |
| `SUMMARY_TYPES` | type display | Gen I |
| `SUMMARY_OT_ID` | OT and Trainer ID | Gen I |
| `SUMMARY_STATS_LEGACY` | Attack/Defense/Speed/Special | Gen I |
| `SUMMARY_STATS_SPLIT` | HP/Atk/Def/SpA/SpD/Spe | Gen II onward |
| `SUMMARY_HELD_ITEM` | held item | Gen II |
| `SUMMARY_EXP` | total EXP / to next level / bar | Gen I/II |
| `SUMMARY_MOVES_BASIC` | four moves + PP | Gen I |
| `SUMMARY_MOVE_DETAILS` | type/power/accuracy/description | Gen III |
| `SUMMARY_MOVE_REORDER` | reorder known moves | Gen II dedicated move screen / Gen III summary onward |
| `SUMMARY_MOVE_CATEGORY` | Physical/Special/Status | Gen IV |
| `SUMMARY_NATURE` | Nature | Gen III |
| `SUMMARY_CHARACTERISTIC` | Characteristic | Gen IV |
| `SUMMARY_ABILITY` | Ability and description | Gen III |
| `SUMMARY_MET_LEVEL` | meeting level | Gen III |
| `SUMMARY_MET_LOCATION` | meeting location/region | Gen III |
| `SUMMARY_MET_DATE` | meeting/transfer date | Gen IV |
| `SUMMARY_CAUGHT_BALL` | captured ball display | Gen III |
| `SUMMARY_MARKINGS_VIEW` | markings display | Gen III |
| `SUMMARY_MARKINGS_EDIT` | markings editable from summary | B2W2 |
| `SUMMARY_POKERUS` | Pokérus status/cured marker | Gen II onward |
| `SUMMARY_RIBBON_COUNT` | count only | RSE |
| `SUMMARY_RIBBON_LIST` | ribbon list/detail | Gen IV onward |
| `SUMMARY_CONDITION` | Contest Condition/Sheen | RSE/Sinnoh family |
| `SUMMARY_CONTEST_MOVES` | Contest/Super Contest move interpretation | RSE/DPPt |
| `SUMMARY_PERFORMANCE` | Pokéathlon five-stat Performance | HGSS |
| `SUMMARY_SHINY_LEAF` | Shiny Leaf/crown | HGSS |
| `SUMMARY_EGG` | dedicated egg presentation | Gen II onward, family-specific |
| `SUMMARY_IN_BATTLE` | reduced battle-safe summary | Gen IV onward |
| `SUMMARY_RIBBON_CONDITIONAL` | omit Ribbon page if none | Gen V |
| `SUMMARY_GAME_SPECIFIC` | game/version-only fields and behaviors | all generations |

---

## 3. Page registry ABI

Recommended conceptual structures:

```text
SummaryContext
├── source_kind
│   ├── PARTY
│   ├── ENEMY_PARTY
│   ├── BOX
│   ├── DAYCARE
│   ├── LINK
│   ├── BATTLE
│   └── TEMP
├── game_profile
├── ruleset_profile
├── mon_handle
├── capability_bits
├── current_page
├── current_mon_index
├── mode
├── input_adapter
├── render_adapter
└── data_adapter

SummaryPageDescriptor
├── page_id
├── required_capabilities
├── forbidden_modes
├── source_game
├── visibility_predicate
├── render_fn
├── input_fn
├── detail_view_fn
└── original_or_integrated
```

This allows a game to preserve its original pages while appending later capabilities without deleting original content.

---

## 4. Preserve-first page policy by target engine

### Generation I target

Keep the original two-screen sequence as an **Original profile**.

Add an Expanded profile that converts the sequence into a page dispatcher while retaining the first two original information groups intact. Later capabilities can be appended as new pages.

Do not silently replace the Gen-I single `Special` presentation when the original battle-rules profile is active. If split SpA/SpD mechanics are enabled, expose them through an expanded stats page while preserving original semantics/documentation.

Pikachu special starter voice behavior remains a version-specific hook.

### Generation II target

Extend the existing three-page dispatcher rather than replacing it.

Original pages 1–3 remain addressable. New pages may include:

- Trainer Memo
- Ability
- detailed Moves
- Ribbons/Markings
- game-specific later-system information

Crystal portrait animation remains active where compatible.

### Generation III target

RSE:

- preserve Info / Skills / Battle Moves / Contest Moves
- append later features rather than sacrificing Contest content

FRLG:

- preserve Info / Skills / Moves family
- retain FRLG portrait response behavior
- add Contest-related pages only if the project later implements Contest systems as imported content; never label them as original FRLG content

### Generation IV target

D/P/Pt:

- preserve all seven original categories
- later BW behavior is layered on top

HGSS:

- preserve the three paired dual-screen groups
- preserve Performance and Shiny Leaf
- Gen V animation/touch behaviors may be added through the same dual-screen application model

### Generation V target/reference

BW/B2W2 remain the Generation V behavior baseline, with BW and B2W2 differences kept separately.

B2W2 marking editability must not be back-projected as BW behavior.

---

## 5. Input abstraction

A unified input layer is required because target hardware differs.

Logical actions:

```text
SUMMARY_PREV_PAGE
SUMMARY_NEXT_PAGE
SUMMARY_PREV_MON
SUMMARY_NEXT_MON
SUMMARY_CONFIRM
SUMMARY_CANCEL
SUMMARY_OPEN_DETAIL
SUMMARY_REORDER_MOVE
SUMMARY_MARK_TOGGLE
SUMMARY_PORTRAIT_INTERACT
```

Adapters map those actions to:

- GB/GBC buttons
- GBA buttons
- DS buttons
- DS touch regions/gestures

Touch-dependent Gen V functions therefore remain available on earlier hardware through button/context-menu equivalents instead of being deleted.

---

## 6. Data-source abstraction

The renderer must not assume the source is always the player's party.

At minimum preserve adapters for:

- party
- opponent/enemy party where legally visible
- box
- daycare
- battle temporary data
- link/trade context

Generation I already demonstrates this abstraction through `wMonDataLocation`; later engines provide their own source-mode structures. The unified system should formalize this as a source adapter rather than duplicating page code.

---

## 7. Conditional visibility rules

Examples:

- Egg -> egg-safe page set; hide invalid battle-stat/move data as required by source behavior.
- No Ribbons + Generation V behavior profile -> omit Ribbon page.
- RSE profile -> enable Contest Moves and Condition capabilities.
- FRLG original profile -> Contest page disabled because original FRLG has no Contest subsystem.
- D/P/Pt -> enable Condition + Super Contest + Ribbon pages.
- HGSS -> enable Performance + Shiny Leaf; no Sinnoh Contest page unless explicitly integrated as imported content.
- BW -> markings view-only.
- B2W2 -> markings view + edit.
- In battle -> reduced battle-safe page registry.

---

## 8. Verification matrix

| Area | Status |
|---|---|
| Gen I Japanese two-screen architecture | CONFIRMED |
| Gen I Japanese displayed fields | CONFIRMED |
| Japanese Pikachu special voice branch | CONFIRMED |
| Gen II three-page dispatcher | CONFIRMED |
| Gen II JP/KR vertical-family layout | CONFIRMED |
| Crystal animation/state-machine changes | CONFIRMED |
| RSE four-page summary model | CONFIRMED |
| FRLG separate three-page family | CONFIRMED |
| Gen III move detail / reorder behavior | CONFIRMED |
| D/P/Pt seven-category model | CONFIRMED |
| HGSS three paired dual-screen groups | CONFIRMED |
| Gen IV met date / move category | CONFIRMED |
| HGSS Performance / Shiny Leaf | CONFIRMED |
| BW Status/Stats/move-detail family | CONFIRMED behaviorally |
| BW conditional Ribbon page | CONFIRMED behaviorally |
| BW markings display-only | CONFIRMED behaviorally |
| B2W2 markings editable in summary | CONFIRMED behaviorally |
| Gen V portrait touch/back-view interaction | CONFIRMED behaviorally |
| Gen V exact overlay/NARC/member mapping | UNRESOLVED |
| Exact per-ROM offsets across all revisions | PARTIAL / PENDING |
| Pixel/hash-equivalent asset dedup across versions | PENDING |

---

## 9. Immediate implementation order

1. Freeze `SummaryCapability` IDs and page registry schema.
2. Build per-generation/per-title page correspondence table.
3. Build field-level data-source map for every capability.
4. Map target-engine input and renderer adapters.
5. Complete direct BW/B2W2 overlay/NARC/member trace.
6. Complete per-ROM status asset extraction and hash deduplication.
7. Implement expanded dispatcher in the earliest target engine first without deleting original pages.
8. Add later capabilities one by one with source-game conditions.
9. Test party/box/daycare/link/battle/egg contexts separately.
10. Compare each original title against original behavior before enabling integrated extensions.

---

## 10. Source anchors

Internal Sakurai audits:

- `GENERATION-I/RGBY/JP/MULTI-REV/ANALYSIS/STATUS-SCREEN/README.md`
- `GENERATION-II/POCKET-MONSTERS-GSC/JP-KR/MULTI-REV/ANALYSIS/STATUS-SCREEN/README.md`
- `GENERATION-III/RSE-FRLG/MULTI-REGION/REV-MIXED/ANALYSIS/STATUS-SCREEN/README.md`
- `GENERATION-IV/DPPt-HGSS/MULTI-REGION/REV-MIXED/ANALYSIS/STATUS-SCREEN/README.md`

External behavioral cross-check:

- Bulbapedia Summary / Summary screen feature and gallery tables
- Bulbapedia Marking
- Bulbapedia Ribbon

Direct Gen V ROM resource mapping remains a pending binary-analysis task and no guessed offsets are included here.
