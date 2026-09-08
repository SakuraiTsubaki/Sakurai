# Pokémon Black / White EUR — full reproducible work-package report

## Measured Black source

- Game code: `IRBO`
- Size: `268,435,456` bytes
- CRC32: `E2BEE619`
- MD5: `F45FD94BB761721E30BD3A0A4FDE124A`
- SHA-1: `A68B3BEDF5C1E53556E41E59CDF396C20B331896`
- SHA-256: `2E40416B8E8183D936084C7BE0ADEAAB4FA3F786A68F90D7291AB77D340F0C1D`

## Measured White source

- Game code: `IRAO`
- Size: `268,435,456` bytes
- CRC32: `EDCD5161`
- MD5: `8DFEF9A099E1269AF5C1FCF9D7736A11`
- SHA-1: `F94D4578956487C09FEE20809A591E858017769E`
- SHA-256: `93E4F473CE9A0543BCCF2E689ECD07AB4FCC39DD00FB4F194343CBD5E70E17ED`

## NDS structure census

Both versions have:

- FAT entries: **484**
- ARM9 overlays: **237**
- named FNT/NitroFS files: **247**
- ARM7 overlays: **0**
- detected top-level NARC containers: **237**

The extended DSi header was also parsed and the referenced ARM9i/ARM7i ranges were preserved in the private workspace.

## Payload census

Per version the complete first-level payload view contains **54,538** rows:

- 484 top-level FAT payloads
- 54,054 unpacked NARC members

Major recognized payload types include 4,232 NCLR palettes, 3,274 NCER cell banks, 1,880 directly visible NCGR graphics, 1,341 BTX0 textures, 503 NSCR screen maps, 413 BMD0 models, 314 NANR animations, 258 BCA0 animations and multiple Nitro animation formats.

The DS-LZ pass successfully decompressed **11,760** members per version. Another **562** first-byte candidates failed structural validation and were deliberately retained unchanged instead of being treated as valid compressed data. The successful decompressed set includes **7,444 NCGR graphics** and **2,960 NANR animations**.

## Black ↔ White consolidation

Top-level FAT payloads:

- identical: **299 / 484**
- different: **185 / 484**
- path mismatches: **0**

Full equivalent-path payload view:

- total paths: **54,538**
- byte-identical: **54,287**
- different: **251**

This supports a common-base + 251-path version-delta workflow. The private workspace hard-links identical equivalent files to avoid duplicate storage.

## Exact rebuild proof

Two independent no-change rebuild routes were tested for both games:

1. immutable source ROM as physical template, then overlay extracted editable regions
2. concatenate 256 private 1 MiB base chunks, then overlay extracted editable regions

Both routes reproduced the uploaded source byte-for-byte, with matching CRC32, MD5, SHA-1 and SHA-256.

## Private/public split

Private-only source-derived binary material includes physical base chunks, executable segments, NitroFS files, unpacked NARC members and decompressed graphics/animation payloads. Those are not committed to GitHub.

GitHub stores only hashes, census results, reports, difference summaries and reproducibility tooling under the canonical `GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE` hierarchy.
