# Gold Fixed Bank Alignment — Phase 2

- Versions compared: 8
- KR Bank 00 labeled entry blocks: 45
- USA/Europe Bank 00 labeled entry blocks: 46
- KR semantic anchors aligned by established meaning: 19
- KR anonymous blocks with an exact normalized USA match: 22
- KR anonymous blocks with a high-confidence fuzzy match: 1
- KR blocks left unmatched: 3
- KR blocks with alignment score >= 0.80: 36 / 45
- Multi-version exact normalized block families: 39

## Method

The Phase 1 control-flow output is split at labeled entry points. Instruction mnemonics are normalized by replacing hexadecimal immediates/targets with `$IMM`, then hashed. This lets structurally identical blocks align even when localization moves code or changes addresses. Fuzzy matches use normalized instruction-sequence similarity and are explicitly marked as heuristic.

This phase **does not assign upstream semantic names to anonymous Korean labels**. It establishes cross-version equivalence first; semantic promotion happens only when an aligned upstream routine can be independently verified.
