# Pinned source-tree inventory

`index_upstream_source.py` turns a checkout of the pinned exact Green disassembly into a reproducible source/asset inventory without copying the upstream tree into this repository.

It emits `source_files.csv` with path/category/size/SHA-256, `include_edges.csv` with every quoted RGBDS `INCLUDE`/`INCBIN` dependency and resolution status, and `source_summary.csv` with category counts. Build products and Git/cache data are excluded.

This completes the provenance chain ROM byte → section/symbol → pinned source checkout → concrete source/asset file/dependency.
