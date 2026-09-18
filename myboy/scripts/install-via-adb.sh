#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "usage: $0 MyBoy-1.8.0-arm64-v2v3.apk" >&2
  exit 2
fi
command -v adb >/dev/null || { echo "ERROR: adb not found. Install Android SDK Platform-Tools first." >&2; exit 3; }

echo "=== Connected devices ==="
adb devices

echo
echo "=== Package check ==="
adb shell pm path com.fastemulator.gba 2>/dev/null || true

echo
echo "=== Installing APK directly via adb ==="
adb install --no-incremental "$1"
echo
echo 'If installation failed, copy the exact "Failure [INSTALL_FAILED_...]" line.'
