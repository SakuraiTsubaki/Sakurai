# Diamond / Pearl 64×64 battle sprite publication — COMPLETE

## Final status

Completed and republished to `SakuraiTsubaki/Tsubaki` after correcting the DP alternate-form NCGR decryption bug.

- Corrected Tsubaki asset commit: `c447f90466ea3e7f0e38347f02aab21d60425e27`
- Base National Dex species processed: `493`
- Logical PNG records published: `7,768`
- Alternate-form PNG records: `536`
- Conversion: preservation-v2 `80×80 -> 64×64`
- AI / generative image use: **none**
- Anti-aliasing / interpolated colors: **none**

## Source structure

Uploaded ROM references:

- `Pokemon_Diamond_USA_NDS-LGC.nds`
- `Pokemon_Pearl_USA_NDS-LGC.nds`

Active base battle graphics:

- `poketool/pokegra/pokegra.narc`
- base mapping: `species_id * 6`
  - `+0` female back
  - `+1` male/shared back
  - `+2` female front
  - `+3` male/shared front
  - `+4` normal palette
  - `+5` shiny palette

Alternate-form graphics:

- `poketool/pokegra/otherpoke.narc`
- Deoxys, Unown, Castform, Burmy, Wormadam, Shellos, Gastrodon, Cherrim, Arceus and Egg mappings are rendered from the DP otherpoke member formulas.

## Root cause of the broken DP forms

The first NCGR-capable form publisher used the wrong Pokémon-character decryption direction. It seeded from the first u16 and walked forward. That produces apparently valid 4bpp indices but visually becomes random/noisy garbage.

The game code in `pret/pokediamond` (`sub_02008A74`) shows the actual algorithm:

1. read the **last** u16 of the 0x1900-byte Pokémon character payload as the initial state;
2. iterate over all u16 words **from the last word backward to the first**;
3. XOR each word with the low 16 bits of the current state;
4. advance the 32-bit state with `state = state * 0x41C64E6D + 0x6073`;
5. interpret the decrypted payload linearly as a `160×80` indexed image containing two `80×80` animation frames.

Applying that routine to the uploaded Diamond ROM immediately restores recognizable form sprites. The corrected workflow now uses this reverse LCRNG-XOR routine and replaces every previously broken form PNG.

## Verification after correction

- corrected alternate-form PNG records: `536`
- form output sanity guard rejects near-full-canvas random-noise renders
- `FORMS_front_normal_f0.png`: corrected gallery (~77 KB)
- `FORMS_back_normal_f0.png`: corrected gallery (~76 KB)
- `summary.json` records `broken_form_assets_replaced: true`
- individual corrected form directories are present under `forms/`

## Published asset path

`GENERATION-IV/DIAMOND-PEARL/USA/REV-UNKNOWN/SPRITES/BATTLE_MASTER_V1/PREVIEWS/`

Contains individual 64×64 base Pokémon PNGs, corrected alternate-form PNGs, visual galleries, `manifest.csv`, `summary.json`, and README documentation.

## Completion boundary

DP is complete for the current **Pokémon battle-sprite 64×64 conversion/publication track**. Icons, overworld sprites, trainers, NPCs, objects, UI, tiles, battle effects and other graphic categories remain independent project tracks.
