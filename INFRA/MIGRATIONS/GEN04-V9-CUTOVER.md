# Generation IV v9 cutover ledger

Date: 2026-09-13

## Completed

- Canonical source spine is `GEN-04/<GAME>/SOURCE/NDS-NTR/CART/<RELEASE-ID>/`.
- Exact supplied images remain dump observations under `DUMPS/<DUMP-ID>/`; no `.nds` image is committed.
- Added per-dump v9 header observations and NitroFS summaries for Diamond `ADAE-HV5`, Pearl `APAE-HV5`, Platinum `CPUK-HV0`, HeartGold `IPKK-HV0`, and SoulSilver `IPGK-HV0`.
- Added complete NDS-header evidence records including ARM9/ARM7, FNT/FAT, overlays, capacity, secure-area/header/logo CRC fields, autoload values and local-source hashes.
- Added the reproducible `INFRA/TOOLS/NDS/gen4_rom_inventory_v9.py` inventory tool.
- Moved `GEN-04/GENERATION-IV/COMPARE/OFFICIAL-SOURCE-AND-TARGET-BASELINE` to `GEN-04/COMPARE/OFFICIAL-SOURCE-AND-TARGET-BASELINE` by preserving the existing subtree/blob identities.
- Moved legacy HGSS→GSC story integration from root `GENERATION-IV/...` to `CROSS-GEN/COMPARE/HGSS-TO-GSC-STORY/ANALYSIS/story_integration`, preserving blob identities.
- Removed the now-obsolete `GEN-04/GENERATION-IV` and root `GENERATION-IV` alias trees in merged PR #94.
- `LIBRARY/GEN-04` is absent after cutover; it is not a valid new-work destination.

## Paired-repository rule

Sakurai owns source identity, exact observations, reverse engineering, specifications and verification. Tsubaki owns production source locks, asset catalogs, extraction/conversion/normalization recipes, implementation, patches and non-ROM build outputs. Both use exactly the same Generation IV release and dump IDs.

## Current locked core-five

- Diamond: `ADAE-HV5` / `LGC-a46233d8`
- Pearl: `APAE-HV5` / `LGC-99083bf1`
- Platinum KR: `CPUK-HV0` / `UPLOAD-f811d9c7`
- HeartGold KR: `IPKK-HV0` / `UPLOAD-5834fb3a`
- SoulSilver KR: `IPGK-HV0` / `UPLOAD-0330e644`
