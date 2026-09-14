# Release identity matrix — Pocket Monsters Aka / Pokémon Red

Verification date: **2026-09-14**

This matrix is rebuilt from public evidence only. No local retail ROM is currently available. Hashes are accepted only when an attributable public source identifies the corresponding release; source-reconstruction status is tracked separately.

## Japanese origin family

| ID | Release | SHA-1 | Public exact-source evidence | Status |
|---|---|---|---|---|
| `aka-jp-v1.0` | Pocket Monsters Red (Japan) V1.0 | `0623ad12f48c259447980d68bd85ddbf8204b2cd` | `Narishma-gb/pokegreen` | verified source target |
| `aka-jp-v1.1` | Pocket Monsters Red (Japan) V1.1 / Rev A | `ef74c79cded14204ac79e77f4964d9cb25003120` | `Narishma-gb/pokegreen` | verified source target |

Reference: https://github.com/Narishma-gb/pokegreen

The Japanese Red revisions remain the historical origin targets. International Red must be compared against them rather than treated as the baseline.

## International Red family

| ID | Release | SHA-1 | Public evidence | Exact-source status |
|---|---|---|---|---|
| `red-en-ue` | Pokémon Red Version (USA, Europe) | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` | `pret/pokered` | verified build target |
| `red-de` | Pokémon Rote Edition (Germany) | `87d523fe1a0c548db7c5477b451ddec1eb083c06` | BizHawk game DB; `einstein95/pokered-de` builds matching German release by MD5 | verified source family; SHA-1 externally cross-checked |
| `red-fr` | Pokémon Version Rouge (France) | `47a7622fa30e6402a3891fe65b3a930bf9bd7aec` | `einstein95/pokered-fr` | verified build target |
| `red-it` | Pokémon Versione Rossa (Italy) | `65b97cf8f2f1cff711a6d08c6c894c8ce65ce522` | BizHawk game DB | release hash verified; exact public source **HOLD** |
| `red-es` | Pokémon Edición Roja (Spain) | `fc17c5b904d551b1b908054ccd1c493f755f832a` | `einstein95/pokered-es` | verified build target |

### Public-source references

- EN: https://github.com/pret/pokered
- DE: https://github.com/einstein95/pokered-de
- FR: https://github.com/einstein95/pokered-fr
- ES: https://github.com/einstein95/pokered-es
- independent SHA-1 cross-check database: https://github.com/TASEmulators/BizHawk/blob/master/Assets/gamedb/gamedb_gb.txt

## Italian-source warning

A repository named `einstein95/pokered-it` exists, but its currently observed default-branch README/hash material identifies German Red/Blue rather than Italian Red/Blue. It is therefore **not accepted as Italian exact-source evidence** without a historical-branch/commit investigation.

The Italian retail hash remains a valid release-identity lead from the independent game database; reconstruction-source coverage remains unresolved.

## Official re-release family

Japanese Red also has a 3DS Virtual Console patch/source lineage exposed by `Narishma-gb/pokegreen`; `pret/pokered` exposes VC patch output for the international Red/Blue source family. VC outputs are separate targets and are not substituted for cartridge identities.

## Matrix rules

- one row = one byte identity, not one marketing name;
- Japanese cartridge revisions remain separate even when gameplay differences appear small;
- same-language regional labels are not assumed byte-identical unless a source/hash proves it;
- debug builds (`BLUEMONS.GB` and similar) are separate development/debug evidence, never retail identities;
- VC patches/rebuilds are official derivative families, not cartridge revisions;
- unknown or unverified language/revision identities remain open rather than being invented.

## Next verification work

- investigate the complete history/branches/forks of `pokered-it` and alternate Italian projects;
- identify whether any retail language has more than one released binary revision;
- inventory VC output hashes and patch bases by language;
- cross-check release identities against additional independent preservation databases;
- attach cartridge-header fields and mapper/SGB metadata to each row after source-level validation.
