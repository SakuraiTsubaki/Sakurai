# AgbMain early-boot analysis

After the shared ARM `Init`/`IntrMain` block, execution switches to Thumb code at `AgbMain`.

## Function placement

| Family | `AgbMain` | Size to next function | Next function |
| --- | ---: | ---: | ---: |
| Japanese (`AXPJ`) | `0x0800024C` | `0xFC` | `UpdateLinkAndCallCallbacks @ 0x08000348` |
| English (`AXPE`) | `0x0800024C` | `0xF4` | `UpdateLinkAndCallCallbacks @ 0x08000340` |
| German/French/Italian | `0x08000380` | `0xF4` | `UpdateLinkAndCallCallbacks @ 0x08000474` |

The Japanese build uses a different register-allocation/prologue pattern (`r8/r9`) and is therefore eight bytes larger than the other analyzed builds before the next function begins.

## Initial call sequence

The first nine call sites in every analyzed `AgbMain` follow the same semantic order:

1. `RegisterRamReset`
2. `InitKeys`
3. `InitIntrHandlers`
4. `m4aSoundInit`
5. `RtcInit`
6. `CheckForFlashMemory`
7. `InitMainCallbacks`
8. `InitMapMusic`
9. `SeedRngWithRtc`

This order agrees with the public `pret/pokeruby` reconstruction of `AgbMain`, and the local ROM call targets provide the per-build addresses below.

## Per-build call targets

| Target | RegisterRamReset | InitKeys | InitIntrHandlers | m4aSoundInit | RtcInit | CheckForFlashMemory | InitMainCallbacks | InitMapMusic | SeedRngWithRtc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| JPN v0 | `081B123C` | `08000404` | `080004C8` | `081AE860` | `08006854` | `08044C9C` | `08000390` | `08071BE8` | `080003E8` |
| USA v0 | `081E0794` | `08000400` | `080004C4` | `081DDDC8` | `08009248` | `080479CC` | `08000388` | `08074BB0` | `080003E4` |
| EUR v1 | `081E07AC` | `08000400` | `080004C4` | `081DDDE0` | `08009248` | `080479EC` | `08000388` | `08074BD0` | `080003E4` |
| USA/EUR v2 | `081E07AC` | `08000400` | `080004C4` | `081DDDE0` | `08009248` | `080479EC` | `08000388` | `08074BD0` | `080003E4` |
| DE v1 | `081ED704` | `08000534` | `080005F8` | `081EAD38` | `08009414` | `08047CF0` | `080004BC` | `08074F70` | `08000518` |
| FR v0/v1 | `081E8B8C` | `08000534` | `080005F8` | `081E61C0` | `08009414` | `08047DDC` | `080004BC` | `08075060` | `08000518` |
| IT v0/v1 | `081E2420` | `08000534` | `080005F8` | `081DFA54` | `08009414` | `08047D04` | `080004BC` | `08074F84` | `08000518` |

A notable revision result is that AXPE Rev 1 and Rev 2 share the same early-call targets, while USA Rev 0 differs in several later-ROM targets (`RegisterRamReset`, `m4aSoundInit`, flash check, and map-music initialization). French Rev 0/1 and Italian Rev 0/1 are identical in this early-boot region.

## Local early-main symbols

The following internal functions are now anchored by direct Thumb branch targets:

| Symbol | Japanese | AXPE | DE/FR/IT |
| --- | ---: | ---: | ---: |
| `UpdateLinkAndCallCallbacks` | `08000348` | `08000340` | `08000474` |
| `InitMainCallbacks` | `08000390` | `08000388` | `080004BC` |
| `SeedRngWithRtc` | `080003E8` | `080003E4` | `08000518` |
| `InitKeys` | `08000404` | `08000400` | `08000534` |
| `InitIntrHandlers` | `080004C8` | `080004C4` | `080005F8` |

These addresses are also recorded in `config/early_boot.yml` so later extraction/disassembly tools can consume them without scraping prose.

## Next boundary

The next reconstruction step is to turn the Thumb functions beginning at `AgbMain` into version-aware source, then continue linearly through `UpdateLinkAndCallCallbacks`, `InitMainCallbacks`, callback dispatch, key input, and interrupt-handler initialization. External call targets will be promoted to symbols as their respective regions are mapped.
