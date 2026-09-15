# Generation III — Full-Ecosystem Decompilation

This directory is the generation-wide coordination layer for Pokémon Generation III reverse engineering and source reconstruction.

## Scope

The project scope is the complete Generation III ecosystem, not only Ruby/Sapphire/Emerald.

### Core GBA titles
- Pokémon Ruby
- Pokémon Sapphire
- Pokémon Emerald
- Pokémon FireRed
- Pokémon LeafGreen

### GameCube titles and software
- Pokémon Colosseum
- Pokémon XD: Gale of Darkness
- Pokémon Box Ruby & Sapphire
- Pokémon Channel when it directly participates in Generation III distribution/link workflows

### Peripherals, distribution, and communication
- Nintendo e-Reader / e-Cards
- Game Boy Advance Wireless Adapter
- GameCube–Game Boy Advance link cable workflows
- Bonus Discs and distribution discs
- Official event cartridges/devices and downloadable event payloads
- Mystery Event / Mystery Gift
- Eon Ticket, AuroraTicket, MysticTicket, Old Sea Map and related event data

## Phase 1

All tracks begin with source identity and evidence capture before interpretation:

1. identify exact platform / product / region / language / revision;
2. hash the user-supplied original source media locally;
3. inventory executable containers, filesystem/data regions, scripts, assets, and protocol payloads;
4. record observed facts separately from hypotheses;
5. derive source structures without committing commercial ROM/disc images;
6. progress toward reproducible rebuilds and binary comparisons where technically applicable.

## Active files

- `workstreams.json` — generation-wide workstream status
- `scope_matrix.csv` — title/platform/region/revision coverage matrix
- `evidence_status.json` — common evidence levels and gates
- `communications.json` — link, wireless, event, and external-distribution tracks
- `unused_data.json` — unused/dummy/debug-data investigation registry
- `tools/gc_baseline.py` — first-pass GameCube disc/image inventory tool
- `tools/payload_baseline.py` — generic event/e-Reader/distribution payload inventory tool

## Repository policy

Original commercial ROMs, disc images, and copyrighted distribution binaries remain outside GitHub. GitHub contains reconstructed source, tools, manifests, derived metadata, documentation, hashes, patches where appropriate, and original project-created assets.
