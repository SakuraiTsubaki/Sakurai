# Stage 4 generated ledgers

The complete generated CSV ledgers are included in the local Stage 4 package and are reproducible with `build_sprite_stage4.py`. This index records their exact final hashes and row counts so generated outputs can be integrity-checked without committing ROM data.

| File | Rows including header | SHA-256 |
|---|---:|---|
| `hgss_core_manifest.csv` | 3,945 | `d06f489df086b7c0a22176cc7fd82a071a6c1d9eed80277771539d6c1892cace` |
| `hgss_form_manifest.csv` | 318 | `3858392b256d1c07335cd78f144930e46b52156f4f03e064c80f63481c4c8a30` |
| `sprite_lineage_493.csv` | 494 | `fdf9a42e9cd4c9ee940e69d1a2fbda987005f855bf6936989ded65e48c91b60f` |

## Contact-sheet integrity

| File | SHA-256 |
|---|---|
| `hgss_kanto_front_sheet.png` | `8d7e5fd872b37ff7fa9fa71da84c680d746509dfbf3d0ae5cfa621f803562b89` |
| `hgss_johto_front_sheet.png` | `bcbfed52c94acba93ddbc0d8043be3fc6b48bbd78c4eeac7f01352f56bfeb318` |
| `hgss_hoenn_front_sheet.png` | `544c04608497bfd5cfdf06a67ba2d5d5b06b83792ea0428e05638efec9d51d4e` |
| `hgss_sinnoh_front_sheet.png` | `7668f1c460d65203b2fe8acb296332f12ecee727b24a7a1af61e4b5e20926fbb` |
| `hgss_forms_front_sheet.png` | `593502078738fd4916b3d879e45a9180c2c83de1097416d1e4b9b8863f101a24` |

## Reproducibility rule

Do not compare encrypted NCGR bytes across DP and Pt/HGSS directly. Diamond/Pearl uses the reverse-direction sprite stream decryption while Platinum/HGSS uses the forward-direction variant. Cross-version lineage must compare canonical decrypted NCGR data plus palette members.

No ROM binaries or extracted raw ROM members are committed here.
