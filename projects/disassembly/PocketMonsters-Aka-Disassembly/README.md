# PocketMonsters-Aka-Disassembly

![Status](https://img.shields.io/badge/status-in_progress-yellow)
![Project](https://img.shields.io/badge/project-disassembly-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Complete disassembly and reconstruction project for **Pocket Monsters Aka (Japan)** and the verified international **Pokémon Red** releases.

## Research restart — 2026-09-14

The current research environment has **no local retail ROM images available**. Work therefore proceeds from publicly accessible evidence: public disassemblies and source reconstructions, repository history, official material, technical documentation, maps, graphics, text, audio, release metadata, glitch/unused-data research, archives, and other attributable public sources.

The governing scope is **Japanese releases as the historical origin point, followed by an exhaustive survey of all regional, language, revision, and official re-release variants**. Existing repository claims and earlier analysis are retained as evidence, but are revalidated rather than automatically trusted.

Current restart ledgers:

- [`analysis/public_source_census.md`](analysis/public_source_census.md) — public-source evidence registry and search frontier.
- [`analysis/public_github_crawl_2026-09-14.md`](analysis/public_github_crawl_2026-09-14.md) — repository/branch/fork discovery and classification queue.

Any older wording below that says ROM files were "supplied" records an earlier analysis state and **does not describe the currently available inputs**.

The goal is to reconstruct each supported ROM into editable source form — code, data, text, graphics, audio, maps, scripts, tables, and build metadata — so a clean clone can eventually reproduce every supported build **without requiring a local `baserom.gb`**.

ROM binaries are read-only source references and are never committed.

## Verified source baselines

| Build ID | Release | Size | Banks | Header version | SHA-1 |
|---|---|---:|---:|---:|---|
| `aka-jp-rev0` | Pocket Monsters Aka (Japan) | 512 KiB | 32 | 0 | `0623ad12f48c259447980d68bd85ddbf8204b2cd` |
| `aka-jp-reva` | Pocket Monsters Aka (Japan) Rev A | 512 KiB | 32 | 1 | `ef74c79cded14204ac79e77f4964d9cb25003120` |
| `red-en-ue` | Pokémon Red Version (USA, Europe) | 1 MiB | 64 | 0 | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` |
| `red-de` | Pokémon Rote Edition (Germany) | 1 MiB | 64 | 0 | `87d523fe1a0c548db7c5477b451ddec1eb083c06` |
| `red-it` | Pokémon Versione Rossa (Italy) | 1 MiB | 64 | 0 | `65b97cf8f2f1cff711a6d08c6c894c8ce65ce522` |
| `red-es` | Pokémon Edicion Roja (Spain) | 1 MiB | 64 | 0 | `fc17c5b904d551b1b908054ccd1c493f755f832a` |
| `red-fr` | Pokémon Version Rouge (France) | 1 MiB | 64 | 0 | `47a7622fa30e6402a3891fe65b3a930bf9bd7aec` |

Eight ROM files were supplied for analysis. The additional English copy is byte-identical to `red-en-ue` (same SHA-1 and MD5), so the source set contains **7 unique builds**.

## Reconstruction policy

- Keep all source ROMs read-only and outside Git.
- Never commit original or rebuilt `.gb`/`.gbc` ROM images.
- Recover ROM contents into meaningful, editable disassembly source wherever possible.
- Prefer structured RGBDS assembly, readable text source, PNG graphics, map/block data, audio sequence source, and explicit data tables over opaque byte dumps.
- Raw extraction is only an intermediate reconstruction stage and should be replaced by structured source as analysis progresses.
- Preserve build-specific differences instead of flattening revisions/localizations into one assumed layout.
- Verify completed outputs against the recorded SHA-1 values.
- When sprite/tile/font/UI graphics are recovered, commit the reconstructed image assets too (PNG plus the relevant 1bpp/2bpp conversion source, manifests, palettes/tilemaps where applicable). Graphics work is not considered complete with ASM metadata alone.
- Deduplicate graphics that are byte-identical across revisions/localizations; preserve genuinely different artwork as build-specific assets.

## Current status

Source inventory and header verification are complete for all 7 unique builds. **Bank 00 reconstruction is active.**

See `analysis/bank00/` for verified offsets, revision differences, and range hashes. The active source is linked from `home.asm`.

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Documentation Hub](docs/README.md) | Central entry point for project documentation |
| [Project Status](docs/PROJECT_STATUS.md) | Reconstruction and matching status |
| [Version Coverage](docs/VERSIONS.md) | Supported releases, revisions, sizes, and hashes |
| [Disassembly Standards](docs/DISASSEMBLY_STANDARDS.md) | Source reconstruction and provenance standards |
| [Project Standards](docs/PROJECT_STANDARDS.md) | Naming, assets, manifests, provenance, and repository-wide conventions |
| [Build and Matching](docs/BUILD_AND_MATCHING.md) | Reproducible build and exact-match workflow |
| [Verification](docs/VERIFICATION.md) | Evidence levels and matching criteria |
| [Asset Workflow](docs/ASSET_WORKFLOW.md) | Graphics, sprites, deduplication, manifests, and review batches |
| [Manifest Guide](manifests/README.md) | Manifest conventions and reusable asset-manifest example |
