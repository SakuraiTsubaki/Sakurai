# BW animated sprite bbox cross-check — #643/#644/#646

Status: **external cross-check complete; ROM-primary v5 execution still pending in the local runtime**

This report exists to verify the clipping problem discovered in the early 96×96 reconstruction experiments. It does **not** replace ROM-primary geometry. The primary implementation source remains the uploaded BW ROM `/a/0/0/4` data and the NMAR→NMCR→NANR→NCER/NCGR scanner.

## External source

PokeAPI `sprites` repository, Generation V / Black-White / animated GIFs. These are used only as an independent visual/data cross-check.

Workflow: `.github/workflows/analyze-bw-animated-bboxes.yml`
Run: `34567920202`
Artifact: `bw-animated-bbox-crosscheck`

## Measured full-animation union envelopes

| Dex | Pokémon | Side | GIF logical size | Frames | Union bbox | Union size |
|---:|---|---|---:|---:|---|---:|
| 643 | Reshiram | front | 108×84 | 143 | (0,0)-(108,84) | **108×84** |
| 643 | Reshiram | back | 101×89 | 91 | (0,0)-(101,89) | **101×89** |
| 644 | Zekrom | front | 104×92 | 98 | (0,0)-(104,92) | **104×92** |
| 644 | Zekrom | back | 107×92 | 82 | (0,0)-(107,92) | **107×92** |
| 646 | Kyurem | front | 99×77 | 97 | (0,0)-(99,77) | **99×77** |
| 646 | Kyurem | back | 80×73 | 156 | (0,0)-(80,73) | **80×73** |

## Immediate conclusion

A fixed 96×96 source window is invalid as a preservation source for these animated BW battle sprites. The full front-animation union exceeds 96 pixels horizontally for all three tested species: Reshiram 108 px, Zekrom 104 px, Kyurem 99 px. Reshiram and Zekrom back-animation unions also exceed 96 px horizontally (101 px and 107 px).

Therefore any pipeline that performs `BW multipart composition → fixed 96×96 crop → downscale` can destroy source pixels **before** the downscale algorithm runs.

## Safe target envelopes from this external cross-check

With a 1-pixel margin on every side, the usable target area is 62×62 for a 64×64 Gen III canvas and 54×54 for a 56×56 Gen II canvas. Uniform aspect-preserving fit of the full animation envelope gives the following maximum envelopes (floor-rounded to avoid overflow):

| Dex | Side | Gen III 64×64 (inner 62) | Gen II 56×56 (inner 54) |
|---:|---|---:|---:|
| 643 | front | 62×48 | 54×42 |
| 643 | back  | 62×54 | 54×47 |
| 644 | front | 62×54 | 54×47 |
| 644 | back  | 62×53 | 54×46 |
| 646 | front | 62×48 | 54×42 |
| 646 | back  | 62×56 | 54×49 |

These are **safe-envelope constraints**, not final authored sprite dimensions. Final static/reanimated conversions must preserve battle anchors, feet/baseline, silhouette readability, and target-generation sprite grammar.

## ROM-primary acceptance rule

The external GIF result is supportive only. Final geometry must be accepted only after the uploaded ROM scanner produces:

1. exact NMAR timeline union for front and back;
2. data-wide conservative union covering all relevant NMAR animation cells / NMCR maps;
3. no analysis-canvas boundary contact;
4. valid NMAR→NMCR→NANR→NCER indices;
5. exact union contained inside the conservative union.

If the ROM and external GIF measurements differ, the ROM data wins and the difference is investigated rather than averaged away.
