# My Boy! 1.8.0 → ARM64 compatibility track

## What is now implemented

The supplied APK's DEX contract was re-checked directly.

- `Console.nativeConsole` is `int` (`I`), so ARM64 uses an opaque handle table.
- `Link.nativeOpenConsole(...)` and `Link.nativeCloseConsole(...)` are **instance** native methods.
- 31 JNI native methods are enumerated in `jni_contract.json`.
- The Java renderer allocates a direct framebuffer of `0x12C00` bytes = **240×160×2**.
- The replacement core is therefore configured for **RGB565**.
- `getAudioSamples(short[], int)` returns the number of `short` elements because Java passes the result directly to `AudioTrack.write(short[], offset, size)`.

`mgba_core_bridge.cpp` now implements a real mGBA-backed bridge for:

- GBA ROM loading and validation
- optional GBA BIOS loading
- 240×160 RGB565 framebuffer
- input keys
- stereo audio extraction
- reset
- file and in-memory savestates
- battery save/load
- ROM code + MD5 hash
- cheat sets
- gyro / tilt / solar sensor hooks
- basic rumble plumbing
- old `setOption()` JNI compatibility surface

`myboy_jni_bridge.cpp` now keeps a **per-Link context** and supports multiple Console handles safely on ARM64.

## Still not exact

These are the remaining compatibility items, not hidden as “done”:

1. **GBA link cable synchronization**: multiple cores advance, but mGBA link/SIO wiring is not connected yet.
2. **`patchRom()` / auto-IPS behavior**: the exact My Boy! 1.8.0 status codes and patch workflow still need matching.
3. **Legacy `.st*` state compatibility**: new mGBA states work with the bridge, but old My Boy! native savestates are a different engine format.
4. **Auxiliary battery/RTC file format**: primary `.sav` data works; the second legacy battery path is retained but not decoded yet.
5. **Rumble pulse shaping**: functional scaffold, not cycle-exact My Boy! behavior.
6. **Legacy engine-only options** such as `cpuCore`, `saveType`, and `smcCheck` are accepted but mostly no-ops because mGBA manages those differently.

## Build

```bash
./scripts/fetch-mgba.sh
export ANDROID_NDK_HOME=/path/to/android-ndk-r30
./scripts/build-arm64.sh
```

Output:

```text
out/libgba.so
```

Then inject it into **your supplied APK copy** and re-sign:

```bash
./scripts/repack-apk.sh "/path/to/My Boy!.1.8.0.apk" out/libgba.so MyBoy-1.8.0-arm64.apk
```

Because the APK must be re-signed with your own key, it cannot be installed as an update over the store-signed original.

## Compatibility strategy

For personal sideload compatibility, keep the original `targetSdkVersion=24` first. Android 15 blocks apps **below** target 24, so this package is exactly at the installation floor. Raising it immediately to API 36 would also activate many modern behavior changes in the old Java UI. The safer order is:

1. make ARM64 + 16-KB native code work;
2. test the original Java UI;
3. modernize storage/Bluetooth/manifest APIs;
4. only then raise target SDK for a Play-distributable rebuild.
