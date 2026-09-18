# STATUS — Phase 3 — 2026-09-18

## GBC.emu 1.5.45

**Route:** source rebuild, because the supplied APK is a split-required base package and contains no ABI split native library.

- current upstream ARM64 build route: prepared
- current upstream source pin: `1c12fac5ce49badaadff2e2f210dcc30b89f4943`
- modern NDK / 16 KiB verification: added to build script
- exact historical 1.5.45 source backport: still separate work; no exact source revision was established from this APK alone

## My Boy! 1.8.0

**Route:** keep legacy Java/UI first, replace native `libgba.so` with an ARM64 mGBA-backed compatibility layer.

### Implemented

- 31-method JNI contract
- ARM64-safe 32-bit Console handle table
- 240×160 RGB565 framebuffer
- audio count semantics matched to `AudioTrack.write(short[])`
- ROM/BIOS, input, audio, savestate, battery save, ROM code/hash, cheats, sensors, basic rumble
- automatic `.ups` then `.ips` handling
- `patchRom()` output-file implementation and legacy-style result codes
- `autoPatch` carried from `Link.loadRom()` into real Console cores
- mGBA GBA SIO lockstep coordinator + per-console driver
- `nativeOpenConsole(..., order)` player-order mapping
- cooperative single-thread lockstep frame scheduler
- ARM64 / 16 KiB APK verifier
- repack/sign/device-smoke-test scripts

### Validation completed in this environment

- shell scripts: syntax OK
- Python tools: compile OK
- C++ bridge/JNI: syntax-checked with API-compatible stubs
- verifier negative test: original My Boy! correctly rejected (no ARM64, old ARM is 4 KiB aligned)
- verifier positive test: synthetic ELF64/AArch64 16 KiB library correctly accepted

### Not yet proven

- actual Android NDK build of Phase 3 (`NDK r28+` is not installed in this execution environment)
- real-device launch/render/audio/save test
- real GBA multiplayer/link-game behavior
- old My Boy! native savestate format conversion
- auxiliary RTC save-file compatibility
- full modern Java/API migration for target API 36 distribution
