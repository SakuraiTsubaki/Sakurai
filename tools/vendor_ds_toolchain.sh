#!/usr/bin/env bash
set -euo pipefail
ROOT="${PROJECT_ROOT:-$PWD}"
VENDOR_ROOT="$ROOT/vendor/toolchain/linux-x86_64"
BINUTILS_VERSION="${BINUTILS_VERSION:-2.47}"
NDSTOOL_VERSION="${NDSTOOL_VERSION:-2.3.1}"
MELONDS_VERSION="${MELONDS_VERSION:-1.1}"
TMP="$ROOT/_toolbuild"
rm -rf "$TMP" "$VENDOR_ROOT"
mkdir -p "$TMP" "$VENDOR_ROOT/source" "$VENDOR_ROOT/bin" "$VENDOR_ROOT/licenses"

sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential bison flex texinfo curl xz-utils unzip ca-certificates autoconf automake libtool pkg-config

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
for tool in "$VENDOR_ROOT/binutils/bin"/arm-none-eabi-*; do
  name="$(basename "$tool")"
  ln -sfn "../binutils/bin/$name" "$VENDOR_ROOT/bin/$name"
done

curl -fL --retry 3 "https://github.com/devkitPro/ndstool/archive/refs/tags/v${NDSTOOL_VERSION}.tar.gz" -o "$TMP/ndstool-${NDSTOOL_VERSION}.tar.gz"
cp "$TMP/ndstool-${NDSTOOL_VERSION}.tar.gz" "$VENDOR_ROOT/source/"
tar -xzf "$TMP/ndstool-${NDSTOOL_VERSION}.tar.gz" -C "$TMP"
NDSSRC="$TMP/ndstool-${NDSTOOL_VERSION}"
(
  cd "$NDSSRC"
  ./autogen.sh
  ./configure --prefix="$VENDOR_ROOT/ndstool"
  make -j2
  make install
)
ln -sfn ../ndstool/bin/ndstool "$VENDOR_ROOT/bin/ndstool"
cp "$NDSSRC/COPYING" "$VENDOR_ROOT/licenses/ndstool-COPYING"

MELON_ZIP="$TMP/melonDS-${MELONDS_VERSION}-appimage-x86_64.zip"
curl -fL --retry 3 "https://github.com/melonDS-emu/melonDS/releases/download/${MELONDS_VERSION}/melonDS-${MELONDS_VERSION}-appimage-x86_64.zip" -o "$MELON_ZIP"
echo 'bf377420a2e95f2cd2cdda17d5372b51c2534f858b038db9ec6d129554875124  '"$MELON_ZIP" | sha256sum -c -
mkdir -p "$TMP/melonds-unzip" "$VENDOR_ROOT/melonds"
unzip -q "$MELON_ZIP" -d "$TMP/melonds-unzip"
MELON_APP="$(find "$TMP/melonds-unzip" -type f -iname '*.AppImage' -print -quit)"
[[ -n "$MELON_APP" ]]
cp "$MELON_APP" "$VENDOR_ROOT/melonds/melonDS.AppImage"
chmod 0755 "$VENDOR_ROOT/melonds/melonDS.AppImage"
curl -fL --retry 3 "https://github.com/melonDS-emu/melonDS/archive/refs/tags/${MELONDS_VERSION}.tar.gz" -o "$VENDOR_ROOT/source/melonDS-${MELONDS_VERSION}.tar.gz"
curl -fL --retry 3 "https://raw.githubusercontent.com/melonDS-emu/melonDS/${MELONDS_VERSION}/LICENSE" -o "$VENDOR_ROOT/licenses/melonDS-LICENSE" || true
cat > "$VENDOR_ROOT/bin/melonds" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
H="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export APPIMAGE_EXTRACT_AND_RUN=1
[[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] || export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
exec "$H/../melonds/melonDS.AppImage" "$@"
EOF
chmod 0755 "$VENDOR_ROOT/bin/melonds"

cat > "$VENDOR_ROOT/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$R/bin:$R/binutils/bin:$R/ndstool/bin:$PATH"
EOF
chmod 0755 "$VENDOR_ROOT/activate.sh"
printf '# DS vendored toolchain\nGNU binutils %s; ndstool %s; melonDS %s. No ROMs/BIOS/firmware/keys.\n' "$BINUTILS_VERSION" "$NDSTOOL_VERSION" "$MELONDS_VERSION" > "$VENDOR_ROOT/VERSIONS.md"
(cd "$VENDOR_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
"$VENDOR_ROOT/bin/arm-none-eabi-as" --version
"$VENDOR_ROOT/bin/ndstool" -h >/dev/null 2>&1 || true
rm -rf "$TMP"
