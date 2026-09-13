# Pokémon Emerald BPEE — DEX649 banked National Pokédex UI

## Build status

This build extends the validated DEX649 core with a coexistence UI for the National Pokédex without changing the retail `PokedexView` structure size.

- Bank A: National #001–386, original Emerald `CreatePokedexList` path preserved. Press **L**.
- Bank B: National #387–649, 263 numerical entries. Press **R**.
- Unseen Bank-B entries keep their National number but use the retail hidden-name / hidden-sprite presentation.
- `SELECT` search is not repurposed.
- Hoenn mode remains on the retail path.
- The bank byte uses original `PokedexView` filler byte `+0x642`, so a fresh Pokédex open defaults to Bank A via `AllocZeroed`.

## Runtime hooks

- `Task_HandlePokedexInput` at ROM `0x0BC0F8`: 8-byte Thumb→ARM entry stub, L/R detection, list rebuild, sprite/list redraw.
- `CreatePokedexList` at ROM `0x0BC8D4`: 8-byte Thumb→ARM entry stub. Bank A resumes the original prologue; Bank B builds #387–649.
- injected ARM block: ROM `0x1805ED0–0x18060BB`.
- DEX649 save/core hooks are preserved unchanged.

The Bank-B list is always 263 physical entries rather than shrinking to the last seen species. This deliberately avoids the retail scrollbar's `(pokemonListCount - 1)` zero-denominator edge case when exactly one post-386 Pokémon has been seen. Names and Pokémon sprites are still hidden until their seen flag is set.

## Reproducibility

The ARM hook source is built with `clang --target=arm-none-eabi -mcpu=arm7tdmi -marm`, linked at `0x09805ED0`, converted to a raw binary, then applied to the exact DEX649 core ROM by `patch_dex649_banked_ui.py`.

A clean rebuild was performed after making the patcher path-independent:

- original hook binary SHA-1: `0c3bb2619691f6452fe8424ecfa156a572a40ee3`
- rebuilt hook binary SHA-1: `0c3bb2619691f6452fe8424ecfa156a572a40ee3`
- original banked ROM SHA-1: `ccff6ab32f5f139d8346366fd5a169e5ddaa533f`
- rebuilt banked ROM SHA-1: `ccff6ab32f5f139d8346366fd5a169e5ddaa533f`

Both the hook binary and final ROM matched byte-for-byte.

## Verification

- Static UI-hook checks: **29/29 passed**.
- Binary diff against DEX649_CORE: every changed byte is confined to the two 8-byte function-entry stubs and the new ARM block.
- Unintended changes outside those regions: **0 bytes**.
- Route 101 Lv.2 Turtwig smoke encounter is preserved.
- Output SHA-1: `ccff6ab32f5f139d8346366fd5a169e5ddaa533f`
- Output SHA-256: `d215b5e311eb664f9a4f659fc7895010cbb9e12c7b4fce1cc885e90f9dfa0cf4`

No compatible GBA emulator is installed in the execution environment, so boot/input/runtime behavior is not claimed as tested yet.

ROM binaries are local build products and are not committed to GitHub.
