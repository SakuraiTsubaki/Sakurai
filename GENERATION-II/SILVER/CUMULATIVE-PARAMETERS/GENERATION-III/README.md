# SILVER cumulative parameters — Generation III

This layer is intentionally built **before** the Generation-IV/HGSS evolution layer.

## Scope

- Canonical species: National Dex **#252 Treecko through #386 Deoxys** (135 species).
- Source of truth: `pret/pokeemerald` `master`, pinned by commit SHA in each generated manifest.
- Pokeemerald raw species IDs are preserved only as provenance. They are **not** canonical IDs: old-Unown placeholders make Treecko's raw ID start at 277, and Chimecho is stored after Deoxys in the GBA table.
- The output preserves Gen-III-only fields instead of squeezing them into the vanilla Silver 32-byte base-data record.

## Generated ledgers

`build_gen3_parameters.py` emits:

- `gen3_species_parameters.csv` — stats, types, catch rate, Gen-III EXP yield, 6-stat EV yield, held items, gender, egg cycles, friendship, growth curve, egg groups, abilities, Safari flee rate, body color/flip.
- `gen3_evolutions.csv` — evolution method/parameter/target.
- `gen3_levelup_learnsets.csv` — level-up moves.
- `gen3_tmhm_learnsets.csv` — Emerald TM/HM compatibility.
- `gen3_tutor_learnsets.csv` — Emerald move-tutor compatibility.
- `gen3_parameter_bundle.json` — normalized per-species bundle keyed by National Dex ID.
- `gen3_manifest.json` — source commit + SHA-256 provenance and engine requirements.

## Engine requirements carried forward

Silver does not natively model several Gen-III parameters. They stay in the canonical layer and will be routed later rather than discarded:

- Abilities
- six-stat EV yields / Gen-III EV-IV semantics
- Erratic and Fluctuating growth curves
- Wurmple personality-based evolution branch
- Nincada/Shedinja special evolution handling
- Feebas Beauty evolution
- Gen-III move/TM/tutor data needed by the new species

## Deoxys

Canonical species identity remains National Dex `386`. Form identity is a separate field in the cumulative engine. If the project chooses separate runtime slots for Normal/Attack/Defense/Speed forms, those slots still map back to canonical species 386 rather than inventing extra National Dex IDs.

## ROM policy

No original or derivative ROM is committed to GitHub. Generated ledgers, scripts, manifests, and later IPS/BPS patches are allowed project outputs.
