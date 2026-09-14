# GOLD-KR Phase 05 — Oak early-game branch

## Goal
Add an early-game Professor Oak branch to the Korean Gold GEN2 Kanto Start build without deleting or overwriting the original late-game Oak behavior.

## Verified Korean Gold locations
- Oak's Lab map: `0D:06`
- Original Oak Lab scripts: bank `59`
- Original Oak object script: `59:56BF`
- Original Oak Lab event table: `59:5C6C`
- Phase 03 relocated working event table: `59:6000`
- Oak object script pointer inside relocated table: `59:6069`

## Phase 05 insertion
- Oak wrapper: `59:6200`
- Pre-starter Korean text: `59:6240`
  - `오박사 포켓몬을 골라 보렴`
- Post-starter Korean text: `59:6280`
  - `좋아 이제 모험을 시작하렴`
- Existing starter-chosen flag: `1936`
- Reserved unused legacy-unlock flag: `1940`

## Branch behavior
1. Oak object now points to `59:6200` in the relocated working event table only.
2. If flag `1940` is set, wrapper `sjump`s to the untouched original Oak routine at `59:56BF`.
3. Otherwise, before starter flag `1936`, Oak displays the starter-selection prompt.
4. After starter flag `1936`, Oak displays the adventure-start prompt.

Flag `1940` is intentionally reserved for a later progression phase so the exact handoff point to legacy/postgame Oak behavior can be set without modifying the original routine.

## Preservation checks
- Original Oak routine at `59:56BF`: byte-for-byte unchanged.
- Original Oak Lab event table at `59:5C6C`: byte-for-byte unchanged.
- All original Oak Lab warps, BG events, assistants, Oak object, and scripts remain present.
- Phase 03 RGB starter objects/scripts remain present.
- Phase 04 Pallet starter gate remains present.
- No original record is deleted.

## Korean text encoding
The new text uses the Korean ROM's native two-byte Hangul charmap. `TX_START` and `<DONE>` follow `macros/scripts/text.asm`.

## Output verification
- SHA-1: `0abf0c0ad98cd6439e37cd515ebd772f622333f3`
- SHA-256: `3e5ea6f42f455e3360b9c5cac84b2243dda4afd6b5aaa3db60480d474f0a40b7`
- Header checksum: `08`
- Global checksum: `E68C`
- Clean-base standalone re-run: identical output (`REPRO_OK`)
