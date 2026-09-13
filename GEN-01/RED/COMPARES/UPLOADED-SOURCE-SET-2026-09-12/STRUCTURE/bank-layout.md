# Pokémon Red uploaded-source bank layout

Scope: the 8 uploaded `.gb` files observed on 2026-09-12, resolving to 7 unique byte images/releases.

## Japanese releases

- `JP-JA-HV0`: 512 KiB, 32 × 16 KiB banks, MBC1+RAM+BATTERY.
- `JP-JA-HV1`: 512 KiB, 32 × 16 KiB banks, MBC1+RAM+BATTERY.
- Neither Japanese image contains a fully zero-filled 16 KiB bank.

## International releases

- `US-EU-EN-HV0`: 1 MiB, 64 banks, MBC3+RAM+BATTERY.
- `EU-DE-HV0`, `EU-FR-HV0`, `EU-IT-HV0`, `EU-ES-HV0`: 1 MiB, 64 banks, MBC5+RAM+BATTERY.
- In all five international releases, banks `2D` through `3F` are fully zero-filled.
- That is 19 × 16 KiB = 304 KiB of bytewise-empty ROM space per international release.
- Empty bytes are not automatically safe expansion space until pointer/reference and mapper behavior are verified for the target build.

## Structural routing

Release-specific facts belong below `LIBRARY/GEN-01/GB/RED/RELEASES/<RELEASE-ID>/`.
Cross-release conclusions such as the shared `2D-3F` empty-bank region belong in this comparison tree.
Original ROM payloads are not committed.
