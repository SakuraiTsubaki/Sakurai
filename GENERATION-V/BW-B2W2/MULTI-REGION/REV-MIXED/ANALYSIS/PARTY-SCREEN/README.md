# Generation V Pokémon Party Screen Audit — BW / B2W2

## Scope

This audit covers the Generation V party interface (Japanese in-game name: ポケモンリスト / Pokémon List) as an implementation reference for Generation V → ポケットモンスター.

Primary evidence used in this pass:

- Nintendo Pokémon Black Version instruction booklet
- Nintendo Pokémon Black Version 2 / White Version 2 instruction booklets
- Bulbapedia Party interface comparison
- representative Japanese BW / B2W2 in-game screenshots
- existing project BW/White ROM images as the intended binary baseline

The current runtime could not complete direct reads of the uploaded BW ROM images because local container access timed out. Therefore exact overlay/NARC/member IDs and ROM offsets are deliberately left UNRESOLVED in this pass.

ROM binaries are not stored in GitHub.

## Core BW field-party presentation

BW displays the six party slots on the Nintendo DS touch screen in a 2-column × 3-row grid. The first party slot is the upper-left panel and the second is the upper-right; Nintendo's manual explicitly identifies the upper-left party Pokémon as the one sent out first when a battle begins.

Representative Japanese screenshots confirm that each normal party panel visibly carries:

- Pokémon menu icon
- nickname/name
- gender when applicable
- level
- HP label/bar
- current HP / maximum HP

The party interface is touch-enabled but also remains operable with the D-pad and A/B controls.

## Party-selection command layer in BW

Nintendo's manual confirms that the Pokémon menu allows the player to:

- view information / Summary
- change party order
- give Pokémon held items
- select usable field moves from Pokémon that know them

A contemporary BW guide describes the selected-Pokémon command family as:

- Summary
- Switch
- Item
- Field Move

These should be modeled as capabilities rather than assumed to be one hard-coded menu for every context, because battle and special selection contexts expose different command sets.

## Party order semantics

The six visible positions are not cosmetic. Party order determines initial send-out order:

- Single Battle: first usable party Pokémon
- Double Battle: first two usable party Pokémon
- Triple / Rotation Battle: first three usable party Pokémon

Nintendo's BW manual explicitly states that the top-left party Pokémon is sent out first. Therefore the grid-to-party-index mapping must be preserved by any backward port even if the target engine renders the party in a different shape.

## Held-item handling

BW allows item give/take handling from the party interface through the selected Pokémon command flow.

B2W2 adds an important improvement: held items can be moved directly between party Pokémon. This is a Generation V sequel-specific capability and should not be back-attributed to BW.

Recommended capability split:

- PARTY_ITEM_GIVE
- PARTY_ITEM_TAKE
- PARTY_ITEM_MOVE_BETWEEN_MEMBERS (B2W2)

## Field moves

BW retains the classic field-move action from the party screen. Nintendo's manual explicitly states that if a Pokémon knows a move usable in the field, that move can be selected for use from the Pokémon menu.

This capability must remain distinct from the battle move list because legality and context depend on field state, map/event rules, badges/permissions where applicable, and the specific move effect.

Recommended capability:

- PARTY_FIELD_MOVE_ACTIONS

## Battle party screen is a distinct context

From Generation IV onward, the battle party interface is not simply the unchanged overworld party screen. Nintendo's BW manual confirms that choosing POKÉMON during battle displays the party and that selecting a replacement exposes SHIFT.

Battle context therefore needs separate command gating:

- view battle-relevant party data
- view Summary
- switch/SHIFT when legal
- reject Eggs / fainted Pokémon / active-slot-invalid selections as appropriate
- enforce battle-format positioning constraints

This matters especially for BW because Triple Battles and Rotation Battles make party index, active position, and selectable replacement semantics more complex than a simple one-active-mon model.

Recommended capability split:

- PARTY_CONTEXT_FIELD
- PARTY_CONTEXT_BATTLE
- PARTY_BATTLE_SHIFT
- PARTY_BATTLE_POSITION_AWARENESS

## Touch interaction

BW continues DS touch interaction for the party interface. D-pad and button navigation remain available, so touch must be treated as an input adapter, not as a required semantic dependency.

For backward ports to GBC/GBA targets, preserve every party action and remap touch-only affordances to buttons/cursor commands rather than deleting the feature.

## BW -> B2W2 changes confirmed in this pass

B2W2 preserves the Generation V party-grid family while adding at least two relevant interface capabilities:

1. the party screen can be registered to the Ready Button menu / registered-menu system;
2. held items can be moved directly between party Pokémon.

The second change is especially important for the unified party ABI because it is a genuine workflow feature, not merely a different graphic.

## Egg / invalid-object presentation

Party rendering is conditional on Pokémon object state. Eggs do not expose the normal full set of level/HP/gender information. Generation V also has distinct Bad Egg behavior documented separately; exact error-object behavior should remain a compatibility/debug path and must not be conflated with ordinary Egg UI.

Recommended capability:

- PARTY_EGG_PRESENTATION
- PARTY_INVALID_OBJECT_PRESENTATION

## Proposed unified Party ABI

Do not hard-code the BW grid itself as the semantics of the system. Separate party data/order from presentation and context.

Suggested structure:

```text
PartyContext
├── source Party[0..5]
├── selectedSlot
├── activeBattleSlots
├── battleFormat
├── mode (field / battle / trade / facility / script selection)
├── capabilityBits
└── returnAction

PartyMemberView
├── species/form/icon
├── nickname
├── gender
├── level
├── hp/maxHp/hpState
├── majorStatus
├── heldItem/mail
├── egg/invalid flags
└── context markers

PartyActionRegistry
├── SUMMARY
├── SWITCH_ORDER
├── ITEM_GIVE
├── ITEM_TAKE
├── ITEM_MOVE_BETWEEN_MEMBERS
├── FIELD_MOVE
├── BATTLE_SHIFT
└── GAME_SPECIFIC
```

Render adapters can then preserve each target game's original party layout while exposing Generation V capabilities through expansion.

## Preservation implications for Generation V → ポケットモンスター

- Do not replace original RBY/GSC/RSE/FRLG/DPPt/HGSS party layouts wholesale merely to imitate BW.
- Preserve original slot order and version-specific icon behavior.
- Add BW/B2W2 commands and metadata through context-aware action registration.
- Preserve B2W2 direct held-item movement as an optional expanded capability.
- Preserve Triple/Rotation positional semantics separately from the six-slot storage order.
- Treat touch as one input adapter; provide button equivalents on targets without touch hardware.
- Keep field-party and battle-party contexts separate.

## Verification state

### CONFIRMED

- BW six-member party is displayed as a 2-column × 3-row DS grid in representative Japanese screenshots.
- top-left party slot is first in battle order: Nintendo BW manual.
- BW Pokémon menu supports viewing Pokémon information, changing order, held-item handling, and field-move use: Nintendo BW manual.
- BW selected-member workflow includes Summary / Switch / Item / Field Move: contemporary guide documentation.
- BW party interface retains touch interaction and button/D-pad navigation.
- battle Pokémon menu allows Summary/switch workflow and exposes SHIFT for a legal replacement: Nintendo BW manual.
- B2W2 allows held items to be moved directly between party members: cross-game interface documentation.
- B2W2 allows the party screen to participate in the registered-menu / Ready Button system: cross-game interface documentation.

### UNRESOLVED / PENDING DIRECT ROM TRACE

- exact BW/B2W2 party-menu overlay number(s)
- exact NARC archives and member IDs for panel graphics, cursor, touch hitboxes, icons, palettes, and strings
- exact state-machine function boundaries
- exact BW-vs-White binary equality/differences for party UI assets
- exact Black-vs-White and B2-vs-W2 version-specific graphical deltas
- language/region/revision-specific asset and string differences

No guessed ROM offsets or archive IDs are recorded as facts.
