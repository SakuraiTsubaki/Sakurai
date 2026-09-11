# Gen IV → Gen III composition reference v1

Native Emerald large-legendary reference values:

## Front
- Kyogre: `64×56`, `y_offset 4`
- Groudon: `64×64`, `y_offset 1`
- Rayquaza: `64×64`, `y_offset 0`

## Back
- Kyogre: `64×32`, `y_offset 19`
- Groudon: `64×56`, `y_offset 7`
- Rayquaza: `56×64`, `y_offset 0`

## Conclusion
There is no valid rule saying a large legendary should simply fill a 64×64 box. The target Generation III engine intentionally uses species-specific composition and `y_offset`.

Therefore v3 separates:
1. pixel-information preservation,
2. silhouette preservation,
3. Gen III composition / breathing room,
4. front-vs-back perspective.

Nearest-reference matching in the CSV is geometric only. It is not evidence that Dialga should literally copy Rayquaza's pose or scale, etc.

## Current finding
The v2 conversions fit the Gen III coordinate envelope surprisingly well in metadata, but several sprites touch the 64×64 boundary. Static non-clipping is therefore not enough for approval; silhouette breathing room, affine animation safety, and battle-screen visual density require separate review.
