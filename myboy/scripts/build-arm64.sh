#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$HERE/app/src/main/cpp"
BUILD="$HERE/build/arm64-v8a"

NDK="${ANDROID_NDK_HOME:-${ANDROID_NDK_ROOT:-}}"
if [ -z "$NDK" ]; then
  echo "Set ANDROID_NDK_HOME (workspace pin: NDK r30 / 30.0.16248370)." >&2
  exit 2
fi

cmake -S "$SRC" -B "$BUILD" -G Ninja   -DCMAKE_TOOLCHAIN_FILE="$NDK/build/cmake/android.toolchain.cmake"   -DANDROID_ABI=arm64-v8a   -DANDROID_PLATFORM=android-24   -DANDROID_STL=c++_static   -DCMAKE_BUILD_TYPE=Release

cmake --build "$BUILD" --target gba -j

SO="$(find "$BUILD" -name 'libgba.so' -type f | head -n1)"
if [ -z "$SO" ]; then
  echo "libgba.so not found" >&2
  exit 3
fi

mkdir -p "$HERE/out"
cp "$SO" "$HERE/out/libgba.so"

echo "Built: $HERE/out/libgba.so"
file "$HERE/out/libgba.so" || true

READELF="${READELF:-readelf}"
echo
echo "PT_LOAD alignment:"
"$READELF" -lW "$HERE/out/libgba.so" | grep ' LOAD ' || true
echo
echo "Expected: AArch64/ELF64 and LOAD Align >= 0x4000."
