# Gold Structural Survey — Phase 1

This layer starts converting the whole-ROM reproducible corpus into classified source material. It does not redistribute ROM images.

Per ROM it records a control-flow-derived candidate disassembly for fixed Bank 00, symbol candidates, coverage ranges, header constants, entropy map, long zero/FF runs, pointer-table candidates, immediate-address candidates, and a machine-readable manifest.

`fixed_bank_cfg.asm` intentionally covers only instructions reachable from reset/RST/interrupt entry points via direct control flow. Unvisited bytes remain unclassified rather than being falsely treated as code.
