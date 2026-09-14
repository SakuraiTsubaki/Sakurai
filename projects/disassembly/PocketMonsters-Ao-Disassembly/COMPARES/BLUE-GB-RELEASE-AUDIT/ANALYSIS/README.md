# Pokémon Blue GB release audit

Status: verified from the six user-uploaded source ROMs on 2026-09-13.

## Scope

This audit covers Japanese, English, German, Spanish, French, and Italian Pokémon Blue source images. ROM binaries are not committed. The repository stores identity, hashes, header observations, per-bank cryptographic hashes, pairwise comparisons, and reproducible tooling.

## Verified observations

- All six images report header version `0`.
- All six pass both the Game Boy header checksum and global checksum.
- `JP-JA-HV0` is 524,288 bytes (32 × 16 KiB banks).
- The five Western releases are 1,048,576 bytes (64 × 16 KiB banks).
- Across every pair of Western releases, banks `27` and `45–63` are byte-identical.
- Between the Japanese release and each Western release, bank `27` is byte-identical within the shared 32-bank range.
- The audit does not treat identical or padding-like banks as disposable; later reverse engineering must determine whether each bank is content, reserve capacity, or structural padding before reuse.

## Canonical coordinates

Release identity lives under:

```text
GEN-01/BLUE/RELEASES/GB/CART/<RELEASE-ID>/
```

Exact observed images are represented only by metadata under:

```text
DUMPS/DUMP-SHA256-<FIRST-16-UPPERCASE>/OBSERVATION.json
```

Cross-release results for this audit live under `GEN-01/BLUE/COMPARES/BLUE-GB-RELEASE-AUDIT/`.

## Next reverse-engineering layer

The next layer should classify banks and subregions by code, text, maps, graphics, audio, tables, free space, and unused/development remnants, then attach each derived artifact to the same release/dump coordinates. Lossless raw bank splitting is intentionally not committed because it would merely reconstruct the ROM binary.
