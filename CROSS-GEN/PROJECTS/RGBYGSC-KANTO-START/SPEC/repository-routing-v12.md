# RGBY カントー地方 -> GSC — repository routing (v12)

## Canonical project coordinate

`CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`

Human-facing project name: **RGBY カントー地方 -> GSC**.

This project is cross-generation because Generation I RED/GREEN/BLUE/YELLOW material is intentionally integrated into a Generation II GOLD/SILVER/CRYSTAL runtime. Korean Silver is the runtime anchor, but the project is not owned solely by `GEN-02/SILVER/PROJECTS/`.

## One-project-home rule

All **project-owned work products** must be discoverable from the canonical project root above. Source release identity remains under:

`GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/CART/<RELEASE-ID>/`

Exact observed images are identified below releases as `DUMPS/DUMP-SHA256-.../` metadata, but project-specific analyses, specifications, mappings, conversions, implementation, patches, build metadata and verification must not exist only at release coordinates or in migration quarantine.

## Sakurai

Sakurai owns the knowledge/control subset: identity/provenance, hashes, headers, direct ROM observations, bank/pointer research, reverse engineering, comparisons, specifications, localization research, mapping tables, research tools and verification evidence.

## Tsubaki

Tsubaki is the complete eligible non-ROM superset and production side: everything eligible from Sakurai plus extraction plans, generated catalogs, ROM-derived semantic working assets, normalized/converted assets, Gen I → Gen II conversion products, implementation data, relocation tables, patches, build recipes/logs, production tools and production verification.

## Binary rule

Complete playable ROM images are excluded. Project source, analysis, documentation, scripts, patches, manifests, hashes, logs, tests, extracted/reconstructed graphics, maps, text, fonts, audio, tables and other non-ROM artifacts are versioned.

## V migration rule

A version upgrade is incomplete until every unique project artifact from the previous live project path has either:

1. been carried into the new live project structure, or
2. been preserved as an explicit versioned snapshot **inside this project root**.

`INFRA/MIGRATION/` and Git history are evidence, not acceptable sole locations for still-relevant project work.
