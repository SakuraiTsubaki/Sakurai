# Android emulator modernization workspace

Modernization work for the two supplied APKs:

- **GBC.emu 1.5.45** — source-rebuild track
- **My Boy! 1.8.0** — legacy Java/UI + replacement ARM64 native engine track

Current build baseline:

- **Android NDK r30**
- SDK/Gradle NDK version: `30.0.16248370`
- `arm64-v8a`
- 16 KiB page-size-compatible native linking
- GitHub Actions build automation

Start with:

- `STATUS.md` — current truth table
- `PHASE3.md` — patch/link/verification work
- `PHASE4.md` — NDK r30 + GitHub Actions
- `myboy/jni_contract.json` — JNI compatibility contract extracted from the supplied APK

## My Boy! build

```bash
cd myboy
./scripts/fetch-mgba.sh
export ANDROID_NDK_HOME=/path/to/android-ndk-r30
./scripts/build-arm64.sh
./scripts/repack-apk.sh "/path/to/My Boy!.1.8.0.apk" out/libgba.so MyBoy-1.8.0-arm64.apk
./scripts/device-smoke-test.sh MyBoy-1.8.0-arm64.apk
```

The repacked APK is signed with a new local key and therefore cannot update over the original store-signed package.

## GBC.emu build

Set `ANDROID_NDK_PATH` or `ANDROID_NDK_HOME` to NDK r30 and run:

```bash
./gbc-emu/build-current-gbc.sh
```

## GitHub Actions

`.github/workflows/android-arm64.yml` builds:

- `myboy-arm64-ndk-r30`
- `gbc-emu-arm64-ndk-r30`

The My Boy job also verifies ELF64/AArch64 and 16 KiB PT_LOAD alignment.
