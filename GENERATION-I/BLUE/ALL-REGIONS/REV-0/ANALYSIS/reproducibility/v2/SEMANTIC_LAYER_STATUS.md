# Semantic layer status

The package currently guarantees **byte-exact whole-ROM coverage** for all six Blue ROMs and provides a stable scaffold for replacing raw chunks with decoded source.

## Proven
- Every ROM byte belongs to exactly one 0x100-byte scaffold chunk.
- Every physical 0x4000-byte bank is represented.
- ROM identity and header/global checksums are verified.
- Split/rebuild round trips are byte exact.
- Exact cross-version alignment runs contain only byte-identical data.
- Pointer tables are explicitly marked as hypotheses until a caller/format is proven.

## Not falsely claimed
Raw bytes are **not** automatically labeled as code, text, graphics, map data, audio, or tables without evidence. A blind linear disassembly would misclassify embedded data and is intentionally not treated as a complete semantic reconstruction.

## Promotion rule
A scaffold chunk may be replaced by `.asm`, `.inc`, text, graphics, map, or table source only when:
1. extractor -> source -> reassembler is lossless for that region;
2. all incoming references are accounted for;
3. the resulting ROM still matches the expected SHA-256 before intentional edits.

This keeps the corpus reproducible while allowing semantic coverage to increase monotonically.
