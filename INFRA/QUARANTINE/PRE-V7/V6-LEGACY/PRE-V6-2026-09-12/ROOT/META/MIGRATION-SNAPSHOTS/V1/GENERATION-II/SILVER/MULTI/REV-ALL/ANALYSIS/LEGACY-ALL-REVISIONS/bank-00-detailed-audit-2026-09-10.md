# BANK 00 detailed audit — Pokémon Silver multi-region

## Scope
- ROM offsets: `0x000000–0x003FFF`
- CPU-visible range: fixed ROM0 `0x0000–0x3FFF`
- Role: reset/RST vectors, hardware interrupt vectors, cartridge header, and Home routines.

## Bank SHA-1
| Build | SHA-1 |
|---|---|
| KR | `59f72dba5fad85ee31c3d0c419d0e25d619d7e26` |
| JP Rev0 | `46580fdd8f266ac2c99c0f52cec1019e665bc787` |
| JP RevA | `4f062dae6083604f6027c9e36c12299836ec3d91` |
| EN | `b436a03004fb1c2e392a326c5042b679a316d0c6` |
| DE | `906e353c3613b0e140a72506a52c226d8d63dbc6` |
| FR | `e9a0092f2d7c009d091d7b83e187ac8f6b5a0e44` |
| IT | `1839fba274284abe5ab3da6c750d71945e4a29b0` |
| ES | `674c23a4eb8005c0afa77f53a8d60cdcd8c0620a` |

## EN-relative byte identity
| Build | Different bytes | Identical |
|---|---:|---:|
| KR | 14,819 | 9.5520% |
| JP Rev0 | 14,938 | 8.8257% |
| JP RevA | 14,936 | 8.8379% |
| DE | 11,991 | 26.8127% |
| FR | 11,944 | 27.0996% |
| IT | 11,943 | 27.1057% |
| ES | 12,070 | 26.3306% |

The vectors/header are much more conserved than the Home body. Against EN, DE/FR/IT/ES retain >99% identity in `0000–00FF` except one byte, while localization shifts make most of `0150–3FFF` differ.

## Header facts
- KR title: `POKEMON_SLVAAXK`, CGB flag `C0`, SGB disabled, ROM-size code `06` (2 MiB), destination `01`, version `00`.
- JP Rev0/RevA title: `POKEMON_SLVAAXJ`, CGB flag `80`, SGB flag `03`, ROM-size code `05` (1 MiB), destination `00`; version byte is `00` / `01` respectively.
- Western builds use title suffixes E/D/F/I/S, CGB flag `80`, SGB `03`, ROM-size code `06` (2 MiB), destination `01`, version `00`.
- Header and global checksums were independently verified valid in the source census.

## RST-vector structural difference
The Korean build is not just a translated Home bank. It repurposes fixed-vector space that the English disassembly leaves as recursive `rst $38` traps:

- `RST $18` (`0018`) in KR starts `WaitHBlank`, polling `rSTAT` until HBlank.
- The same routine flows across the nominal `RST $20` location.
- `RST $38` (`0038`) in KR contains a `nop` followed by `WaitOneLine`, a timing loop documented for double-speed mode.
- EN/pret places `rst $38` at `0018`, `0020`, and `0038` instead.

The actual uploaded KR ROM bytes at `0018–0024` and `0038–003E` match this structural change, so these are real executable-code differences rather than layout comments.

## JP Rev0 → RevA changes inside BANK 00
There are 179 changed bytes in BANK 00, grouped into six exact contiguous spans:

- `014C–014F`: version/checksum fields (4 bytes)
- `3C6B`: 1 byte
- `3F0F–3F27`: 25 bytes
- `3F29–3F2C`: 4 bytes
- `3F2E–3F43`: 22 bytes
- `3F45–3FBF`: 123 bytes

The large change cluster is therefore near the end of ROM0, not in the main header. It still requires symbol/routine mapping before assigning bug-fix semantics.

## Disassembly status
- `0000–014F`: structure identified (RST vectors, interrupt vectors, entry/header).
- `0150–3FFF`: Home code/data region; requires routine-by-routine control-flow and data-boundary mapping per build.
- KR-specific vector timing code is already semantically identified and verified against the uploaded ROM.
- JP Rev0/RevA end-of-bank revision cluster is isolated for the next semantic pass.
