# Pokémon Crystal source-ROM direct audit — v6

Source: seven supplied 2 MiB Game Boy Color ROM images. Original ROM binaries are not committed.

## Identity result

Canonical release identity uses the verified four-byte token at ROM header `0x013F–0x0142` plus header version `HV<n>`:

- `BXTJ-HV0` — Japan / Japanese
- `BYTE-HV0` — USA/Europe / English, Rev 0
- `BYTE-HV1` — USA/Europe / English, Rev A
- `BYTD-HV0` — Germany / German
- `BYTF-HV0` — France / French
- `BYTI-HV0` — Italy / Italian
- `BYTS-HV0` — Spain / Spanish

All seven observed images are exactly 2,097,152 bytes / 128 × 16 KiB banks. All seven pass both Game Boy header checksum and stored global checksum verification.

## Structural comparison

Nine banks are byte-identical across all seven releases: `30`, `31`, `37`, `3B`, `3C`, `3D`, `4B`, `4C`, `7A`.

English `BYTE-HV0` → `BYTE-HV1` leaves 120/128 banks byte-identical. Only banks `00`, `10`, `11`, `3E`, `47`, `5C`, `7E`, and `7F` differ.

Zero-filled-bank layout differs substantially by release family:

- `BXTJ-HV0`: banks `60`–`7C` (29 banks).
- `BYTE-HV0`, `BYTE-HV1`: `75`, `76`, `79`, `7A`.
- `BYTD-HV0`, `BYTF-HV0`, `BYTI-HV0`, `BYTS-HV0`: `7A` only.

This proves that high-bank occupancy cannot be modeled as one language-independent Crystal layout.

## Repository routing

Sakurai owns release/dump identity, bank fingerprints, comparison facts, reverse-engineering notes, extraction/rebuild specifications, and verification evidence.

Tsubaki owns production-side source locks, asset catalogs/equivalence maps, transformed/normalized resources, patches, and build inputs.

Full ROMs and whole raw bank dumps stay outside GitHub.
