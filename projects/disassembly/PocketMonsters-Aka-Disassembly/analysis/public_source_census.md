# Public source census — research restart

Date started: 2026-09-14

## Research rule

This census starts the Generation I research again from public evidence. No local retail ROM is assumed to be available. Existing repository material is evidence to re-check, not an automatically trusted conclusion.

The governing scope is **Japanese releases as the historical origin point, followed by an exhaustive survey of every publicly documented regional, language, revision, and official re-release variant**. Findings must be cross-checked before they are promoted into reconstruction source.

This file is a living census. Its existence is **not** a claim that the public-source search is complete. Search continues recursively through repositories, forks, branches, tags, commits, issues, pull requests, wikis, archived pages, citations, mirrors, manuals, technical databases, asset archives, glitch research, and official material until no material new source families are being found.

## Evidence classes

- **A1** — byte-exact/public reconstruction or first-party official material.
- **A2** — independent technical database or documentation corroborated by A1 material.
- **B** — specialist secondary research useful for differences, bugs, unused content, or historical context.
- **C** — derivative projects, old forks, hacks, translations, or unverified material; useful for leads only.
- **Rejected/hold** — misleading, contradictory, ROM-distribution-focused, or insufficiently attributable material.

## A1 — reconstruction anchors

### Japanese Red / Green

- Narishma-gb/pokegreen — https://github.com/Narishma-gb/pokegreen
  - Builds Japanese Red V1.0 / V1.1 and Green V1.0 / V1.1.
  - Published SHA-1 targets:
    - Red V1.0 `0623ad12f48c259447980d68bd85ddbf8204b2cd`
    - Red V1.1 `ef74c79cded14204ac79e77f4964d9cb25003120`
    - Green V1.0 `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
    - Green V1.1 `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`
  - Primary public reconstruction anchor for Japanese Aka/Midori revision comparison.

### International Red / Blue lineage

- pret/pokered — https://github.com/pret/pokered
  - Builds English USA/Europe Red and Blue byte-exact targets and documents VC patch artifacts/debug build.
  - Red SHA-1 `ea9bcae617fdf159b045185467ae58b2e4a48b9a`.
- einstein95/pokered-de — https://github.com/einstein95/pokered-de
  - German Red/Blue disassembly; verify all hashes/branches independently before importing data.
- einstein95/pokered-fr — https://github.com/einstein95/pokered-fr
  - French Red/Blue disassembly.
  - Red SHA-1 `47a7622fa30e6402a3891fe65b3a930bf9bd7aec`.
- einstein95/pokered-es — https://github.com/einstein95/pokered-es
  - Spanish Red/Blue disassembly.
  - Red SHA-1 `fc17c5b904d551b1b908054ccd1c493f755f832a`.
- einstein95/pokered-it — https://github.com/einstein95/pokered-it
  - **HOLD / not accepted as Italian reconstruction yet.** Repository exists, but the current default-branch README and `roms.md5` inspected on 2026-09-14 describe German Rote/Blaue builds, not Italian Rossa/Blu. Treat as a lead requiring history/commit investigation, not as proof of an Italian byte-exact disassembly.

## A1 — official Nintendo material

- Pocket Monsters Red/Green original Nintendo page — https://www.nintendo.co.jp/n02/dmg/apajapbj/index.html
  - Original release date, pricing, two-version concept, communication warning, contemporary presentation.
- Pocket Monsters Blue original Nintendo page — https://www.nintendo.co.jp/n02/dmg/apej/index.html
  - Officially documents Blue-specific Pokémon artwork and Pokédex-text changes and release history.
- Pocket Monsters Pikachu original Nintendo page — https://www.nintendo.co.jp/n02/dmg/apsj/index.html
  - Official feature and compatibility reference for the next branch in the Generation I lineage.
- Nintendo 3DS Virtual Console Red page — https://www.nintendo.co.jp/titles/50010000038658
- Nintendo 3DS Generation I feature page — https://www.nintendo.co.jp/kids/sp/160224/pokemon/index.html

## A2 — technical maps / identity corroboration

- Data Crystal: Pokémon Red and Blue — https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue
- Data Crystal ROM map — https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue/ROM_map
- Data Crystal RAM map — https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue/RAM_map
  - Important warning: international and Japanese addresses differ; addresses are never transplanted without version verification.
- Data Crystal notes / map-object formats — https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue%3ANotes
- BizHawk Game Boy game database (`TASEmulators/BizHawk`, `Assets/gamedb/gamedb_gb.txt`) — independent release-hash identity corroboration.
- No-Intro metadata mirrors may be used for identity cross-checking only; ROM downloads are outside project scope.

## B — specialist research

- Bulbapedia: Pokémon Red and Green Versions — https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Red_%28Japanese%29
  - Useful revision-history index; every technical claim must be checked against disassembly/code when possible.
- Glitch City Wiki: natural Generation I glitches — https://glitchcity.wiki/List_of_natural_glitches_in_Generation_I
- Glitch City Laboratories archive: unused-content project — https://archives.glitchcity.info/forums/board-107/thread-6347/page-0.html
- Helix Chamber / Capsule Monsters source index — https://helixchamber.com/media/capsule-monsters/
  - Historical/development-source lead index; each cited primary source must be followed separately.

## C — derivative / historical leads

- luckytyphlosion/pokered-jp — https://github.com/luckytyphlosion/pokered-jp
  - Historical Japanese-focused repository name, but current README visible publicly still describes UE Red/Blue outputs. Use commit history/source fragments as leads, not as a modern canonical baseline.
- digita-LUNA/pokejp — https://github.com/digita-LUNA/pokejp
  - Restoration/translation project derived from existing disassemblies; useful for locating Japanese-vs-international asset differences, not an original retail baseline.
- Masaru2/pokejp — https://github.com/Masaru2/pokejp
  - Modified/debug derivative; lead source only.

## First-pass findings that change prior assumptions

1. Japanese Red has two publicly reconstructed retail revisions (V1.0 and V1.1), so revision-specific code/data must stay separate.
2. Western Red is not represented only by English: dedicated public German, French, and Spanish disassembly families are visible and must be surveyed independently.
3. A repository named `pokered-it` cannot be trusted by name alone; its current default-branch metadata points at German builds. Repository identity and target identity must be verified separately.
4. Official Nintendo pages are usable first-party evidence for release chronology and explicitly advertised version differences.

## Search frontier — mandatory next waves

- All forks, branches, tags, commit histories, issues and PRs of the A1 repositories.
- Italian Red/Blue byte-exact reconstruction search and historical state of `pokered-it`.
- All known revision/hash databases and cartridge/header catalogs.
- Original manuals, package/back-cover scans, official guide material, Nintendo/Game Freak interviews and archived official webpages.
- Complete sprite, trainer, overworld, tileset, UI, font, SGB-border and map archives; deduplicate and provenance-check every asset.
- Music/SFX/cry sequence research and audio-engine documentation.
- Text dumps, charmaps, control-code documentation and localization research for every language.
- Link-cable, save/SRAM, battle-engine, field-engine and RNG research.
- Unused/debug/garbage/padding data, beta remnants and glitch research.
- Virtual Console patch differences and official re-release behavior.

Every newly found source must be recorded here or in a more specific repository manifest with URL, target release(s), evidence class, coverage, conflicts, and verification status.
