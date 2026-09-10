# Generation I Japanese Pokémon status screen audit — Red / Green / Blue / Pikachu

## Scope

This audit covers the Japanese Generation I status/summary screen implementation used by:

- ポケットモンスター 赤
- ポケットモンスター 緑
- ポケットモンスター 青
- ポケットモンスター ピカチュウ

Primary implementation references:

- Narishma-gb/pokegreen — Japanese Red/Green disassembly
- Narishma-gb/pokeblue — Japanese Blue disassembly
- Narishma-gb/pokeyellow-jp — Japanese Yellow disassembly
- pret/pokered — international Red/Blue comparison reference

ROM binaries are not stored in this repository.

## Confirmed project-source identities

File-library audit data already confirms Japanese Red Rev0 and RevA:

- Pocket Monsters - Aka (Japan) (SGB Enhanced).gb — SHA-1 `0623ad12f48c259447980d68bd85ddbf8204b2cd`
- Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb — SHA-1 `ef74c79cded14204ac79e77f4964d9cb25003120`

Japanese Pikachu revision manifests already confirm:

- Rev 0A — SHA-1 `1fb6c264e950d97ce3fd99b347e485b2150df4ff`
- Rev B — SHA-1 `28e4b8531ea4ea1de5a396fccb0cfba51b06b149`
- Rev C — SHA-1 `91864ecdf26d1c593bde4d9ed615520eb57d5e41`
- Rev D — SHA-1 `a40298a8123613ee60cd7aab204d788b8425976e`

The public Japanese disassemblies additionally build Japanese Green Rev0/RevA and Japanese Blue.

## Core architecture: two sequential screens, not a page state machine

Generation I does not have the later left/right page dispatcher used in Generation II and beyond.

The normal flow explicitly invokes two independent routines in sequence:

1. `StatusScreen`
2. `StatusScreen2`

Call sites in the start-menu, Bill's PC, battle, and link/trade paths invoke both routines consecutively.

Each routine waits for a button press before returning. Therefore the practical user flow is:

`open status -> screen 1 -> button -> screen 2 -> button -> close/return`

There is no persistent page index, no left/right page loop, and no up/down party-Pokémon switching inside the status-screen routines themselves.

## Screen 1 — identity / HP / battle stats / type / OT

`StatusScreen` loads the selected Pokémon into the common loaded-mon structure and renders:

- front sprite
- Pokédex number
- nickname/name
- level
- HP bar
- current HP / maximum HP
- status condition; `ふつう` when no ailment is present
- Attack
- Defense
- Speed
- Special
- Type 1
- Type 2
- Trainer ID number
- Original Trainer (`おや`)

Japanese labels confirmed in Red/Green/Blue/Pikachu source include:

- `じょうたい／`
- `ふつう`
- `タイプ１／`
- `タイプ２／`
- `<ID>№／`
- `おや／`
- `こうげき`
- `ぼうぎょ`
- `すばやさ`
- `とくしゅ`

The routine draws two major right-side line boxes and a separate lower-left stats box. The Pokémon front sprite is loaded at the left side after the text/UI setup, and its cry is played before waiting for input.

## Screen 2 — experience / moves / PP

`StatusScreen2` reuses the selected loaded Pokémon and replaces the lower content with:

- Pokémon name
- total experience (`けいけんち`)
- experience remaining to the next level (`あと`)
- target next level
- four move names
- current PP / maximum PP for each move

Unused move slots are filled with dash glyphs. Maximum PP is calculated per move through the common PP routine rather than stored as a rendered constant.

At level 100, the experience-to-next-level calculation is explicitly zeroed.

Japanese labels confirmed include:

- `けいけんち／`
- `あと`
- full-width `ＰＰ`

## Shared data model

The two screens are fed from `LoadMonData` and the `wLoadedMon*` temporary structure. The display source can represent:

- player party
- enemy party
- box Pokémon
- daycare Pokémon

For box/daycare sources, battle stats are recalculated from the boxed level before display because full party-style calculated battle stats are not stored in the same form.

Nickname and OT pointers are selected by `wMonDataLocation` and then indexed by `wWhichPokemon` where applicable.

## Graphics / tile behavior

The status screen reuses a notable amount of battle/UI tile infrastructure rather than owning a later-generation self-contained summary resource package.

Confirmed reused resources include:

- HP/status tile patterns
- selected Battle HUD line/box tiles
- a dedicated bold `P` glyph used for PP
- standard textbox-border drawing routines
- normal front Pokémon graphics loader

Tile animation is temporarily disabled during status-screen drawing and restored when each screen exits.

## Japanese Red/Green vs Blue

The audited Japanese Red/Green and Japanese Blue `status_screen.asm` implementations are structurally equivalent in the status-screen flow and displayed fields:

- same two-routine model
- same identity/HP/stats/type/OT first screen
- same experience/moves/PP second screen
- same Japanese field labels
- same loaded-mon data-source model

Any version-specific differences outside this routine (species graphics, SGB palettes, game data, text elsewhere) must not be incorrectly promoted into status-screen differences without direct evidence.

## Pikachu version difference

Japanese Pikachu preserves the same two-screen structure and almost all rendering logic, but changes the cry path on the first status screen.

When the displayed Pokémon is the player's special starter Pikachu (party or box source), the routine calls the dedicated Pikachu voice/sound-clip path instead of the ordinary species cry. Enemy-party Pikachu and ordinary Pikachu use the regular cry path.

This is a confirmed status-screen-specific version feature and must be preserved independently when integrating later-generation UI behavior.

## Generation I -> Generation II structural transition

Generation I model:

`two hard-sequenced render routines`

Generation II model:

`persistent identity area + 3-page dispatcher + page-specific renderer + up/down Pokémon switching`

The key architectural step between generations is therefore not merely 'one more page'. Generation II converts a fixed two-screen script into a reusable interactive page system.

## Integration implication for Generation V -> ポケットモンスター

Do not delete the Generation I information model when adopting later summary-screen presentation.

Preserve at minimum:

- original Generation I four-stat presentation semantics (Attack / Defense / Speed / Special) when operating in an original-rule profile
- Type 1 / Type 2 presentation
- OT / ID
- total EXP / EXP-to-next-level
- four moves and current/max PP
- Pokémon cry behavior
- Pikachu-version special starter voice branch

A Generation-V-style expanded screen can present these through a modernized page dispatcher, but the original fields and special branches remain source content rather than being silently replaced.

## Verification state

- Japanese Red Rev0/RevA ROM identities: confirmed in existing project file-library audit.
- Japanese Pikachu Rev0A/B/C/D identities: confirmed in existing project file-library glyph manifest.
- Japanese Red/Green two-screen code: confirmed in Narishma-gb/pokegreen.
- Japanese Blue two-screen code: confirmed in Narishma-gb/pokeblue.
- Japanese Pikachu two-screen code and special starter-Pikachu voice branch: confirmed in Narishma-gb/pokeyellow-jp.
- Exact ROM offsets for all routines across every Japanese revision: pending direct per-ROM symbol/address-map pass.
- Pixel-identical graphics-resource comparison across Red/Green/Blue/Pikachu: pending direct asset/hash pass.
