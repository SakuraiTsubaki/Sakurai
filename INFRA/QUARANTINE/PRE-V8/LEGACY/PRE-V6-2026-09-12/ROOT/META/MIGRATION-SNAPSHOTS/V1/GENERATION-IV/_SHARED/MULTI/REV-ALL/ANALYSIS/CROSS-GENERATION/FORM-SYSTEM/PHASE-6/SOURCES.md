# Phase 6 source provenance

Primary implementation evidence was cross-checked against current pret
decompilation sources and the uploaded Generation IV ROM data used in previous
phases.

## Platinum
- Pokémon form constants:
  https://github.com/pret/pokeplatinum/blob/3a85029d78d42a809125076e1cf2752f15739adb/include/constants/forms.h
- Core form routines (Rotom, Giratina, Shaymin, Arceus):
  https://github.com/pret/pokeplatinum/blob/3a85029d78d42a809125076e1cf2752f15739adb/src/pokemon.c
- Burmy terrain update:
  https://github.com/pret/pokeplatinum/blob/3a85029d78d42a809125076e1cf2752f15739adb/src/battle/battle_system.c
- Distortion World Giratina form scripts:
  https://github.com/pret/pokeplatinum/blob/3a85029d78d42a809125076e1cf2752f15739adb/res/field/scripts/scripts_spear_pillar_distorted.s
  https://github.com/pret/pokeplatinum/blob/3a85029d78d42a809125076e1cf2752f15739adb/res/field/scripts/scripts_distortion_world_1f.s
- Shaymin PC storage reversion:
  https://github.com/pret/pokeplatinum/blob/3a85029d78d42a809125076e1cf2752f15739adb/src/pc_boxes.c

## HeartGold / SoulSilver
- Core Pokémon/form routines:
  https://github.com/pret/pokeheartgold/blob/0985e8718df4f25e64d6507d89c0c97c0d288981/src/pokemon.c
- HGSS Pichu form constants:
  https://github.com/pret/pokeheartgold/blob/0985e8718df4f25e64d6507d89c0c97c0d288981/include/constants/pokemon.h
- Spiky-eared Pichu event creation evidence:
  https://github.com/pret/pokeheartgold/blob/0985e8718df4f25e64d6507d89c0c97c0d288981/src/field/scrcmd_pokemon_misc.c

## ROM-side data
Personal-data/form records were extracted directly in Phase 5 from the uploaded
HeartGold/SoulSilver `a/0/0/2` NARC and are not replaced by wiki-derived values.
