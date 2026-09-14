# Japanese Bank 00 — Serial block (`$0BA7` to `Timer`)

This block continues immediately after `FadePal8` and reconstructs the Japanese Red link-cable/serial engine through the byte before the timer interrupt handler.

## ROM-verified ranges

| Build | Serial range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$0BA7-$0D99` | 499 bytes | `4a3a536ed5fbc9b1f86d680e47e5317f3eb58006` | `Timer` at `$0D9A` |
| V1.1 | `$0BA7-$0D87` | 481 bytes | `23ba0cb6c6793f1a5f807c5ab2619f1ed211b8b3` | `Timer` at `$0D88` |

The source is split into `home/jp_serial.asm` and `home/jp_serial2.asm`.

## Revision structure

Both revisions begin `Serial` at `$0BA7` and `Serial_ExchangeBytes` at `$0BF1`. The first material layout change occurs inside `Serial_ExchangeBytes`.

V1.0 contains an 18-byte block at `$0C14-$0C25` that checks the unused `LINK_STATE_RESET` state and, only when using the internal serial clock, redirects `de` to `wNameBuffer`. V1.1 removes this block entirely.

The link-menu synchronization block (`jp_serial2.asm`) is also deliberately placed at different positions:

| Routine/block | V1.0 | V1.1 |
|---|---:|---:|
| `Serial_ExchangeByte` | `$0CAA` | `$0C1C` |
| `WaitLoop_15Iterations` | `$0D41` | `$0CB3` |
| `IsUnknownCounterZero` | `$0D47` | `$0CB9` |
| `SetUnknownCounterToFFFF` | `$0D4F` | `$0CC1` |
| link-menu synchronization block | `$0C2E-$0CA9` | `$0CC9-$0D44` |
| `Serial_ExchangeNybble` | `$0D57` | `$0D45` |
| `Serial_SendZeroByte` | `$0D81` | `$0D6F` |
| `Serial_TryEstablishingExternallyClockedConnection` | `$0D8E` | `$0D7C` |

The reconstruction preserves this ordering with `IF DEF(AKA_JP_REV0)` / `IF DEF(AKA_JP_REVA)` includes rather than flattening both revisions into one artificial layout.

## Verified state addresses

The machine code and symbol cross-checks identify the serial HRAM block as `$FFA9-$FFAD`:

- `hSerialReceivedNewData = $FFA9`
- `hSerialConnectionStatus = $FFAA`
- `hSerialIgnoringInitialData = $FFAB`
- `hSerialSendData = $FFAC`
- `hSerialReceiveData = $FFAD`

Relevant Japanese WRAM includes `wLinkMenuSelectionReceiveBuffer = $CC3D`, `wSerialExchangeNybbleReceiveData = $CC3E`, `wLinkMenuSelectionSendBuffer = $CC42`, `wUnknownSerialCounter = $CC47`, `wNameBuffer = $CD68`, and `wUnknownSerialCounter2 = $D051`.

## Revision-dependent external targets

The link-menu helper calls ROM0 utility routines whose addresses move by `$12` in V1.1:

| Target | V1.0 | V1.1 |
|---|---:|---:|
| `Bankswitch` | `$3620` | `$360E` |
| `SaveScreenTilesToBuffer1` | `$3761` | `$374F` |
| `LoadScreenTilesFromBuffer1` | `$376D` | `$375B` |

`PrintWaitingText` remains bank 1 address `$49ED`; the reconstructed source expands its far call explicitly until the shared farcall macro layer is recovered.

All hashes and range boundaries above were calculated from the supplied Japanese Red ROMs. Public `Narishma-gb/pokegreen` symbols/source were used only to cross-check semantic labels and the revision-specific source ordering.
