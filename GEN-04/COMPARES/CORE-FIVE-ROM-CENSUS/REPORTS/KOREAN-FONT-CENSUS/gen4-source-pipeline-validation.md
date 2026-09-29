# Generation IV Korean source-first pipeline validation

Date: 2026-09-29

Status: **validated** for the supplied Korean SoulSilver retail ROM `IPGK01 Rev.00` and the full modern Hangul build.

## Source

- ROM SHA-256: `8e1c82d2f718fa404f0b13df1666c70cdfaa75cb67e0adcbdcfb6c002f4d8b55`
- localized font archive: `a/0/1/6`
- archive file ID: `145`
- archive SHA-256: `58638e5171d526c59595ecd229b9be6fd3e0a8462688b1ced8dacae85ab0a56f`
- tested source font: member `1` (MESSAGE / 12 px Korean fixed advance)
- exact mapped source coverage used for modern Hangul: Wansung `2350` syllables
- compatibility jamo `51` are also extracted by the source-pack tool but are outside `U+AC00..U+D7A3` and therefore are not part of the 11,172-syllable full-modern test.

The extractor intentionally omits unresolved non-fallback slots `3427/3428`.

## Reproducible source extraction

Tool:

`extract-gen4-korean-font.py`

The source pack keeps each mapped Generation IV glyph as its original 64-byte 16×16 semantic 2bpp block. The compressed storage representation is deterministic gzip with `mtime=0`; raw source SHA-256 is recorded separately from compressed-file SHA-256.

Member 1 raw mapped-source SHA-256:

`99667821c84f39c4e2fd20a48d731547f0c9fb24dcec25a9df324f1c0e2d78c9`

## Full modern Hangul generator test

Generator input range:

`U+AC00..U+D7A3` = `11,172` modern Hangul syllables.

Result for `--sizes 16 --gen4-member 1`:

| source class | count |
| --- | ---: |
| `gen4_official` | 2,350 |
| `project_derived_vector` | 8,822 |
| total | 11,172 |

The first syllable `가` resolves to Generation IV slot `1024` and is tagged `gen4_official`. The final syllable `힣`, which is outside the Wansung source set, is tagged `project_derived_vector`.

## Exact-pixel verification

For every one of the 2,350 official Wansung syllables, the corresponding 64-byte block in the generated:

`glyphs_16x16_semantic2bpp.bin`

was compared against the extracted member-1 source block.

Result:

- compared official glyphs: `2350`
- byte mismatches: **0**
- exact source preservation: **PASS**

The complete 11,172-glyph semantic 2bpp output is `715008` bytes and has SHA-256:

`18783705cce4d9a9e8aa502f481f5c6302045d0a2343ea83f92ff6d7648fa2e9`

This hash includes both official source blocks and project-derived blocks and therefore is a build-output identity, not an official-ROM resource hash.

## Derived outputs

The following remain intentionally derived and must not be mislabeled as original Generation IV pixels:

- 8×8 glyph output
- 1bpp projection
- Game Boy planar 2bpp output
- modern Hangul outside the 2,350-syllable Wansung source set
- any manually overridden glyph

For original-pixel verification, use the semantic 2bpp source/output path only.

## Conclusion

Generation IV Korean source pixels are now integrated into the existing Hangul generator as the first-priority source. Official-covered 16×16 syllables no longer pass through vector rasterization, resampling, antialiasing or shape regeneration. Only missing modern syllables are generated as explicitly marked project derivatives.

This completes Korean-font census executable task 4. The next executable task is the Emerald multi-byte Korean token and 16px-capable runtime glyph lookup.
