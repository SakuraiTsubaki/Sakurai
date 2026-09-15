# XY Generation VI public model-range ledger validation

## Result

**PASS — structural validation only.**

Validated file:

`source-ledgers/xy_model_ranges_public_gen6.csv`

Validator:

`tools/validate_xy_model_range_ledger.py`

## Structural checks

- ledger rows: **123**
- archive: **`a/0/0/7`**
- first recorded member: **6868**
- last recorded member: **7851**
- covered member span: **984 members**
- block size in this public mapping segment: **8 members per row**
- total represented block members: **123 × 8 = 984**
- National Dex new-species coverage: **650–721 inclusive = 72 species**
- explicit public-list label gaps: **4 blocks**
- overlapping ranges: **0**
- unrepresented member-number gaps inside 6868–7851: **0** because the four omitted labels are represented explicitly as unresolved rows

## Explicit unresolved blocks

| Range | Associated public-list neighborhood | Status |
| --- | --- | --- |
| 7708–7715 | between reported Pumpkaboo small and big blocks | unresolved label; no form name inferred |
| 7716–7723 | between reported Pumpkaboo small and big blocks | unresolved label; no form name inferred |
| 7740–7747 | between reported Gourgeist small and big blocks | unresolved label; no form name inferred |
| 7748–7755 | between reported Gourgeist small and big blocks | unresolved label; no form name inferred |

The existence of these contiguous blocks is structurally implied by the member-number sequence, but their semantic form names are **not** promoted from inference. They remain unresolved until supported by stronger member-level evidence.

## What this validation does not prove

This PASS does **not** mean the public species/form labels are retail-ROM verified.

It does not yet prove:

- individual member signatures inside each 8-member block;
- exact geometry/texture/animation role for every offset;
- X/Y byte identity;
- game loading behavior for every form/gender state;
- battle-idle animation selection;
- opponent/player camera state;
- exact canonical render transform;
- equivalence with ORAS members.

Those remain separate validation stages.

## Acceptance level

Current evidence level for normal labeled rows: **reported-public / requires-member-signature-verification**.

Current evidence level for the four missing labels: **observed-public-gap / unresolved**.

No row in this ledger is eligible to be labeled `confirmed-game-data`, `Observed`, `Matched`, or final `BATTLE_MASTER_V1` solely because this structural validation passes.
