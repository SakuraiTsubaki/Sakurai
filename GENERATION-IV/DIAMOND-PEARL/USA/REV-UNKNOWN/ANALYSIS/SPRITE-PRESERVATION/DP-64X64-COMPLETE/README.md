# Diamond / Pearl 64×64 battle sprite publication — COMPLETE

## Status

Completed and published to `SakuraiTsubaki/Tsubaki`.

- Tsubaki asset commit: `f0a642ef09dc71c7bc4f14fceece3ea4c5c3b517`
- GitHub Actions run: `34595931316`
- Run conclusion: `success`
- Base National Dex species processed: `493`
- Logical PNG records published: `7,232`
- Conversion: preservation-v2 `80×80 -> 64×64`
- AI / generative image use: **none**
- Anti-aliasing / interpolated colors: **none**

## Source structure

Uploaded ROM reference:

- `Pokemon_Diamond_USA_NDS-LGC.nds`
- `Pokemon_Pearl_USA_NDS-LGC.nds`

Active DP battle Pokémon graphics archive:

- `poketool/pokegra/pokegra.narc`
- base mapping: `species_id * 6`
  - `+0` female back
  - `+1` male/shared back
  - `+2` female front
  - `+3` male/shared front
  - `+4` normal palette
  - `+5` shiny palette

Alternate-form archive:

- `poketool/pokegra/otherpoke.narc`
- Deoxys, Unown, Castform, Burmy, Wormadam, Shellos, Gastrodon, Cherrim, Arceus, and Egg form mappings are preserved using the DP member formulas used by the batch publisher.

## Failure found and corrected

The first GitHub Actions attempt failed because it tried to read generated files such as `narc_0010.NCLR` directly from `pret/pokediamond`.

In the upstream source tree those generated NCLR files are intentionally ignored. Their original JASC-PAL source files, e.g. `narc_0010.pal` and `narc_0011.pal`, are committed instead.

The publisher was corrected to:

1. read an existing `.NCLR` when it is actually committed;
2. otherwise read the original `JASC-PAL` `.pal` source directly;
3. preserve palette index 0 as transparent in the rendered Pokémon sprite;
4. apply the same preservation-v2 indexed-pixel reduction used by the Gen IV sprite preservation work.

## ROM cross-check

Bulbasaur palette members were independently checked against the uploaded Diamond ROM.

- normal palette member 10: JASC-PAL source == ROM NCLR decoded RGB values
- shiny palette member 11: JASC-PAL source == ROM NCLR decoded RGB values

This verifies the upstream palette-source interpretation used to fix the publisher.

## Published asset path

`GENERATION-IV/DIAMOND-PEARL/USA/REV-UNKNOWN/SPRITES/BATTLE_MASTER_V1/PREVIEWS/`

Contains:

- individual 64×64 Pokémon PNGs under `base/`
- alternate-form PNGs under `forms/`
- complete and paged visual sheets under `GALLERIES/`
- `manifest.csv`
- `summary.json`
- `README.md`

## Completion rule

DP is considered complete for the current **Pokémon battle-sprite 64×64 conversion/publication track**. Other graphic categories such as icons, overworld sprites, trainers, NPCs, objects, UI, tiles and effects remain separate project categories and are not represented as completed by this record.
