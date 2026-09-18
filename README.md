# Android emulator modernization workspace

Modernization work for the two APKs supplied in this chat:

- **GBC.emu 1.5.45** — source-rebuild track
- **My Boy! 1.8.0** — legacy Java/UI + replacement ARM64 native engine track

Start with:

- `STATUS.md` — current truth table
- `PHASE3.md` — newest patch/link/verification work
- `myboy/jni_contract.json` — JNI compatibility contract extracted from the supplied APK

## My Boy! build order

```bash
cd myboy
./scripts/fetch-mgba.sh
export ANDROID_NDK_HOME=/path/to/android-ndk-r28-or-newer
./scripts/build-arm64.sh
./scripts/repack-apk.sh "/path/to/My Boy!.1.8.0.apk" out/libgba.so MyBoy-1.8.0-arm64.apk
./scripts/device-smoke-test.sh MyBoy-1.8.0-arm64.apk
```

The repacked APK is signed with a new local key and therefore cannot update over the original store-signed package.

## GBC.emu build order

Set `ANDROID_NDK_PATH`/`ANDROID_NDK_HOME` to a recent NDK and run:

```bash
./gbc-emu/build-current-gbc.sh
```

The script builds the currently pinned upstream ARM64 app and then runs the same ARM64/16 KiB APK verifier.

## Distribution vs. sideload compatibility

For the first My Boy! compatibility milestone, the old Java application's target SDK is intentionally not raised immediately. Native ARM64/16 KiB compatibility is isolated first. A store-ready modern fork is a later migration because raising the target SDK activates storage, Bluetooth, exported-component, notification, and other modern Android behavior requirements across the old Java layer.
