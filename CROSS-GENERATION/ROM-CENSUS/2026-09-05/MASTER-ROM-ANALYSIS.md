# Pokémon Project — Cross-Generation Master ROM Analysis

Date: 2026-09-05 (Asia/Seoul)

## Policy

- Original ROM binaries are never committed to GitHub.
- GitHub contains only analysis reports, hashes, metadata, ledgers, reproducible tools/scripts, patches, and other non-ROM outputs.
- Every physical ROM file is classified separately as retail/canonical, revision, alias/duplicate, debug, or modified/non-retail before semantic comparison.
- Analysis is keyed by cryptographic identity + semantic table/function identity. Absolute offsets are never assumed portable across languages/revisions.

## Current project-wide inventory state

The current Library raw-ROM scan returns more than 100 GB/GBC/GBA/NDS images. The collection includes official regional builds, revisions, aliases/duplicates, a German Ruby debug build, and at least one modified/non-retail Gold-family image (`Pokemon_Another_Gold+(K).GBC`). Therefore physical file count is intentionally not treated as canonical build count.

### Coverage matrix

| Generation | Family | Current analysis depth | Status |
|---|---|---|---|
| I | Red | identity + revision + cross-language structural work | substantial |
| I | Green | full ROM census + Rev0/RevA semantic revision analysis | deep |
| I | Blue | 6-ROM JP/EN/DE/FR/IT/ES full structural census | deep |
| I | Yellow | 14-file / 9-unique forensic census + JP revision semantics | deep |
| II | Gold | 8 official-build bank census; modified Gold-family image kept separate | bank-level |
| II | Silver | 8-build multi-region full bank census including Korean | deep bank-level |
| II | Crystal | 7-build identity/revision baseline | baseline |
| III | Ruby | 13-build identity/revision census including German debug | baseline/revision |
| III | Sapphire | 9-build audit exists, but current Library now contains additional Spanish builds | stale/incomplete |
| III | Emerald | six-unique multilingual deep semantic census | deep |
| III | FireRed | 8-build identity/revision/bank baseline | baseline |
| III | LeafGreen | 7-build full-image Stage 3 census | deep structural |
| IV | D/P/Pt/HG/SS | Stage 2 deep census for Diamond USA, Pearl USA, Platinum KR, HG KR, SS KR | deep but current-set incomplete |
| V | Black/White EUR | full NDS/NARC/overlay/member census | deep |

## Cross-generation findings

### 1. Localization is structural, not text-only

Generation I proves this most starkly. Japanese Blue is 512 KiB / MBC1, English Blue is 1 MiB / MBC3, and continental European Blue builds are 1 MiB / MBC5. Fixed name widths and save-layout boundaries also differ. Yellow likewise has different JP/Western fixed-length name tables and PC storage layouts. Any localization patch must therefore carry charset/font/text engine/save/UI structure together, not only translated strings.

Generation II continues the same pattern. Korean Gold/Silver are not Western text swaps: the Korean builds use distinct high banks for Hangul tables/font/name-entry infrastructure and different CGB/SGB header behavior. Korean must be modeled as its own localization subsystem.

### 2. Raw byte-diff size is often a bad measure of semantic change

Green Rev0→RevA shows tens of thousands of same-offset changed bytes, but aligned/source-level analysis reduces the meaningful revision to targeted battle/link/serial maintenance plus relocation and revision-specific garbage changes.

Silver JP Rev0→RevA similarly has a small substantive sprite-animation allocation fix whose insertion shifts later addresses and inflates raw binary differences.

Ruby/Sapphire show the opposite pattern: several adjacent Western revisions are exactly four bytes apart (two header bytes plus two Thumb branch-condition bytes), while earlier English regional/revision transitions involve multi-megabyte relink/rebuild deltas. Revision identity must be modeled per build, not inferred from the revision byte alone.

### 3. Semantic anchors survive relocation

Emerald is the cleanest Gen III proof. Physical addresses vary heavily by language, while semantic gameplay tables remain identical across all six unique language builds: species parameters, battle move parameters, item numeric fields, trainer parties, and main wild-encounter data. The Game Freak ROM API header provides stable semantic pointers even when layout shifts.

Therefore the master patch architecture should use `semantic_id -> per-ROM address/pointer/record schema`, never `English address -> copy everywhere`.

### 4. Asset reuse is very high even when layout differs

Emerald retains thousands of identical decompressed LZ77 assets across languages, and essentially all Pokémon front/back graphics match; the main regional Pokémon-asset exception found is Jynx palette/icon data.

Generation IV also contains large exact-reuse islands across DPPt/HGSS despite major filesystem and code-layout evolution. HGSS even retains DPPt/PBR-compatible resource bundles alongside its expanded main resources.

### 5. Version differences are increasingly data-packaged

HeartGold and SoulSilver both contain Gold and Silver normal encounter archives; runtime code selects the appropriate version data. Their named filesystem differences are concentrated in a tiny set of Pokédex/location/Headbutt resources even though ARM9/overlay code differs much more broadly.

Black/White pushes this further: both ROMs contain 54,054 NARC members, of which 53,988 are identical and only 66 differ. The major confirmed version-data differences are concentrated in encounter data, a species-indexed seasonal/location table, title resources, and version-specific help/manual graphics.

## Source-hygiene findings

### Duplicates and aliases

- Red contains an English copied filename in addition to the original; canonicalization must be hash-based.
- Yellow contains `.gb`/`.gbc` filename aliases for the same localized builds; 14 physical files reduce to 9 unique binaries in the forensic census.
- Emerald has two English filenames that are byte-identical; six unique binaries are used for semantics.

### Debug / modified images

- Ruby German Debug is a real distinct build, not a renamed retail ROM; it differs from German retail Rev0 by millions of bytes and must remain a separate provenance class.
- `Pokemon_Another_Gold+(K).GBC` is kept outside the official retail Gold census until independently identified; it must never contaminate official baseline comparisons.

### FireRed English tail anomaly

The two project English FireRed files differ from recognized canonical retail hashes only at the final two file bytes. Replacing those bytes with `FF FF` reproduces the canonical hashes exactly. The workspace ROMs remain untouched; canonical normalization is analysis metadata only.

## Coverage gaps discovered against the current Library

### Sapphire report is stale

The existing Sapphire audit covers 9 files and states that Spanish retail revisions are missing. The current Library now contains Spanish Sapphire Rev0 and Rev1. Therefore Sapphire must be rerun against the current input set; the old 9-ROM report remains historically valid only for its original input snapshot.

### Generation IV report does not cover every currently visible NDS input

The Stage 2 census targets Diamond USA, Pearl USA, Platinum Korea, HeartGold Korea, and SoulSilver Korea. The current Library also contains a `Pokemon_Platinum_USA_NDS-XPA.nds` input. That USA Platinum image needs to be added to the next Gen IV census rather than silently treated as covered by the Korean Platinum analysis.

### Crystal remains shallower than Silver

Crystal currently has a solid 7-ROM identity/revision baseline (JP, EN Rev0, EN RevA, DE, FR, IT, ES), but not yet the same symbol/table/string-level census reached by the strongest Silver/Green/Emerald work.

### FireRed is identity/revision-deep but not yet semantic-table-deep

FireRed Stage 1 confirms eight builds and trustworthy hashes/revision relationships, but still needs full table/text/map/script/graphics/save semantic mapping.

## Priority queue

1. Re-run Sapphire against all currently present builds, including Spanish Rev0/Rev1.
2. Extend Generation IV census to the currently present Platinum USA image and compare it with Platinum KR at filesystem/NARC/record/text-resource levels.
3. Promote Crystal from identity baseline to full 128-bank + pointer/table/string/font/map/event census.
4. Promote FireRed from Stage 1 identity/revision census to semantic table and localization-layout census.
5. Extend Gold beyond bank-level census to the same semantic layer as Silver; keep `Another_Gold+(K)` quarantined as modified/unknown provenance.
6. Build one cross-generation semantic registry for Pokémon/move/item/trainer/map/text/font/graphics tables with per-build addresses, schemas, hashes, and provenance.

## Engineering rule established by the census

The safe universal model is:

`ROM identity -> revision/region class -> structural container -> semantic object/table/function -> per-build address/schema -> patch/change`

The unsafe model is:

`one known ROM offset -> assume every language/revision matches`

All future analysis and localization/expansion work should follow the first model.

## Existing repository anchors

- `GENERATION-I/RED/analysis/`
- `GENERATION-I/GREEN/analysis/`
- `GENERATION-I/BLUE/`
- `GENERATION-I/YELLOW/`
- `GENERATION-II/GOLD/analysis/`
- `GENERATION-II/SILVER/ANALYSIS/`
- `GENERATION-II/CRYSTAL/analysis/`
- `GENERATION-III/RUBY/ANALYSIS/`
- `GENERATION-III/SAPPHIRE/`
- `GENERATION-III/EMERALD/`
- `GENERATION-III/FIRERED/MULTI-REGION/ALL-REVISIONS/`
- `GENERATION-III/LEAF-GREEN/`
- `GENERATION-IV/analysis/rom-census/`
- `GENERATION-V/BLACK-WHITE-EUR/`

This cross-generation report contains no ROM bytes.