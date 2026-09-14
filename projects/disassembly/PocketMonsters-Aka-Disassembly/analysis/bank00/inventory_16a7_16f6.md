# Japanese Bank 00 — inventory helpers

This range continues immediately after `CountSetBits` and contains the Bank 00 wrappers used for money and inventory operations.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$16A7-$16F6` | 80 bytes | `813d252dc96dc56b0b33c7e2f1604843814cec41` | `DisplayListMenuID` at `$16F7` |
| V1.1 | `$1695-$16E4` | 80 bytes | `f1bb8d54c035add4f6adb6e6e86ff24f6a6a89c3` | `DisplayListMenuID` at `$16E5` |

Aligned by relative offset, the two revisions differ in only six bytes. All six are address operands for routines that moved in V1.1; the instruction stream and data flow are otherwise identical.

## Recovered routines

- `SubtractAmountPaidFromMoney`
- `AddAmountSoldToMoney`
- `RemoveItemFromInventory`
- `AddItemToInventory`

## Revision-dependent targets

| Target | V1.0 | V1.1 |
|---|---:|---:|
| bank-1 `SubtractAmountPaidFromMoney_` | `$6ABC` | `$6A61` |
| `Bankswitch` | `$3620` | `$360E` |
| `Predef` | `$3E9D` | `$3E8B` |
| `DisplayTextBoxID` | `$3130` | `$311E` |
| `PlaySoundWaitForCurrent` | `$3788` | `$3776` |
| `WaitForSoundToFinish` | `$3790` | `$377E` |

The bank-3 inventory workers remain at `AddItemToInventory_ = $45E2` and `RemoveItemFromInventory_ = $4652` in both revisions.

Relevant RAM/HRAM decoded from the machine code includes `hMoney = $FF9F`, `wTextBoxID = $D0EA`, and `wPlayerMoney = $D2CB`.

All range hashes and byte comparisons above were calculated directly from the supplied Japanese Red ROMs. Public Japanese Red/Green disassembly symbols were used only to cross-check semantic labels.
