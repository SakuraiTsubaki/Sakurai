# Candidate scanner semantics

The pointer/xref CSVs are deliberately conservative inventories:
- `far-pointer-candidates.csv`: every byte triplet shaped like `[bank, little-endian address]` with a valid switchable-ROM target.
- `code-xref-pattern-candidates.csv`: raw byte positions that resemble JP/CALL/RST opcodes and ROM addresses. These are not instruction-alignment claims.
- `memory-reference-candidates.csv`: raw byte positions resembling absolute/LDH memory references into SRAM/WRAM/OAM/IO/HRAM.
- `mbc-bank-switch-candidates.csv`: the common `LD A,imm8 ; LD [a16],A` pattern targeting the MBC bank-select register range.

These inventories are useful for proving/rejecting candidate free space and for bootstrapping a control-flow graph, but semantic confirmation must come from exact disassembly anchors or validated execution/data analysis.
