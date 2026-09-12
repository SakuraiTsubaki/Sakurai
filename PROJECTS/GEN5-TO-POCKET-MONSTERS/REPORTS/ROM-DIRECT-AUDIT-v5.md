# GEN5 → Pocket Monsters — direct ROM audit (v5)

Direct re-read of the 16 project ROM images in `/mnt/data` on 2026-09-12. ROM binaries are not GitHub artifacts.

## Canonical bindings

| Game | Platform | Release | Size | SHA-1 | Structural units |
|---|---|---|---:|---|---:|
| CRYSTAL | GBC | `JP-JA-HV0` | 2097152 | `95127b901bbce2407daf43cce9f45d4c27ef635d` | 128 |
| EMERALD | GBA | `BPEJ-HV0` | 16777216 | `d7cf8f156ba9c455d164e1ea780a6bf1945465c2` | 256 |
| FIRERED | GBA | `BPRJ-HV1` | 16777216 | `7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857` | 256 |
| LEAFGREEN | GBA | `BPGJ-HV0` | 16777216 | `5946f1b59e8d71cc61249661464d864185c92a5f` | 256 |
| RUBY | GBA | `AXVJ-HV0` | 8388608 | `5c5e546720300b99ae45d2aa35c646c8b8ff5c56` | 128 |
| SAPPHIRE | GBA | `AXPJ-HV0` | 8388608 | `3233342c2f3087e6ffe6c1791cd5867db07df842` | 128 |
| SILVER | GBC | `KR-KO-HV0` | 2097152 | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` | 128 |
| GOLD | GBC | `KR-KO-HV0` | 2097152 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | 128 |
| CRYSTAL | GBC | `US-EU-EN-HV1` | 2097152 | `f2f52230b536214ef7c9924f483392993e226cfb` | 128 |
| EMERALD | GBA | `BPEE-HV0` | 16777216 | `f3ae088181bf583e55daf962a92bb46f4f1d07b7` | 256 |
| FIRERED | GBA | `BPRE-HV1` | 16777216 | `c4d0119d9bcb36687f41a8f7ca72ab7af60558e4` | 256 |
| LEAFGREEN | GBA | `BPGE-HV1` | 16777216 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | 256 |
| RUBY | GBA | `AXVE-HV2` | 16777216 | `5b64eacf892920518db4ec664e62a086dd5f5bc8` | 256 |
| SAPPHIRE | GBA | `AXPE-HV2` | 16777216 | `89b45fb172e6b55d51fc0e61989775187f6fe63c` | 256 |
| BLACK | NDS-TWL | `IRBO-HV0` | 268435456 | `a68b3bedf5c1e53556e41e59cdf396c20b331896` | 484 |
| WHITE | NDS-TWL | `IRAO-HV0` | 268435456 | `f94d4578956487c09fee20809a591e858017769e` | 484 |

## Direct structural observations

- GBC targets: 16 KiB bank inventories were regenerated; all four headers/checksums are recorded in the audit.
- GBA targets: 64 KiB chunk inventories were regenerated; GBA header checksums validate for all ten supplied targets.
- Black/White: unit code `0x02` confirms the supplied images are TWL-enhanced (`NDS-TWL`), not plain `NDS-NTR` packages.
- Black/White each expose 484 FAT entries, 237 ARM9 overlays and 31 FNT directories in this direct scan.

## Same-offset unit comparison

- GOLD-KR ↔ SILVER-KR: 92/128 same-offset units byte-identical at 16384 bytes per unit.
- CRYSTAL-JP ↔ CRYSTAL-EN-HV1: 12/128 same-offset units byte-identical at 16384 bytes per unit.
- RUBY-JP ↔ RUBY-EN-HV2: 0/128 same-offset units byte-identical at 65536 bytes per unit.
- SAPPHIRE-JP ↔ SAPPHIRE-EN-HV2: 0/128 same-offset units byte-identical at 65536 bytes per unit.
- EMERALD-JP ↔ EMERALD-EN: 36/256 same-offset units byte-identical at 65536 bytes per unit.
- FIRERED-JP-HV1 ↔ FIRERED-EN-HV1: 93/256 same-offset units byte-identical at 65536 bytes per unit.
- LEAFGREEN-JP ↔ LEAFGREEN-EN-HV1: 84/256 same-offset units byte-identical at 65536 bytes per unit.

## Routing

- Release/dump/native-structure facts → Sakurai `LIBRARY`.
- Cross-release/cross-game factual deltas → Sakurai `COMPARE`.
- Port semantics/crosswalk/design → Sakurai `PROJECTS/GEN5-TO-POCKET-MONSTERS`.
- Converted insertion assets, build indexes and patches → Tsubaki project tree.
- Original ROM images and byte-identical bulk dumps → never committed.
