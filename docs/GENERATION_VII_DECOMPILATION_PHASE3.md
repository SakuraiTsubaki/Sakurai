# Generation VII Decompilation — Phase 3 Tracker

All six Generation VII main-series targets have Phase 3 evidence/diff tooling ready.

## Targets

| Family | Game | Platform | Pair comparison | Phase 3 status |
| --- | --- | --- | --- | --- |
| Alola | Pokémon Sun | Nintendo 3DS | Sun ↔ Moon | Tooling ready; target data pending |
| Alola | Pokémon Moon | Nintendo 3DS | Moon ↔ Sun | Tooling ready; target data pending |
| Alola | Pokémon Ultra Sun | Nintendo 3DS | Ultra Sun ↔ Ultra Moon | Tooling ready; target data pending |
| Alola | Pokémon Ultra Moon | Nintendo 3DS | Ultra Moon ↔ Ultra Sun | Tooling ready; target data pending |
| Let's Go | Pokémon: Let's Go, Pikachu! | Nintendo Switch | Pikachu ↔ Eevee | Tooling ready; target data pending |
| Let's Go | Pokémon: Let's Go, Eevee! | Nintendo Switch | Eevee ↔ Pikachu | Tooling ready; target data pending |

## Common Phase 3 tools

Each target repository contains:

- `tools/extract_binary_evidence.py`
- `tools/compare_binary_blocks.py`
- `tools/scan_pointer_candidates.py`
- `docs/PHASE_03_EVIDENCE_AND_DIFF.md`

The string-evidence tool omits literal string contents by default. The binary comparator stores hashes/status rather than bytes. The pointer scanner emits unverified candidates only inside researcher-supplied address ranges.

## Full pipeline now available

1. exact target identity / revision inventory
2. extracted-tree SHA-256 inventory
3. platform-specific executable layout mapping
4. RomFS structural classification
5. paired-version file inventory comparison
6. executable string/evidence indexing
7. fixed-block executable diff
8. pointer-candidate worklist inside verified mapped ranges
9. verified symbol/data worklist
10. progressive source reconstruction and matching

## Phase 4 gate

Phase 4 starts only from actual target evidence. For every build, record exact hashes and generate the relevant executable layout before assigning function names, data labels, or pointer identities.

The first Phase 4 artifact is a symbol/data worklist tied to exact build hashes. Sun/Moon, Ultra Sun/Ultra Moon, and Let's Go Pikachu/Eevee remain separate comparison pairs; addresses and labels are never inherited across families without verification.
