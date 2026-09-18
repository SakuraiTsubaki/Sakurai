# Phase 3 — patch compatibility, GBA link cable, and build verification

## My Boy! 1.8.0

### `patchRom()` compatibility

The old Java/native call flow was reconstructed far enough to preserve its public behavior:

- Java looks next to the ROM for `.ups`, then `.ips`.
- Java asks native code to create `" (patched).gba"`.
- JNI receives `(outputPath, originalRomPath)`, not a patch path.
- Phase 3 now re-discovers the patch file, applies it, and writes the patched ROM.

Compatibility result codes used by the bridge:

| Code | Meaning |
|---:|---|
| `0` | success |
| `-1` | patch file not found |
| `-2` | ROM/patch/output I/O failure |
| `-3` | invalid/malformed patch |
| `-4` | patch is valid but does not match this ROM / checksum mismatch |

mGBA's patch engine is used for IPS/UPS (and understands BPS data through its UPS/BPS loader). Exact IPS output length is computed before writing so a small patched game is not padded to mGBA's generic 16 MiB IPS work size.

`Link.loadRom(path, autoPatch)` also carries the old auto-patch flag forward to each subsequently opened Console. Auto-patch failure is non-fatal, matching the old load path's behavior.

### Real mGBA SIO lockstep wiring

The old Phase 2 bridge only advanced multiple emulator cores sequentially. Phase 3 now uses mGBA's actual GBA SIO lockstep pieces:

- `GBASIOLockstepCoordinator`
- one `GBASIOLockstepDriver` per Console
- `mPERIPH_GBA_LINK_PORT`
- `nativeOpenConsole(path, order)` → `order` becomes the preferred GBA player ID
- up to four local players

Like mGBA's Qt frontend, one console is left on the normal SIO path. When a second console is opened, all consoles are attached to the shared lockstep coordinator.

The JNI thread is single-threaded, so the bridge uses a small cooperative scheduler: it runs only awake cores until every attached core advances one video frame. mGBA's lockstep sleep/wake callbacks determine which core may run next. A pass limit prevents an infinite deadlock.

**Status:** source-wired and syntax-checked, but still needs an NDK build plus real multiplayer game testing before this should be called proven link-cable compatibility.

## Modern APK verification

`tools/verify_modern_apk.py` now checks:

- presence of `lib/arm64-v8a/*.so`
- ELF64 + AArch64 machine type
- every `PT_LOAD` alignment is at least `0x4000` (16 KiB)
- 16 KiB ZIP offset alignment for uncompressed native libraries

The original My Boy! APK intentionally fails this check because it has only 32-bit ARM/x86 libraries aligned to 4 KiB.

The verifier was also tested against a synthetic ELF64/AArch64 shared library linked with 16 KiB `PT_LOAD` alignment and correctly accepted it.

## Scripts added/updated

- `myboy/scripts/build-arm64.sh`
  - pins ARM64
  - Android API 24 floor for the legacy UI
  - explicit `c++_static`, so the repacked old APK does not need a new `libc++_shared.so`
- `myboy/scripts/repack-apk.sh`
  - `zipalign -P 16`
  - signs the rebuilt APK
  - runs the modern APK verifier after signing
- `myboy/scripts/device-smoke-test.sh`
  - reports device ABI / API / page size
  - checks APK ARM64 + 16 KiB readiness
  - installs and launches the package
  - extracts relevant crash/linker/native logs
- `gbc-emu/build-current-gbc.sh`
  - now verifies every generated APK for ARM64 + 16 KiB native compatibility

## What remains

1. Compile the My Boy! Phase 3 bridge with a real Android NDK r28+.
2. Fix any API/build drift exposed by the exact NDK/mGBA combination.
3. Repack and sign a test APK.
4. Run on an ARM64 Android 15/16 phone, ideally a 16 KiB-page device/emulator.
5. Test real GBA link games (trade/battle/multiboot cases).
6. Investigate old My Boy! savestate conversion and its auxiliary RTC save file format.
7. Only after native compatibility is stable, modernize the legacy Java/storage/Bluetooth layer and raise target SDK for store distribution.
