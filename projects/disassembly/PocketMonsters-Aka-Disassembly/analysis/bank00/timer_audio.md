# Japanese Bank 00 — Timer/audio (`Timer` through `PlaySound`)

This block begins immediately after the revision-dependent serial engine and runs through the final byte of `PlaySound`.

## ROM-verified ranges

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$0D9A-$0EBC` | 291 bytes | `0feb78732f7f1741069cb74ced196ce8d1062e92` | `UpdateSprites` at `$0EBD` |
| V1.1 | `$0D88-$0EAA` | 291 bytes | `dd039c3cdf6bf2ee03eabf0d3390c1213d44f818` | `UpdateSprites` at `$0EAB` |

V1.1 starts exactly `$12` bytes earlier because its Serial block is 18 bytes shorter. Once aligned by relative offset, the 291-byte Timer/audio blocks differ in only four bytes.

## Recovered routines

- `Timer` (a one-byte `reti`; the timer interrupt is effectively unused)
- `PlayDefaultMusic`
- `PlayDefaultMusicFadeOutCurrent`
- `PlayDefaultMusicCommon`
- `UpdateMusic6Times`
- `CompareMapMusicBankWithCurrentBank`
- `PlayMusic`
- `PlaySound`

The source is `home/jp_timer_audio.asm` and uses `constants/audio.asm` for audio-bank IDs, engine entry points, channel indexes, and the bike/surf music IDs.

## Four revision-byte differences

After aligning V1.1 by `$12`, only these absolute-call/jump operands differ:

| Relative operation | V1.0 byte location | V1.1 byte location | Reason |
|---|---:|---:|---|
| `call WaitForSoundToFinish` low byte | `$0D9C` | `$0D8A` | external helper moved `$3790 → $377E` |
| `call CompareMapMusicBankWithCurrentBank` low byte | `$0DDC` | `$0DCA` | local routine moved with the block |
| `jp PlaySound` low byte | `$0DF1` | `$0DDF` | local routine moved with the block |
| `call Bankswitch` low byte | `$0E11` | `$0DFF` | external helper moved `$3620 → $360E` |

Everything else in the range is byte-identical after relocation.

## Audio constants verified from code/symbols

- bike music ID: `$D2`
- surfing music ID: `$D6`
- bike/surf audio bank: `$1F`
- Audio engine banks: `$02`, `$08`, `$1F`
- update entry points: `$4000`, `$455F`, `$4417`
- play-sound entry points: `$4773`, `$4D1B`, `$4B8A`

Relevant RAM recovered/confirmed while decoding this block includes `wChannelSoundIDs = $C026`, `wAudioFadeOutCounterReloadValue = $CFAF`, `wAudioFadeOutCounter = $CFB0`, `wMapMusicSoundID = $D2DA`, `wMapMusicROMBank = $D2DB`, `wWalkBikeSurfState = $D67F`, and `wStatusFlags4 = $D6AD`.

All range hashes and byte-difference counts were calculated from the supplied Japanese Red ROMs. Public Japanese Red/Green disassembly symbols were used only as semantic cross-checks.
