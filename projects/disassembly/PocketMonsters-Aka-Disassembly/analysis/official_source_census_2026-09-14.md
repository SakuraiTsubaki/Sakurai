# Official-source census — Pocket Monsters Aka / Pokémon Red

Research restart date: **2026-09-14**

This ledger records first-party/public-publisher evidence separately from disassemblies and community technical references. The current research environment has no local retail ROM, so official material is used to establish release identity, documented behavior, peripherals, and official re-release changes before technical reconstruction claims are accepted.

## Evidence grades

- **A1** — Nintendo / The Pokémon Company first-party product page or official electronic manual.
- **A2** — other official Nintendo / Pokémon promotional or historical material.
- **B** — reproducible public disassembly/source reconstruction with release hashes.
- **C** — specialist technical reference/wiki; useful for discovery and cross-checking, but not accepted over A/B evidence when they conflict.

## Verified official sources

### Original Japanese Red / Green

**Source:** Pokémon official site, 「ポケットモンスター 赤・緑」  
https://www.pokemon.co.jp/game/other/gb-rg/

**Grade:** A1

Verified statements:

- Japanese `ポケットモンスター 赤・緑` release date: **1996-02-27**.
- Publisher: Nintendo.
- Platform: Game Boy, with the official page also listing later Game Boy-family compatibility.
- Officially documented Red/Green difference: species appearance and encounter-rate differences, including version-exclusive Pokémon.
- Link Cable is listed as a supported peripheral.

This page is the historical release anchor for Aka/Midori. International Red must not be used to overwrite Japanese-origin behavior or terminology.

### 3DS Virtual Console release family

**Sources:**

- Pokémon official VC site: https://www.pokemon.co.jp/ex/VCAMAP/
- Nintendo 3DS product page for Red: https://www.nintendo.co.jp/titles/50010000038658
- Nintendo official electronic manual: https://www.nintendo.co.jp/data/software/manual/manual_CTRNRCPA.pdf

**Grade:** A1

Verified statements:

- Japanese 3DS Virtual Console distribution began **2016-02-27**.
- The official site groups `赤・緑・青・ピカチュウ` as the four Generation I VC titles.
- 3DS local wireless replaces the original physical-link use for supported trade/battle communication.
- Nintendo explicitly warns that VC behavior/expression can differ from the original game.
- The VC release disables normal VC suspend-state and full-save-backup features for this software family.
- The official manual describes one save file and documents wireless Trade Center / Colosseum behavior.
- The manual states that the four versions share the same story while Pokémon species and encounter rates differ.

These VC builds are therefore a **separate official revision family**, not interchangeable evidence for the original cartridge binaries.

## Research consequences

1. Cartridge Red Rev 0 / Rev A remain the origin targets for Japanese Aka reconstruction.
2. 3DS VC changes must be catalogued separately as official re-release modifications.
3. Any claimed Red/Green difference beyond the officially documented encounter/species split still requires code/data verification.
4. Communication behavior must be split into original Link Cable implementation versus 3DS wireless emulation/patch behavior.
5. Peripheral features absent from VC must not be inferred to have been removed from the original cartridge.

## Official-source search frontier

Still to locate, preserve, and index where publicly accessible:

- Japanese 1996 cartridge manual scans / official instruction material.
- Japanese package front/back/spine and inserts for Rev 0 / Rev A if revision-identifiable.
- Nintendo/Game Freak contemporary press or retailer material establishing revision chronology.
- Official strategy books and Nintendo-authorized guides, clearly separated from ROM truth when they contain mistakes.
- Official 3DS download-card special-edition inserts and town-map material.
- Any first-party errata or support pages for link compatibility and peripheral restrictions.
- Official documentation for Pokémon Bank / Poké Transporter transfer behavior from Generation I VC.

## Rule

An official statement documents what Nintendo / Pokémon said or supported; it does **not** automatically prove byte-level implementation. Where the official manual and ROM/disassembly behavior differ, both are retained and the implementation is recorded separately.
