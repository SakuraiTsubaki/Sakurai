# Upstream symbols/map bridge

The public `pret/pokecrystal` `symbols` branch exposes generated symbol and linker-map outputs for the English builds. These are not bundled here; this workpack records how they fit into the reconstruction pipeline.

Relevant upstream artifacts include:

- `pokecrystal.sym` / `pokecrystal.map` — USA/Europe Rev 0 source build symbols/layout.
- `pokecrystal11.sym` / `pokecrystal11.map` — USA/Europe Rev 1 source build symbols/layout.

Use these as the authoritative English symbolic-address bridge, then verify every address-bearing regional mapping against the supplied target ROM before promoting it to a JP/DE/ES/FR/IT symbol. Same-offset equality is strong evidence for reuse; unequal offsets require structural alignment, not blind address copying.

`upstream_bank_roles.csv` contains a deliberately coarse, paraphrased bank-role map derived from the pinned upstream linker layout. It is a navigation aid rather than a replacement for `.sym`/`.map` data.
