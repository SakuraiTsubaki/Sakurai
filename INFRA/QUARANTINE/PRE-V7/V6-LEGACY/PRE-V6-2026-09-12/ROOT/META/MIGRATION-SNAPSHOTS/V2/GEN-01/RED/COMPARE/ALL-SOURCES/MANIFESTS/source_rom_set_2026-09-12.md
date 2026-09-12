# Pokémon Red source ROM set — 2026-09-12

Original ROM binaries are not stored in GitHub. This manifest records identity and routing only.

| Canonical source path | Source file | Size | Header revision | Cartridge controller | SHA-1 | Status |
|---|---|---:|---:|---|---|---|
| `GEN-01/RED/SOURCE/JP-JA/REV-0` | Pocket Monsters - Aka (Japan) (SGB Enhanced).gb | 524288 | 0 | MBC1+RAM+BATTERY | `0623ad12f48c259447980d68bd85ddbf8204b2cd` | unique source |
| `GEN-01/RED/SOURCE/JP-JA/REV-A` | Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb | 524288 | 1 | MBC1+RAM+BATTERY | `ef74c79cded14204ac79e77f4964d9cb25003120` | unique source |
| `GEN-01/RED/SOURCE/US-EU-EN/REV-0` | Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb | 1048576 | 0 | MBC3+RAM+BATTERY | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` | unique source |
| `GEN-01/RED/SOURCE/EU-DE/REV-0` | Pokemon - Rote Edition (Germany) (SGB Enhanced).gb | 1048576 | 0 | MBC5+RAM+BATTERY | `87d523fe1a0c548db7c5477b451ddec1eb083c06` | unique source |
| `GEN-01/RED/SOURCE/EU-FR/REV-0` | Pokemon - Version Rouge (France) (SGB Enhanced).gb | 1048576 | 0 | MBC5+RAM+BATTERY | `47a7622fa30e6402a3891fe65b3a930bf9bd7aec` | unique source |
| `GEN-01/RED/SOURCE/EU-IT/REV-0` | Pokemon - Versione Rossa (Italy) (SGB Enhanced).gb | 1048576 | 0 | MBC5+RAM+BATTERY | `65b97cf8f2f1cff711a6d08c6c894c8ce65ce522` | unique source |
| `GEN-01/RED/SOURCE/EU-ES/REV-0` | Pokemon - Edicion Roja (Spain) (SGB Enhanced).gb | 1048576 | 0 | MBC5+RAM+BATTERY | `fc17c5b904d551b1b908054ccd1c493f755f832a` | unique source |

## Duplicate observation

`Pokemon - Red Version (USA, Europe) (SGB Enhanced) - 복사본.gb` has the same SHA-1 (`ea9bcae617fdf159b045185467ae58b2e4a48b9a`) as the canonical USA/Europe English source. It is a duplicate copy and does not receive a second repository path.

## Routing consequence

The old `GENERATION-I/RED/MULTI/REV-ALL` tree is cross-source work, not a source release. Its content must migrate under `GEN-01/RED/COMPARE/ALL-SOURCES/...`, split by truthful work type. Release-specific results belong under the corresponding `SOURCE/<RELEASE-ID>/<REV>/...` branch.
