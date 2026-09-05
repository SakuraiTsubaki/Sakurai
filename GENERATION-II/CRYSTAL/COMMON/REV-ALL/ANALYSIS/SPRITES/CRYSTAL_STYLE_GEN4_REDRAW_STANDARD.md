# Crystal-style Gen IV sprite redraw standard

## Status
This document supersedes the automatic `HGSS PNG -> resize -> median-cut -> 2bpp` prototype for final sprite artwork.

## Target
Use Generation IV artwork/sprites (HGSS first; Platinum/Diamond/Pearl only when needed) as the **design and pose reference**, but redraw the result in the visual language of Pokémon Crystal rather than mechanically shrinking it.

## Core rule
A valid result is **not** a reduced HGSS image. It must read as a hand-authored Pokémon Crystal sprite at native resolution.

## Pixel-art requirements
1. Preserve a deliberate four-level 2bpp value structure. Every pixel must have a role: background/highlight, light/base plane, shadow plane, or deepest contour/detail.
2. Reconstruct lighting. Follow the light direction and plane logic visible in Crystal's original sprite work; highlights, form shadows, cast/occlusion shadows, and contour accents must describe volume rather than merely follow source RGB brightness.
3. Redraw the silhouette. Do not accept nearest-neighbour resizing as the final contour. Curves, horns, ears, tails, wings, limbs, leaves, flames, etc. must be re-pixelled so the silhouette reads cleanly at 5x5, 6x6, or 7x7 tiles.
4. Preserve anatomy and identity-critical details. Eyes, mouth, claws, markings, joints, facial planes and species-specific features may require one-pixel exaggeration so they remain readable at Game Boy Color scale.
5. Use selective outlining. Deepest pixels belong where separation, occlusion, or contour weight requires them; avoid a uniform black ring around the whole sprite.
6. Preserve material differences. Fur, scales, shell, metal, leaves, flame, water-like surfaces, etc. should not all receive the same shading pattern.
7. Do not use generic dithering to fake detail. Dither only where it serves an intentional texture or gradient and remains consistent with Crystal-era pixel art.
8. Keep the sprite readable at 1x native scale. Enlarged previews are for inspection only.
9. Front and back sprites are separate redraws. The back sprite must not be derived by a generic transform from the front.
10. Crystal's original sprite is a style/lighting/detail reference; HGSS is the pose/design reference. Neither source is copied blindly.

## Palette requirements
- Do not derive the final palette with a blind global median-cut.
- Build the palette around value roles first, then hue/chroma.
- Keep strong separation between light plane, mid/base plane, shadow plane, and deepest contour/detail.
- White/background may also function as intentional highlight where the original Crystal rendering language does so.
- Each species must be checked against both the original Crystal palette behaviour and the Gen IV reference colors.

## Production pipeline
1. Choose Gen IV reference pose (HGSS preferred).
2. Inspect original Crystal front/back sprite at native size and enlarged nearest-neighbour view.
3. Establish silhouette on the original Crystal tile canvas.
4. Place anatomy/identity-critical pixels.
5. Establish light direction and major planes.
6. Place deepest contour and occlusion pixels.
7. Add secondary detail and material cues.
8. Build/adjust the four-color GBC palette.
9. Inspect at 1x and enlarged view.
10. Encode to 2bpp, LZ-compress, round-trip verify, then insert into ROM.

## Acceptance gate
A sprite is not accepted merely because it is 2bpp, fits the tile dimensions, and compresses correctly. It must pass a visual review for silhouette, lighting, form, anatomy, palette separation, and native-scale readability.

## Rejected prototype
The previous automatic median-cut conversion remains useful only as a rough pose/layout reference. It must not be used as final artwork or as the source for final IPS releases.
