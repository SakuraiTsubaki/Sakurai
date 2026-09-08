# Semantic workspace extension status

- Canonical ROMs: **9**
- Banks mapped per ROM: **64**
- Bank instances in atlas: **576**
- EN layout sections recorded: **148**
- Relationship × bank diff rows: **512**
- Unique bank hashes rendered as raw 2bpp inspection sheets: **473**
- Full bank instances mapped to those sheets: **576**
- Full relationship heatmaps: **8**
- Literal 00/FF free-space candidate runs (>=16 bytes): **4408**
- Pinned pret semantic commit: `e89ead154b9968aa50eed9328ff2b38b6c194382`
- Pinned EN symbol Git blobs: `.sym` `ec51cf4c4944ece30fd3f2dbb3197b996fd20a97`, `.map` `718762330b33bef8f4329402a36d2932447de27d`

The literal 2bpp views, free-space scans, pointer scans, and text scans are discovery aids. The EN section order is source-backed by the pinned linker layout; exact section ranges/symbols are reproducibly materialized from the pinned symbols branch.
