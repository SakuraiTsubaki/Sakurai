# GSC Kanto → RGBY

Canonical v11 project ID: `GSC-KANTO-TO-RGBY`.

This project ports Generation II Kanto content into a Generation I RGBY engine while preserving version, region, revision, event, map, text, and localization differences as explicit data.

## Pair contract

The semantic project coordinate is identical in both repositories:

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`

- **Sakurai** is the curated knowledge/control subset: release and dump identity, hashes, provenance, schemas, mappings, reverse-engineering conclusions, reports, specifications, research tools, and verification.
- **Tsubaki** is the complete non-ROM superset. Every eligible project artifact that is not a playable whole-ROM image belongs there.

## Canonical Korean Gold/Silver source

The full tracked Korean Gold/Silver disassembly is stored once in Tsubaki at:

`GEN-02/PROJECTS/POKEGOLD-KR/IMPLEMENTATION/`

That tree is exactly `SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c` (`fe50ec090dbf514da2aaa80f331ceedbb30f3197`) and contains **4,126 tracked non-ROM files**.

The cross-generation GSC→RGBY project references this shared Generation II source instead of duplicating it.

## Primary Korean Generation II ROM identities

- Gold: `GEN-02/GOLD/RELEASES/GBC/CART/AAUK-HV0/`
- Silver: `GEN-02/SILVER/RELEASES/GBC/CART/AAXK-HV0/`

Exact dump hashes are recorded in `MANIFESTS/ROM-BASELINES.json`. ROM images themselves are never committed.

See `PROJECT.json`, `MANIFESTS/UPSTREAM-LOCKS.json`, and `SPEC/REPOSITORY-SPLIT.md`.
