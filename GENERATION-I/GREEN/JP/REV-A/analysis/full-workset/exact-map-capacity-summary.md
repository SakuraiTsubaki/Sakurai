# Exact build-map capacity summary

Pinned upstream `symbols` build maps report:

| Revision | ROM0 used | ROM0 free | ROMX used | ROMX free | ROMX banks |
|---|---:|---:|---:|---:|---:|
| REV-0 | 16,384 | 0 | 507,903 | 1 | 31 |
| REV-A | 16,384 | 0 | 507,904 | 0 | 31 |

Therefore the stock 512 KiB image has effectively no linker-reported ROM space available. Homogeneous 0x00/0xFF runs found by raw heuristics are **not** free-space declarations; many belong to intentionally preserved data/garbage/padding sections required for byte-identical reconstruction.

Any substantial engine/data expansion should plan for ROM expansion and explicit bank/layout changes rather than assuming filler-looking runs are safely reusable.
