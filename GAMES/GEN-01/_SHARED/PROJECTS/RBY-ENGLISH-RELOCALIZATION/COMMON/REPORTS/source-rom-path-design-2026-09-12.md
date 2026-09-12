# RBY English relocalization — source-ROM path design

## Final ownership model

Keep repository structure v3. The actual ROM set confirms that exact official builds should be immutable `RELEASES`, while the retranslation/reimplementation is a `PROJECTS` tree.

### Official source builds

`GAMES/GEN-01/<GAME-ID>/RELEASES/<RELEASE-ID>/<WORK-TYPE>/...`

For Generation I, `RELEASE-ID` uses `GB-<MARKET>-<LANGUAGE>-<REVISION>` because the game root already identifies Red/Green/Blue/Yellow. SGB/CGB compatibility, mapper, ROM size, header version, hashes, and dump provenance remain manifest metadata.

### Cross-game project common

`GAMES/GEN-01/_SHARED/PROJECTS/RBY-ENGLISH-RELOCALIZATION/COMMON/<WORK-TYPE>/...`

### Per-game derived targets

`GAMES/GEN-01/<GAME-ID>/PROJECTS/RBY-ENGLISH-RELOCALIZATION/TARGETS/<TARGET-ID>/<WORK-TYPE>/...`

`TARGET-ID` is `<BASE-RELEASE-ID>-EN-RELOCALIZED`, so each output stays tied to one exact Japanese ROM base. The target manifest lists the English implementation reference(s) used.

## Confirmed release IDs from the supplied ROMs

| Game | Release ID | Project role | Size | Header ver. | CGB | Cart | SHA-1 |
|---|---|---|---:|---:|---|---|---|
| RED | `GB-JP-JA-REV-0` | TRANSLATION-ORIGINAL, BUILD-BASE | 512 KiB | 0 | `0x00` | `0x03` | `0623ad12f48c259447980d68bd85ddbf8204b2cd` |
| RED | `GB-JP-JA-REV-A` | TRANSLATION-ORIGINAL, BUILD-BASE | 512 KiB | 1 | `0x00` | `0x03` | `ef74c79cded14204ac79e77f4964d9cb25003120` |
| GREEN | `GB-JP-JA-REV-0` | TRANSLATION-ORIGINAL, BUILD-BASE | 512 KiB | 0 | `0x00` | `0x03` | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` |
| GREEN | `GB-JP-JA-REV-A` | TRANSLATION-ORIGINAL, BUILD-BASE | 512 KiB | 1 | `0x00` | `0x03` | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` |
| BLUE | `GB-JP-JA-REV-0` | TRANSLATION-ORIGINAL, BUILD-BASE | 512 KiB | 0 | `0x00` | `0x03` | `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` |
| YELLOW | `GB-JP-JA-REV-0A` | TRANSLATION-ORIGINAL, BUILD-BASE | 1024 KiB | 0 | `0x00` | `0x13` | `1fb6c264e950d97ce3fd99b347e485b2150df4ff` |
| YELLOW | `GB-JP-JA-REV-B` | TRANSLATION-ORIGINAL, BUILD-BASE | 1024 KiB | 1 | `0x00` | `0x13` | `28e4b8531ea4ea1de5a396fccb0cfba51b06b149` |
| YELLOW | `GB-JP-JA-REV-C` | TRANSLATION-ORIGINAL, BUILD-BASE | 1024 KiB | 2 | `0x00` | `0x13` | `91864ecdf26d1c593bde4d9ed615520eb57d5e41` |
| YELLOW | `GB-JP-JA-REV-D` | TRANSLATION-ORIGINAL, BUILD-BASE | 1024 KiB | 3 | `0x00` | `0x13` | `a40298a8123613ee60cd7aab204d788b8425976e` |
| RED | `GB-US-EU-EN-REV-0` | IMPLEMENTATION-REFERENCE | 1024 KiB | 0 | `0x00` | `0x13` | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` |
| BLUE | `GB-US-EU-EN-REV-0` | IMPLEMENTATION-REFERENCE | 1024 KiB | 0 | `0x00` | `0x13` | `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` |
| YELLOW | `GB-US-EU-EN-REV-0` | IMPLEMENTATION-REFERENCE | 1024 KiB | 0 | `0x80` | `0x1B` | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` |

## Important consequences

- Japanese Red/Green/Blue/Pikachu are both the translation originals and the ROM bases that receive the new English implementation.
- English Red/Blue/Yellow are official source releases too, but in this project their role is implementation reference only.
- Japanese Pikachu `REV-0A`, `REV-B`, `REV-C`, and `REV-D` are separate immutable releases. `REV-0A` must never be normalized to `REV-0`.
- International Yellow has CGB flag `0x80`, but remains a Game Boy-compatible release; the CGB capability is manifest metadata rather than a separate platform ownership layer.
- No `MULTI`, `REV-ALL`, or locale-only fake release directories are needed. Cross-release results go to `COMPARISONS`, and project-wide policy/tools go to `_SHARED/PROJECTS/.../COMMON`.

## Target examples

- `GAMES/GEN-01/RED/PROJECTS/RBY-ENGLISH-RELOCALIZATION/TARGETS/GB-JP-JA-REV-0-EN-RELOCALIZED/...`
- `GAMES/GEN-01/GREEN/PROJECTS/RBY-ENGLISH-RELOCALIZATION/TARGETS/GB-JP-JA-REV-A-EN-RELOCALIZED/...`
- `GAMES/GEN-01/YELLOW/PROJECTS/RBY-ENGLISH-RELOCALIZATION/TARGETS/GB-JP-JA-REV-0A-EN-RELOCALIZED/...`
