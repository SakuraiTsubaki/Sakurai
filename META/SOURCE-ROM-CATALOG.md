# Source ROM Catalog — Gen I / Gen II

Verified from the 23 ROM files supplied to the GS Korean → Pokémon project. Original ROM binaries are never committed to GitHub.

## Canonical V2 ownership

Official source-build artifacts belong under:

`GEN-XX/<GAME>/SOURCE/<RELEASE-ID>/<REV>/<WORK-TYPE>/...`

Derived Korean localization output belongs under:

`GEN-XX/<GAME>/TARGET/KR-KO/<BASE-ID>/<WORK-TYPE>/...`

where `<BASE-ID>` identifies the actual source release and revision, for example `JP-JA-REV-0` or `US-EU-EN-REV-0`.

Important rules:

- `US-EU-EN` is one source release identity for the supplied shared USA/Europe English ROMs.
- `KR-KO` is a SOURCE release only where an actual Korean source ROM exists. In this supplied set that is Gold and Silver only.
- There is no Korean Crystal source ROM in this source set. A Korean Crystal project therefore belongs under `TARGET/KR-KO/...`, never `SOURCE/KR-KO/...`.
- Japanese Yellow keeps the source revision labels `REV-0A`, `REV-B`, `REV-C`, `REV-D`. The Game Boy header revision byte is recorded separately below.
- Cross-source work goes under `COMPARE`; game-wide release-independent material goes under `SHARED`.

## Verified inventory

| Canonical source path | Header rev | Bytes | SHA-1 | Supplied file |
|---|---:|---:|---|---|
| `GEN-01/BLUE/SOURCE/JP-JA/REV-0` | 0 | 524288 | `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` | `Pocket Monsters - Ao (Japan) (SGB Enhanced).gb` |
| `GEN-01/BLUE/SOURCE/US-EU-EN/REV-0` | 0 | 1048576 | `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` | `Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb` |
| `GEN-01/GREEN/SOURCE/JP-JA/REV-0` | 0 | 524288 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | `Pocket Monsters - Midori (Japan) (SGB Enhanced).gb` |
| `GEN-01/GREEN/SOURCE/JP-JA/REV-A` | 1 | 524288 | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` | `Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb` |
| `GEN-01/RED/SOURCE/JP-JA/REV-0` | 0 | 524288 | `0623ad12f48c259447980d68bd85ddbf8204b2cd` | `Pocket Monsters - Aka (Japan) (SGB Enhanced).gb` |
| `GEN-01/RED/SOURCE/JP-JA/REV-A` | 1 | 524288 | `ef74c79cded14204ac79e77f4964d9cb25003120` | `Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb` |
| `GEN-01/RED/SOURCE/US-EU-EN/REV-0` | 0 | 1048576 | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` | `Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb` |
| `GEN-01/YELLOW/SOURCE/JP-JA/REV-0A` | 0 | 1048576 | `1fb6c264e950d97ce3fd99b347e485b2150df4ff` | `Pocket Monsters - Pikachu (Japan) (Rev 0A) (SGB Enhanced).gb` |
| `GEN-01/YELLOW/SOURCE/JP-JA/REV-B` | 1 | 1048576 | `28e4b8531ea4ea1de5a396fccb0cfba51b06b149` | `Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb` |
| `GEN-01/YELLOW/SOURCE/JP-JA/REV-C` | 2 | 1048576 | `91864ecdf26d1c593bde4d9ed615520eb57d5e41` | `Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb` |
| `GEN-01/YELLOW/SOURCE/JP-JA/REV-D` | 3 | 1048576 | `a40298a8123613ee60cd7aab204d788b8425976e` | `Pocket Monsters - Pikachu (Japan) (Rev D) (SGB Enhanced).gb` |
| `GEN-01/YELLOW/SOURCE/US-EU-EN/REV-0` | 0 | 1048576 | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` | `Pokemon - Yellow Version (USA, Europe).gbc` |
| `GEN-02/CRYSTAL/SOURCE/JP-JA/REV-0` | 0 | 2097152 | `95127b901bbce2407daf43cce9f45d4c27ef635d` | `Pocket Monsters - Crystal Version (Japan).gbc` |
| `GEN-02/CRYSTAL/SOURCE/US-EU-EN/REV-0` | 0 | 2097152 | `f4cd194bdee0d04ca4eac29e09b8e4e9d818c133` | `Pokemon - Crystal Version (USA, Europe).gbc` |
| `GEN-02/CRYSTAL/SOURCE/US-EU-EN/REV-A` | 1 | 2097152 | `f2f52230b536214ef7c9924f483392993e226cfb` | `Pokemon - Crystal Version (USA, Europe) (Rev A).gbc` |
| `GEN-02/GOLD/SOURCE/JP-JA/REV-0` | 0 | 1048576 | `8814f1039450a5d3684b1389f588ccd7ee7c3436` | `Pocket Monsters Kin (Japan).gbc` |
| `GEN-02/GOLD/SOURCE/JP-JA/REV-A` | 1 | 1048576 | `a222402235d484ee8e39f3f31bae57cf13daf585` | `Pocket Monsters Kin (Japan) (Rev A).gbc` |
| `GEN-02/GOLD/SOURCE/KR-KO/REV-0` | 0 | 2097152 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | `Pocket Monsters Geum (Korea).gbc` |
| `GEN-02/GOLD/SOURCE/US-EU-EN/REV-0` | 0 | 2097152 | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` | `Pokemon - Gold Version (USA, Europe).gbc` |
| `GEN-02/SILVER/SOURCE/JP-JA/REV-0` | 0 | 1048576 | `fa8c51059c1642faa570db56ef089f54d1d2011f` | `Pocket Monsters Gin (Japan).gbc` |
| `GEN-02/SILVER/SOURCE/JP-JA/REV-A` | 1 | 1048576 | `a11d5ddc26eb826086593f82370b15d16404d33e` | `Pocket Monsters Gin (Japan) (Rev A).gbc` |
| `GEN-02/SILVER/SOURCE/KR-KO/REV-0` | 0 | 2097152 | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` | `Pocket Monsters Eun (Korea).gbc` |
| `GEN-02/SILVER/SOURCE/US-EU-EN/REV-0` | 0 | 2097152 | `49b163f7e57702bc939d642a18f591de55d92dae` | `Pokemon - Silver Version (USA, Europe).gbc` |

## Coverage

- Generation I: 12 supplied ROMs.
- Generation II: 11 supplied ROMs.
- Total: 23 supplied ROMs.
- Korean official source ROMs present: Gold and Silver only.
