#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "usage: $0 ORIGINAL.apk libgba.so OUTPUT.apk [KEYSTORE]" >&2
  exit 2
fi

ORIGINAL="$(realpath "$1")"
LIB="$(realpath "$2")"
OUTPUT="$(realpath -m "$3")"
KEYSTORE="${4:-$HOME/.android/myboy-modern-debug.keystore}"
ALIAS="androiddebugkey"
PASS="android"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

for tool in unzip zip zipalign apksigner keytool; do
  command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 3; }
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/apk"
(
  cd "$TMP/apk"
  unzip -q "$ORIGINAL"
  rm -rf META-INF
  mkdir -p lib/arm64-v8a
  cp "$LIB" lib/arm64-v8a/libgba.so
  zip -qr "$TMP/unsigned.apk" .
)

zipalign -P 16 -f 4 "$TMP/unsigned.apk" "$TMP/aligned.apk"

if [ ! -f "$KEYSTORE" ]; then
  mkdir -p "$(dirname "$KEYSTORE")"
  keytool -genkeypair -noprompt     -keystore "$KEYSTORE"     -storepass "$PASS" -keypass "$PASS"     -alias "$ALIAS"     -dname "CN=MyBoy Modern Local Build,O=Local,C=KR"     -keyalg RSA -keysize 2048 -validity 10000
fi

apksigner sign   --ks "$KEYSTORE"   --ks-key-alias "$ALIAS"   --ks-pass "pass:$PASS"   --key-pass "pass:$PASS"   --out "$OUTPUT"   "$TMP/aligned.apk"

apksigner verify --verbose --print-certs "$OUTPUT"
python3 "$ROOT/tools/verify_modern_apk.py" "$OUTPUT" --require-arm64 --require-16k

echo
echo "Created: $OUTPUT"
echo "NOTE: this APK is signed with a new key and cannot update over the original"
echo "Play/store-signed package. Back up saves, uninstall the old app, then install."
