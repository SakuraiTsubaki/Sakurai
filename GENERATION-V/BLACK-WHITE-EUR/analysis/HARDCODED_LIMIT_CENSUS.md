# Pokémon Black/White EUR — hardcoded boundary constant census

No ROM bytes were modified. Executable scan covers decompressed ARM9, ARM7, DSi ARM9i/ARM7i, and all 237 decompressed ARM9 overlays for both current project ROMs.

## Method
- Exact aligned `u32` literals are strong candidates for literal pools / word tables.
- Exact aligned `u16` values are noisy until consumer code is established.
- Numeric occurrence alone is not promoted to a game limit.

## Exact u32 literal occurrence counts (Black)
|Value|ARM9|Overlays|ARM7/DSi|
|---:|---:|---:|---:|
|151|1|14|0|
|152|1|34|0|
|155|0|22|0|
|156|1|19|0|
|386|1|8|2|
|387|1|9|0|
|493|5|12|0|
|494|3|5|0|
|649|11|20|0|
|650|8|17|0|
|651|6|8|0|
|652|0|4|0|
|667|0|3|0|
|668|0|0|0|
|669|3|0|0|
|999|13|15|0|

Strong consumer verification is in `HARDCODED_LITERAL_XREF_CENSUS.md`; generation scripts are stored under `scripts/`.