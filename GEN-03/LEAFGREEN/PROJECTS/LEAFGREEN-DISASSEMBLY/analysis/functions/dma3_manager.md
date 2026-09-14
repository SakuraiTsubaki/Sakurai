# dma3_manager module

## Scope

The DMA3 request manager immediately follows `gpu_regs` in every supported LeafGreen target.

USA/Japan reference range: `0x000BFC–0x001027` (ROM), size `0x42C` / 1068 bytes.

The whole module is byte-identical across all seven supported ROMs once each target's module base is used.

SHA-1 of the 1068-byte module payload:

`8b2718bf8a170d9da2998e724a8ab51659d59f01`

## Target ranges

| Target | Start | End inclusive | Size |
|---|---:|---:|---:|
| Japan | `0x000BFC` | `0x001027` | `0x42C` |
| USA | `0x000BFC` | `0x001027` | `0x42C` |
| Europe Rev 1 | `0x000C10` | `0x00103B` | `0x42C` |
| Germany | `0x000C0C` | `0x001037` | `0x42C` |
| France | `0x000BF8` | `0x001023` | `0x42C` |
| Italy | `0x000C0C` | `0x001037` | `0x42C` |
| Spain | `0x000BF8` | `0x001023` | `0x42C` |

## Functions

The function layout is invariant relative to the module base.

| Relative | USA address | Symbol |
|---:|---:|---|
| `+0x000` | `0x08000BFC` | `ClearDma3Requests` |
| `+0x038` | `0x08000C34` | `ProcessDma3Requests` |
| `+0x2B0` | `0x08000EAC` | `RequestDma3Copy` |
| `+0x348` | `0x08000F44` | `RequestDma3Fill` |
| `+0x3EC` | `0x08000FE8` | `WaitDma3Request` |

The next module begins at relative offset `+0x42C` and is `bg` (`ResetBgs`).

## Reconstruction decision

This module can be represented by one shared source implementation for all supported targets. No language-specific source fork is needed for the retail bytes observed here; only the module placement differs among target families.

## Verification method

The seven read-only 16 MiB reference ROMs were sliced at the target-specific bases above and compared directly. All seven slices have the same SHA-1 and exact byte content.
