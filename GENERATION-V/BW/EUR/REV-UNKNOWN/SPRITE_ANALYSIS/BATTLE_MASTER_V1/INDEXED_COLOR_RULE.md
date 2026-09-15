# Indexed color preservation

For indexed Generation IV/V battle-sprite sources, the conversion operates on source palette indices.

It must not render to true-color RGB, resize, and then infer a replacement palette. Output pixels are selected from indices already present in the source palette relationship.

Automatic “most frequent 15 colors” reduction is prohibited because low-frequency colors can be species-defining details.
