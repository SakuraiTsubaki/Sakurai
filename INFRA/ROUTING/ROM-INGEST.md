# ROM Ingest Routing — v9

This document decides what moves from a locally owned ROM workflow into Sakurai, Tsubaki, or nowhere in Git.

## Sakurai — commit here

Commit facts and specifications that can be reviewed without possessing the ROM:

- release identity and source provenance
- SHA-256/SHA-1/CRC32 and dump observation metadata
- address/bank/symbol maps and semantic ROM maps
- text/event/map/object/specification tables
- cross-version and cross-generation mapping tables
- research notes and evidence summaries
- target requirements and acceptance criteria
- validators and verification definitions that do not embed proprietary payloads
- references and citations

For `RGBY-KANTO-TO-GSC`, these live under:

```text
CROSS-GEN/TARGET/RGBY-KANTO-TO-GSC/
├── MANIFESTS/
├── SPEC/
├── MAPPING/
├── RESEARCH/
├── REFERENCE/
└── VERIFICATION/
```

## Tsubaki — commit there

Commit reproducible production material:

- extraction scripts
- converters and normalizers
- assembler/source implementation
- build and verification tools
- patch payloads/deltas that do not contain a complete ROM
- generated catalogs and non-proprietary manifests
- build/verification reports
- redistributable derived data whose provenance permits redistribution

The matching Tsubaki target is:

```text
CROSS-GEN/TARGET/RGBY-KANTO-TO-GSC/
```

## Local only — do not commit to either repository

- `*.gb`, `*.gbc`, and other original ROM images
- complete patched ROM images
- ROM archives such as ZIP/7z containing original or patched images
- complete extracted proprietary graphics/audio/text/data sets when redistribution is not permitted
- temporary decompositions, emulator scratch, and local build ROMs

Use hashes and manifests as the Git-visible boundary.

## Handoff rule

Every production input in Tsubaki must be resolvable to a Sakurai identity/manifest ID or an explicitly documented project-owned input. Paths must never encode uncertainty with `UNKNOWN`, `MISC`, or `MULTI`; uncertainty belongs in manifest fields.
