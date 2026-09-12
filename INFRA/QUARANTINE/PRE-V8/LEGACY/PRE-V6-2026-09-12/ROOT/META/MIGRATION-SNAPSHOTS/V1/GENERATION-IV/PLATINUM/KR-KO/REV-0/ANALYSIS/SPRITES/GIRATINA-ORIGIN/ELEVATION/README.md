# Giratina Origin Forme -> Gen III elevation candidate

## Verified target-engine facts
- Emerald uses `gEnemyMonElevation` to lift opponent-side Pokémon that fly/float.
- Native Rayquaza: front size `64x64`, `y_offset = 0`, enemy elevation `6`.
- Stock Emerald does not apply this enemy elevation table to the player-side backsprite.

## Project candidate
- Origin Forme front: `64x64`, `y_offset = 0`, enemy elevation `6`.
- Origin Forme back: `64x56`, `y_offset = 0`, no new player-side elevation logic.

## Why 6
Origin Forme's converted front geometry is in the same target-engine composition class as Rayquaza (`64x64 / y_offset 0`). Using Rayquaza's native 6-pixel lift is therefore a target-engine reference mapping, not an arbitrary freehand value.

## Platinum note
`height_o` entries corresponding to the Origin Forme pair were extracted as `0 / 0` (entries 154 and 155). Those are Platinum sprite y-offset data and are not treated as Gen III elevation.

No generative image tools were used.
