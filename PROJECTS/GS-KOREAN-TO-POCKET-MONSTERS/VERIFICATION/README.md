# Verification ownership

Verification evidence is kept separate from mutable production artifacts.

Required verification layers include:

- source ROM SHA-1/SHA-256 and GB/GBC header/global checksums;
- release/dump identity and canonical path checks;
- per-bank hashes and Gold/Silver implementation-region comparisons;
- lossless extraction/reassembly checks where applicable;
- text decode/encode round trips;
- pointer and bank-target validation after relocation;
- UI/text-box/name/SRAM boundary tests;
- event progression and battle/system regression tests;
- final patch/build hashes recorded against the intended canonical source release.

Tsubaki stores production-side extraction/build verification; Sakurai remains authoritative for research conclusions and cross-release verification evidence.
