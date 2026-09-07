# GEN2 Kanto Start — GOLD KR Phase 06
## Pallet Town / 태초마을 RGBY+GOLD full survey baseline

Status: SURVEY / NO ROM PATCH IN THIS PHASE
Base implementation ROM: `Pocket Monsters Geum (Korea).gbc`

## Scope
Phase 06 treats **Pallet Town as a complete map cluster**, not only the exterior field:

1. Pallet Town exterior
2. Red's House 1F
3. Red's House 2F
4. Blue/Green's House
5. Professor Oak's Lab

All RGBY and GOLD/GSC content is preserved as integration input. Phase 04's direct north-exit warp is now classified as a temporary bootstrap and must be superseded by the full RGB+Yellow Oak encounter flow rather than treated as final content.

## Uploaded ROMs verified

| Variant | Size | SHA-1 |
|---|---:|---|
| Pocket Monsters Aka JP Rev A | 524288 | ef74c79cded14204ac79e77f4964d9cb25003120 |
| Pocket Monsters Midori JP Rev A | 524288 | 4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b |
| Pocket Monsters Ao JP | 524288 | 0da501e3e5c51ab8fef55b092dcdd7e6b050e424 |
| Pocket Monsters Pikachu JP Rev D | 1048576 | a40298a8123613ee60cd7aab204d788b8425976e |
| Pokemon Red INT | 1048576 | ea9bcae617fdf159b045185467ae58b2e4a48b9a |
| Pokemon Blue INT | 1048576 | d7037c83e1ae5b39bde3c30787637ba1d4c48ce2 |
| Pokemon Yellow INT | 1048576 | cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1 |
| Pocket Monsters Geum KR | 2097152 | c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65 |

## 1. Pallet Town exterior — direct ROM confirmation

### Dimensions
- RGB: 10 x 9 blocks
- Yellow: 10 x 9 blocks
- GOLD: 10 x 9 blocks

No dimension reduction exists here. Integration pressure is primarily tileset/metatile, NPC and event content.

### RGBY block data
All seven uploaded Gen I ROMs contain the exact same 90-byte Pallet Town block sequence at ROM offset `0x0182FD`.

- length: 90 bytes
- SHA-1 of block sequence: `f84b8475280e576bcf2309b7c3b41cd853dec349`

This directly verifies that the Pallet exterior block layout is identical across the uploaded Japanese Red/Green/Blue/Pikachu and international Red/Blue/Yellow ROMs. Yellow's major Pallet differences are therefore event/script/object behavior, not the 10x9 block grid.

### GOLD KR block data
GOLD KR Pallet map attributes resolve the map blocks to ROM offset `0x0A9497` (bank `0x2A`, address `0x5497`).

- length: 90 bytes
- SHA-1: `f3ab2cc98af2bfa47e36850f5a74439bd68c8766`

Raw block-byte differences versus RGBY occur at 9 positions:

| block index | block x | block y | RGBY | GOLD |
|---:|---:|---:|---:|---:|
| 3 | 3 | 0 | 0x52 | 0x4F |
| 4 | 4 | 0 | 0x4F | 0x0B |
| 5 | 5 | 0 | 0x0B | 0x50 |
| 6 | 6 | 0 | 0x50 | 0x52 |
| 45 | 5 | 4 | 0x0C | 0x20 |
| 46 | 6 | 4 | 0x0D | 0x54 |
| 47 | 7 | 4 | 0x0E | 0x21 |
| 55 | 5 | 5 | 0x10 | 0x37 |
| 57 | 7 | 5 | 0x00 | 0x7E |

**Important:** these numbers are not yet safe to interpret visually because Gen I `OVERWORLD` and Gen II `KANTO` metatile tables differ. The next technical gate is a metatile/graphics/collision mapping before any Pallet block replacement.

## 2. Pallet exterior event/object inventory

### RGB common content
- Oak appears when the player approaches the north exit before following him into the lab.
- Oak stops the player, walks to the player, warns that going out is unsafe, and leads the player to the lab.
- Exterior NPCs:
  - Oak (event object)
  - girl at `(3,8)`
  - fisher at `(11,14)`
- Warps:
  - `(5,5)` -> Red's House 1F
  - `(13,5)` -> Blue's House
  - `(12,11)` -> Oak's Lab
- Four exterior signs: town, player house, rival house, lab.

### Yellow additions/changes
- Uses the same 10x9 Pallet block grid as RGB.
- Oak north-exit encounter is expanded.
- Detects which side of the north exit the player used.
- Adds the **Lv.5 wild Pikachu encounter** before Oak leads the player to the lab.
- Adds extra Oak dialogue/state around the Pikachu incident.
- Oak's initial object position differs from RGB because of the expanded encounter choreography.

### GOLD additions/changes
- Keeps the same three building warp locations and four sign locations.
- Adds `MAPCALLBACK_NEWMAP` Pallet Fly-point registration.
- Exterior NPCs change to:
  - teacher at `(3,8)`
  - fisher at `(12,14)`
- No normal GSC exterior Oak-start event exists.
- GOLD fisher dialogue is a Gen II time-capsule/computer-communication reference, distinct from the RGBY fisher content.

### Integration requirement
Final Pallet exterior must preserve:
- GOLD Fly-point callback.
- RGB Oak interception + escort structure.
- Yellow's unique Lv.5 Pikachu incident and its Oak dialogue/choreography.
- RGBY girl content.
- GOLD teacher content.
- RGBY fisher content.
- GOLD fisher content.
- all four sign interactions and both generations' unique text variants.
- all three building warps.

The temporary Phase 04 direct warp must therefore be replaced, not treated as final behavior.

## 3. Red's House 1F

Dimensions are 4 x 4 in both generations.

### RGBY
- Mom object.
- Before starter: wake-up/early-game Mom branch.
- After starter: Mom heals the party, including fade/music/heal flow.
- TV interaction has facing-direction logic and a movie reference.
- Warps: two exits + stairs to 2F.

Yellow preserves the same user-visible Mom/heal and TV logic, moved through a far-call implementation.

### GOLD
- Red's Mom remains, but is repurposed to post-Gen-I dialogue about Red being away.
- First-meeting event flag and repeat dialogue.
- TV text is different.
- Adds two picture-bookshelf interactions.
- Mom position changes from RGBY `(5,4)` to GOLD `(5,3)`.
- Stair warp y-position differs from RGBY (`y=1` vs GOLD `y=0`).

### Integration requirement
Preserve both:
- early-game Mom wake/heal function from RGBY,
- later Red-away dialogue from GOLD,
- RGBY TV behavior/text,
- GOLD TV text,
- GOLD bookshelf interactions.

These should be staged by project progression flags, not by deleting one generation's Mom behavior.

## 4. Red's House 2F

Dimensions are 4 x 4 in both generations.

### RGBY
- Initial bedroom map state/script exists.
- No normal map objects.
- Stair warp at `(7,1)`.
- Some room interactions are handled by Gen I engine/tile behavior rather than explicit Gen II-style BG event entries.

### GOLD
- Stair warp becomes `(7,0)`.
- Adds explicit N64 interaction at `(3,5)`.
- Adds explicit PC interaction at `(0,1)`.
- PC text reflects Red's long absence.

### Integration requirement
Retain the RGBY starting-room behavior and Gen I room interaction semantics while retaining GOLD's N64/PC interactions and later-state text. Tile-level interactions must be audited before implementation because Gen I does not express all room interactions as map BG-event records.

## 5. Blue/Green's House

Dimensions are 4 x 4 in both generations.

### RGBY / Yellow
- Daisy has sitting and walking states.
- Entering the house sets a dedicated entered-house state.
- Daisy can give the Town Map after the Pokédex condition.
- Bag-full branch exists.
- Town Map object can disappear after pickup.
- Objects include sitting Daisy, walking Daisy, and Town Map.

Yellow keeps the same player-facing content here with small implementation differences.

### GOLD
- Daisy remains as a single map object.
- Adds 3 PM tea / Pokémon grooming event.
- Has daily grooming state and refusal/egg/already-groomed branches.
- Outside 3 PM she gives her later-era Viridian Gym/Blue dialogue.
- The map uses shared `House1.blk`; its 16-byte grid differs from the Gen I Blue's House grid at two block positions.

### Integration requirement
Preserve:
- RGBY Town Map acquisition and all branches.
- sitting/walking Daisy state content.
- GOLD Daisy later dialogue.
- GOLD grooming interaction.
- Project time/day rule: grooming must be accessible regardless of actual clock time while the 3 PM presentation variant remains available as flavor.

## 6. Professor Oak's Lab

Dimensions are 5 x 6 in both generations, but event content differs dramatically.

### RGB
Objects include:
- rival,
- Charmander / Squirtle / Bulbasaur balls,
- Oak in two choreography positions,
- two Pokédex objects,
- girl,
- two scientists.

Major event chain includes:
- Oak and player lab entrance choreography,
- rival waiting dialogue,
- choose-a-Pokémon speech,
- player starter choice,
- rival chooses counter-starter,
- first rival battle,
- rival exit,
- later Oak request / Pokédex distribution flow,
- Poké Ball distribution progression and post-event text states.

### Yellow
Keeps the broad Oak/rival/Pokédex structure but makes major unique changes:
- Eevee ball instead of RGB three-ball setup for rival selection.
- player receives Pikachu through Oak's event flow.
- rival pushes player away and takes Eevee.
- Pikachu leaves its Poké Ball / dislikes Poké Balls sequence.
- Yellow-specific rival evolution state is seeded by early battle results.

### GOLD
Objects include:
- Oak,
- three scientists/assistants.

Major later-era Oak functionality includes:
- Kanto arrival dialogue,
- badge-state advice,
- Pokédex check,
- Mt. Silver unlock after all badges.

### Current project bootstrap already present
Earlier project phases added three RGB-style starter balls and an early Oak wrapper to GOLD KR. Those are bootstrap implementations, not the complete RGBY integration described above.

### Integration requirement
Final lab must contain and expose:
- RGB Bulbasaur/Charmander/Squirtle selection content,
- RGB rival counter-selection and first rival battle,
- RGB Pokédex and later Oak request chain,
- Yellow Pikachu/Eevee-specific event chain,
- Yellow Pikachu out-of-ball behavior event content where technically appropriate,
- GOLD Oak later-era badge/Pokédex/Mt. Silver content,
- GOLD three assistants and their interactions,
- all unique RGBY lab NPC interactions.

No existing GOLD later-era Oak branch is to be overwritten by the early-game chain; progression flags must route between preserved eras/states.

## 7. Tileset / metatile gate before map modification

Pallet Town uses Gen I `OVERWORLD` and Gen II `KANTO` map graphics systems. The metatile binary formats and collision systems differ.

Known source structures:
- Gen I Overworld blockset: `gfx/blocksets/overworld.bst`
- Gen I Overworld tileset header: GFX + blockset + collision tile list
- Gen II Kanto metatiles: `data/tilesets/kanto_metatiles.bin`
- Gen II Kanto collision: `data/tilesets/kanto_collision.asm`

Before changing any of the 9 Pallet field block bytes or internal map block grids:
1. decode the Gen I block IDs used by the five Pallet maps,
2. decode corresponding Gen I 4x4 tile composition,
3. decode Gen II Kanto/House/Lab metatiles and collision quadrants,
4. identify direct visual/collision equivalents,
5. allocate new Gen II metatiles for RGBY structures with no faithful equivalent,
6. only then modify the GOLD map block grids.

## 8. Phase 06 conclusions

1. Pallet Town is not a Route 1 prelude; it is itself a full RGBY+GSC integration target.
2. Exterior map dimensions happen to match, but content does not.
3. All uploaded RGBY ROMs use the same Pallet exterior block grid; Yellow's large differences are event-layer differences.
4. GOLD introduced distinct Pallet NPC/state content and must not replace RGBY content.
5. The four Pallet interiors must be integrated together with the exterior.
6. The existing direct north-exit warp is a temporary bootstrap and will be superseded by a complete Oak/Pikachu/escort sequence.
7. No map-block replacement should occur before the tileset/metatile correspondence is complete.

## Public disassembly references used for semantic cross-check
- https://github.com/pret/pokered/blob/master/scripts/PalletTown.asm
- https://github.com/pret/pokered/blob/master/data/maps/objects/PalletTown.asm
- https://github.com/pret/pokeyellow/blob/master/scripts/PalletTown.asm
- https://github.com/pret/pokeyellow/blob/master/data/maps/objects/PalletTown.asm
- https://github.com/Narishma-gb/pokegold-kr/blob/master/maps/PalletTown.asm
- https://github.com/pret/pokered/blob/master/scripts/RedsHouse1F.asm
- https://github.com/pret/pokeyellow/blob/master/scripts/RedsHouse1F_2.asm
- https://github.com/Narishma-gb/pokegold-kr/blob/master/maps/RedsHouse1F.asm
- https://github.com/pret/pokered/blob/master/scripts/RedsHouse2F.asm
- https://github.com/Narishma-gb/pokegold-kr/blob/master/maps/RedsHouse2F.asm
- https://github.com/pret/pokered/blob/master/scripts/BluesHouse.asm
- https://github.com/pret/pokeyellow/blob/master/scripts/BluesHouse.asm
- https://github.com/Narishma-gb/pokegold-kr/blob/master/maps/BluesHouse.asm
- https://github.com/pret/pokered/blob/master/scripts/OaksLab.asm
- https://github.com/pret/pokeyellow/blob/master/scripts/OaksLab.asm
- https://github.com/Narishma-gb/pokegold-kr/blob/master/maps/OaksLab.asm
