# Pokémon Silver KR REV-0 whole-ROM work corpus

- Source SHA-256: `ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22`
- ROM bytes included: **no**
- Physical banks: **128 × 16 KiB**
- Coverage: **8192 × 0x100 = 2,097,152 bytes**, exactly the full ROM
- Candidate text strings: **2,115**
- Candidate local pointer tables: **6,020**
- Candidate far-pointer tables: **7,757**
- Fill runs ≥64 bytes: **139**
- Repeated non-fill 0x100 fingerprint groups: **6**

The scanner is aware that Korean text uses 2-byte codepoints whose first byte `0x01..0x0B` selects a Hangul table. Reference-role transfer remains confidence-scored until Korean symbols are verified.
