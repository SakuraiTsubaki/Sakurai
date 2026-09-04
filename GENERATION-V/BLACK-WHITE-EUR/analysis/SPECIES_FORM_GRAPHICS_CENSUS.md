# Pokémon Black / White EUR — Species/Form Graphics Census

No ROM bytes were modified. Current project Black/White ROMs were compared directly.

## Shared identity
- `/a/0/0/4` battle sprites — SHA-1 `e7b361a7208464d58462378912601b5c25967827`
- `/a/0/0/7` menu icons — SHA-1 `41a5727a111742fe775944b3c0cdb5a41109385a`
- `/a/1/6/7` footprints — SHA-1 `1915614b4900b3a1e2a827c5546e78d4991a44fc`
All three are byte-identical Black/White.

## Battle sprites `/a/0/0/4`
- 14,285 members; groups `0..711` are 712 complete 20-file groups.
- `0..649` map to species IDs `0..649`; `650..651` are special post-species slots; `652..711` are exactly 60 alternate-form groups.
- Non-Arceus alternate routing: `sprite_group = 652 + FormSprite + (form - 1)`.
- Unown `652..678`, Castform `679..681`, Deoxys `682..684`, Genesect `708..711`.
- Arceus has no separate full-sprite group and uses 32 tail palettes (16 forms × normal/shiny) at `14253..14284`.
- `14240..14252` remain a probable special shared battle object pending code-consumer identification.

## Menu icons `/a/0/0/7`
- 1,431 members; common `0..6`, then exactly `712 × 2` group slots.
- Primary: `7 + 2×group`; secondary/female: `8 + 2×group`.
- All 712 primary slots populated; only secondary groups `521`, `592`, `593` populated (Unfezant, Frillish, Jellicent).

## Footprints `/a/1/6/7`
- 655 members; common `0..4`; members `5..654` are exactly 650 LZ10 graphics.
- `footprint_member = 5 + species_id` for species `0..649`.
- No alternate-form footprint tail.

## Expansion consequence
Battle sprites/icons share a 712-group identity space, while footprints use a fixed 650-species range. Post-649 special slots and alternate base 652 must be preserved or deliberately relocated during species expansion.