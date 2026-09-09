# Generation 2 uploaded ROM audit (2026-09-10)

- Physical ROM files: **11**
- Total 16 KiB banks: **1152**
- Header checksum valid: **11/11**
- Global checksum valid: **11/11**

## ROM set

|Game|Language|Revision|Size|Banks|Hardware|SGB|Header title|SHA-1|
|---|---|---|---:|---:|---|---|---|---|
|Crystal|Japanese|0|2.0 MiB|128|CGB only|No|`PM_CRYSTAL`|`95127b901bbce2407daf43cce9f45d4c27ef635d`|
|Silver|Korean|0|2.0 MiB|128|CGB only|No|`POKEMON_SLVAAXK`|`cb22d7e03a74dc3a563fde6be8626626b2b392e7`|
|Gold|Korean|0|2.0 MiB|128|CGB only|No|`POKEMON_GLDAAUK`|`c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`|
|Silver|Japanese|A|1.0 MiB|64|CGB enhanced|Yes|`POKEMON_SLVAAXJ`|`a11d5ddc26eb826086593f82370b15d16404d33e`|
|Silver|Japanese|0|1.0 MiB|64|CGB enhanced|Yes|`POKEMON_SLVAAXJ`|`fa8c51059c1642faa570db56ef089f54d1d2011f`|
|Gold|Japanese|A|1.0 MiB|64|CGB enhanced|Yes|`POKEMON_GLDAAUJ`|`a222402235d484ee8e39f3f31bae57cf13daf585`|
|Gold|Japanese|0|1.0 MiB|64|CGB enhanced|Yes|`POKEMON_GLDAAUJ`|`8814f1039450a5d3684b1389f588ccd7ee7c3436`|
|Crystal|English|A|2.0 MiB|128|CGB only|No|`PM_CRYSTAL`|`f2f52230b536214ef7c9924f483392993e226cfb`|
|Crystal|English|0|2.0 MiB|128|CGB only|No|`PM_CRYSTAL`|`f4cd194bdee0d04ca4eac29e09b8e4e9d818c133`|
|Gold|English|0|2.0 MiB|128|CGB enhanced|Yes|`POKEMON_GLDAAUE`|`d8b8a3600a465308c9953dfa04f0081c05bdcb94`|
|Silver|English|0|2.0 MiB|128|CGB enhanced|Yes|`POKEMON_SLVAAXE`|`49b163f7e57702bc939d642a18f591de55d92dae`|

## Revision comparison

|Pair|Byte differences|Changed banks|Changed bank list|
|---|---:|---:|---|
|Gold JP Rev0→RevA|10841|10|`00 04 05 09 0A 0F 14 21 23 24`|
|Silver JP Rev0→RevA|19150|16|`00 01 03 04 05 09 0A 0B 0F 14 21 23 24 25 3E 3F`|
|Crystal EN Rev0→RevA|584|8|`00 10 11 3E 47 5C 7E 7F`|

## Notes

- ROM binaries are intentionally excluded. This directory contains only identification and analysis metadata.
- A local `bank_manifest.csv` fingerprints every 16 KiB ROM bank with SHA-1 for later bank-by-bank structural work.
- Revision comparisons are byte-level observations, not assumptions that all changed bytes are meaningful game-data changes; unused/padding/build-layout differences can also contribute.
