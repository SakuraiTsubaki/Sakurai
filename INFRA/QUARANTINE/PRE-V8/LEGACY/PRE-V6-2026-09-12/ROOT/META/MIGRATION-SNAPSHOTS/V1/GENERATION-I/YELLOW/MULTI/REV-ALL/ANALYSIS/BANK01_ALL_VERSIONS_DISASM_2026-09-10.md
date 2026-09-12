# Bank 01 — all 9 ROM recursive disassembly status (enriched seeds)

Function seeds for EN and JP Rev D come from exact-matching public `.sym` builds. Other builds receive a function start only when either a unique exact-byte anchor or a unique 6–14-instruction opcode signature proves the mapping. Recursive control-flow discovery then follows direct intra-bank calls/jumps.

| ROM | proven seeds | instruction starts | candidate code bytes | coverage | local targets | byte representation |
|---|---:|---:|---:|---:|---:|---|
| EN | 35 | 3,653 | 7,711 | 47.064% | 341 | PASS |
| FR | 35 | 3,649 | 7,706 | 47.034% | 340 | PASS |
| DE | 35 | 3,650 | 7,705 | 47.028% | 341 | PASS |
| IT | 35 | 3,646 | 7,697 | 46.979% | 340 | PASS |
| ES | 35 | 3,649 | 7,706 | 47.034% | 340 | PASS |
| JP0A | 34 | 3,524 | 7,478 | 45.642% | 331 | PASS |
| JPB | 35 | 3,545 | 7,527 | 45.941% | 331 | PASS |
| JPC | 35 | 3,545 | 7,527 | 45.941% | 331 | PASS |
| JPD | 35 | 3,545 | 7,527 | 45.941% | 331 | PASS |

All nine mixed ASM representations preserve exactly 16,384 source bytes when raw instruction bytes plus DB regions are recombined. This is a byte-preservation check, not yet an RGBDS semantic rebuild proof.

Next: add canonical section/data boundaries and convert auto labels into shared semantic labels, then run the same integrated process on Bank 03.
