# ROM source catalog

This directory contains **identity metadata only** for the local RGBY/GSC source set used by the Kanto restoration project.

## Policy

- Original ROM images are never committed to Sakurai or Tsubaki.
- SHA-256 is the primary exact-dump identifier.
- File names are convenience labels only; tools must identify a source by hash.
- Header fields are recorded as secondary diagnostics.
- Stable logical IDs in `manifest.json` are shared with Tsubaki.
- Raw/bulk extracted graphics, audio, text, and map dumps remain local working data unless a compact derived fact is specifically approved for version control.

## Project use

Generation I sources are authoritative evidence for Kanto geography, map scale, connections, facilities, dungeons, and source-era events. Generation II sources are authoritative evidence for the target engine/era, GSC event behavior, systems, localization behavior, and version differences.

The unified restoration does not select a single RGBY or GSC edition and discard the others. Version differences are cataloged and reconciled explicitly in research/specification work.