# Sapphire ROM reproducibility baseline summary

- ROMs verified: **9**
- 64 KiB chunks fingerprinted: **2176**
- Pairwise comparisons: **36**
- Coalesced revision-diff regions: **7560**
- Local split/rebuild verification: **9/9 SHA-256 exact matches**

## GBA identities

| Language/region | Rev | Game code | Size | Software version | Header checksum |
|---|---:|---|---:|---:|---|
| JAPANESE-JAPAN | REV-0 | `AXPJ` | 8 MiB | 0 | valid |
| GERMAN-GERMANY | REV-1 | `AXPD` | 16 MiB | 1 | valid |
| ENGLISH-USA | REV-0 | `AXPE` | 16 MiB | 0 | valid |
| ENGLISH-EUROPE | REV-1 | `AXPE` | 16 MiB | 1 | valid |
| ENGLISH-USA-EUROPE | REV-2 | `AXPE` | 16 MiB | 2 | valid |
| FRENCH-FRANCE | REV-0 | `AXPF` | 16 MiB | 0 | valid |
| FRENCH-FRANCE | REV-1 | `AXPF` | 16 MiB | 1 | valid |
| ITALIAN-ITALY | REV-0 | `AXPI` | 16 MiB | 0 | valid |
| ITALIAN-ITALY | REV-1 | `AXPI` | 16 MiB | 1 | valid |

## Revision-diff region counts

- `Pokemon - Sapphire Version (USA).gba` → `Pokemon - Sapphire Version (Europe) (Rev 1).gba`: 7551 regions, 5,638,997 changed bytes inside 6,357,260 bytes of coalesced spans.
- `Pokemon - Sapphire Version (Europe) (Rev 1).gba` → `Pokemon - Sapphire Version (USA, Europe) (Rev 2).gba`: 3 regions, 4 changed bytes inside 4 bytes of coalesced spans.
- `Pokemon - Version Saphir (France).gba` → `Pokemon - Version Saphir (France) (Rev 1).gba`: 3 regions, 4 changed bytes inside 4 bytes of coalesced spans.
- `Pokemon - Versione Zaffiro (Italy).gba` → `Pokemon - Versione Zaffiro (Italy) (Rev 1).gba`: 3 regions, 4 changed bytes inside 4 bytes of coalesced spans.

Large deterministic CSV datasets are generated locally by `tools/analyze_sapphire.py` and fingerprinted in `data/generated_dataset_manifest.json`.
