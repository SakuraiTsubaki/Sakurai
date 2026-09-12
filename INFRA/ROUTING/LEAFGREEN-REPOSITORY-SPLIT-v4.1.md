# LeafGreen repository split — ROM-derived ownership contract v4.1

Status: **canonical extension of repository structure v4 for LeafGreen**.

This contract was revalidated directly against the seven supplied 16 MiB Pokémon LeafGreen GBA ROM images on 2026-09-12. The raw `.gba` files are read-only local inputs and are never committed.

## Canonical identity

Game root:

`LIBRARY/GEN-03/GBA/LEAFGREEN/`

Release IDs:

- `BPGJ-R0` — Japan / Japanese
- `BPGE-R0` — English / header revision 0
- `BPGE-R1` — English / header revision 1
- `BPGD-R0` — German
- `BPGF-R0` — French
- `BPGI-R0` — Italian
- `BPGS-R0` — Spanish

Release identity and exact dump identity are separate. A release is an official build identity; a dump is an exact observed file with provenance and complete hashes.

## Sakurai owns facts and reverse engineering

Commit here:

- complete ROM identity, hashes, GBA header validation and provenance;
- exact dump manifests;
- bank/byte census, similarities and localization/revision differences;
- pointer maps, data structure maps, disassembly, symbols and annotations;
- text/data extraction schemas and decoding research;
- bugs, glitches, unused/dummy/development-leftover research;
- reproducible analyzers and verification tests;
- design specifications and project release/source locks.

Canonical placement:

```text
LIBRARY/GEN-03/GBA/LEAFGREEN/
├── RELEASES/<RELEASE-ID>/
│   ├── MANIFESTS/
│   ├── DUMPS/<DUMP-ID>/MANIFESTS/
│   ├── ANALYSIS/
│   ├── STRUCTURE/
│   ├── DATA/
│   ├── TEXT/
│   ├── MAPS/
│   ├── EVENTS/
│   ├── DISASSEMBLY/
│   ├── SYMBOLS/
│   ├── TOOLS/
│   └── VERIFICATION/
├── COMPARISONS/<COMPARISON-ID>/
└── SHARED/
```

Project research/design lives under `PROJECTS/<PROJECT-ID>/`.

## Tsubaki owns production

Tsubaki uses the exact same release IDs but owns redistributable production assets, dedup/conversion indices, converted resources, build inputs, patches, builds and generated implementation resources.

Sakurai must not become an asset/build mirror, and Tsubaki must not become an independent source of ROM identity facts.

## Hard routing rules

- Raw original ROM -> neither repository.
- ROM hash/header/provenance -> Sakurai only.
- Bank/pointer/disassembly/structure fact -> Sakurai only.
- Asset hash/dedup production index -> Tsubaki.
- Redistributable converted or newly created asset -> Tsubaki.
- Project patch/build -> Tsubaki.
- Project design/source lock/verification specification -> Sakurai.
- Project implementation asset/build input -> Tsubaki.

Legacy `GENERATION-*`, standalone `GEN-*`, `GAMES/...`, `MULTI`, `REV-ALL` and language-first LeafGreen owners are migration sources only and must receive no new LeafGreen files.

## ROM-derived bank evidence

Every current image is exactly 256 × 64 KiB banks. `bank-variant-distribution.json` stores the checked aggregate result, while `SHARED/TOOLS/bank_variant_map.py` reproducibly emits the complete per-bank release grouping from the local ROM set. This research evidence belongs in Sakurai; Tsubaki receives only production-oriented reuse summaries derived from it.
