# Generation X BATTLE_MASTER_V1 — source selection

Research date: 2026-09-15

## Current conclusion

Generation X is still pre-release. No native 2D indexed battle-sprite format is currently established by the source set available to this project.

Therefore the first Generation X battle-sprite pass is a **true-color / 3D-source reconstruction track**, not an indexed-source preservation track.

This classification is provisional. If later official game data exposes native sprite, model, texture, render-target, atlas, or other stronger source material, the source ranking must be revisited and weaker reconstructions must not be treated as permanently authoritative.

## Official source classes currently available

### A. Japanese official transparent Pokémon artwork

The Pokémon Japan Winds/Waves site distributes four PNG source files. They are present byte-identically in both Winds and Waves upstream decompilation repositories and are now preserved in Tsubaki.

| Source | Subject | Canvas | RGBA colors | Alpha bbox | Status |
| --- | --- | ---: | ---: | --- | --- |
| `image_101.png` | ハブロウ | 960×960 | 13,582 | (103,53)-(851,891) | provisional canonical visual source candidate |
| `image_102.png` | ポムケン | 960×960 | 16,575 | (53,0)-(883,960) | provisional canonical visual source candidate |
| `image_103.png` | ミオリー | 960×960 | 19,217 | (55,132)-(902,825) | provisional canonical visual source candidate |
| `image_104.png` | カゼピカくん + ナミピカちゃん | 1536×960 | 59,322 | (3,90)-(1536,934) | combined source; per-subject split/source still required |

All four are RGBA true-color images containing substantial partially transparent pixels and thousands of RGBA colors. They therefore must **not** be treated as if they were native 16-color indexed sprites.

### B. Official 1st Trailer — 2026-02-27

The official Pokémon YouTube 1st Trailer is retained as an in-game/development-footage visual cross-check.

Use it for:

- model proportions;
- silhouette cross-checking;
- 3D body-volume interpretation;
- visible markings/details not clear in flat artwork;
- motion/pose behavior;
- relative presentation evidence when scenes permit it.

Do not treat a compressed trailer frame as a higher-quality pixel/color source than a lossless official transparent PNG unless a specific property is only available in the footage.

The trailer itself states that the shown game footage is under development and specifications may change.

## Provisional source ranking by subject

### ハブロウ

1. future verified game-internal model/texture/render data — not currently available;
2. `image_101.png` official lossless artwork — current static canonical candidate;
3. official 1st Trailer frames — geometry/motion cross-check;
4. other official regional assets if they contain higher-quality or different-angle evidence;
5. third-party mirrors only as verification/fallback.

### ポムケン

1. future verified game-internal model/texture/render data — not currently available;
2. `image_102.png` official lossless artwork — current static canonical candidate;
3. official 1st Trailer frames — geometry/motion cross-check;
4. other official regional assets;
5. third-party mirrors only as fallback.

### ミオリー

1. future verified game-internal model/texture/render data — not currently available;
2. `image_103.png` official lossless artwork — current static canonical candidate;
3. official 1st Trailer frames — geometry/motion cross-check;
4. other official regional assets;
5. third-party mirrors only as fallback.

### ピカチュウ（カゼピカくん） / ピカチュウ（ナミピカちゃん）

`image_104.png` is a combined 1536×960 artwork containing both subjects. It is authoritative as a public official combined visual source, but it is not yet sufficient by itself to define two independently provenance-complete sprite source files without a documented split.

Priority:

1. search for official individual images/model/render data for each subject;
2. if none exist, derive deterministic per-subject source crops/masks from `image_104.png` while preserving the untouched combined original;
3. record split rectangle/mask, source hash, derived-source hash, and validation;
4. never overwrite or replace the combined source with the split derivatives.

## Why automatic 16-color extraction is rejected

The official PNGs have 13k–59k distinct RGBA values because they are true-color rendered/illustrated assets with antialiased/partially transparent edges and shading.

Selecting the fifteen most frequent opaque colors would overweight broad body regions and can erase low-frequency identity-critical colors such as eyes, small markings, highlights, accessories, or special Pikachu distinguishing details.

Any automatic palette candidate must therefore be treated only as an intermediate proposal and must incorporate more than raw frequency. Visual acceptance remains mandatory.

## Planned reconstruction stages

1. preserve official source bytes and SHA-256;
2. inventory alpha/color/bounds and source provenance;
3. gather additional official visual evidence, especially individual special-Pikachu sources and in-game views;
4. create deterministic full-canvas 64×64 geometry/silhouette candidate without AI/generative processing;
5. construct an identity-aware <=16-entry target palette;
6. map to indexed target with transparency index 0;
7. generate PNG, BGR555 palette, 4bpp tiled graphics and compressed graphics;
8. decode/decompress round-trip validation;
9. visually compare source and target;
10. apply only documented minimal manual pixel corrections when necessary;
11. global rendered-pixel SHA-256 deduplication while retaining all Winds/Waves logical mappings.

## Approval state

No current Generation X subject has passed the final Generation III insertion acceptance gate yet. The current work is source preservation and canonical-source qualification, which is a required prerequisite rather than a finished sprite conversion.
