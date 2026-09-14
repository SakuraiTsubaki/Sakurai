# Japanese Bank 00 — name helpers

This range contains `GetMonName`, item/TM/HM naming helpers, HM checks, and `GetMoveName`, ending immediately before `ReloadMapData`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$1AAB-$1B85` | 219 bytes | `699996dbe7a1bd9e40e95458e42da4e1e1a0a7b4` | `ReloadMapData` at `$1B86` |
| V1.1 | `$1A99-$1B73` | 219 bytes | `cf2afbacee6d6b778c7e0ca22ed901a2ad6b612f` | `ReloadMapData` at `$1B74` |

Aligned by relative offset, only eight bytes differ. They are relocated local/external address operands; name formatting data is unchanged.

## Recovered content

- five-byte Japanese Pokémon-name lookup from `MonsterNames` (bank `$0E`, address `$5068`)
- ordinary item-name lookup through the generic name engine
- TM/HM machine-name generation with two decimal digits
- original Japanese prefixes `わざマシン` and `ひでんマシン`
- `IsItemHM` and `IsMoveHM`
- HM move ID list `0F 13 39 46 94 FF`
- move-name lookup from `MoveNames` bank `$04`

Verified constants include `HM01=$C4`, `TM01=$C9`, `NUM_HMS=5`, item-name type `$04`, move-name type `$02`, and full-width zero tile `$F6`.

Revision-dependent helper targets are `GetName` (`$37B3/$37A1`) and `IsInArray` (`$3DDB/$3DC9`).

All hashes and byte comparisons were calculated directly from the supplied Japanese Red ROMs.
