# Generation IV battle sprites -> Generation III — Phase 1

## Scope

ROM-primary first playable insertion pass for the uploaded Japanese Generation III ROMs. The authoritative visual source for this phase is the uploaded Korean HeartGold ROM `pbr/pokegra.narc`; the previously published DP / Platinum / HGSS master remains the cross-version preservation layer.

Phase 1 does **not** claim the Generation IV species/form engine is complete. It makes the 386 National Dex species already represented by the Gen III engine use HGSS-derived battle graphics while embedding an HGSS base bank for National Dex 001-493 for later table expansion.

## Source

- HeartGold SHA-256: `659f20ca1d4f43b8b675d3c47217bb875a4f14c62438b08fa42f60467e2bed43`
- NitroFS source: `pbr/pokegra.narc`
- Pokémon NCGR decryption: reverse LCRNG-XOR, seed from final u16, walk backwards, state `state * 0x41C64E6D + 0x6073`
- Conversion: project preservation-v2 80x80 -> 64x64, source indices only, no anti-aliasing/new colors
- GBA graphics: OBJ 4bpp tiled, 64x64
- GBA palettes: source 16-color BGR555
- Compression: BIOS-compatible LZ10

## Embedded HGSS bank

- Species: 001-493
- Front/back: retained
- Frames: f0/f1 retained
- Normal/shiny palettes: retained
- Unique 4bpp frame payloads after dedup: 1,488
- Unique palettes after dedup: 974
- Bank size: 1,171,584 bytes

The vanilla Gen III display tables are redirected only for the 386 species already supported by the engine. HGSS male/shared f0 is the Phase-1 default; Emerald's animated front table receives an f0+f1 two-frame payload.

## Gen III species-ID rule

Do not treat National Dex number as raw Gen III species ID after Celebi. Gen III reserves 252-276 for `SPECIES_OLD_UNOWN_B` ... `SPECIES_OLD_UNOWN_Z`; `SPECIES_TREECKO` starts at 277. Therefore:

- National 001-251 -> internal 001-251
- National 252-386 -> internal National+25 (277-411)
- internal 252-276 are preserved untouched

## Target results

| Target | Source SHA-256 | Front table | Back table | Animated front | Palette table | Bank offset | Output size | IPS32 bytes | Verification |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Ruby JP Rev0 | `e911caa1ffbf8704cd45bbe064ade40e24efa50dfdce82adf4b2899b5f733852` | `0x1BCB60` | `0x1BE000` | — | `0x1BEDC0` | `0x800000` | 16 MiB | 1,186,666 | 0 errors |
| Sapphire JP Rev0 | `6a5ff7656531ab41d1ea9cd8f2d045ab6228405b43f3ee09ea3ff5077c0f60c9` | `0x1BCAF0` | `0x1BDF90` | — | `0x1BED50` | `0x800000` | 16 MiB | 1,186,666 | 0 errors |
| Emerald JP Rev0 | `33f5610b9186b4add09fef68895deb00f552b997b3d133b5a961e5123506343c` | `0x2D4CA8` | `0x2D6148` | `0x2DDA1C` | `0x2D6F08` | `0x1000000` | 32 MiB | 1,721,078 | 0 errors |
| FireRed JP Rev1 | `cec5fc4dbe38cd8026bd6664a1a041d9dc91e8d4249bab04e7bde70c3cdf4e06` | `0x1EFEA8` | `0x1F1348` | — | `0x1F2108` | `0x1000000` | 32 MiB | 1,189,359 | 0 errors |
| LeafGreen JP Rev0 | `2957b392dc09fc8df45a660af5493368d7bd378d299862f4cc115998e9da0bf2` | `0x1F466C` | `0x1F5B0C` | — | `0x1F68CC` | `0x1000000` | 32 MiB | 1,189,359 | 0 errors |

Verification iterates every redirected National Dex 001-386 entry and BIOS-LZ10-decompresses front, back, normal palette and shiny palette. Emerald additionally verifies every two-frame animated front payload. All five outputs passed with zero structural decompression failures.

## Phase boundary / next work

Not active yet: species 387-493 as real Gen III species IDs, female sprite selection, DP/Pt/HGSS runtime version selection, alternate forms from `otherpoke`, Gen IV animation command timing, and Gen-IV-derived front/back coordinate/y-offset retuning. These must be implemented by extending the engine rather than consuming or overwriting the old-Unown/reserved slots.
