# Generation 1 uploaded ROM audit (2026-09-10)

- Physical ROM files: **12**
- Total 16 KiB banks: **608**
- Header checksum valid: **12/12**
- Global checksum valid: **12/12**

## ROM set

|Game|Language|Revision|Size|Banks|Hardware|SGB|Header title|SHA-1|
|---|---|---|---:|---:|---|---|---|---|
|Red|Japanese|A|0.5 MiB|32|DMG|Yes|`POKEMON RED`|`ef74c79cded14204ac79e77f4964d9cb25003120`|
|Red|Japanese|0|0.5 MiB|32|DMG|Yes|`POKEMON RED`|`0623ad12f48c259447980d68bd85ddbf8204b2cd`|
|Blue|Japanese|0|0.5 MiB|32|DMG|Yes|`POKEMON BLUE`|`0da501e3e5c51ab8fef55b092dcdd7e6b050e424`|
|Green|Japanese|A|0.5 MiB|32|DMG|Yes|`POKEMON GREEN`|`4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`|
|Green|Japanese|0|0.5 MiB|32|DMG|Yes|`POKEMON GREEN`|`82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`|
|Yellow/Pikachu|Japanese|0A|1.0 MiB|64|DMG|Yes|`POKEMON YELLOW`|`1fb6c264e950d97ce3fd99b347e485b2150df4ff`|
|Yellow/Pikachu|Japanese|B|1.0 MiB|64|DMG|Yes|`POKEMON YELLOW`|`28e4b8531ea4ea1de5a396fccb0cfba51b06b149`|
|Yellow/Pikachu|Japanese|C|1.0 MiB|64|DMG|Yes|`POKEMON YELLOW`|`91864ecdf26d1c593bde4d9ed615520eb57d5e41`|
|Yellow/Pikachu|Japanese|D|1.0 MiB|64|DMG|Yes|`POKEMON YELLOW`|`a40298a8123613ee60cd7aab204d788b8425976e`|
|Blue|English|0|1.0 MiB|64|DMG|Yes|`POKEMON BLUE`|`d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`|
|Red|English|0|1.0 MiB|64|DMG|Yes|`POKEMON RED`|`ea9bcae617fdf159b045185467ae58b2e4a48b9a`|
|Yellow/Pikachu|English|0|1.0 MiB|64|CGB enhanced|Yes|`POKEMON YELLOW`|`cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`|

## Revision comparison

|Pair|Byte differences|Changed banks|Changed bank list|
|---|---:|---:|---|
|Aka JP Rev0→RevA|46167|31|`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1C 1D 1E 1F`|
|Midori JP Rev0→RevA|46168|31|`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1C 1D 1E 1F`|
|Pikachu JP 0A→B|307668|61|`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 1A 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30 31 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F`|
|Pikachu JP B→C|39485|60|`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 1A 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30 31 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F`|
|Pikachu JP C→D|245538|61|`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 1A 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30 31 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F`|

## Notes

- ROM binaries are intentionally excluded. This directory contains only identification and analysis metadata.
- A local `bank_manifest.csv` fingerprints every 16 KiB ROM bank with SHA-1 for later bank-by-bank structural work.
- Revision comparisons are byte-level observations, not assumptions that all changed bytes are meaningful game-data changes; unused/padding/build-layout differences can also contribute.
