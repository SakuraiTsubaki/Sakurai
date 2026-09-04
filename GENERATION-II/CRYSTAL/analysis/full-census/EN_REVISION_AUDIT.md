# Pokémon Crystal EN Rev0 → RevA audit

## Byte-exact result
- Different bytes: **584** of 2,097,152 (0.027847%).
- Contiguous changed ranges: **79**.
- Affected banks: `00`, `10`, `11`, `3E`, `47`, `5C`, `7E`, `7F`.

## Classified changes
- `00:014C–014F` — ROM version and header/global checksum bytes. Rev0 version byte `00` becomes RevA `01`; checksum bytes change accordingly.
- bank `47`, one byte — Battle Tower trainer-dialog class/gender bug fix. The public disassembly documents that Crystal 1.0 used the sixth character of the trainer name instead of the trainer class, causing dialog to sample from the female array; RevA uses `wBT_OTTrainerClass`.
- bank `7E`, two bytes — Battle Tower trainer sampling bug fix. Crystal 1.0 used `BATTLETOWER_NUM_UNIQUE_MON` where the trainer-count constant was required, restricting the selectable trainer pool; RevA uses `BATTLETOWER_NUM_UNIQUE_TRAINERS`.
- bank `5C`, **546 changed bytes** — overwhelmingly the Stadium 2 N64 tilemap area. The disassembly explicitly records that Crystal 1.1 contains a corrupted tilemap produced by converting `0A` bytes as if they were Unix newlines into `0D 0A` Windows newlines. This is a notable case where RevA intentionally reproduces a data-corruption artifact rather than simply fixing code.
- banks `10`, `11`, `3E` — small code/data-reference changes associated with RevA build differences; exact byte ranges are preserved in `en_rev0_reva_changed_ranges.csv`. These should be symbol-resolved before patch transplantation.
- bank `7F` — checksum/reference bytes in the Stadium 2 checksum tail plus final ROM checksum consequences.

## Policy for the project
- Keep Rev0 and RevA as separate baselines; do not silently collapse them.
- When porting fixes, distinguish **bug fix** from **revision artifact** (notably the corrupted Stadium 2 tilemap in RevA).
- Any final multilingual patch set should record whether it follows Rev0 behavior, RevA behavior, or a corrected behavior chosen deliberately.
