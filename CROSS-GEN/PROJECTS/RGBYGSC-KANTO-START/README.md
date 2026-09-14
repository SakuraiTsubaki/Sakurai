# RGBYGSC Kanto Start

Canonical knowledge/control-plane project under repository layout v12.

The game uses the Generation II engine and starts a new adventure in Kanto. Generation I RGBY Kanto is restored into and integrated with Generation II GSC Kanto. Larger structures are preserved; source maps, rooms, NPCs, events and interactions are not deleted merely to fit the Generation II layout.

Primary runtime anchor: Korean Silver `AAXK-HV0` / `DUMP-SHA256-EBBAC63C0C4309C8`.

Sakurai owns identity, provenance, direct ROM observations, reverse-engineering research, comparisons, specifications, mapping tables, analysis tools and verification evidence. Production assets and implementation live at the same project coordinate in `SakuraiTsubaki/Tsubaki`.

## Recovered working tree

The historical `GENERATION-II/GEN2-KANTO-START/` working tree was accidentally omitted during the repository-version migrations. It is restored here as a live canonical child:

`CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/GEN2-KANTO-START/`

This recovered Sakurai tree contains the surviving Kanto-start research/control work through Phase 15, including Pallet Town surveys, collision conversion, integrated tileset analysis, RGBY intro/fidelity work, palette-selector documentation and static regression evidence.

Future repository-layout migrations must move this child atomically with `RGBYGSC-KANTO-START`; it must never be removed from the old live path until destination coverage is verified.

`projects/gscrgby/` from repository layouts v2-v4 is a different project direction (Generation II Kanto rebuilt for a Generation I engine) and remains correctly owned by `CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`.

ROM images are never committed.
