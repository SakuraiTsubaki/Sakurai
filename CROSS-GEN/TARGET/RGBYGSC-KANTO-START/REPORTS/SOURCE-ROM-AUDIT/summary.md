# RGBYGSC Kanto Start — supplied ROM audit

Directly re-read from the supplied GB/GBC project files on 2026-09-13.

- File observations: **16**
- Unique byte images / dump locks: **15**
- Games covered: **RED, GREEN, BLUE, YELLOW, GOLD, SILVER, CRYSTAL**
- Generations covered: **GEN-01 + GEN-02**
- Header checksums valid: **16/16**
- Global checksums valid: **16/16**
- 16 KiB bank observations: **1,312**
- Cross-release shared bank-hash groups: **235**
- Primary implementation base: **GEN-02 / SILVER / AAXK-HV0 / PROJECT-cb22d7e0 (Korean Silver)**

## Exact duplicate observation

`Pokemon - Yellow Version (USA, Europe).gbc` and `Pokemon - Yellow Version - Special Pikachu Edition (USA, Europe) (GBC,SGB Enhanced).gb` are byte-identical. Both have SHA-256 `8cbaa499397e4f1a679c992ea9382a2dd7942ab398b48c19829c2d9529de47bf` and therefore share the canonical dump lock `USER-UPLOAD-cc7d0326`. Both filenames remain recorded as provenance observations.

## Repository routing

- **Sakurai**: identity, hashes, headers, bank fingerprints, source comparisons, map/event/tileset/sprite research, specifications and verification.
- **Tsubaki**: source locks, extraction/materialization tooling, production catalogs, normalized/converted assets, implementation, patches, build metadata and production verification.
- **ROM binaries**: excluded from both repositories.

The project lives at `CROSS-GEN/TARGET/RGBYGSC-KANTO-START/` because it intentionally integrates Generation I material into a Generation II runtime target.
