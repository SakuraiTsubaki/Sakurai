# Generation IV battle sprite master v1

## Scope

This pass covers the current **Pokémon battle-sprite** category for Generation IV across Diamond/Pearl, Platinum, and HeartGold/SoulSilver.

- species slots 0–493 from each active main battle-sprite archive
- front / back
- logical male / female slots, including shared-slot aliases
- animation frames 0 / 1
- normal / shiny palettes
- all alternate forms addressed by the original game sprite-loading code
- every `otherpoke` member inventoried, including unreferenced/leftover candidates

## Result

- logical rendered records: **25,136**
- unique 64×64 RGBA assets after global SHA-256 deduplication: **11,947**
- atlas pages: **24** (32×16 cells, 64×64 per cell)
- `otherpoke` members inventoried: **727**

## Conversion rule

Source battle graphics were decoded from the project ROMs as 80×80 frames and converted to 64×64 using preservation-v2.

- no generative-image tools
- no antialiasing
- no interpolated/new colors
- output selects source palette indices only
- mild rare-color preservation
- identical rendered results are merged by SHA-256 rather than duplicated

## Source archive set

The exact archive paths, member counts, byte sizes and SHA-256 values are in `archive_hashes.csv`.

Diamond and Pearl are tracked as separate game identities even where their active sprite archives are byte-identical. HeartGold and SoulSilver are handled the same way. Platinum remains a separate source set.

## Repository split

Analysis, manifests, source-code mappings, validation records and rebuild scripts belong in **Sakurai**. Rendered/insertable sprite assets belong in **Tsubaki**.

The complete locally verified package is `gen4_battle_sprite_master_v1.zip` with SHA-256 `53f44689a6b11eb789b40285a6be1f2687ce00ce7831219c9bdf874c42325252`.
