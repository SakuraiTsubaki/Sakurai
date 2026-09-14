# Japanese Bank 00 — list menu core

This range begins at `DisplayListMenuID` and ends immediately before `DisplayChooseQuantityMenu`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$16F7-$1869` | 371 bytes | `665b4bc5175610a4dd1d193bbe759ad835db5b31` | `DisplayChooseQuantityMenu` at `$186A` |
| V1.1 | `$16E5-$1857` | 371 bytes | `8b3b30883f47bc7bebe5a49219c0a02a3ffaf694` | `DisplayChooseQuantityMenu` at `$1858` |

After aligning V1.1 by `$12`, 28 bytes differ. They are address operands for relocated Bank 00 helpers/local labels plus the revision-specific bank-1 `HandleItemListSwapping` target; the menu logic and data flow are unchanged.

## Recovered behavior

- list setup and text-box initialization
- Old Man battle list handling
- automatic BG transfer toggling
- list scrolling and current-entry bookkeeping
- A/B/SELECT input handling
- item-price and quantity lookup
- item-name and Pokémon nickname lookup
- chosen-entry copy to `wNameBuffer`
- return through `BankswitchBack`
- item-swap dispatch

## Key revision-dependent targets

| Target | V1.0 | V1.1 |
|---|---:|---:|
| `BankswitchHome` | `$3606` | `$35F4` |
| `HandleMenuInput` | `$3B08` | `$3AF6` |
| `PlaceMenuCursor` | `$3BC6` | `$3BB4` |
| `PlaceUnfilledArrowMenuCursor` | `$3C1C` | `$3C0A` |
| `GetItemPrice` | `$3827` | `$3815` |
| `GetName` | `$37B3` | `$37A1` |
| `GetPartyMonName` | `$2FB1` | `$2F9F` |
| `CopyToStringBuffer` | `$386E` | `$385C` |
| `BankswitchBack` | `$3617` | `$3605` |
| bank-1 `HandleItemListSwapping` | `$6ADF` | `$6A84` |
| `PrintListMenuEntries` | `$1968` | `$1956` |
| `ExitListMenu` | `$194C` | `$193A` |

The active source is `home/jp_list_menu_core.asm`. All range hashes and byte-difference counts were calculated directly from the supplied Japanese Red ROMs; public Japanese disassembly symbols were used only for semantic cross-checking.
