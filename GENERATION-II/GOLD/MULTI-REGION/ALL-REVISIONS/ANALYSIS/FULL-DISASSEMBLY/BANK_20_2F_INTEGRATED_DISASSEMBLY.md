# Bank $20-$2F integrated survey + disassembly

This report couples bank census work with actual disassembly progress. CPU code is recursively decoded only when control-flow evidence exists; script/audio/text/graphics bytes are not blindly interpreted as LR35902 instructions.

## Bank status

| Bank | Primary role | Domain | Active ROMs | Decoded bytes (8 ROMs) | Current treatment |
|---|---|---|---:|---:|---|
| $20 | trainer pic pointers + pics 13 | data/gfx | 0/8 | 0 | needs-structured-data-decoder:8 |
| $21 | printer/battle animation GFX/Hall of Fame + credits | data/gfx | 8/8 | 26,328 | cpu-disassembly-validated-partial:8 |
| $22 | all-zero/reserved in EN | empty | 0/8 | 0 | empty-confirmed:6, needs-script-bytecode-disassembly:2 |
| $23 | engine: save/phone ring/RTC reset/delete save/palettes/transitions/field moves/sprite anims/icons/credits init | cpu/mixed-data | 8/8 | 16,366 | cpu-disassembly-validated-partial:8 |
| $24 | engine: phone/RTC time set/Pokégear/landmarks/fishing/slot machine | cpu/mixed-data | 8/8 | 26,188 | cpu-disassembly-validated-partial:8 |
| $25 | maps + events | mixed:data+cpu | 8/8 | 26,968 | cpu-disassembly-validated-partial:8 |
| $26 | title screen | data/gfx | 0/8 | 0 | needs-structured-data-decoder:6, needs-script-bytecode-disassembly:2 |
| $27 | all-zero/reserved in EN | cpu/mixed-data | 4/8 | 356 | cpu-disassembly-validated-partial:4, empty-confirmed:2 |
| $28 | all-zero/reserved in EN | empty | 0/8 | 0 | empty-confirmed:6, needs-script-bytecode-disassembly:2 |
| $29 | all-zero/reserved in EN | empty | 0/8 | 0 | empty-confirmed:6, needs-script-bytecode-disassembly:2 |
| $2A | map blocks 1 | data/gfx | 0/8 | 0 | needs-structured-data-decoder:8 |
| $2B | map blocks 2 | data/gfx | 0/8 | 0 | needs-structured-data-decoder:8 |
| $2C | all-zero/reserved in EN | empty | 0/8 | 0 | empty-confirmed:6, needs-script-bytecode-disassembly:2 |
| $2D | all-zero/reserved in EN | empty | 0/8 | 0 | empty-confirmed:6, needs-script-bytecode-disassembly:2 |
| $2E | pics 14 + hidden items/tree mons/radio/mail2 engine | mixed:gfx+cpu | 8/8 | 2,494 | cpu-disassembly-validated-partial:8 |
| $2F | all-zero/reserved in EN | empty | 0/8 | 0 | empty-confirmed:6, needs-script-bytecode-disassembly:2 |

## Verified mixed/code boundaries and relocations

- **$21**: executable printer / Hall of Fame / credits-side engine code is recursively decoded; source-symbol anchors line up with the uploaded English ROM.
- **$23**: executable save/RTC/palette/battle-transition/sprite-animation/icon code; also contains the overwhelming majority of the Japanese Rev 0→Rev A byte changes.
- **$24**: executable phone / RTC / Pokégear / landmark / fishing / slot-machine code.
- **$25**: **mixed data + CPU**. Map scene/group/attribute data begins at $4000; verified CPU event/script engine starts at **$65F9 (OverworldLoop in the English baseline)**. `rst $28` jump-table dispatch is followed by the recursive decoder.
- **EU $27**: English/Korean $27 are empty and Japanese $27 is map-script data, but Spanish/German/French/Italian $27 contains executable relocated localization overflow. Functions at $4000 and $400F decode cleanly, with additional region-shifted call targets.
- **$2E**: **mixed graphics + CPU**. Picture data occupies the first part; verified executable hidden-item/tree/radio/mail-side code begins at **$6300** in the English baseline.

## Symbol propagation

English symbols were matched into the uploaded regional ROMs using byte-window voting rather than address equality. 81 English anchors × 8 ROMs = 648 mapping rows. High-confidence matches dominate Western releases and remain substantial in Korean/Japanese versions; unmapped rows are deliberately left unresolved rather than guessed.

## Next disassembly rule

Each bank is completed as a unit: **survey → domain classification → correct decoder (CPU/script/audio/text/gfx/data) → symbol mapping → cross-region comparison → byte/rebuild verification → next bank**. “Disassembly” therefore means decoding the bank in its actual language, not forcing every byte through the CPU decoder.
