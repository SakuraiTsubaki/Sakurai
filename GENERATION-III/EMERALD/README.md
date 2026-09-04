# Pokémon Emerald — multi-language ROM analysis

This directory contains reproducible **non-ROM** analysis artifacts for the Pokémon Emerald ROM set used by the EMERALD project.

## Current source set

- Japanese — `BPEJ`
- English — `BPEE`
- German — `BPED`
- French — `BPEF`
- Italian — `BPEI`
- Spanish — `BPES`

Seven uploaded filenames are currently present locally, representing six unique binaries. The two English-labeled inputs are byte-for-byte identical.

## Repository policy

- **Never commit ROM images.**
- Commit analysis reports, inventories, hashes, derived metadata, scripts/tools, patches that do not contain the original ROM payload, and other non-ROM project artifacts.
- Keep provenance explicit: source filename, internal game code, hashes, and analysis date.
- New analysis work should be reflected here as it is produced.

## Layout

- `analysis/` — census reports, inventories, structural comparisons, extracted metadata.
- `tools/` — reproducible analysis tooling.

## Baseline

Start with `analysis/2026-09-05-rom-baseline.md` for the first complete file/header/hash and pairwise byte-difference census.
