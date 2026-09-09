# Bank 00 deep audit — ROM0 / HOME

## Revision structure

- Rev 0 HOME: `$0150-$3FD5` = `$3E86` bytes; tail residual `$3FD6-$3FFF` = `$2A` bytes.
- Rev A HOME: `$0150-$3FC3` = `$3E74` bytes; tail residual `$3FC4-$3FFF` = `$3C` bytes.
- Semantic HOME body therefore shrinks exactly `$12` (18) bytes in Rev A.

## Direct revision change

`home/serial.asm` has an 18-byte Rev-0-only block inside `Serial_ExchangeBytes.storeReceivedByte`. It checks reset/link state and internal-clock state and can redirect the receive destination to `wNameBuffer`. Rev A removes this block.

`home/serial2.asm` is not deleted. Its include position moves across revisions:

- Rev 0: serial2 routines occur before `Serial_ExchangeByte`.
- Rev A: serial2 routines occur after `SetUnknownCounterToFFFF`.

This is a layout/reordering change, not a wholesale rewrite of the serial2 routines.

## Address consequences

| Symbol | Rev 0 | Rev A |
|---|---:|---:|
| `Serial_ExchangeBytes.storeReceivedByte` | `00:0C14` | `00:0C14` |
| `Serial_ExchangeLinkMenuSelection` | `00:0C2E` | `00:0CC9` |
| `Serial_ExchangeByte` | `00:0CAA` | `00:0C1C` |
| `Timer` | `00:0D9A` | `00:0D88` |

Everything after the removed 18-byte region can inherit a `-0x12` address shift, while the moved serial2 block creates an additional local reorder. Consequently, many `call`, `jp`, pointer, predef and cross-bank operands across the ROM change even when their higher-level behavior does not.

## Audit interpretation

The raw byte comparison reports 13,109 different bytes in bank 00. That number must **not** be interpreted as 13,109 bytes of unique new logic. The dominant causes are the 18-byte direct removal, serial2 relocation, resulting address cascade, and revision-specific residual/filler bytes.

## Other ROM0 notes

- Standard Game Boy reset/interrupt vectors occupy the low ROM0 addresses.
- The source marks reset vectors as unused; `rst $38` ultimately jumps to `$F080` echo RAM and is intentionally unreachable in normal use.
- VBlank, Timer and Serial vectors are active hardware entry points.
- Bank-switch helpers in ROM0 are root infrastructure for the semantic call-graph pass.
