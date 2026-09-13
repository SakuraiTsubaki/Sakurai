# RGBYGSC Kanto Start — repository routing (v10)

## Canonical project coordinate

`CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`

The project is cross-generation because Generation I RED/GREEN/BLUE/YELLOW material is intentionally integrated into a Generation II GOLD/SILVER/CRYSTAL runtime. It must not be owned solely by `GEN-02/SILVER/PROJECTS/` even though Korean Silver is the runtime anchor.

## Source release coordinates

Every official source remains owned by its game under:

`GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/CART/<RELEASE-ID>/`

Exact observed images are content-addressed below the release as:

`DUMPS/DUMP-SHA256-<FIRST-16-UPPERCASE-HEX>/`

Project manifests reference those coordinates; the project never redefines release identity.

## Sakurai

Sakurai is the knowledge/control plane and owns identity/provenance, hashes, headers, bank and pointer research, reverse engineering, map/event/tileset/sprite structure analysis, comparisons, specifications, mapping tables, research tools and verification evidence.

## Tsubaki

Tsubaki is the production/data plane and owns source references, extraction plans, generated catalogs, ROM-derived working assets, normalized/converted assets, Gen I -> Gen II conversion products, implementation data, relocation tables, patches, build recipes/logs, production tools and production verification.

The operating rule is: **ROM images are excluded; generated non-ROM project artifacts are versioned.** A raw set of bank slices that is merely a lossless ROM re-encoding is not treated as a useful extracted asset. Semantic assets such as maps, tilesets, tile graphics, sprites, text, scripts, events, tables and audio data are tracked as they are identified and materialized.

## Legacy v9 path

`CROSS-GEN/TARGET/RGBYGSC-KANTO-START/` is migration-only. New work must never be added there. After all unique files are represented in v10, the legacy path is removed from the current tree; Git history remains the archive.
