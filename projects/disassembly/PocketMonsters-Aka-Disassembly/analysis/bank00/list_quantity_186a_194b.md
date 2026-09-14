# Japanese Bank 00 — quantity / price selector

This range is `DisplayChooseQuantityMenu`, immediately following the list-menu core and ending before `ExitListMenu`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$186A-$194B` | 226 bytes | `0304290679d2b8092d0d3e0b02bf6c04e0080630` | `ExitListMenu` at `$194C` |
| V1.1 | `$1858-$1939` | 226 bytes | `d729a0088b1020236b14ab61ea3e70bb61caaa82` | `ExitListMenu` at `$193A` |

Aligned by relative offset, only 11 bytes differ. They are relocated internal jump operands and external helper operands; the quantity/price algorithm and embedded strings are unchanged.

## Recovered behavior

- draws either the compact quantity box or the Pokémart quantity+price box
- cycles quantity from 1 through `wMaxItemQuantity`
- handles A/B/Up/Down input
- multiplies BCD item price by selected quantity using `AddBCDPredef`
- optionally halves the total for item selling using `DivideBCDPredef3`
- prints total price and two-digit quantity
- returns `0` for confirm and `$FF` for cancel

## Verified constants/data

- `AddBCDPredef` predef ID: `$0B`
- `DivideBCDPredef3` predef ID: `$0D`
- `hItemPrice = $FF8B`
- `hHalveItemPrices = $FF8E`
- `hMoney = $FF9F`
- `hDivideBCDDivisor / hDivideBCDQuotient = $FFA2`
- `wItemQuantity = $CF7D`
- initial quantity string bytes: `F1 F6 F7 50` (`×０１@`)
- quantity/price spacing string: seven `$7F` spaces followed by `$50`

Revision-dependent helper targets used by this block include `JoypadLowSensitivity` (`$3879/$3867`), `PrintBCDNumber` (`$2FC4/$2FB2`), `PrintNumber` (`$3C8F/$3C7D`), and the already-recorded revision-specific `Predef` address.

All range hashes and byte comparisons were calculated directly from the supplied Japanese Red ROMs.
