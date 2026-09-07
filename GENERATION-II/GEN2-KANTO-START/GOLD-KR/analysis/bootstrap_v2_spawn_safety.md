# GOLD KR bootstrap v2 — spawn safety audit

## Base ROM
- File: `Pocket Monsters Geum (Korea).gbc`
- SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`

## Confirmed New Game spawn write
The Korean Gold ROM New Game routine contains the initial default spawn selection at ROM offset `0x005C5C`.

Original byte:
- `00` = `SPAWN_HOME`

Bootstrap edit:
- `02` = `SPAWN_PALLET`

## Confirmed SpawnPoints table
The SpawnPoints table is located at ROM offset `0x015319` in this ROM.

Original first entry (`SPAWN_HOME`):
- bytes: `18 07 03 03`
- map: `PLAYERS_HOUSE_2F`
- coordinates: `(3,3)`
- this is the Johto home spawn and is unsafe as a generic fallback for a Kanto-start new game.

Existing `SPAWN_PALLET` entry:
- bytes: `0D 02 05 06`
- map: `PALLET_TOWN`
- coordinates: `(5,6)`

Bootstrap v2 changes `SPAWN_HOME` to the same Pallet Town target. This prevents generic HOME fallback logic (including whiteout fallback when no valid last spawn exists) from returning the player to Johto.

## Whiteout behavior
`GetWhiteoutSpawn` checks `wLastSpawnMapGroup` / `wLastSpawnMapNumber`; if the last map is not a valid spawn point, it falls back to `SPAWN_HOME`. Therefore changing only the New Game selector is insufficient for a Kanto-start bootstrap.

## v2 edits
1. `0x005C5C: 00 -> 02` — New Game uses `SPAWN_PALLET`.
2. `0x015319: 18 07 03 03 -> 0D 02 05 06` — HOME fallback points to Pallet Town.

## Patched image verification
- SHA-1: `ab52d75c1dba4ac8f2f9d08f15cdd95980b5fcbd`
- SHA-256: `75721876fe0840306e6956dd620eacfcbe5105bb6c94a83ec1f65663a5486254`
- Header checksum: `08` (valid)
- Global checksum: `7781` (valid)

## Scope boundary
This phase only establishes safe Kanto-side spawning. It does not yet implement starter acquisition, Kanto early-game story flags, or Oak's Lab intro flow.
