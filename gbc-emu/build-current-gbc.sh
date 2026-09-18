#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PIN="1c12fac5ce49badaadff2e2f210dcc30b89f4943"
: "${WORKDIR:=$PWD/gbc-modern-build}"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [ ! -d emu-ex-plus-alpha/.git ]; then
  git clone https://github.com/Rakashazi/emu-ex-plus-alpha.git
fi

cd emu-ex-plus-alpha
git fetch --all --tags
git checkout --detach "$PIN"

export IMAGINE_PATH="$PWD/imagine"
export EMUFRAMEWORK_PATH="$PWD/EmuFramework"
export IMAGINE_SDK_PATH="$WORKDIR/imagine-sdk"
mkdir -p "$IMAGINE_SDK_PATH"

if [ -z "${ANDROID_NDK_PATH:-${ANDROID_NDK_HOME:-}}" ]; then
  echo "Set ANDROID_NDK_PATH or ANDROID_NDK_HOME to workspace pin: NDK r30 / 30.0.16248370." >&2
  exit 2
fi
export ANDROID_NDK_PATH="${ANDROID_NDK_PATH:-$ANDROID_NDK_HOME}"

(
  cd imagine/bundle/all
  ./makeAll-android.sh install
)

"$IMAGINE_PATH/android.sh" config
"$IMAGINE_PATH/android.sh" installLinks --config Release
"$EMUFRAMEWORK_PATH/android.sh" config
"$EMUFRAMEWORK_PATH/android.sh" installLinks --config Release

cd GBC.emu
make -f android.mk android-apk CONFIG=Release android_arch="arm64" -j"$(nproc)"

echo
echo "APK output:"
find build/android/build/outputs/apk -name '*.apk' -print

ROOT_TOOLS="$SCRIPT_DIR/../tools"
while IFS= read -r apk; do
  python3 "$ROOT_TOOLS/verify_modern_apk.py" "$apk" --require-arm64 --require-16k
done < <(find build/android/build/outputs/apk -name '*.apk' -type f)
