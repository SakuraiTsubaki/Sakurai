# Repository topology

The project consumes 23 verified ROM images across Generation I and II and therefore is a true `CROSS-GEN` project.

## Identity axes

`release` describes official software identity; `dump` describes exact observed bytes; `target` describes a derived Korean project output. These IDs are never interchangeable.

## Key implementation references

- Korean Gold: `LIBRARY/GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0`
- Korean Silver: `LIBRARY/GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0`
- Korean implementation comparison: `LIBRARY/GEN-02/COMPARE/GOLD-AAUK-HV0--SILVER-AAXK-HV0`

## Non-negotiable routing

- source fact → `LIBRARY`
- cross-release/cross-game equality or delta → `COMPARE`
- translation/modernization design → Sakurai `PROJECTS/CROSS-GEN`
- production implementation/patch/build → Tsubaki `PROJECTS/CROSS-GEN`
- original ROM binaries → never committed
