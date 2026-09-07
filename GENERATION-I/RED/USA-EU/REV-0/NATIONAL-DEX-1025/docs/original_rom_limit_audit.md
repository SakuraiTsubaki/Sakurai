# Pokémon Red (USA/Europe) original ROM expansion-limit audit

Target ROM: `Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb`

## Direct binary findings

- ROM size: 1,048,576 bytes (1 MiB), 64 × 16 KiB banks (`$00-$3F`)
- Cartridge type byte `$0147`: `$13` = MBC3 + RAM + Battery
- ROM size byte `$0148`: `$05` = 1 MiB
- RAM size byte `$0149`: `$03` = 32 KiB / 4 × 8 KiB SRAM banks
- Last non-zero ROM byte: file offset `$0B060E` = bank `$2C` offset `$060E`
- Contiguous zero tail: 326,129 bytes = 318.485 KiB
- Banks `$2D-$3F`: 19 completely zero banks = 304 KiB
- The source layout also ends at bank `$2C` (Move Names), confirming `$2D-$3F` are unused/padding in the stock international ROM layout.

## Mapper / ROM addressing ceilings

1. Stock MBC3 hardware ceiling: 2 MiB / 128 ROM banks.
   - From the end of the used stock data to 2 MiB: 1,374,705 bytes (1.311 MiB) of potential address space.
2. MBC5 hardware ceiling: 8 MiB / 512 ROM banks.
3. Stock engine keeps the current ROM bank in an 8-bit variable and bank-switch code writes one byte.
   - After an MBC5 conversion, keeping the old 8-bit bank ABI naturally covers banks `$00-$FF` = 4 MiB.
   - Reaching banks `$100-$1FF` (full 8 MiB) requires adding/supporting the MBC5 ninth ROM-bank bit throughout bank references / far calls.

## Species / Pokédex identifier ceilings

- Stock `wCurSpecies` is 1 byte.
- Party species arrays are byte arrays; `$FF` is used as a terminator.
- Box/party mon structures store Species as 1 byte.
- `PokedexOrder` stores Pokédex numbers as bytes.
- Therefore 1025 Species cannot be represented without widening identifiers.
- Raw 8-bit namespace has 256 values, but `$00` is NO_MON and `$FF` is a list terminator in stock structures; a redesigned-but-still-8-bit scheme tops out around 254 usable IDs.
- Stock internal index table currently ends at `$BE` (190 indexes). `GetName` has a stock bug/constraint that treats indexes `>= HM01 ($C4)` as machine names; simple appending therefore only reaches `$C3` (195) before that routine must be fixed.

## Fixed-size table ceilings

Original base-stat record size is 28 bytes:
- HP, Attack, Defense, Speed, Special: 1 byte each
- Type 1/2: 1 byte each
- Catch Rate, Base EXP: 1 byte each
- sprite dimension: 1 byte
- front/back sprite addresses: 16-bit pointers
- four starting moves: 1 byte each
- growth rate: 1 byte
- TM/HM compatibility: 7 bytes
- padding: 1 byte

Capacity implications:
- 151 × 28 = 4,228 bytes
- 1025 × 28 = 28,700 bytes (28.03 KiB)
- 1351 × 28 = 37,828 bytes (36.94 KiB)
- A single 16 KiB ROM bank can hold at most 585 dedicated 28-byte records, before any other data.
- Stock `GetMonHeader` assumes one `BaseStats` bank, so 1025/1351 records require a banked/far-pointer/page lookup even apart from the 16-bit Species change.

## Sprite ceiling

- Stock battle picture workspace is fixed at 7×7 tiles (56×56 pixels).
- Front/back pointers in the mon header are only 16-bit addresses; the ROM bank is selected separately by a hard-coded species-index range routine (`Pics 1` through `Pics 5`).
- 1579 visual forms therefore require replacing the hard-coded sprite-bank routing with explicit banked/far sprite references.
- Graphics, not base-stat records, will be the dominant ROM consumer once hundreds/thousands of forms are added.

## Pokédex/save ceiling

- Stock Pokédex Owned/Seen are bit arrays sized for 151 species: ceil(151/8) = 19 bytes each.
- For 1025 species: ceil(1025/8) = 129 bytes each (258 bytes total), only +220 bytes over stock.
- For a future-proof 4096-species reservation: 512 bytes each (1024 bytes total).
- Stock SRAM is 32 KiB in four 8 KiB banks. PC storage is 12 boxes × 20 mons; six boxes are stored in each of SRAM banks 2 and 3.
- Widening persistent species/form fields breaks the stock save format but is not, by itself, a large storage burden. Save layout/checksum code must be versioned or rewritten.

## Other stock data-width limits relevant to modernization

- Move ID: 1 byte; four move slots. >254/255 modern move IDs would require a separate move-ID widening project.
- Type ID: 1 byte; adding types is table work, not an immediate width problem.
- Base HP/Atk/Def/Spd/Special, catch rate, base EXP: 1 byte each (0-255).
- Gen I has one Special stat, so modern Sp. Atk/Sp. Def cannot both be represented without changing battle/stat structures.
- Party structure: 44 bytes; box mon structure: 33 bytes. Changing Species or adding persistent Form/Variety fields shifts save/link formats.
- Retail link/trade protocol compatibility is broken by widened party structures unless a legacy translation layer is added.

## Practical breakpoints for RED1025+

### Stock ROM, no engine widening
- Plenty of byte-level ROM padding in international Red (~318.5 KiB contiguous tail).
- But species identity hits the 8-bit / `$FF` terminator / `GetName $C4` constraints long before ROM space does.
- This route cannot reach 1025.

### MBC3 retained, engine widened
- Up to 2 MiB total ROM.
- Enough for substantial extra data, but likely too restrictive once 1351 battle varieties + 1579 visual forms + sprites + Pokédex text are included.

### MBC5, old 8-bit bank ABI retained
- Natural ceiling: 4 MiB / 256 banks.
- This matches the current RED1025 foundation strategy and avoids needing the ninth MBC5 bank bit immediately.

### MBC5, bank ABI widened to 9 bits
- Full ceiling: 8 MiB / 512 banks.
- Best long-term target if Gen 10+ and a large visual-form asset set must be appendable without another mapper/banking redesign.

## Conclusion

The original Red ROM is **not primarily limited by file space**. The first true blocker is the **8-bit species/index architecture** and the many byte-based structures that depend on it. After that, the next architectural blockers are **single-bank tables / 16-bit same-bank pointers**, then **8-bit ROM-bank bookkeeping** when crossing 4 MiB on MBC5. The stock 7×7 sprite system and save/link structures are secondary but mandatory refactors for a complete 1025/1351/1579 implementation.
