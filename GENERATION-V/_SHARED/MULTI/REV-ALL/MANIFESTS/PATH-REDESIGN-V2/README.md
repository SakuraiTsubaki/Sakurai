# Generation V path redesign v2

Status: canonical semantic redesign in progress.

## Canonical shape

`GENERATION-V / GAME / LANGUAGE-REGION / REV / WORK-TYPE / DOMAIN / SUBJECT`

### GAME

`BLACK`, `WHITE`, `BLACK2`, `WHITE2`, `_SHARED`.

Bundle labels such as `BW`, `BW-B2W2`, `BW-EUR-REV-UNKNOWN`, and `BW-MULTI-REGION` are provenance labels only and must not be structural axes.

### LANGUAGE-REGION

Use the existing canonical locale IDs. `MULTI` is valid only when an artifact genuinely spans multiple locales. The supplied Black/White SweeTnDs images are tracked as `EU-EN` provenance because that is the supplied distribution label; their internal IRBO/IRAO O-code is recorded separately as a USA/Europe English binary-family identifier.

### REV

The supplied Black and White images have ROM version byte `0`, therefore ROM-derived work from those images is `REV-0`. Dump quality (`SweeTnDs`, bad-dump classification, clean-dump verification state) is provenance metadata and must never be encoded as a revision folder.

`REV-ALL` is reserved for genuinely revision-independent specifications/tools. `REV-MIXED` and `REV-UNKNOWN` are not canonical destinations.

### Ownership rules

1. Direct ROM evidence belongs to the exact GAME/locale/revision that produced it.
2. Black-vs-White comparisons belong under `_SHARED/EU-EN/REV-0/DIFFS/BLACK-WHITE/...`.
3. BW1 structures shared by Black and White belong under `_SHARED/EU-EN/REV-0/.../BW1/...` when tied to the supplied ROMs, or `_SHARED/MULTI/REV-ALL/.../BW1/...` only when revision/locale-independent.
4. B2W2-only common research uses `_SHARED/.../.../.../B2W2/...`.
5. All-four-game Generation V research uses `_SHARED/MULTI/REV-ALL/.../ALL-GAMES/...`.
6. Runtime code, patches, builds, or converted assets that execute in Generation II/III are owned by the target generation. Their Generation V origin is provenance metadata, not their primary tree location.
7. Source-only Generation V format/schema research remains in Generation V even when later ports consume it.
8. One canonical copy per artifact. Other generations reference it by manifest path/hash rather than duplicating it.

## Standard domains below WORK-TYPE

`ROM`, `FILESYSTEM`, `EXECUTABLE`, `OVERLAYS`, `GAME-DATA`, `FIELD`, `MAPS`, `SCRIPTS`, `EVENTS`, `BATTLE`, `POKEMON`, `TRAINERS`, `ITEMS`, `MOVES`, `TEXT`, `UI`, `GRAPHICS`, `SPRITES`, `AUDIO`, `SAVE`, `COMMUNICATIONS`, `ONLINE`, `DISTRIBUTIONS`, `UNUSED`, `BUGS`, `LOCALIZATION`, `PORTS`.

## Current Gen V native inventory found in Sakurai

Legacy provenance groups discovered under the previous wrapper:

- `BW-B2W2/GAME-PARAMETERS`
- `BW-B2W2/PARTY-SCREEN`
- `BW-B2W2/STATUS-SCREEN`
- `BW-EUR-REV-MIXED/GAME-PARAMETERS`
- `BW-EUR-REV-UNKNOWN-SPRITES`
- `BW-EUR-REV-UNKNOWN/CORE-RECORD-DATABASES`
- `BW-EUR-REV-UNKNOWN/MAP-RELATION-GRAPH`
- `BW-EUR-REV-UNKNOWN/ROM-BASELINE-SWEETNDS`
- `BW-EUR-REV-UNKNOWN/ROM-DATA-CATALOG`
- `BW-EUR-REV-UNKNOWN/SCRIPT-EVENT-GRAPH`
- `BW-MULTI-REGION/PARAMETER-PORT`
- `BW-MULTI-REGION/ROM-INTEGRITY`

## Cross-generation Gen V material found outside Generation V

Sakurai also contains Generation II and III implementation/reference material whose subject is Gen V data. Tsubaki contains Generation III conversion/runtime outputs derived from Gen V. These are not to be dragged back into Generation V automatically: target-runtime artifacts stay with the target generation, while shared source schemas are referenced from Generation V by canonical path and hash.

## Migration principle

The previous migration preserved history but wrapped legacy path strings below `_SHARED/MULTI/REV-ALL`. V2 performs semantic decomposition: GAME, locale, revision, work type, and domain are separated into independent axes. Git history is the legacy-path archive; the current tree must not keep a second nested legacy hierarchy merely for compatibility.
