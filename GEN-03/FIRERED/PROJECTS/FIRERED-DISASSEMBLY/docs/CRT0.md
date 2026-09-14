# ARM startup / IRQ dispatcher audit

The first executable block after the standard GBA header and the Game Freak compatibility header has now been independently decoded from all eight FireRed baselines.

## Verified range

- ROM offsets: `0x000204..0x0003A3`
- GBA ROM addresses: `0x08000204..0x080003A3`
- Size: `0x1A0` (416) bytes
- `AgbMain` begins immediately after this block at `0x080003A4` in Thumb state; the startup literal contains `0x080003A5`.

The entry instruction at ROM `0x000000` branches to `0x08000204`.

## Cross-version result

The ARM instruction stream is byte-identical across:

- Japanese Rev 0
- Japanese Rev 1
- USA Rev 0
- USA Rev 1
- French
- German
- Italian
- Spanish

The first cross-version byte difference occurs at ROM `0x00039C`, after all executable instructions in the IRQ dispatcher. Only two linker-generated literal words vary:

| Baseline | `gSTWIStatus` literal @ `0x39C` | `gIntrTable` literal @ `0x3A0` |
|---|---:|---:|
| JP Rev 0 | `0x03007488` | `0x03003580` |
| JP Rev 1 | `0x030073E8` | `0x030034E0` |
| US Rev 0 | `0x03007438` | `0x03003540` |
| US Rev 1 | `0x03007438` | `0x03003540` |
| FR | `0x03007328` | `0x03003490` |
| DE | `0x03007328` | `0x03003490` |
| IT | `0x03007328` | `0x03003490` |
| ES | `0x03007328` | `0x03003490` |

The variation therefore comes from each build's IWRAM/BSS layout, not from variant-specific startup logic.

## Source reconstruction

`src/crt0.s` represents this block as one common ARM source file. `gSTWIStatus` and `gIntrTable` remain symbolic linker references so each language/revision naturally emits its own literal values.

A local reconstruction test using LLVM's ARM assembler/linker produced a **416-byte byte-for-byte match** to the canonical US Rev 0 ROM when the verified US Rev 0 symbol addresses were supplied. This proves the block can be regenerated from source rather than preserved as an opaque ROM slice.

## Functional outline

The startup code:

1. enters IRQ mode and initializes the IRQ stack;
2. switches to system mode and initializes the user/system stack;
3. installs the IRQ dispatcher address at `0x03007FFC`;
4. calls `AgbMain` in Thumb state;
5. dispatches GBA interrupts through `gIntrTable`;
6. includes the RFU/STWI timer-selection logic using `gSTWIStatus`.

## Status

**Reconstruction status: VERIFIED / SOURCE-REGENERATABLE**

This is the first executable ROM region promoted from raw analysis to shared disassembly source in this repository.
