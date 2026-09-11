# Generation IV form rules → Gen II / Gen III — Phase 6

This phase implements the **behavioral rules** that sit on top of the persisted
5-bit form field established in Phases 4–5.

## Important version differences preserved

- Diamond/Pearl do not have Rotom appliance forms, Giratina Origin Forme, or
  Shaymin Sky Forme.
- Platinum introduces those systems.
- HGSS retains the appliance/Sky/Origin systems but has no Distortion World,
  so Giratina Origin is driven by the Griseous Orb rather than map context.
- HGSS additionally has Spiky-eared Pichu (`form = 1`).

## Exact rules captured

### Rotom
Form -> move:
0 none, 1 Overheat, 2 Hydro Pump, 3 Blizzard, 4 Air Slash, 5 Leaf Storm.

The Platinum/HGSS replacement algorithm is reproduced: an existing appliance
move is replaced; returning to base deletes it; an empty moveset receives
ThunderShock; if a new appliance move cannot fit, a caller-selected slot is
overwritten.

### Giratina
Outside Platinum's Distortion World:
Griseous Orb -> Origin; otherwise Altered.
Platinum field scripts explicitly force Origin on entering the Distortion World
and force Altered when leaving; the target engine therefore needs both an item
rule and a map-context hook.

### Shaymin
Gracidea can change Land -> Sky only when:
- species is Shaymin
- current form is Land
- HP > 0
- fateful encounter flag is set
- not frozen
- local time is from 04:00 through 19:59

Platinum also forces Land form when stored in PC boxes, daycare, and relevant
trade/GTS paths, and has time-transition reversion logic.

### Arceus
Gen IV stores a 5-bit form and synchronizes it from the held item's hold effect
when the ability is Multitype.

The form id follows the Gen IV type id. Therefore form id 9 is the
TYPE_MYSTERY/??? slot. It has no normal Plate access and is retained as an
unused/inaccessible original slot rather than being deleted.

### Burmy
Platinum's exact terrain groups are preserved in
`burmy_battle_terrain_map_platinum.csv`.

### Spiky-eared Pichu
HGSS has Pichu form 1. The HGSS evolution code explicitly blocks that form from
evolving, and the battle-facility ban logic also treats it specially.

## Safety / dependencies

The generated Gen III C file is an integration layer, not a claim that the
retail ROM is already fully playable with all forms.

Before binary activation:
- canonical species-ID reorder must be live,
- Gen IV move IDs/effects must be expanded,
- Gen IV items/hold effects must be translated,
- every direct form-sensitive personal-data lookup must use the Phase-5 accessor,
- save/link compatibility must be regression-tested.

Gen II additionally needs its 9-bit move-ID migration before Rotom's Gen IV
moves above 255 can be stored.

Sprites remain intentionally out of scope.
