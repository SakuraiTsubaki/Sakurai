# FireRed ROM Physical Layout Audit

This document records the first physical-layout pass across all eight verified Pokémon FireRed baselines used by this repository.

The analysis is offset-based and intentionally conservative: it identifies long `0xFF` gaps, aligned 4 KiB equivalence ranges, and fixed late-data islands. It does **not** assign semantic names to an island until the content has been matched to source structures.

## Baselines

| ID | Game code | Revision | GF language | Size |
|---|---|---:|---:|---:|
| `jp_rev0` | `BPRJ` | 0 | 1 | 16 MiB |
| `jp_rev1` | `BPRJ` | 1 | 1 | 16 MiB |
| `us_rev0` | `BPRE` | 0 | 2 | 16 MiB |
| `us_rev1` | `BPRE` | 1 | 2 | 16 MiB |
| `fr` | `BPRF` | 0 | 3 | 16 MiB |
| `de` | `BPRD` | 0 | 5 | 16 MiB |
| `it` | `BPRI` | 0 | 4 | 16 MiB |
| `es` | `BPRS` | 0 | 7 | 16 MiB |

All eight GBA header checksums validate.

## Major physical layout difference

The Japanese and international ROMs do not place their late graphics/data island at the same address.

- Japanese Rev 0/Rev 1: corresponding late island begins at ROM offset **`0xC00000`** (`0x08C00000` in GBA ROM address space).
- International builds: corresponding late island begins at ROM offset **`0xD00000`** (`0x08D00000`).

The public `pret/pokefirered` linker script places `gfx_data` at `0x08D00000`, matching the international baselines. Our Japanese baselines prove that a separate Japanese linker/layout configuration is required rather than treating Japanese as text-only localization.

The first 64 bytes at Japanese `0xC00000` and international `0xD00000` are byte-identical. Across the first `0x195DC4` bytes of this shifted island, Japanese Rev 1 and US/FR/ES are about 83.3% byte-identical; German and Italian diverge more strongly because localized assets/data alter the packed layout.

## Long `0xFF` gaps

Long gaps are defined here as contiguous `0xFF` runs of at least `0x1000` bytes.

### Japanese Rev 0

- `0x6C7D38..0xBFFFFF` — large middle padding gap
- `0xD95DC4..0xEFFFFF` — late padding gap
- `0xFDFFFF..0xFFFFFF` — trailing padding

### Japanese Rev 1

- `0x6C32B4..0xBFFFFF`
- `0xD95DC4..0xEFFFFF`
- `0xF3F3E4..0xFFFFFF`

### USA Rev 0

- `0x71A23C..0xCFFFFF`
- `0xEB0B20..0xFFFFFF`

### USA Rev 1

- `0x71A29C..0xCFFFFF`
- `0xEB0B20..0xFFFFFF`

### French

- `0x7105B8..0xCFFFFF`
- `0xEB21A0..0xFFFFFF`

### German

- `0x718C40..0xCFFFFF`
- `0xEB218C..0xFFFFFF`

### Italian

- `0x70DE68..0xCFFFFF`
- `0xEB22EC..0xFFFFFF`

### Spanish

- `0x710DE4..0xCFFFFF`
- `0xEB229C..0xFFFFFF`

## 4 KiB aligned comparison

The eight 16 MiB ROMs contain 4096 aligned 4 KiB blocks. Compressing blocks by their cross-version equality pattern yields only **65 contiguous range patterns**, which gives us a compact first-pass relocation map.

Important caution: a range that is identical across all eight versions is not automatically shared game content. The largest all-version-identical ranges are pure `0xFF` padding:

- `0x71B000..0xBFFFFF` — 5,132,288 bytes of `0xFF`
- `0xEB3000..0xEFFFFF` — 315,392 bytes of `0xFF`
- `0xFE0000..0xFFFFFF` — 131,072 bytes of `0xFF`

Therefore semantic source matching must use pointers/symbols/content, not aligned equality alone.

## Revision similarity

At 4 KiB aligned resolution:

- `jp_rev0` vs `jp_rev1`: **2199 / 4096 blocks (53.6865%)** are identical.
- `us_rev0` vs `us_rev1`: **2298 / 4096 blocks (56.1035%)** are identical.

These percentages are physical-offset similarity, not a measure of logical code similarity. Small code/data changes can relocate large portions of a linked ROM.

## Consequence for the disassembly

The repository will use a shared logical source tree with explicit per-version layout configuration. It must support at least:

1. different GBA header game/language/revision values;
2. different Game Freak compatibility-header pointers and string limits;
3. Japanese vs international save-structure sizing;
4. Japanese late-data placement at `0x08C00000` vs international `0x08D00000`;
5. revision-specific link ordering/addresses where byte-exact output requires it.

Raw ROMs are analysis inputs only and are never committed.
