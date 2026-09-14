# Japanese Bank 00 — Start Menu and `CountSetBits`

These ranges continue immediately after the common text-script dispatcher.

## `DisplayStartMenu`

| Build | Range | Size | SHA-1 |
|---|---:|---:|---|
| V1.0 | `$15DE-$168F` | 178 bytes | `cc6fb15025912f7e57b3a9db951009005a731c48` |
| V1.1 | `$15CC-$167D` | 178 bytes | `5782135ea78406c03be66b22cabd4df5367e4796` |

An aligned comparison finds 14 differing bytes. They are revision-specific helper/banked target addresses and relocated Bank 00 targets; the Start Menu control flow is unchanged.

Recovered behavior includes Start Menu music, menu drawing, Safari Zone step display, cursor wraparound with/without Pokédex, selected-item dispatch, B/Start close handling, and restoration of the text-box/map view path.

## `CountSetBits`

| Build | Range | Size | SHA-1 |
|---|---:|---:|---|
| V1.0 | `$1690-$16A6` | 23 bytes | `d35127402ee6098bf3c35edab9342bd78f877e22` |
| V1.1 | `$167E-$1694` | 23 bytes | `d35127402ee6098bf3c35edab9342bd78f877e22` |

The routine is byte-identical between revisions and counts set bits across `b` bytes at `hl`, storing the result in `wNumSetBits` (`$D0E3`).

## Next boundary

The following Bank 00 file is the inventory helper block, beginning with `SubtractAmountPaidFromMoney` at:

- V1.0 `$16A7`
- V1.1 `$1695`

No graphics payload is present in either range.
