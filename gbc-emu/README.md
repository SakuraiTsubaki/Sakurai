# GBC.emu 1.5.45 → modern Android track

## Verified from the supplied APK

- Package: `com.explusalpha.GbcEmu`
- Version: `1.5.45`
- `minSdkVersion=9`, `targetSdkVersion=28`
- The supplied file declares `android:isSplitRequired="true"`.
- It is therefore a **base split APK**, not a self-contained universal APK.
- This base APK contains no `.so` files; ABI-specific native code was delivered in split APK(s).
- Legacy storage permissions and Bluetooth permissions are present.

## Best path

Do not try to turn this single base split into a modern universal APK by manifest editing alone.

The upstream EX Emulators repository is still maintained and its current build system already builds
Android architectures through Imagine + EmuFramework. Use current upstream as the modern Android
baseline, then port any 1.5.45-specific behavior you actually want to preserve.

The included `build-current-gbc.sh` mirrors the current upstream build flow at a high level and
restricts the app build to `arm64`.

## If exact 1.5.45 behavior must be preserved

Locate the historical source revision that produced 1.5.45, then backport the modern Android platform
layer/build changes instead of modifying this split APK binary in place. Keep the emulator behavior
changes isolated from the Android compatibility changes.
