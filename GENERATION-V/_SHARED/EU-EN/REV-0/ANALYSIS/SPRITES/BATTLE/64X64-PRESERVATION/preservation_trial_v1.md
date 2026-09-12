# BW sprite preservation downscale trial v1

Source: uploaded European Pokémon Black ROM, Pokegra `/a/0/0/4`.

Test species: #643 Reshiram, #644 Zekrom, #646 Kyurem.

The source stills used for this test are reconstructed animation frame 0 images from each species' multipart front battle graphic: parts NCGR + NCER + NANR + NMCR + normal NCLR palette. The composition canvas follows the BW multipart structure and the final test input is a 96×96 battle-sprite window.

Two target envelopes were tested independently from the 96×96 Gen V source: 64×64 for the Gen III-style target envelope and 56×56 for the Gen II-style target envelope. The 56×56 output is generated directly from the Gen V source, not by shrinking the 64×64 result again.

`nearest` is a direct nearest-neighbor resize and is retained only as a failure/control baseline. `preserve_v1` keeps the source visible palette exactly, restores silhouette pixels when meaningful source coverage would otherwise disappear, and restores small/rare same-color components when nearest sampling eliminates the entire component. It does not interpolate or invent new RGB colors.

Observed visible-color counts:

- Reshiram: source 9; 64 nearest 9; 64 preserve 9; 56 nearest 9; 56 preserve 9.
- Zekrom: source 12; 64 nearest 11; 64 preserve 12; 56 nearest 10; 56 preserve 12.
- Kyurem: source 14; 64 nearest 14; 64 preserve 14; 56 nearest 13; 56 preserve 14.

This is an automatic baseline, not a final cartridge-ready sprite. A final pass still needs species-by-species pixel review for silhouette weight, eyes/facial marks, thin appendages, high-contrast accents, and target-generation battle-screen placement. The intended production pipeline is source preservation -> direct per-target reduction -> pixel cleanup -> palette/placement validation -> in-engine test. Chained reduction (96 -> 64 -> 56) is prohibited for the production path.
