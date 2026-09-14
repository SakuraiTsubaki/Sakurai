# Japanese Bank 00 — `$04C9-$0773`

This range continues the Japanese Red V1.0/V1.1 text engine immediately after `NextChar`.

Recovered structured source includes:

- `NullChar` and the debug `TextIDErrorText`
- player/rival/trainer/TM/PC/Rocket/Pokémon command-character expansion
- Japanese fixed strings such as `わざマシン`, `トレーナー`, `パソコン`, `ロケットだん`, and `ポケモン`
- continuation/prompt/paragraph/scroll handling
- `TextCommandProcessor` and the complete command dispatch table through `$0773`
- BCD/number formatting calls
- text-triggered sound effects and Pokémon cries
- dot printing and wait-for-button commands

## ROM verification

The complete range is 683 bytes (`$04C9-$0773` inclusive).

- V1.0 SHA-1: `6c92c40d04501cf17112f156e3534f66e298633e`
- V1.1 SHA-1: `d0227822405afc8e33bf51694cd0fea271cb0d2f`
- differing bytes between revisions: 15

The 15 differences are all operands of external calls whose targets moved in V1.1. The text-engine layout, local branches, fixed strings, data tables, and jump table retain the same addresses.

| External target | V1.0 | V1.1 |
|---|---:|---:|
| `ManualTextScroll` | `$38E1` | `$38CF` |
| `DelayFrames` | `$3781` | `$376F` |
| `PrintBCDNumber` | `$2FC4` | `$2FB2` |
| `PrintNumber` | `$3C8F` | `$3C7D` |
| `PlaySound` | `$0E45` | `$0E33` |
| `WaitForSoundToFinish` | `$3790` | `$377E` |
| `PlayCry` | `$2DC7` | `$2DB5` |

The recovered source is `home/jp_text_engine.asm`; revision-specific target addresses are selected in `constants/builds.asm`, while RAM/HRAM addresses decoded from the machine code are documented in `constants/memory.asm`.
