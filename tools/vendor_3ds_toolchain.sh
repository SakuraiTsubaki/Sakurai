#!/usr/bin/env bash
set -euo pipefail
ROOT="${PROJECT_ROOT:-$PWD}"
VENDOR_ROOT="$ROOT/vendor/toolchain/linux-x86_64"
BINUTILS_VERSION="${BINUTILS_VERSION:-2.47}"
THREEDSTOOL_COMMIT="${THREEDSTOOL_COMMIT:-3771ae967d64092370b646db86aa626401c279e8}"
PROJECT_CTR_COMMIT="${PROJECT_CTR_COMMIT:-e8f5f529c54ff9b22a2491a480ffa69206bf7b19}"
AZAHAR_VERSION="${AZAHAR_VERSION:-2126.1.1}"
TMP="$ROOT/_toolbuild"
rm -rf "$TMP" "$VENDOR_ROOT"
mkdir -p "$TMP" "$VENDOR_ROOT/source" "$VENDOR_ROOT/bin" "$VENDOR_ROOT/licenses"

sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential bison flex texinfo curl xz-utils ca-certificates git cmake pkg-config libcurl4-openssl-dev libssl-dev zlib1g-dev

curl -fL --retry 3 "https://ftp.gnu.org/gnu/binutils/binutils-${BINUTILS_VERSION}.tar.xz" -o "$TMP/binutils-${BINUTILS_VERSION}.tar.xz"
cp "$TMP/binutils-${BINUTILS_VERSION}.tar.xz" "$VENDOR_ROOT/source/"
tar -xJf "$TMP/binutils-${BINUTILS_VERSION}.tar.xz" -C "$TMP"
mkdir "$TMP/binutils-build"
(
  cd "$TMP/binutils-build"
  "../binutils-${BINUTILS_VERSION}/configure" --target=arm-none-eabi --prefix="$VENDOR_ROOT/binutils" --disable-nls --disable-werror --disable-gdb --disable-sim
  make -j2
  make install
)
for tool in "$VENDOR_ROOT/binutils/bin"/arm-none-eabi-*; do name="$(basename "$tool")"; ln -sfn "../binutils/bin/$name" "$VENDOR_ROOT/bin/$name"; done

git clone https://github.com/dnasdw/3dstool.git "$TMP/3dstool"
git -C "$TMP/3dstool" checkout "$THREEDSTOOL_COMMIT"
git -C "$TMP/3dstool" archive --format=tar.gz --output="$VENDOR_ROOT/source/3dstool-${THREEDSTOOL_COMMIT}.tar.gz" "$THREEDSTOOL_COMMIT"
cmake -S "$TMP/3dstool" -B "$TMP/3dstool/build" -DUSE_DEP=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build "$TMP/3dstool/build" -j2
THREEDSTOOL_BIN="$(find "$TMP/3dstool/build" -type f -name 3dstool -perm -111 -print -quit)"
[[ -n "$THREEDSTOOL_BIN" ]]
cp "$THREEDSTOOL_BIN" "$VENDOR_ROOT/bin/3dstool"
chmod 0755 "$VENDOR_ROOT/bin/3dstool"
find "$TMP/3dstool" -maxdepth 2 -iname 'LICENSE*' -o -iname 'COPYING*' | head -n1 | xargs -r -I{} cp '{}' "$VENDOR_ROOT/licenses/3dstool-LICENSE"

git clone https://github.com/3DSGuy/Project_CTR.git "$TMP/Project_CTR"
git -C "$TMP/Project_CTR" checkout "$PROJECT_CTR_COMMIT"
git -C "$TMP/Project_CTR" archive --format=tar.gz --output="$VENDOR_ROOT/source/Project_CTR-${PROJECT_CTR_COMMIT}.tar.gz" "$PROJECT_CTR_COMMIT"
(cd "$TMP/Project_CTR" && make -j2)
for name in ctrtool makerom; do
  f="$(find "$TMP/Project_CTR" -type f -name "$name" -perm -111 -print -quit)"
  [[ -n "$f" ]]
  cp "$f" "$VENDOR_ROOT/bin/$name"
  chmod 0755 "$VENDOR_ROOT/bin/$name"
done
find "$TMP/Project_CTR" -maxdepth 2 -iname 'LICENSE*' -o -iname 'COPYING*' | head -n1 | xargs -r -I{} cp '{}' "$VENDOR_ROOT/licenses/Project_CTR-LICENSE"

mkdir -p "$VENDOR_ROOT/azahar"
curl -fL --retry 3 "https://github.com/azahar-emu/azahar/releases/download/${AZAHAR_VERSION}/azahar.AppImage" -o "$VENDOR_ROOT/azahar/azahar.AppImage"
echo 'e445dabc18fe7665867e24a18a78e24e133261a9cc320fae6a4a45bd2e7c4783  '"$VENDOR_ROOT/azahar/azahar.AppImage" | sha256sum -c -
chmod 0755 "$VENDOR_ROOT/azahar/azahar.AppImage"
curl -fL --retry 3 "https://github.com/azahar-emu/azahar/releases/download/${AZAHAR_VERSION}/azahar-unified-source-${AZAHAR_VERSION}.tar.xz" -o "$VENDOR_ROOT/source/azahar-unified-source-${AZAHAR_VERSION}.tar.xz"
echo '023b4b37fe8cbc6b59a7be5270a8c93d9c58f90cd8c6d8e00705b43f4c9ebee1  '"$VENDOR_ROOT/source/azahar-unified-source-${AZAHAR_VERSION}.tar.xz" | sha256sum -c -
cat > "$VENDOR_ROOT/bin/azahar" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
H="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export APPIMAGE_EXTRACT_AND_RUN=1
[[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] || export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
exec "$H/../azahar/azahar.AppImage" "$@"
EOF
chmod 0755 "$VENDOR_ROOT/bin/azahar"

cat > "$VENDOR_ROOT/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$R/bin:$R/binutils/bin:$PATH"
EOF
chmod 0755 "$VENDOR_ROOT/activate.sh"
printf '# 3DS vendored toolchain\nGNU binutils %s; 3dstool %s; Project_CTR %s; Azahar %s. No ROMs/keys/firmware.\n' "$BINUTILS_VERSION" "$THREEDSTOOL_COMMIT" "$PROJECT_CTR_COMMIT" "$AZAHAR_VERSION" > "$VENDOR_ROOT/VERSIONS.md"
(cd "$VENDOR_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
"$VENDOR_ROOT/bin/3dstool" -h >/dev/null 2>&1 || true
"$VENDOR_ROOT/bin/ctrtool" --help >/dev/null 2>&1 || true
"$VENDOR_ROOT/bin/makerom" -h >/dev/null 2>&1 || true
rm -rf "$TMP"
