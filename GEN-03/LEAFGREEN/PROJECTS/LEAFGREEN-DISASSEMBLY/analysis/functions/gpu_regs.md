# GPU register manager module

The module immediately following `main.c` is the GPU register manager. USA ROM offsets are `0x000968–0x000BFB` (end-exclusive `0x000BFC`).

## Cross-version result

After applying each target's established post-`AgbMain` layout delta, the entire 660-byte module is byte-identical across all seven LeafGreen targets.

**Aligned module SHA-1:** `b85b55f65bcb2a4b5acc23c67d691f8d73506229`

| Target | start | end (exclusive) | size | delta vs USA |
|---|---:|---:|---:|---:|
| Japan | `0x000968` | `0x000BFC` | `0x294` | `+0x00` |
| USA | `0x000968` | `0x000BFC` | `0x294` | `+0x00` |
| Europe Rev 1 | `0x00097C` | `0x000C10` | `0x294` | `+0x14` |
| Germany | `0x000978` | `0x000C0C` | `0x294` | `+0x10` |
| France | `0x000964` | `0x000BF8` | `0x294` | `-0x04` |
| Italy | `0x000978` | `0x000C0C` | `0x294` | `+0x10` |
| Spain | `0x000964` | `0x000BF8` | `0x294` | `-0x04` |

This makes the module a strong candidate for a single shared source implementation with target-specific placement handled only by the linker/layout.

## Function boundaries (USA baseline)

| Function | start | end | size |
|---|---:|---:|---:|
| `InitGpuRegManager` | `0x000968` | `0x0009C0` | `0x58` |
| `CopyBufferedValueToGpuReg` | `0x0009C0` | `0x000A04` | `0x44` |
| `CopyBufferedValuesToGpuRegs` | `0x000A04` | `0x000A38` | `0x34` |
| `SetGpuReg` | `0x000A38` | `0x000AC4` | `0x8C` |
| `GetGpuReg` | `0x000AC4` | `0x000AF4` | `0x30` |
| `SetGpuRegBits` | `0x000AF4` | `0x000B14` | `0x20` |
| `ClearGpuRegBits` | `0x000B14` | `0x000B34` | `0x20` |
| `SyncRegIE` | `0x000B34` | `0x000B68` | `0x34` |
| `EnableInterrupts` | `0x000B68` | `0x000B94` | `0x2C` |
| `DisableInterrupts` | `0x000B94` | `0x000BC0` | `0x2C` |
| `UpdateRegDispstatIntrBits` | `0x000BC0` | `0x000BFC` | `0x3C` |

Every individual function is also byte-identical across all seven targets after relocation by the target delta.

## Functional role

The module maintains a software buffer for GBA display registers, queues register writes outside safe display periods, exposes buffered set/get/bit operations, and synchronizes interrupt enable state with `DISPSTAT` interrupt bits.

The next function at the module end belongs to `dma3_manager` and begins at USA offset `0x000BFC` (target-adjusted by the same layout delta).
