# RBY ENGLISH → Japanese RGBY — Opening Architecture Audit v0.1

## Fixed base-ROM rule

The Japanese Red, Green, Blue, and Pikachu ROMs are the source/work ROMs. Existing English Red, Blue, and Yellow are implementation references.

## Japanese Red / Green / Blue

The opening pipeline is:

1. Copyright display (180-frame delay in the shared intro setup)
2. Game Freak shooting-star animation
3. `PRESENTS` in the Japanese presentation
4. Letterboxed monster battle intro
5. Fade to white
6. Title screen

The battle composition is version-specific:

- **Red:** Gengar vs Nidorino
- **Green:** Gengar vs Nidorino
- **Blue:** Gengar vs Jigglypuff

The front fighter uses a 6×6 OAM layout (36 objects) and three dedicated intro graphics states. The choreography uses scripted X/Y offsets and 2-pixel scroll movement. It is not the normal battle engine.

The English Red/Blue disassembly explicitly documents that the Japanese `PRESENTS` graphic call was removed in localization. Therefore that element must be treated as a deliberate JP→EN presentation difference rather than accidental leftover text.

## Japanese Pikachu

Pikachu shares the copyright/Game Freak shooting-star prefix, then replaces the RGB monster battle entirely with a dedicated 18-state scene machine:

| Active scene | Action | Paired wait | Timer |
|---:|---|---:|---:|
| 0 | Running Pikachu 1 | 1 | 130 f |
| 2 | Pikachu kick | 3 | 128 f |
| 4 | Running Pikachu 2 | 5 | 128 f |
| 6 | Surfing Pikachu | 7 | 88 f |
| 8 | Running Pikachu 3 | 9 | 128 f |
| 10 | Flying Pikachu | 11 | 128 f |
| 12 | Pikachu close-up | 13 | 128 f |
| 14 | Thunderbolt / palette-flash sequence | 15 | then 40 f |
| 16 | Fade to white | 17 | final 64 f |

The opening uses `MUSIC_YELLOW_INTRO`, animated-object structures, per-scene BG/OAM effects, raster/LY effects for surfing, cloud tile animation while flying, and palette flashing for Thunderbolt. A/B/Start can skip to the title.

## Japanese Pikachu vs English Yellow technical difference

Direct header inspection of the supplied ROMs:

- Japanese Pikachu Rev D: CGB flag `0x00`, SGB flag `0x03`
- English Yellow: CGB flag `0x80`, SGB flag `0x03`

The English Yellow intro source also contains native CGB palette/attribute handling absent from the Japanese source. This is a technical localization/enhancement difference and should be considered separately from the English text translation.

## Project preservation rule

- Preserve Red/Green Nidorino choreography.
- Preserve Blue Jigglypuff choreography.
- Preserve Pikachu's dedicated montage.
- Localize only language-dependent presentation unless a technical port is deliberately approved.
- Do not replace Japanese version-specific opening behavior with the English Red/Blue/Yellow behavior wholesale.
