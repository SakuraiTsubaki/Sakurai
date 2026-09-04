# Pokémon Gold bank census summary — 2026-09-05

16 KiB bank-level census. Full bank metrics are reproducible with `tools/rom_census.py` / follow-up tooling. No ROM bytes are included.

## Zero-filled banks

| ROM | Banks | All-zero banks | Highest non-zero bank |
|---|---:|---:|---:|
| Pocket Monsters Geum (Korea).gbc | 128 | 24 | `0x7F` |
| Pocket Monsters Kin (Japan) (Rev A).gbc | 64 | 0 | `0x3F` |
| Pocket Monsters Kin (Japan).gbc | 64 | 0 | `0x3F` |
| Pokemon - Edicion Oro (Spain).gbc | 128 | 26 | `0x7F` |
| Pokemon - Gold Version (USA, Europe).gbc | 128 | 28 | `0x7F` |
| Pokemon - Goldene Edition (Germany).gbc | 128 | 26 | `0x7F` |
| Pokemon - Version Or (France).gbc | 128 | 26 | `0x7F` |
| Pokemon - Versione Oro (Italy).gbc | 128 | 26 | `0x7F` |

## Cross-localization exact bank equality

- EN/DE/FR/IT/ES share **47 exact same-index banks** byte-for-byte.
- EN and KR share **29 exact same-index banks**.
- All six 2 MiB localizations (EN/DE/FR/IT/ES/KR) share **27 exact same-index banks**.
- JP Rev 0 and Rev A have **54/64 exact identical banks**; all changes are confined to 10 banks.

## Interpretation guardrail

An all-zero bank or large zero-filled tail is only a storage observation. It is **not yet declared safe free space** until references, bank-call topology, pointer tables, and runtime behavior are checked.
