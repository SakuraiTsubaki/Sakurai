# Generation VII Decompilation Matrix

This document tracks the six Generation VII main-series decompilation targets as separate projects while defining their required cross-version comparisons.

## Targets

| Family | Game | Platform | Executable baseline | Pair comparison | Current bootstrap |
| --- | --- | --- | --- | --- | --- |
| Alola | Pokémon Sun | Nintendo 3DS | ExHeader + ExeFS `.code` | Sun ↔ Moon | Phase 2 tooling ready; local target data pending |
| Alola | Pokémon Moon | Nintendo 3DS | ExHeader + ExeFS `.code` | Moon ↔ Sun | Phase 2 tooling ready; local target data pending |
| Alola | Pokémon Ultra Sun | Nintendo 3DS | ExHeader + ExeFS `.code` | Ultra Sun ↔ Ultra Moon | Phase 2 tooling ready; local target data pending |
| Alola | Pokémon Ultra Moon | Nintendo 3DS | ExHeader + ExeFS `.code` | Ultra Moon ↔ Ultra Sun | Phase 2 tooling ready; local target data pending |
| Let's Go | Pokémon: Let's Go, Pikachu! | Nintendo Switch | ExeFS NSO0 modules | Pikachu ↔ Eevee | Phase 2 tooling ready; local target data pending |
| Let's Go | Pokémon: Let's Go, Eevee! | Nintendo Switch | ExeFS NSO0 modules | Eevee ↔ Pikachu | Phase 2 tooling ready; local target data pending |

## Common pipeline

1. Identify exact target revision/update/language/region from evidence.
2. Generate complete extracted-tree inventory with path, size, and SHA-256.
3. Generate executable memory/file map using the platform-specific parser.
4. Generate complete RomFS structural classification.
5. Compare paired versions with `tools/compare_gen7_inventories.py`.
6. Establish function/data/resource labels only from verified evidence.
7. Reconstruct source progressively and record validation level.

## 3DS lane

Repositories:

- `PocketMonsters-Sun-Decompilation`
- `PocketMonsters-Moon-Decompilation`
- `PocketMonsters-UltraSun-Decompilation`
- `PocketMonsters-UltraMoon-Decompilation`

Required tools in each target repository:

- `tools/inventory_extracted_tree.py`
- `tools/inspect_3ds_exheader.py`
- `tools/map_3ds_code_layout.py`
- `tools/classify_romfs.py`

Sun/Moon and Ultra Sun/Ultra Moon are separate comparison pairs. Ultra targets must not be treated as address-compatible replacements for Sun/Moon without verification.

## Switch lane

Repositories:

- `PocketMonsters-LetsGoPikachu-Decompilation`
- `PocketMonsters-LetsGoEevee-Decompilation`

Required tools in each target repository:

- `tools/inventory_extracted_tree.py`
- `tools/inspect_nso.py`
- `tools/map_nso_modules.py`
- `tools/classify_romfs.py`

`main`, `rtld`, `sdk`, `subsdk*`, and any additional NSO0 modules are inventoried independently. Let's Go does not inherit 3DS executable-layout assumptions.

## Evidence policy

Use these labels consistently:

- **Unverified** — planned or hypothesized only.
- **Observed** — directly confirmed in target data.
- **Reproduced** — extraction/parsing/behavior can be recreated.
- **Matched** — reconstructed output is verified against the intended target.

Unknown values remain unknown. Do not invent offsets, function names, structures, file formats, or version differences.

## Repository policy

ROM/cartridge images, encrypted packages, keys, and redistributed proprietary executable payloads are not committed. Analysis metadata, hashes, reconstructed source, documentation, manifests, scripts, tests, patches, and independently created work products may be committed according to project policy.
