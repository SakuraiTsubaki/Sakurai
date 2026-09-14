# RGBYGSC-KANTO-START v12 recovery

Status: recovered to canonical live tree — 2026-09-14.

## Incident

The working tree at `GENERATION-II/GEN2-KANTO-START/` contained real RGBYGSC Kanto-start work but was not included as a migration source when later repository layouts were cut over. The legacy Generation-II root was subsequently retired, leaving the work reachable only through Git history.

## Sakurai recovery source

- final verified historical commit used for recovery: `e3b32a5c25863304d84348424e8735ad08a03ba6`
- historical subtree: `GENERATION-II/GEN2-KANTO-START/`
- recovered tree SHA: `b3b97e49fbc225a6a33df229e400da1d77228012`
- canonical destination: `CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/GEN2-KANTO-START/`
- recovered scope: surviving knowledge/control artifacts through Phase 15

The subtree is grafted by its exact Git tree SHA so the recovered files are byte-identical to the historical tree.

## Version audit

The v2-v4 `projects/gscrgby/` lineage was checked separately. Its own README defines the opposite engine direction: Generation II Kanto rebuilt for a Generation I engine. Those artifacts therefore correctly belong to `CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/` and are not duplicated into RGBYGSC-KANTO-START.

## Migration invariant

For every future repository-layout version:

1. enumerate every non-placeholder legacy project subtree before retiring a root;
2. assign each subtree exactly one canonical semantic owner;
3. compare source and destination tree/file coverage;
4. only remove the old live path after the destination is verified;
5. preserve Sakurai/Tsubaki semantic coordinates for paired projects;
6. never treat Git history alone as an acceptable replacement for a live project artifact.
