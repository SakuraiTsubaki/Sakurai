# Bank $30-$3F integrated survey + disassembly

CPU traversal and bank census are performed together. Data/script/audio banks are kept out of the LR35902 decoder unless a verified CPU entry point exists.

## Bank-by-bank result

| Bank | Role | Exact asset-family result | CPU disassembly |
|---|---|---|---|
| $30 | overworld sprites 1 | **all 8 byte-identical** | not LR35902-decoded |
| $31 | overworld sprites 2 + Pokérus/lucky number/nickname engine | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 280 bytes |
| $32 | battle animation BG/effects + The End | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 664 bytes |
| $33 | move animations + extra songs 2 | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 11,626 bytes |
| $34 | all-zero/reserved in EN | JP pair used; other 6 are zero | not LR35902-decoded |
| $35 | all-zero/reserved in EN | JP pair used; other 6 are zero | not LR35902-decoded |
| $36 | inverted font | KR / JP-RevA+JP-Rev0 / ES+IT / EN / DE+FR | not LR35902-decoded |
| $37 | map blocks 3 + tileset data 5 | **all 8 byte-identical** | not LR35902-decoded |
| $38 | diploma/Unown printing/card flip/Unown puzzle/memory game/Bill PC | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 19,051 bytes |
| $39 | copyright/title/options/splash/intro | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 4,405 bytes |
| $3A | audio engine + songs 1 | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 5,104 bytes |
| $3B | songs 2 | **all 8 byte-identical** | not LR35902-decoded |
| $3C | songs 3 + SFX + cries | **all 8 byte-identical** | not LR35902-decoded |
| $3D | songs 4 | **all 8 byte-identical** | not LR35902-decoded |
| $3E | font/collision + shrink pics + time capsule/name rater/Unown dex/battle helpers | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 11,836 bytes |
| $3F | tileset animations/NPC trade/mom phone/mystery gift/debug | KR / JP-RevA+JP-Rev0 / ES / EN / DE / FR / IT | 8/8 active, 9,598 bytes |

## Findings

- **$30 (overworld sprites 1)** is byte-identical across all eight ROMs. One canonical asset decode can be shared.
- **$37 (map blocks 3 + tileset data 5)** is also byte-identical across all eight ROMs.
- **$3B, $3C, $3D (songs 2 / songs 3+SFX+cries / songs 4)** are byte-identical across all eight ROMs. Localization did not alter these audio-command banks; they should be decoded once with an audio-bytecode decoder, not as CPU.
- **$34/$35** are a hard layout split: only Japanese Rev 0/A use them (map scripts 10/11); KR + EN + four EU ROMs are all-zero there.
- **$36** is another layout split: Western/Korean versions use it for inverted-font data, while Japanese uses script content. It must be dispatched to different decoders by region.
- **$31** mixes sprite data with a small executable tail (Pokérus/lucky-number/nickname engine). The recursive pass reaches 35 CPU bytes in every ROM.
- **$32** includes battle-animation BG/effect engine code plus The End assets; 83 reachable CPU bytes are found in every ROM in the current seed set.
- **$33** is mixed move-animation CPU code + audio data. Current recursive pass finds 1.4–1.5 KiB CPU code per ROM; the remaining music/animation tables require domain decoders.
- **$38/$39/$3E/$3F** are substantial mixed engine banks and are actively CPU-disassembled; their data islands remain intentionally undecoded until structure-specific parsers are attached.
- **$3A** contains the audio engine plus songs 1. The CPU engine portion is reachable (638 bytes per ROM in this pass), while song streams are reserved for the audio-command decoder.

## Integrated rule

For this range, “bank complete” will require both sides: LR35902 functions where executable, plus the correct structured decoder for sprites, map blocks, scripts, audio commands, fonts, compressed graphics, and tables. A bank is not marked complete merely because a CPU disassembler can consume its bytes.
