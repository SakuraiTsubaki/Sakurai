# Bank 00 Semantic Pass — Pokémon Yellow / Pikachu

## Status

Bank `00` is partially promoted from byte-exact Stage 0 to semantic structure. The English ROM uses the exact-matching `pret/pokeyellow` source as the naming reference; Japanese and other international variants are mapped by ROM bytes and anchors.

## Fixed ROM0 regions

- `$0000`–`$003F`: RST vectors / unused padding
- `$0040`: VBlank vector
- `$0048`: LCD STAT vector
- `$0050`: Timer vector
- `$0058`: Serial vector
- `$0060`: Joypad vector (`reti`)
- `$0100`: cartridge entry point (`nop` + `jp`)
- `$0104`–`$014F`: cartridge header area
- `$0150` onward: Home routines / fixed-bank engine

## Entry points and interrupt targets

| ROM | Entry JP | VBlank | LCD | Timer | Serial | CGB flag | Cart type | Header rev |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| EN | `$01AB` | `$1DE5` | `$15AC` | `$216A` | `$1F79` | `$80` | `$1B` | 0 |
| FR | `$01AB` | `$1DE1` | `$15A9` | `$2166` | `$1F75` | `$80` | `$1B` | 0 |
| DE | `$01AB` | `$1DEA` | `$15AC` | `$216F` | `$1F7E` | `$80` | `$1B` | 0 |
| IT | `$01AB` | `$1DE5` | `$15AC` | `$216A` | `$1F79` | `$80` | `$1B` | 0 |
| ES | `$01AB` | `$1DE4` | `$15AC` | `$2169` | `$1F78` | `$80` | `$1B` | 0 |
| JP Rev 0A | `$1D60` | `$1E35` | `$1580` | `$2193` | `$1FA2` | `$00` | `$13` | 0 |
| JP Rev B | `$1D66` | `$1E3B` | `$1586` | `$219C` | `$1FAB` | `$00` | `$13` | 1 |
| JP Rev C | `$1D66` | `$1E3B` | `$1586` | `$219C` | `$1FAB` | `$00` | `$13` | 2 |
| JP Rev D | `$1D66` | `$1E3B` | `$1586` | `$219C` | `$1FAB` | `$00` | `$13` | 3 |

## Startup structure

The canonical English entry at `$01AB` performs the CGB boot-register test and then jumps to `Init` at `$1D10`. Japanese B/C/D enter directly at `$1D66`, and Rev 0A at `$1D60`; these addresses contain the same hardware-initialization sequence corresponding to EN `Init`.

So the large ROM0 difference is not a completely different engine. A major cause is the international CGB-aware entry shim versus direct Japanese initialization.

## Bank-switch core mapping

| Routine | EN | JP Rev B/C/D | JP Rev 0A |
|---|---:|---:|---:|
| `BankswitchCommon` | `$3E7E` | `$3E78` | `$3E77` |
| `Bankswitch` | `$3E84` | `$3E7E` | `$3E7D` |
| `JumpToAddress` | `$3E98` | `$3E92` | `$3E91` |
| `OpenSRAM` | `$3E99` | `$3E93` | `$3E92` |
| `BankswitchHome` | `$35D9` | `$35FB` | `$35FA` |
| `BankswitchBack` | `$35E8` | `$360A` | `$3609` |

`BankswitchCommon` retains the same core operation: save the active bank in HRAM, write the ROM bank register at `$2000`, and return. `Bankswitch` saves the old bank, switches to bank `B`, jumps through `HL`, then restores the old bank.

## Conclusions

1. Bank `00` can use the English canonical Home symbols as the semantic naming base.
2. Japanese B/C/D are very close to each other in the bank-switch tail; Rev 0A is typically shifted by one byte there.
3. The largest startup-layout difference is the CGB-aware international entry path versus direct Japanese initialization.
4. Interrupt routine addresses move by language/revision, so labels must transfer semantically rather than by absolute address.
5. ROM-wide cross-bank call analysis should normalize calls through `Bankswitch`, `BankswitchHome`, and `BankswitchCommon` first.

## Next Bank 00 work

- Resolve all Home routine boundaries/labels from canonical EN.
- Build EN → JP Rev D symbol-address mapping from exact byte anchors.
- Propagate Rev D symbols to Rev C/B/0A.
- Propagate EN symbols to FR/DE/IT/ES.
- Mark variant-only code/data and header-specific differences.
- Rebuild and SHA-1 verify after semantic replacement of confirmed code regions.
