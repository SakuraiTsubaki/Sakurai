# Sprite engine reconstruction — Phase 2, Part 4

Part 4 closes the remaining `sprite.c` code after Part 3 and identifies the exact linked-object boundary from `sprite.o` to `text.o`.

## Coverage

The final block contains exactly three functions in every verified target:

1. `SetSubspriteTables`
2. `AddSpriteToOamBuffer`
3. `AddSubspritesToOamBuffer`

After the literal pool belonging to `AddSubspritesToOamBuffer`, the next code is the first `text.c` function, `UpdateBGRegs`.

Public `pret/pokeruby` source confirms that `AddSubspritesToOamBuffer` is the final function in `sprite.c`, while `UpdateBGRegs` is the first function body in `text.c`. The addresses, sizes and fingerprints below are derived from the verified local ROM set.

## Exact object boundaries

| Family | Part-4 / `SetSubspriteTables` | `text.o` / `UpdateBGRegs` | Part-4 bytes |
|---|---:|---:|---:|
| Japan Rev 0 | `0x2540` | `0x27DC` | `0x29C` |
| English Rev 0/1/2 | `0x2730` | `0x29AC` | `0x27C` |
| DE/FR/IT/ES retail | `0x2864` | `0x2AE0` | `0x27C` |
| German Debug | `0x287C` | `0x2AF8` | `0x27C` |

The Japanese compiler/layout makes `AddSubspritesToOamBuffer` plus its trailing literal pool `0x20` bytes larger than the international layout.

## Function layouts

International/debug:

| Function | Relative offset | Size |
|---|---:|---:|
| `SetSubspriteTables` | `+0x0` | `0xC` |
| `AddSpriteToOamBuffer` | `+0xC` | `0x6C` |
| `AddSubspritesToOamBuffer` | `+0x78` | `0x204` |

Japanese:

| Function | Relative offset | Size |
|---|---:|---:|
| `SetSubspriteTables` | `+0x0` | `0xC` |
| `AddSpriteToOamBuffer` | `+0xC` | `0x6C` |
| `AddSubspritesToOamBuffer` | `+0x78` | `0x224` |

## Region fingerprints

- `japan_rev0`: `ca08a13dfa8d15f9593114ae7be4cb583ffb36cd`
- `english_rev0`: `03a817b8640db6b95e8df6a38a314c93b74bbebf`
- `english_rev1`: `895b771a5a74d4bbc7ba4ed00fb9a9b484991286`
- `english_rev2`: `895b771a5a74d4bbc7ba4ed00fb9a9b484991286`
- `germany_rev0`: `6317c5e82ffb6b8a0af8ee338cb7e1d4d8529403`
- `germany_rev1`: `6317c5e82ffb6b8a0af8ee338cb7e1d4d8529403`
- `germany_debug_rev0`: `965dd5065f46ba0bc20f68451f7bf2bad2b79a9c`
- `france_rev0`: `e52b525fb26b4aec05badb524e5f5b2d236a3f90`
- `france_rev1`: `e52b525fb26b4aec05badb524e5f5b2d236a3f90`
- `italy_rev0`: `8f8073e143b2b0d961a773b63caaaea771bc8ac7`
- `italy_rev1`: `8f8073e143b2b0d961a773b63caaaea771bc8ac7`
- `spain_rev0`: `60250a96fadd79d50b8ae05c0ff2e2db6379df38`
- `spain_rev1`: `60250a96fadd79d50b8ae05c0ff2e2db6379df38`

## Completed contiguous `sprite.o` coverage

With Parts 1–4 combined, the complete linked `sprite.o` text/code region is now mapped continuously:

| Family | `sprite.o` start | `sprite.o` end / `text.o` start | Total bytes |
|---|---:|---:|---:|
| Japan Rev 0 | `0x74C` | `0x27DC` | `0x2090` |
| English retail | `0x748` | `0x29AC` | `0x2264` |
| DE/FR/IT/ES retail | `0x87C` | `0x2AE0` | `0x2264` |
| German Debug | `0x87C` | `0x2AF8` | `0x227C` |

This completes the first full post-`main.o` engine object mapping. No ROM bytes are stored in the repository; the committed tables contain only addresses, sizes, hashes and reproducible analysis logic.

## Next object

Continue at `text.o` / `UpdateBGRegs` and map the text/font/window engine. Text work must eventually be paired with reconstructed font graphics and language-specific character/width tables so the repository remains independently rebuildable.
