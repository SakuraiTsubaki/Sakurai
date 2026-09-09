# Pokémon FireRed — exhaustive 16 KiB analytical-bank census (pass 1)

Date: 2026-09-10

## Scope

Eight uploaded 16 MiB FireRed ROM images were read without modification. GBA does not use the GB/GBC switchable-ROM-bank model, so this survey defines an **analytical bank** as a fixed `0x4000`-byte (16 KiB) chunk. Each ROM therefore contains 1024 analytical banks (`0x000`–`0x3FF`).

ROM IDs used by the scripts:

- `JP_R0` — Pocket Monsters - Fire Red (Japan)
- `JP_R1` — Pocket Monsters - Fire Red (Japan) (Rev 1)
- `EN_R0` — Pokemon - Fire Red Version (USA)
- `EN_R1` — Pokemon - Fire Red Version (USA, Europe) (Rev 1)
- `DE_R0`, `FR_R0`, `IT_R0`, `ES_R0`

For each of the 8192 ROM/bank instances the census records SHA-1, entropy, FF ratio, 00 ratio, aligned ROM-pointer-like words, revision byte differences, and cross-ROM identity groups.

## Structural result

| Banks | File offsets | Count | Class | Meaning |
|---|---|---:|---|---|
| `000–1B1` | `000000–6C7FFF` | 434 | JP+EN revision changed | Both JP and EN Rev0/Rev1 differ |
| `1B2–1C6` | `6C8000–71BFFF` | 21 | EN revision changed only | JP revisions stable; EN revisions differ |
| `1C7–2FF` | `71C000–BFFFFF` | 313 | all-eight FF | byte-identical all-FF in every ROM |
| `300–3AC` | `C00000–EB3FFF` | 173 | revision-stable regional tail | stable within revisions, varies by language/region |
| `3AD–3BF` | `EB4000–EFFFFF` | 19 | all-eight FF | byte-identical all-FF in every ROM |
| `3C0–3CE` | `F00000–F3BFFF` | 15 | revision-stable regional tail | stable within revisions, varies by language/region |
| `3CF–3F7` | `F3C000–FDFFFF` | 41 | JP revision changed only | JP Rev0/Rev1 differ; EN revisions stable |
| `3F8–3FE` | `FE0000–FFBFFF` | 7 | all-eight FF | byte-identical all-FF in every ROM |
| `3FF` | `FFC000–FFFFFF` | 1 | EN revision changed only | EN pair differs; includes final-byte difference |

Class totals: 434 JP+EN revision-changed, 22 EN-only changed, 41 JP-only changed, 188 revision-stable language/region variants, 339 all-eight FF = 1024 banks.

## Revision-level findings

- JP Rev0 ↔ Rev1: 549/1024 banks identical, 475 changed; total changed bytes: 7,016,197.
- EN Rev0 ↔ Rev1: 568/1024 banks identical, 456 changed; total changed bytes: 6,367,135.
- Longest JP identical run: banks `1B2–3CE` (541 banks).
- Longest EN identical run: banks `1C7–3FE` (568 banks).
- All eight ROMs share 339 identical banks. Three long all-eight FF runs account for all of them: `1C7–2FF`, `3AD–3BF`, `3F8–3FE`.

## Main-payload / tail boundary observations

The first major all-eight FF run begins at file offset `0x71C000`. This is a strong structural boundary for the localized main payloads in this first-pass map, but it is **not yet declared the semantic end of game data** because later non-FF tail regions exist from `0xC00000` onward and must be classified separately rather than discarded as padding.

The high-address regions show repeated/shifted binary patterns across languages. These are retained as `regional tail data` pending semantic identification.

## Source-image verification flag

The two uploaded English images pass their internal GBA header checks, but their whole-ROM hashes do **not** match the standard English FireRed hashes targeted by the current `pret/pokefirered` decompilation or a verified physical Rev-1 cartridge dump:

- uploaded EN_R0 SHA-1: `d3b806453369b4b086c792eb3c05a02f00057f50`
- pret FireRed Rev0 target SHA-1: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`
- uploaded EN_R1 SHA-1: `c4d0119d9bcb36687f41a8f7ca72ab7af60558e4`
- pret / verified physical Rev1 SHA-1: `dd5945db9b930750cb39d00c84da8571feebf417`

Therefore EN_R0 and EN_R1 remain usable as the uploaded project sources, but are flagged **external-reference mismatch / investigate**. No assumption is made yet about whether the discrepancy is meaningful game data, dump-tail data, or prior modification.

References:

- https://github.com/pret/pokefirered
- https://gbhwdb.gekkio.fi/cartridges/AGB-BPRE-1/fexcollects-1.html

## Next pass

Pass 2 should classify each non-FF analytical bank semantically by combining pointer targets, text/string tables, script signatures, graphics/LZ blocks, audio structures, ARM/Thumb code ranges, and public decompilation symbol cross-reference. The 1024-bank map from this pass is the immutable coarse index for that work.
