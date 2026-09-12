# Generation II Pokémon status screen audit — JP Crystal / KR Gold & Silver

## Scope

Source ROM set already audited in this repository:

- Pocket Monsters Geum (Korea) — SHA-1 `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`
- Pocket Monsters Eun (Korea) — SHA-1 `cb22d7e03a74dc3a563fde6be8626626b2b392e7`
- Pocket Monsters - Crystal Version (Japan) — SHA-1 `95127b901bbce2407daf43cce9f45d4c27ef635d`

ROM binaries are not stored in GitHub.

## Confirmed Generation II state-machine structure

Gold/Silver and Crystal use three stat pages:

1. `PINK_PAGE`
2. `GREEN_PAGE`
3. `BLUE_PAGE`

Input behavior in Gold/Silver:

- Left / Right: previous or next page, wrapping 1↔3.
- Up / Down: previous or next party Pokémon when the source is a party/OT party object.
- B: exit.
- A: advance to the next page; on the last page, exit.
- Eggs use a dedicated status-screen path and can still be traversed with Up/Down.

Crystal preserves the three-page model but rewrites the screen driver into a jumptable/state-machine flow and adds animated front-picture handling.

## Korean Gold/Silver layout

The Korean localization uses the Japanese-style vertical split rather than the western horizontal split.

### Persistent left column

The left side remains visible while page content on the right changes. Confirmed coordinates in the Korean disassembly include:

- Pokédex No.: `(1,0)`
- Level: `(1,8)`
- Gender: `(5,8)`
- Nickname: `(1,10)`
- Species name after `/`: `(1,12)`
- Shiny marker: `(6,8)`
- Vertical divider: x=7 for all 18 tile rows
- Front sprite origin: `(0,1)`
- Page indicator area: left column bottom

`StatsScreen_PlacePageSwitchArrows` in Korean Gold/Silver is localized as a four-tile `◀페이지▶` graphic rather than the western top-area arrow placement.

## Page 1 — PINK

Right side displays:

- HP bar and current/max HP
- Status condition or Pokérus
- Type(s)
- Total experience
- Experience remaining to next level
- Next level value
- Experience bar

The Korean strings in the disassembly include `상태/`, `타입/`, `보통`, `포케러스`, `경험치`, `앞으로`, and `에서`.

Pokérus immunity is represented by a dot marker, matching the original Generation II logic.

## Page 2 — GREEN

Right side displays:

- Held item (`소지품`; `없음` if none)
- Four moves
- Current / maximum PP for each move

Korean page heading string: `사용할수 있는기술`.

The screen copies the four move IDs to the move-list buffer and renders names and PP with a three-row spacing per move in the Korean vertical layout.

## Page 3 — BLUE

Right side displays:

- Trainer ID number
- Original Trainer name (`어버이/` in the Korean original)
- Attack
- Defense
- Special Attack
- Special Defense
- Speed

This page directly uses the temporary Pokémon stat structure populated before screen rendering.

## Egg screen

Eggs do not reuse the normal three-page presentation. Gold/Silver use a dedicated egg status screen containing:

- `알`
- Unknown ID / OT placeholders
- Hatch-progress message selected from four happiness/egg-status thresholds

The Korean original has four distinct hatch-proximity messages.

## Crystal changes confirmed against the Gold/Silver implementation

Crystal keeps `PINK_PAGE`, `GREEN_PAGE`, and `BLUE_PAGE`, but the implementation has important changes:

- Screen execution is managed through `wJumptableIndex` and `wStatsScreenFlags`.
- Pokémon front sprites can animate from the status screen.
- Animation behavior distinguishes party, OT party, boxed, temporary, and wild Pokémon sources.
- The Blue page can display the Original Trainer's gender when Crystal caught-data fields contain it.
- Crystal adds support around caught-data structures used elsewhere by Crystal, while keeping the three status pages.
- Mobile/link battle paths receive dedicated status-screen entry handling.

## GS → Crystal structural conclusion

The core Generation II status-screen model is already modular:

`persistent Pokémon identity/sprite area + page dispatcher + page-specific renderer + source-Pokémon copier`

This is a useful integration point for Generation V → Pocket Monsters. A future expanded summary screen does not need to delete the Generation II UI model. The existing page dispatcher can be expanded while preserving the original three pages and egg path.

## Verification state

- KR Gold/Silver ROM identity: confirmed by existing local ROM audit and matching public Korean disassembly hashes.
- KR Gold/Silver three-page state machine: confirmed in Korean disassembly.
- KR vertical layout and exact tile coordinates: confirmed in Korean disassembly.
- JP/KR vertical-vs-western layout distinction: independently documented by Bulbapedia.
- Crystal three-page state machine and animation rewrite: confirmed in `pret/pokecrystal` disassembly.
- Exact Japanese Crystal ROM offsets/addresses: pending direct address-map pass against the uploaded JP Crystal ROM.

## External technical references

- Narishma-gb/pokegold-kr — Korean Gold/Silver WIP disassembly, `engine/pokemon/stats_screen.asm`
- pret/pokegold — Gold/Silver disassembly, `engine/pokemon/stats_screen.asm`
- pret/pokecrystal — Crystal disassembly, `engine/pokemon/stats_screen.asm`
- Bulbapedia — Generation II summary-screen localization/layout comparison
