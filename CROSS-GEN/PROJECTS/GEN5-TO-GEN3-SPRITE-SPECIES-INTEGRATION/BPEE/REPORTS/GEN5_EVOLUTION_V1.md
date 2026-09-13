# BPEE Generation V Evolution Integration V1

## Status

This phase integrates the BW evolution corpus into the current Emerald BPEE Generation V species prototype while preserving original Emerald evolution behavior first.

- BW source: `/a/0/1/9`
- archive: 668 members, 42 bytes/member
- member layout: 7 × `(method u16, parameter u16, target National species u16)`
- edges with source or target National #387–649: 136
- active in V1: 113
  - native-table: 103
  - extension hook: 10
- pending dependencies: 23
- final static verification: 38/38
- runtime emulator test: not yet performed in this environment

## Critical correction: retail evolution ABI

The retail BPEE binary addresses five 8-byte evolution slots per species, so the runtime species stride is 40 bytes. An earlier prototype had assumed a 30-byte stride from the three `u16` fields alone. That prototype table is superseded.

V1 reconstructs the table at ROM `0x1812000` / GBA `0x09812000`, with 703 species × 40 bytes. Internal species 0–411 are copied byte-for-byte from the retail Emerald ROM. Six confirmed retail table literals are redirected to the corrected table, and the obsolete `0x090E83F4` pointer has no remaining references in the first 16 MiB.

Representative preserved vanilla records are explicitly checked for Bulbasaur, Eevee, Wurmple and Nincada.

## Critical correction: National ↔ internal IDs

Generation III Hoenn species are not a simple National+25 ordering. V1 therefore inverts the actual internal→National table already present in the target ROM. Old/reserved alias slots are skipped for new National #387–649 so the canonical project range remains internal 440–702.

Confirmed examples:

- #252 Treecko → internal 277
- #290 Nincada → internal 301
- #351 Castform → internal 385
- #358 Chimecho → internal 411
- #386 Deoxys → internal 410
- #387 Turtwig → internal 440
- #649 Genesect → internal 702

This fixes real cross-generation targets. In particular, Budew→Roselia now targets Roselia #315 / internal 363, and Chingling→Chimecho targets #358 / internal 411. Any earlier Evolution V1 ROM using a blanket National+25 Hoenn conversion must not be used.

## Runtime policy

`GetEvolutionTargetSpecies` is wrapped rather than replaced semantically:

1. Run the original Emerald routine first.
2. If Emerald returns a valid evolution, return it unchanged.
3. Only when vanilla returns none, evaluate supported Gen V extension methods.
4. Respect Everstone / prevent-evolution hold effects before extension checks.

This preserves original 1–386 evolution behavior and adds Generation V-dependent branches without displacing it.

## Active native methods

- friendship
- friendship day/night using current Emerald RTC semantics
- level
- trade
- evolution item when the required stone already exists in Emerald: Sun, Moon, Fire, Thunder, Water, Leaf

## Active extension-hook methods

Ten edges are currently handled by the ARM extension:

- level while knowing an existing Gen III move
  - Lickitung→Lickilicky: Rollout
  - Tangela→Tangrowth: AncientPower
  - Yanma→Yanmega: AncientPower
  - Piloswine→Mamoswine: AncientPower
  - Bonsly→Sudowoodo: Mimic
  - Mime Jr.→Mr. Mime: Mimic
- gendered level evolution
  - Burmy→Wormadam
  - Burmy→Mothim
  - Combee→Vespiquen
- required non-Egg party species
  - Mantyke→Mantine with Remoraid present

## Pending 23 edges

Pending rather than approximated:

- Shiny/Dusk/Dawn Stone and other Gen IV/V item dependencies
- Oval Stone, Razor Claw/Fang and trade-held items
- Karrablast/Shelmet partner-species trade context
- magnetic-field, Moss Rock and Ice Rock location semantics
- Aipom→Ambipom because Double Hit (move 458) is not yet implemented in the Emerald move engine

Exact Generation V time/season semantics are also a later integration phase; friendship day/night currently follows Emerald RTC behavior.

## Binary verification

- hook region: ROM `0x1810000`, 728 bytes
- corrected table: ROM `0x1812000`, 28,120 bytes
- hook source rebuild is byte-identical to the injected binary
- a second complete patch run produces a byte-identical ROM
- patch diff is confined to the declared function stub, six pointer literals, hook allocation and corrected table allocation
- final ROM SHA-1: `c90e3e7504ff9b6a71c21283cf6d525c320b2f07`
- final ROM SHA-256: `36cdd266ec52cc87d8445d582d2d62f40d3d74fee66c9109d39b4de48f379e05`

ROM binaries are intentionally not committed to GitHub.
