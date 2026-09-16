#!/usr/bin/env bash
set -euo pipefail
ROOT="${PROJECT_ROOT:-$PWD}"
VENDOR_ROOT="$ROOT/vendor/toolchain/linux-x86_64"
BINUTILS_VERSION="${BINUTILS_VERSION:-2.47}"
AGBCC_COMMIT="${AGBCC_COMMIT:-da598c1d918402c42c0c0d7128ba14567f3175e9}"
MGBA_VERSION="${MGBA_VERSION:-0.10.5}"
TMP="$ROOT/_toolbuild"
rm -rf "$TMP" "$VENDOR_ROOT"
mkdir -p "$TMP" "$VENDOR_ROOT/source" "$VENDOR_ROOT/bin" "$VENDOR_ROOT/licenses"

sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential bison flex texinfo curl xz-utils ca-certificates

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

mkdir -p "$VENDOR_ROOT/agbcc"
curl -fL --retry 3 https://github.com/pret/agbcc/releases/download/release/agbcc.tar.gz -o "$TMP/agbcc.tar.gz"
echo 'bcf0197e3e27d8e08506a142e25fa68ea7f6679a98347a6406804eb3f9ff4d29  '"$TMP/agbcc.tar.gz" | sha256sum -c -
tar -xzf "$TMP/agbcc.tar.gz" -C "$VENDOR_ROOT/agbcc"
cp "$TMP/agbcc.tar.gz" "$VENDOR_ROOT/source/agbcc-release.tar.gz"
curl -fL --retry 3 "https://github.com/pret/agbcc/archive/${AGBCC_COMMIT}.tar.gz" -o "$VENDOR_ROOT/source/agbcc-source-${AGBCC_COMMIT}.tar.gz"

mkdir -p "$VENDOR_ROOT/mgba"
curl -fL --retry 3 "https://github.com/mgba-emu/mgba/releases/download/${MGBA_VERSION}/mGBA-${MGBA_VERSION}-appimage-x64.appimage" -o "$VENDOR_ROOT/mgba/mGBA.AppImage"
echo 'fdf0a5c1588e1606c38315735cf48a9f9dca3573f32a3947ebc956f8297e85cd  '"$VENDOR_ROOT/mgba/mGBA.AppImage" | sha256sum -c -
chmod 0755 "$VENDOR_ROOT/mgba/mGBA.AppImage"
curl -fL --retry 3 "https://github.com/mgba-emu/mgba/archive/refs/tags/${MGBA_VERSION}.tar.gz" -o "$VENDOR_ROOT/source/mgba-${MGBA_VERSION}.tar.gz"
curl -fL --retry 3 "https://raw.githubusercontent.com/mgba-emu/mgba/${MGBA_VERSION}/LICENSE" -o "$VENDOR_ROOT/licenses/mGBA-LICENSE"
cat > "$VENDOR_ROOT/bin/mgba" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
H="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export APPIMAGE_EXTRACT_AND_RUN=1
[[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] || export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
exec "$H/../mgba/mGBA.AppImage" "$@"
EOF
chmod 0755 "$VENDOR_ROOT/bin/mgba"
cat > "$VENDOR_ROOT/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$R/bin:$R/binutils/bin:$PATH"
EOF
chmod 0755 "$VENDOR_ROOT/activate.sh"
printf '# GBA vendored toolchain\nGNU binutils %s; agbcc %s; mGBA %s. No ROMs/keys/firmware.\n' "$BINUTILS_VERSION" "$AGBCC_COMMIT" "$MGBA_VERSION" > "$VENDOR_ROOT/VERSIONS.md"
(cd "$VENDOR_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
"$VENDOR_ROOT/bin/arm-none-eabi-as" --version
rm -rf "$TMP"
