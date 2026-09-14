# Japanese Bank 00 — list exit and entry renderer

This block contains `ExitListMenu`, `PrintListMenuEntries`, and the embedded Japanese Cancel label, ending immediately before `GetMonName`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$194C-$1AAA` | 351 bytes | `9c9e9f13da075c2517cc42f6fd63da25c402a5e5` | `GetMonName` at `$1AAB` |
| V1.1 | `$193A-$1A98` | 351 bytes | `dd7e35b994b52cef9f3cdb43d7900477d59a2591` | `GetMonName` at `$1A99` |

Aligned by relative offset, only 14 bytes differ. The differences are relocated local/external address operands; rendering behavior and embedded data are unchanged.

## Recovered behavior

- clean list-menu cancellation and bank restoration
- clears and redraws the four visible list rows
- renders item, move, party Pokémon, or boxed Pokémon names
- optionally renders Pokémart prices
- renders Pokémon levels for PC Pokémon lists
- renders item quantities except for key items
- draws swap-item and scrolling arrows
- emits the Japanese Cancel text `やめる`

## Key targets

Revision-dependent targets in this block include `GetItemName` (`$1ADD/$1ACB`), `GetMoveName` (`$1B6D/$1B5B`), `LoadMonData` (`$2D68/$2D56`), `PrintLevel` (`$2F02/$2EF0`), and `IsKeyItem` (`$3121/$310F`). Earlier list-menu helper targets are reused from `jp_list_menu_core.asm` and `jp_list_quantity.asm`.

The `ItemPrices` data pointer remains bank-1 address `$421C` in both revisions. The embedded Cancel bytes are `D4 D2 D9 50` (`やめる@`).

All range hashes and byte comparisons were calculated directly from the supplied Japanese Red ROMs.
