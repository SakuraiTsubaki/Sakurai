# Key Findings — Pokémon Ruby ROM Set

## Corpus

- 13 supplied ROMs verified.
- Japanese `AXVJ` is 8 MiB.
- English/German/French/Italian/Spanish builds are 16 MiB.
- All 13 GBA header complement checksums validate.
- 13/13 deterministic 1 MiB split/rebuild round-trips reproduce the exact source SHA-256.

## Revision pattern

The retail German, French, Italian and Spanish Rev 0 → Rev 1 pairs each differ by exactly four bytes. The English Europe Rev 1 → USA/Europe Rev 2 pair also differs by four bytes.

- Header software version: offset `0x000000BC`.
- Header complement: offset `0x000000BD`.
- German/French/Italian/Spanish code changes: `0x00009367` (`DD→DB`) and `0x0000938B` (`DC→DA`).
- English Europe Rev 1 → Rev 2 code changes: `0x0000919B` (`DD→DB`) and `0x000091BF` (`DC→DA`).

The English USA Rev 0 versus Europe Rev 1/2 lineage and the German Debug build show large rebuild-level differences; those pairs are represented by changed-page maps plus deterministic range-regeneration tooling rather than a huge committed byte-range listing.

## Whole-ROM coverage

- 3,200 x 64 KiB page fingerprints cover every byte of every supplied ROM with no gaps.
- 40,987 structurally valid, 4-byte-aligned GBA BIOS-LZ77 (`0x10`) candidates were indexed in the generated local report.
- 443 revision changed-page records summarize all same-language pair comparisons.

No original ROM bytes are included in the GitHub-safe package.
