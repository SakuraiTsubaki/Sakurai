# Banks $10–$1F deep dive

## Summary

This range contains Pokédex/evolution engine code plus the first large Pokémon picture block. The strongest structural result is a clean graphics lineage split:

- **JP/KR graphics lineage:** Korean Gold, Japanese Rev 0, and Japanese Rev A are byte-identical in `$12` and every picture bank `$15–$1F`.
- **Western graphics lineage:** English, Spanish, German, French, and Italian Gold are byte-identical in those same banks.
- Therefore the uploaded ROMs contain two exact picture-data families, not eight independent localized copies.

| Bank | Role | JP Rev0↔A | Western localization relation | KR relation | Finding |
|---:|---|---:|---|---|---|
| `$10` | Pokédex/moves/evolution + evolutions/attacks | 0 | heavily relocated/localized vs EN | heavily differs from EN | semantic engine role shared, layout not portable by address |
| `$11` | events/battle/Pokédex2/start battle/mail; JP packs additional Pokédex/mail material here | 0 | ~2,024–2,029 byte deltas vs EN | 2,155-byte delta vs EN | structurally close in non-JP localizations, but Japanese packing must be treated separately |
| `$12` | Pokémon pic pointers + pics 1 | 0 | **ES=EN=DE=FR=IT exactly** | **KR=JP Rev0=JP RevA exactly** | first exact two-lineage graphics split |
| `$13` | EN/KR/European reserved zero; JP map scripts 1 | 0 | all zero | all zero | Japanese-only semantic use at same physical bank number |
| `$14` | party/stats/base stats + egg pic | **2 bytes** | large regional deltas | large regional delta | mixed code+data; one of the ten Japanese revision banks |
| `$15` | Pokémon pics 2 | 0 | **all five Western byte-identical** | **KR byte-identical to both JP revisions** | exact graphics-family split |
| `$16` | Pokémon pics 3 | 0 | same | same | exact graphics-family split |
| `$17` | Pokémon pics 4 | 0 | same | same | exact graphics-family split |
| `$18` | Pokémon pics 5 | 0 | same | same | exact graphics-family split |
| `$19` | Pokémon pics 6 | 0 | same | same | exact graphics-family split |
| `$1A` | Pokémon pics 7 | 0 | same | same | exact graphics-family split |
| `$1B` | Pokémon pics 8 | 0 | same | same | exact graphics-family split |
| `$1C` | Pokémon pics 9 | 0 | same | same | exact graphics-family split |
| `$1D` | Pokémon pics 10 | 0 | same | same | exact graphics-family split |
| `$1E` | Pokémon pics 11 | 0 | same | same | exact graphics-family split |
| `$1F` | Unown pic pointers + pics 12 | 0 | same | same | exact graphics-family split continues through Unown bank |

## Exact grouping

For every bank in `$12,$15,$16,$17,$18,$19,$1A,$1B,$1C,$1D,$1E,$1F`, SHA-1 grouping is exactly:

1. `KR + JP Rev0 + JP RevA`
2. `EN + ES + DE + FR + IT`

This means those graphics banks can be deduplicated into two provenance groups during analysis. They should still remain logically referenced by every target ROM, but there is no need to independently reverse identical copies.
