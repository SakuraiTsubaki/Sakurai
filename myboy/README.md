# My Boy! 1.8.0 → ARM64 compatibility track

## Verified contract

- `Console.nativeConsole` is Java `int` (`I`), so ARM64 uses opaque 32-bit handles.
- `Link.nativeOpenConsole(...)` and `Link.nativeCloseConsole(...)` are instance native methods.
- 31 JNI native methods are listed in `jni_contract.json`.
- framebuffer: `0x12C00` bytes = **240×160×2**, configured as RGB565.
- `getAudioSamples(short[], int)` returns the number of `short` elements written.

## Implemented native bridge

`mgba_core_bridge.cpp` covers:

- ROM and BIOS loading
- RGB565 framebuffer
- input and stereo audio
- savestates and battery saves
- ROM code and MD5
- cheats
- gyro / tilt / solar
- basic rumble
- UPS/IPS patch handling
- mGBA GBA SIO lockstep link wiring

`myboy_jni_bridge.cpp` provides:

- ARM64-safe handle management
- per-Link contexts
- preferred player ordering from `nativeOpenConsole(path, order)`
- local link-cable scheduling across multiple Console instances

## Build baseline

Use **Android NDK r30 / 30.0.16248370**.

```bash
./scripts/fetch-mgba.sh
export ANDROID_NDK_HOME=/path/to/android-ndk-r30
./scripts/build-arm64.sh
```

Output:

```text
out/libgba.so
```

Repack your supplied APK copy:

```bash
./scripts/repack-apk.sh "/path/to/My Boy!.1.8.0.apk" out/libgba.so MyBoy-1.8.0-arm64.apk
```

## Remaining compatibility work

- prove the NDK r30 build in CI
- real-device rendering/audio/save testing
- real multiplayer game testing
- legacy My Boy! `.st*` savestate conversion
- auxiliary RTC save mapping
- tune rumble behavior
- modernize old Java storage/Bluetooth/manifest APIs before raising target SDK for store distribution
