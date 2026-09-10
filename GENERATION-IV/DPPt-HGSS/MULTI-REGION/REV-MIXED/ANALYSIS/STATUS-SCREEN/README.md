# Generation IV Pokémon Summary / Status Screen Audit — DP / Pt / HGSS

## Scope

This pass records the Generation IV summary-screen model as an implementation reference for Generation V → ポケットモンスター. It does not replace earlier-generation UI; it identifies what Generation IV added, preserved, regrouped, or specialized.

Existing local ROM audit in this repository confirms the following Generation IV source baseline:

- Pokémon Diamond — EN-US, 64 MiB
- Pokémon Pearl — EN-US, 64 MiB
- Pokémon Platinum — KO-KR, 128 MiB
- Pokémon HeartGold — KO-KR, 128 MiB
- Pokémon SoulSilver — KO-KR, 128 MiB

ROM binaries are not stored in GitHub.

## Major Generation IV additions

Compared with Generation III, Generation IV adds or formalizes several summary-screen features that matter for later integration:

- Meeting date is displayed in the summary beginning in Generation IV.
- Move category is displayed: Physical / Special / Status.
- A dedicated reduced-information summary path exists during battle.
- Touch-screen page navigation is supported in the Sinnoh games, with D-pad navigation also retained.
- Move ordering remains available from the summary screen.
- Ribbons receive a full summary page/view rather than only a count in the RSE summary.

## Diamond / Pearl / Platinum — seven primary tabs

The Sinnoh summary model has seven main tabs:

1. Pokémon Info
2. Trainer Memo
3. Pokémon Skills
4. Battle Moves
5. Condition
6. Contest Moves
7. Ribbons

The gallery/manual flow additionally has detail states for:

- Battle Move description
- Contest Move description
- Ribbon description

These are detail views/substates rather than additional independent top-level information categories.

### Pokémon Info

Confirmed labels in the Diamond message archive include:

- Pokédex No.
- Name
- Type
- OT
- ID No.
- Exp. Points
- To Next Lv.
- Held Item is also part of the persistent summary presentation.

### Trainer Memo

The Trainer Memo is a distinct tab in D/P/Pt. It includes Nature and origin/met information. Generation IV summary text includes the met date in addition to met location and met level.

The Diamond message archive contains templates for:

- Nature
- date
- met/arrived location
- met/arrived level
- egg obtained/received date and place
- hatch date/place

### Pokémon Skills

The Skills page contains:

- HP
- Attack
- Defense
- Special Attack
- Special Defense
- Speed
- Ability and Ability description

D/P/Pt show the stat values but do not yet use the HGSS-and-later nature-based stat-color emphasis.

### Battle Moves

The Battle Moves page displays the four moves and their detailed battle properties. Generation IV adds the Physical / Special / Status category to the already existing type, power, accuracy, PP and description information.

Selecting a move opens its detail view. The summary also supports move reordering.

### Condition

Sinnoh preserves the Contest condition system as a dedicated main tab. The Diamond summary message data explicitly contains `CONDITION` and `SHEEN` labels.

### Contest Moves

This is separate from Battle Moves and represents Super Contest move properties. It therefore must not be discarded when integrating later-generation summary-screen layouts.

The Diamond summary message archive explicitly contains a `CONTEST MOVES` heading and an `INFO` detail mode.

### Ribbons

D/P/Pt expose Ribbons directly in the summary and provide a Ribbon description view. This is a major preservation point when moving toward later-generation UI.

The Diamond summary message archive explicitly contains a `RIBBONS` heading and `INFO` detail state.

## D/P versus Platinum

Confirmed functional structure:

- Diamond/Pearl and Platinum use the same seven main summary categories listed above.
- Both belong to the Sinnoh summary-screen family.

Not yet promoted to confirmed:

- exact per-asset Platinum-vs-D/P summary graphics differences
- exact overlay/function-address correspondence between D/P and Platinum
- exact NARC/member-level delta list for summary graphics and touch regions

These must be obtained by direct binary/overlay/NARC comparison rather than assumed from visual similarity.

## HeartGold / SoulSilver — three paired dual-screen tabs

HGSS reorganize the much larger Sinnoh page set into three paired top-screen / bottom-screen groups:

1. Trainer Memo / Info
2. Skills / Battle Moves
3. Performance / Ribbons

This is a major architectural bridge toward Generation V: two logically related pages are presented simultaneously as one dual-screen state instead of making every information category a separate linear tab.

### Pair 1 — Trainer Memo / Info

Trainer Memo includes Nature and met/origin information. Info includes basic identity data such as Dex number, species/name, type, OT, ID, EXP and next-level EXP.

HGSS retain Generation IV met-date handling.

HGSS also add the game-specific Shiny Leaf display to the summary. Five Shiny Leaves can occupy five fixed positions and can be completed into a crown.

### Pair 2 — Skills / Battle Moves

Skills contains the six battle stats and Ability information. Battle Moves contains the move list and move detail interaction.

A notable HGSS change is that nature-increased/decreased stats receive visual emphasis from HGSS onward; D/P/Pt do not yet use this convention.

### Pair 3 — Performance / Ribbons

`Performance` is HGSS-specific and exposes Pokéathlon performance values:

- Speed
- Power
- Skill
- Stamina
- Jump

Each is represented by stars and belongs to the Pokéathlon subsystem, not normal battle stats.

The lower paired page is the Ribbon list and Ribbon-detail interface.

This pair is a strong example of the preservation rule: Generation V has no Pokéathlon Performance page, so a Gen V-style UI port must not erase it.

## HGSS implementation structure confirmed in pret/pokeheartgold

The current pokeheartgold decomp/disassembly exposes the Pokémon Summary application as an overlay-driven subsystem.

### Launch arguments

`PokemonSummaryArgs` currently includes fields/pointers for:

- Party
- Options
- party count
- current party slot
- move to learn
- National Dex enabled state
- SaveSpecialRibbons
- MenuInputState manager
- additional mode/flag fields

This confirms the summary application is not a passive renderer. It is invoked in multiple operational modes and can participate in move-learning/forgetting and ribbon-aware flows.

### Overlay state machine

`PokemonSummary_Main` uses a jump-table driver with 23 numbered states (0–22 in the current disassembly). Initialization creates a dedicated heap and summary overlay state block.

Current raw constants observed in `PokemonSummary_Init` include NARC IDs:

- `0x27` (39 decimal)
- `0xA2` (162 decimal)
- `0xB4` (180 decimal)

In the current filesystem enum these correspond to unnamed/partially named archives (`NARC_a_0_3_9`, `NARC_a_1_6_2`, `NARC_a_1_8_0`). Their exact summary-resource semantics should remain `unresolved` until member-level tracing is completed.

The summary message bank in the current HGSS project is `msg_0302`; it contains confirmed labels including:

- INFO
- TRAINER MEMO
- SKILLS
- BATTLE MOVES
- PERFORMANCE
- RIBBONS

## In-battle summary

Generation IV introduces a separate reduced summary presentation during battle.

D/P/Pt and HGSS both expose the in-battle family as:

- Summary
- Check Moves
- Check Moves description

This should be tracked separately from the field/party/PC summary because its information density and invocation constraints differ.

## Generation III → IV → V lineage

A useful structural lineage is:

Generation III:
`single-screen multi-page summary + detailed move/contest views`

Sinnoh Generation IV:
`seven information categories + touch navigation + met date + move category + dedicated in-battle summary`

HGSS:
`three paired dual-screen states + Pokéathlon Performance + Ribbon pairing + nature-stat emphasis`

Generation V:
`further consolidation of dual-screen summary + animated Pokémon + stronger touch interaction`

Therefore HGSS is not just another Generation IV skin. Its paired-page architecture is one of the clearest direct predecessors to BW's dual-screen summary design.

## Integration implications for Generation V → ポケットモンスター

Do not replace the earlier summary-screen families with BW wholesale.

Preserve and make coexist:

- Generation II original stats-page identity where required
- RSE Contest content
- FRLG-specific summary behavior
- D/P/Pt Condition and Super Contest move information
- D/P/Pt Ribbon list/detail behavior
- HGSS Pokéathlon Performance
- HGSS Shiny Leaf indicators
- Generation IV met-date handling
- Generation IV Physical/Special/Status move-category display
- Generation IV in-battle reduced summary
- Generation V animated/touch-oriented dual-screen behavior

A future unified summary ABI should therefore treat pages/panes as registered capabilities rather than a fixed hard-coded page count.

## Verification state

- D/P/Pt seven-category summary model: CONFIRMED from Nintendo manual / summary documentation and Diamond message archive.
- Diamond summary labels/message bank contents: CONFIRMED in `pret/pokediamond` `narc_0404.gmm`.
- Meeting date introduced in Generation IV summary: CONFIRMED.
- Physical/Special/Status move-category display introduced in Generation IV summary: CONFIRMED.
- Separate in-battle reduced summary from Generation IV onward: CONFIRMED.
- HGSS three paired top/bottom summary groups: CONFIRMED.
- HGSS Performance = five Pokéathlon stats: CONFIRMED.
- HGSS Shiny Leaf summary display: CONFIRMED.
- HGSS nature-stat visual emphasis: CONFIRMED as beginning with HGSS.
- HGSS `PokemonSummaryArgs` and overlay-driven application: CONFIRMED in `pret/pokeheartgold`.
- HGSS exact semantic names for raw NARC IDs 39/162/180: UNRESOLVED; member-level trace required.
- Platinum-vs-D/P exact summary overlay/NARC/asset delta: PARTIAL; functional family confirmed, exact binary delta pending.

## External technical references

- Nintendo Pokémon Diamond/Pearl manual — Summary controls and information categories
- Bulbapedia — Summary screen Generation IV gallery and cross-generation feature table
- pret/pokediamond — `files/msgdata/msg/narc_0404.gmm`
- pret/pokeheartgold — `include/unk_02088288.h`, `asm/unk_02088288.s`, `files/msgdata/msg/msg_0302.gmm`, filesystem NARC definitions
- StrategyWiki / Pokémon HGSS gameplay reference — three paired summary tabs
- Bulbapedia Shiny Leaf documentation
