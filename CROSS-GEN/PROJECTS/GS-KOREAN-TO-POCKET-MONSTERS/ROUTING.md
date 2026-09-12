# GS Korean -> Pocket Monsters — v10 routing

Canonical project root: `CROSS-GEN/PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/`.

Canonical source releases live at `GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/CART/<RELEASE-ID>/`. Exact supplied images are observations at `DUMPS/DUMP-SHA256-<16HEX>/OBSERVATION.json`.

All 23 supplied images are independently registered. Japanese sources are translated directly from Japanese, English sources directly from English, and Korean Gold/Silver are both modernization targets and the primary Korean implementation references. Regional localization and revision differences are preserved.

Sakurai is the knowledge/control plane: identity, hashes, headers, reverse engineering, text/pointer/UI/SRAM analysis, translation crosswalks, specifications, reports, tools and verification. Tsubaki uses the same release/dump/project IDs for source references, extraction plans, catalogs, ROM-derived production assets, normalized/converted resources, implementation data, patches, builds and production verification.

Legacy v9 `SOURCE/`, `TARGET/`, and `CROSS-GEN/TARGET/` paths are read-only migration inputs. New work is v10 only. ROM binaries are never committed.
