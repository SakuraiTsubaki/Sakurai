# STATUS — Phase 4 — 2026-09-18

## Build baseline

- Android NDK: **r30**
- SDK package: **30.0.16248370**
- My Boy ABI: **arm64-v8a**
- Native alignment target: **16 KiB**
- CI: **GitHub Actions**

## GBC.emu 1.5.45

**Route:** source rebuild.

The supplied APK is a split-required base package and contains no ABI-specific native library.

- upstream ARM64 build route prepared
- upstream source pin: `1c12fac5ce49badaadff2e2f210dcc30b89f4943`
- NDK r30 workflow added
- ARM64/16 KiB verification added
- exact historical 1.5.45 source backport remains separate work

## My Boy! 1.8.0

**Route:** preserve the legacy Java/UI initially and replace `libgba.so`.

### Implemented

- 31-method JNI contract
- ARM64-safe 32-bit Console handle table
- 240×160 RGB565 framebuffer
- legacy AudioTrack short-count semantics
- ROM/BIOS, input, audio, savestate, battery save, ROM code/hash
- cheats, gyro/tilt/solar, basic rumble
- UPS then IPS auto-patch handling
- `patchRom()` output-file implementation and legacy-style return codes
- mGBA `GBASIOLockstepCoordinator` / `GBASIOLockstepDriver`
- `mPERIPH_GBA_LINK_PORT` wiring
- `nativeOpenConsole(..., order)` player ordering
- cooperative local link scheduler
- ARM64 / 16 KiB verifier
- repack/sign/device smoke-test scripts
- GitHub Actions NDK r30 build

### Validated so far

- shell syntax
- Python tools
- C++ bridge/JNI syntax with compatible stubs
- original APK correctly fails modern ARM64/16 KiB verification
- synthetic ELF64/AArch64 16 KiB test correctly passes

### Still to prove

- real NDK r30 compilation in GitHub Actions
- real-device launch/render/audio/save behavior
- real GBA multiplayer/link-game behavior
- old My Boy! native savestate conversion
- auxiliary RTC save-file compatibility
- later Java/API modernization for target API 36 distribution
