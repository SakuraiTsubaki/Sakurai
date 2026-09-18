# Direct ADB install

Use this when tapping the APK does not open Android's Package Installer at all.

## Windows

1. Install the latest Android SDK Platform-Tools.
2. Enable **Developer options → USB debugging** on the phone.
3. Connect USB and approve the RSA debugging prompt.
4. Put the APK next to `install-via-adb.bat`.
5. Run:

```bat
install-via-adb.bat MyBoy-1.8.0-arm64-v2v3.apk
```

## macOS / Linux

```bash
bash install-via-adb.sh MyBoy-1.8.0-arm64-v2v3.apk
```

## Existing original My Boy!

The modernized APK is signed with a different key from the store/original package. If the original
`com.fastemulator.gba` is still installed, Android can reject the new APK with
`INSTALL_FAILED_UPDATE_INCOMPATIBLE`.

Back up saves first, then uninstall the original package and retry:

```bash
adb uninstall com.fastemulator.gba
adb install --no-incremental MyBoy-1.8.0-arm64-v2v3.apk
```

The exact `Failure [INSTALL_FAILED_...]` text is the most useful diagnostic if installation still fails.
