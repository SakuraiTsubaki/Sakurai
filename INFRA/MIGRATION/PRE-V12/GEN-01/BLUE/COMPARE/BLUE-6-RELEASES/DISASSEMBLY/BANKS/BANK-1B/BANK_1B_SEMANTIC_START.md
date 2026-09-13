# Bank $1B semantic disassembly start

Bank `$1B` is byte-identical across JP/EN/FR/DE/IT/ES (SHA-1 `682b94550690d2e4c4103fe93753ed74ab38fc72`).

Reference source: `pret/pokered` section `Tilesets 3` in `gfx/tilesets.asm`.
Because the complete 16 KiB bank is identical across all six uploaded ROMs, the following semantic order and labels transfer 1:1 to every ROM:

1. `Cemetery_GFX`
2. `Cemetery_Block`
3. `Cavern_GFX`
4. `Cavern_Block`
5. `Lobby_GFX`
6. `Lobby_Block`
7. `Ship_GFX`
8. `Ship_Block`
9. `Lab_GFX`
10. `Lab_Block`
11. `Club_GFX`
12. `Club_Block`
13. `Underground_GFX`
14. `Underground_Block`

This bank is data-only tileset/blockset material, not executable SM83 code. Treating it as linear CPU instructions would be incorrect. It is the first proof bank for the cross-language semantic-label pipeline.

Next recommended semantic passes:
- Near-identical/easy alignment: `$02`, `$0A`, `$0B`, `$0C`, `$13`, `$19`, `$1F`
- Core/gameplay: `$00-$1F`
- Localization-heavy text/data: `$20-$2C`
- `$2D-$3F`: classify as zero padding only; no semantic disassembly required.
