# Pokémon Generation III — Full Ecosystem Disassembly

This workspace coordinates **disassembly and low-level reverse engineering across the complete Generation III ecosystem**, not only the five GBA main-series cartridges.

## Scope rule

Generation III is treated as one connected technical ecosystem. Nothing is excluded merely because it is a spin-off, peripheral, distribution medium, regional feature, revision, unused resource, or external event mechanism.

### Core GBA titles

- Pokémon Ruby
- Pokémon Sapphire
- Pokémon Emerald
- Pokémon FireRed
- Pokémon LeafGreen

Dedicated repositories already exist and are active:

- `SakuraiTsubaki/PocketMonsters-Ruby-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Sapphire-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Emerald-Disassembly`
- `SakuraiTsubaki/PocketMonsters-FireRed-Disassembly`
- `SakuraiTsubaki/PocketMonsters-LeafGreen-Disassembly`

### GameCube software

- Pokémon Colosseum
- Pokémon XD: Gale of Darkness
- Pokémon Box Ruby & Sapphire
- Pokémon Channel where it participates in Generation III distribution/link behavior

### Peripherals and link systems

- Nintendo e-Reader / e-Card payloads and protocols
- Game Boy Advance Wireless Adapter
- GameCube–Game Boy Advance Link Cable protocols
- Mystery Event / Mystery Gift transport and save interactions

### Distribution ecosystem

- Bonus Discs and other official distribution discs
- Official event cartridges and distribution devices
- Eon Ticket
- AuroraTicket
- MysticTicket
- Old Sea Map
- other verified Generation III official distribution payloads

## Platform-specific disassembly rules

### GBA

Use the actual ARM7TDMI architecture and distinguish ARM code, Thumb code, literal pools, structured data, scripts, graphics, audio, maps, compressed resources, save-related structures, and unknown ranges. Do not impose the 16 KiB bank model used by GB/GBC projects.

### GameCube

Treat each disc and revision as an independently verified target. Inventory disc filesystem layout first, then reconstruct executable and module structure using PowerPC/Gekko code, DOL/REL boundaries where applicable, data sections, archives, scripts, assets, save structures, and GBA-link components. Do not copy assumptions from the GBA layout.

### e-Reader / peripherals / distribution hardware

Separate executable code, firmware or device-side behavior where legally and technically available, card/payload data, protocol framing, transfer routines, save flags, region locks, checksums, cryptographic or encoding layers, and title-side handlers. Protocol reconstruction is tracked alongside binary disassembly when no standalone executable image is available.

## Verification levels

Every claim and recovered region must be marked as one of:

1. **Hypothesis** — plausible but not yet demonstrated.
2. **Observed** — directly observed in verified source media/data.
3. **Reproduced** — behavior or structure independently reproduced.
4. **Matched** — rebuilt output is byte-identical or otherwise meets the target's exact matching criterion.

Region, language, and revision are never silently merged. Unknown or unavailable targets remain explicitly listed as pending instead of being treated as nonexistent.

## Repository policy

Original ROMs, optical-disc images, firmware dumps, event cartridge dumps, raw copyrighted distribution payloads, and other source-media binaries are **never committed**. They remain local-only. GitHub contains reconstructed source, symbols, scripts, metadata, manifests, hashes, analyses, patches, and distributable project assets.

## Active phase

**Phase 1 — complete target inventory and binary/container map**

For every scope item:

1. enumerate official regions, languages, releases, and revisions;
2. record verifiable hashes and media/header metadata without committing source media;
3. map executable/container/filesystem boundaries;
4. identify code/data/script/asset/link/distribution ranges;
5. create reproducible extraction and verification tooling;
6. move into sequential disassembly only after the target identity is fixed.

See `scope_matrix.csv` and `workstreams.json` for the active generation-wide queue.
