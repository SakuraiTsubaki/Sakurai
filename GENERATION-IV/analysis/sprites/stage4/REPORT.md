# Generation IV Sprite Census — Stage 4

## Result

This stage performs complete HGSS battle-sprite extraction from the user-supplied ROM and builds a DP → Platinum → HGSS lineage ledger. ROM bytes are not included in repository artifacts.

- HGSS main battle archive: `a/0/0/4`, **2964 members = 494 × 6**.
- Main group layout: 4 encrypted NCGR graphics + normal/shiny NCLR palettes.
- Ordinary species slots: 1–493.
- HGSS alternate-form archive: `a/1/1/4`, **261 members**.
- HeartGold/SoulSilver main archive identical: **True**.
- HeartGold/SoulSilver alternate-form archive identical: **True**.
- Diamond/Pearl main archive identical: **True**.

## Extracted HGSS ordinary battle sprites

Each species has logical slots for female back, male back, female front, male front, each rendered with normal and shiny palettes. Empty gender-difference NCGR slots are preserved as empty in the manifest rather than duplicated.

- Rendered PNGs: **3,616**
- Empty logical variant/palette rows caused by absent gender-specific graphics: **328**
- Manifest: `hgss_core_manifest.csv`

## Alternate forms

Runtime formulas from `pret/pokeheartgold/src/pokemon.c` were used to map character and palette member IDs. Covered form families: Deoxys, Unown, Castform, Burmy, Wormadam, Shellos, Gastrodon, Cherrim, Arceus, Shaymin, Rotom, Giratina and Pichu (including Spiky-eared Pichu), plus egg, Manaphy egg, Substitute and battle shadow special resources.

- Rendered alternate/special PNGs: **317**
- Manifest: `hgss_form_manifest.csv`

## Cross-version lineage

Species-group equality is canonicalized across all six members: DP NCGR members are decrypted with the DP cipher, Platinum/HGSS NCGR members with the Pt/HGSS cipher, and palettes are compared directly. This removes encryption-format noise and reflects actual sprite-resource equality.

| Comparison | identical species groups | changed groups |
|---|---:|---:|
| Diamond/Pearl base → Platinum active | 5 | 488 |
| Platinum active → HGSS active | 229 | 264 |
| Diamond/Pearl base → HGSS active | 5 | 488 |

Full per-species member-level differences are in `sprite_lineage_493.csv`. This is the basis for the project priority rule **HGSS first → Platinum fallback → Diamond/Pearl fallback**.

## Comparison correction recorded during Stage 4

An early lineage pass compared encrypted NCGR member bytes directly. Because Diamond/Pearl and Platinum/HGSS use different sprite-stream decryption directions, that raw comparison falsely made all 493 DP → Platinum species groups appear changed. The lineage pass was corrected before finalization to compare canonical decrypted NCGR payloads plus palette data.

- Correct DP → Platinum result: **5 identical / 488 changed**.
- The five unchanged species groups are National IDs **201, 351, 386, 421, 423**.
- This correction is retained here so future stages do not regress to encrypted-byte comparison.

## Validation

- Main sprite NCGR data decrypts with the Platinum/HGSS stream cipher and renders correctly at 80×80.
- The HGSS `otherpoke` index layout matches `pret/pokeheartgold/files/poketool/pokegra/otherpoke.txt`.
- Runtime form selection formulas match `pret/pokeheartgold/src/pokemon.c`.

## Generated local package

The user-facing ZIP contains extracted PNGs, CSV ledgers, contact sheets, this report and the reproducible extractor. The repository should keep the report/ledgers/tooling; ROM files themselves are never committed.
