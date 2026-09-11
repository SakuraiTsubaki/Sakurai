# Diamond / Pearl 64×64 battle sprite publication — COMPLETE

## Final status

Completed and published to `SakuraiTsubaki/Tsubaki`.

- Final Tsubaki asset commit: `4319af69a48b0e8cf3fcaf891b96fab9585ffb35`
- Final GitHub Actions run: `34596285567`
- Run conclusion: `success`
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
- Deoxys, Unown, Castform, Burmy, Wormadam, Shellos, Gastrodon, Cherrim, Arceus and Egg mappings are rendered from the DP otherpoke member formulas.
- The upstream `pret/pokediamond` tree commits these alternate-form character assets as actual `.NCGR` files, so the final publisher decodes those NCGR members directly rather than expecting PNG derivatives.

## Problems found and corrected

### Palette source

The first publisher attempted to read generated `narc_0010.NCLR` files from `pret/pokediamond`. Those generated base-archive NCLR files are gitignored upstream; the original JASC-PAL `.pal` sources are committed instead.

The final publisher therefore:

1. reads an existing `.NCLR` when it is committed;
2. otherwise reads its original `JASC-PAL` `.pal` source;
3. preserves palette index 0 as transparent;
4. applies preservation-v2 indexed-pixel reduction without interpolated colors.

Bulbasaur normal/shiny palette sources were independently decoded from the uploaded Diamond ROM and match the corresponding JASC-PAL RGB values.

### Alternate forms

The first successful base-species publication produced blank form galleries because it looked for `otherpoke/narc_xxxx.png`. DP `otherpoke` actually commits the relevant character members as `narc_xxxx.NCGR`.

The final publisher now decrypts/decodes those NCGR members directly and applies their NCLR palettes. A zero-form-record guard intentionally fails the workflow if alternate forms are ever skipped again.

Final verification:

- alternate-form PNG records: `536`
- `forms/` contains actual per-form directories
- `FORMS_front_normal_f0.png`: non-empty visual gallery (~417 KB)
- `FORMS_back_normal_f0.png`: non-empty visual gallery (~417 KB)

## Published asset path

`GENERATION-IV/DIAMOND-PEARL/USA/REV-UNKNOWN/SPRITES/BATTLE_MASTER_V1/PREVIEWS/`

Contains:

- individual 64×64 Pokémon PNGs under `base/`
- alternate-form PNGs under `forms/`
- complete and paged visual sheets under `GALLERIES/`
- `manifest.csv`
- `summary.json`
- `README.md`

## Completion boundary

DP is complete for the current **Pokémon battle-sprite 64×64 conversion/publication track**. Icons, overworld sprites, trainers, NPCs, objects, UI, tiles, battle effects and other graphic categories remain independent project tracks and are not marked complete by this document.
