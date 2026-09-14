# Source ROM Inventory

This document records the locally verified source ROM set used for identification, reverse engineering, and byte-identity validation. **No ROM binary is stored in this repository.**

## Verified targets

| ID | Region / language | Revision | Game code | Size | SHA-1 |
|---|---|---:|---|---:|---|
| `japan_rev0` | Japan / Japanese | 0 | AXVJ | 8 MiB | `5c5e546720300b99ae45d2aa35c646c8b8ff5c56` |
| `english_rev0` | USA / English | 0 | AXVE | 16 MiB | `f28b6ffc97847e94a6c21a63cacf633ee5c8df1e` |
| `english_rev1` | Europe / English | 1 | AXVE | 16 MiB | `610b96a9c9a7d03d2bafb655e7560ccff1a6d894` |
| `english_rev2` | USA, Europe / English | 2 | AXVE | 16 MiB | `5b64eacf892920518db4ec664e62a086dd5f5bc8` |
| `germany_rev0` | Germany / German | 0 | AXVD | 16 MiB | `1c2a53332382e14dab8815e3a6dd81ad89534050` |
| `germany_rev1` | Germany / German | 1 | AXVD | 16 MiB | `424740be1fc67a5ddb954794443646e6aeee2c1b` |
| `germany_debug_rev0` | Germany / German debug | 0 | AXVD | 16 MiB | `ca5e3d415c4b47353a73a616878ba833f3648b7a` |
| `france_rev0` | France / French | 0 | AXVF | 16 MiB | `a6ee94202bec0641c55d242757e84dc89336d4cb` |
| `france_rev1` | France / French | 1 | AXVF | 16 MiB | `ba888dfba231a231cbd60fe228e894b54fb1ed79` |
| `italy_rev0` | Italy / Italian | 0 | AXVI | 16 MiB | `2b3134224392f58da00f802faa1bf4b5cf6270be` |
| `italy_rev1` | Italy / Italian | 1 | AXVI | 16 MiB | `015a5d380afe316a2a6fcc561798ebff9dfb3009` |
| `spain_rev0` | Spain / Spanish | 0 | AXVS | 16 MiB | `1f49f7289253dcbfecbc4c5ba3e67aa0652ec83c` |
| `spain_rev1` | Spain / Spanish | 1 | AXVS | 16 MiB | `9ac73481d7f5d150a018309bba91d185ce99fb7c` |

Full CRC32/SHA-1/SHA-256 metadata is stored in `manifests/source_roms.json`.

## Header observations

- All verified targets identify as `POKEMON RUBY` in the GBA header.
- Maker code is `01` across the set.
- Language/region game codes are `AXVJ`, `AXVE`, `AXVD`, `AXVF`, `AXVI`, and `AXVS`.
- The Japanese Rev 0 source image is 8 MiB; the verified western targets in this set are 16 MiB.
- The German debug build shares game code `AXVD` and software version byte `0` with German retail Rev 0, so it must be distinguished by hash and content rather than header version alone.

## Reconstruction rule

These files are read-only local references. Extraction results, source-form reconstructions, tools, manifests, tests, graphics, text, audio, and other non-ROM project artifacts belong in Git; complete ROM images do not.
