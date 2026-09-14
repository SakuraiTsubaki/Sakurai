# Japanese Bank 00 — `$09DA-$0B3B`

This range continues directly after `SoftReset` and covers the main program initialization path, VRAM/audio reset helpers, the VBlank interrupt handler, and `DelayFrame`.

Recovered structured source in `home/jp_init_vblank.asm` includes:

- `Init` at `$09DA`
- WRAM/VRAM/HRAM clearing and DMA bootstrap
- SGB/intro predef dispatch
- `ClearVram` at `$0A8C`
- `StopAllSounds` at `$0A96`
- `VBlank` at `$0AAC`
- BG/OAM/VBlank-copy dispatch
- RNG/audio/play-time updates during VBlank
- ROM-bank save/restore around the interrupt
- `DelayFrame` at `$0B31`

## ROM verification

| Range | Size | V1.0 SHA-1 | V1.1 SHA-1 | differing bytes |
|---|---:|---|---|---:|
| `$09DA-$0A8B` (`Init`) | 178 | `5343422533809c88d2f93e38d71e966222411653` | `f49ebe21a7867a2f7efe323557f370411f554e37` | 5 |
| `$0A8C-$0A95` (`ClearVram`) | 10 | `77b3d43b06b99233307eb0177e80ce4b7e6b79d1` | `31cd81a42e471aea221afea4e62d8c7f50056baf` | 1 |
| `$0A96-$0AAB` (`StopAllSounds`) | 22 | `dd6f8b1a17c5c565cb630ee8d17fe2575171c381` | `140b51b4f8e71407bc24daff133d6072fc9d6f4d` | 1 |
| `$0AAC-$0B30` (`VBlank`) | 133 | `ca2d786fbf888d5806c000b0f1cef9c695f7d937` | `b1ad29b78d790533210b321c6f04eb5162246c3a` | 3 |
| `$0B31-$0B3B` (`DelayFrame`) | 11 | `6c3f94a6f9517316390417c1788b7364f249cd14` | same | 0 |
| `$09DA-$0B3B` complete | 354 | `cf56458872b8a86c9d4d020b4f6ee6c0ba10f64a` | `71ee2578110ae4c9f6fb9aad1a5e3bbe9cb03fba` | 10 |

All ten V1.0/V1.1 byte differences are operands of moved external targets; the local routine layout is unchanged.

| External target | V1.0 | V1.1 |
|---|---:|---:|
| `FillMemory` | `$372A` | `$3718` |
| `Predef` | `$3E9D` | `$3E8B` |
| `GBPalNormal` | `$3E0C` | `$3DFA` |
| `PlaySound` | `$0E45` | `$0E33` |
| `Random` | `$3E8C` | `$3E7A` |
| `FadeOutAudio` | `$139C` | `$138A` |
| `Bankswitch` | `$3620` | `$360E` |

`WriteDMACodeToHRAM = $4750`, `PrepareOAMData = $4672`, and `PrepareTitleScreen = $476E` remain fixed in this range for both revisions.

The RAM/HRAM and hardware register addresses decoded from the machine code are recorded in `constants/memory.asm` and `constants/hardware.asm`.
