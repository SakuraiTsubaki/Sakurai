# Public GitHub crawl — 2026-09-14

This is a discovery ledger, not a trust list. Every entry must be inspected before source or data is imported.

## Query family: `pokegreen`

Primary upstream candidate:

- `Narishma-gb/pokegreen` — Japanese Red/Green byte-exact reconstruction anchor.

Other repositories surfaced by the first repository-name crawl and retained for inspection:

- `JcFerggy/pokegreen`
- `Mirepo/pokegreen`
- `MDTravisYT/pokegreen`
- `SeafarersWind/pokegreen`
- `pokegreen/pokegreen`
- `GB-Recomp/pokegreen`
- `SteppoBlazer/pokegreen-crysaudio`
- `msmrrenda/pokegreen_syms`
- `Remoraid/pokegreen_ultra`
- `funnymonke0/pokegreen`
- `Masaru2/pokegreen`
- `GoddessMaria15/pokegreen`
- `ChainSwordCS/pokegreen`
- `Rangi42/pokegreen`

Status: **pending individual inspection** unless classified below. Search hits can be forks, hacks, experiments, symbol mirrors, recompilation projects, or unrelated naming collisions.

## `Narishma-gb/pokegreen` branch census

Branches visible on 2026-09-14:

- `master` — retail reconstruction baseline.
- `symbols` — generated/research symbol branch; valuable for address/symbol cross-reference.
- `debug_mew` — **derivative/mock-up**, not a recovered retail/debug ROM baseline. Head commit explicitly describes itself as `Mock-up debug build (Green Rev.0)` and adds a reconstructed debug configuration.
- `sgb_mon` — **derivative/WIP modification**, not retail baseline. Head commit adds a dynamic SGB border using Pokémon Pinball images.

Rule: data from `debug_mew` and `sgb_mon` cannot be described as original retail or recovered development data without separate primary evidence.

## Retail and official-re-release targets exposed by upstream

`Narishma-gb/pokegreen` master declares byte-exact targets for Japanese Red/Green V1.0 and V1.1 and also exposes two Virtual Console patch targets:

- `DMGAPAJ1.B90.patch` SHA-1 `df7aabbfdaffd2d257c526cec20c279974526791`
- `DMGAPBJ1.B91.patch` SHA-1 `d1ffec642f924ef1b8a7e05c05f1e5c5becf700d`

The repository includes:

- `vc/pokered11.patch.template`
- `vc/pokegreen11.patch.template`
- `vc/vc_constants.asm`

These are a high-priority source for separating original cartridge Rev 1 behavior from Japanese 3DS Virtual Console modifications.

## Cross-source technical anchors discovered in this crawl

`pret/pokered` contains directly inspectable source for domains that will later be compared back to Japanese Red/Green rather than copied blindly:

- `constants/charmap.asm` — Western character/control-code map.
- `engine/menus/save.asm` — save logic / `SaveGameData`.
- `home/serial.asm` — serial byte-exchange primitives.
- `engine/link/cable_club.asm` — trade/battle data exchange.
- `home/random.asm` and `engine/math/random.asm` — RNG paths.
- `data/wild/probabilities.asm` — encounter-slot probabilities.

These paths prove that text encoding, save, link and RNG research can be grounded in executable source, but their addresses/semantics must be revalidated for Japanese Aka revisions.

## External public-source families surfaced in wave 2

First-party:

- Pokémon official Red/Green page: `https://www.pokemon.co.jp/game/other/gb-rg/`
- Game Freak works archive: `https://www.gamefreak.co.jp/works/pokemon/page/2/`
- Nintendo original Red/Green page: `https://www.nintendo.co.jp/n02/dmg/apajapbj/index.html`
- Nintendo 3DS VC Red page: `https://www.nintendo.com/jp/titles/50010000038658.html`

Asset/map archives (secondary; provenance and accuracy must be checked against source data):

- The Spriters Resource Red/Blue: `https://www.spriters-resource.com/game_boy_gbc/pokemonredblue/`
- VGMaps Game Boy/Game Boy Color atlas: `https://www.vgmaps.com/`

Technical secondary/lead sources:

- Bulbapedia Generation I character encoding: `https://bulbapedia.bulbagarden.net/wiki/Character_encoding_in_Generation_I`
- `Phasip/PokemonLinkHack`: `https://github.com/Phasip/PokemonLinkHack` — link-protocol/exploit research lead; not a retail reconstruction baseline.
- Helix Chamber Red/Green prototype coverage: `https://helixchamber.com/` — historical lead; underlying primary material must be tracked separately.

## Crawl rules

1. Repository names are not evidence of target identity.
2. Forks/branches are retained even when derivative because they may contain old symbols, comments, lost research, or citations.
3. A derivative source can locate a lead but cannot override byte-exact reconstruction or first-party evidence.
4. Every inspected repository must eventually receive one of: `PRIMARY`, `CORROBORATING`, `DERIVATIVE`, `HISTORICAL`, `IRRELEVANT`, `HOLD`.
5. Crawl is recursive: README links, history, forks, issues, PRs and external citations become new queue entries.
