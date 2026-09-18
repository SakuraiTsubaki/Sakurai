# Phase 4 — GitHub Actions + Android NDK r30

Verified from the official `android/ndk` GitHub repository on 2026-09-18:

- latest stable release: **NDK r30**
- SDK/Gradle package version: **30.0.16248370**
- release date: **2026-09-08**

The build is now pinned to r30 instead of a loose `r28+` requirement.

## GitHub Actions

`.github/workflows/android-arm64.yml` provides two independent jobs.

### My Boy! ARM64

- installs `ndk;30.0.16248370`
- fetches the pinned mGBA revision
- builds `arm64-v8a/libgba.so`
- verifies ELF64/AArch64
- rejects PT_LOAD alignment below 16 KiB (`0x4000`)
- uploads artifact `myboy-arm64-ndk-r30`

### GBC.emu ARM64

- installs the same NDK r30
- checks out the pinned EX Emulators revision
- uses the upstream-style Linux build dependencies
- builds GBC.emu for ARM64
- uploads artifact `gbc-emu-arm64-ndk-r30`

## Repository placement

The authenticated user's `SakuraiTsubaki/Sakurai` default branch was inspected first. Its newest default-branch commit is `Reset repository to empty state` (2026-09-18), so this phase intentionally does **not** push the emulator modernization project into that reset repository without an explicit destination choice.

Once this workspace is placed in the intended repository, run:

**Actions → Android ARM64 compatibility build → Run workflow**
