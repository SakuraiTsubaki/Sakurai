#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 MyBoy-1.8.0-arm64.apk" >&2
  exit 2
fi
APK="$1"
PKG="com.fastemulator.gba"

command -v adb >/dev/null || { echo "adb is required" >&2; exit 3; }
adb get-state >/dev/null

ABI="$(adb shell getprop ro.product.cpu.abi | tr -d '')"
SDK="$(adb shell getprop ro.build.version.sdk | tr -d '')"
PAGE="$(adb shell getconf PAGESIZE 2>/dev/null | tr -d '' || true)"
echo "Device ABI: $ABI"
echo "Android API: $SDK"
echo "Page size: ${PAGE:-unknown}"

python3 "$(cd "$(dirname "$0")/../.." && pwd)/tools/verify_modern_apk.py"   "$APK" --require-arm64 --require-16k

if adb shell pm path "$PKG" >/dev/null 2>&1; then
  echo
  echo "$PKG is already installed. If it is the original store-signed app," >&2
  echo "back up saves and uninstall it before installing this differently signed build." >&2
  exit 4
fi

adb install "$APK"
adb logcat -c
adb shell monkey -p "$PKG" -c android.intent.category.LAUNCHER 1 >/dev/null
sleep 2

echo
echo "--- relevant logcat ---"
adb logcat -d -v brief | grep -E 'MyBoyArm64|AndroidRuntime|linker|UnsatisfiedLinkError|FATAL EXCEPTION' || true
