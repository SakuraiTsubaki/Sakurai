#!/usr/bin/env bash
set -euo pipefail
ROOT="${PROJECT_ROOT:-$PWD}"
VENDOR_ROOT="$ROOT/vendor/toolchain/linux-x86_64"
BINUTILS_VERSION="${BINUTILS_VERSION:-2.47}"
MELONDS_VERSION="${MELONDS_VERSION:-1.1}"
MELONDS_SHA256="${MELONDS_SHA256:-99465129f5413b2aad332e4377e523cf3cda905dc329d47dcb1ad01ce2cb3f66}"
TMP="$ROOT/_toolbuild"
rm -rf "$TMP" "$VENDOR_ROOT"
mkdir -p "$TMP" "$VENDOR_ROOT/source" "$VENDOR_ROOT/bin" "$VENDOR_ROOT/licenses" "$VENDOR_ROOT/melonds"

sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential bison flex texinfo curl xz-utils unzip ca-certificates zstd clang llvm lld

# Portable ARM GNU binutils, committed directly in the repository.
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

# melonDS 1.1 release, pinned by the repository manifests used by HG/SS.
curl -fL --retry 3 "https://github.com/melonDS-emu/melonDS/releases/download/${MELONDS_VERSION}/melonDS-${MELONDS_VERSION}-ubuntu-x86_64.zip" -o "$TMP/melonds.zip"
echo "$MELONDS_SHA256  $TMP/melonds.zip" | sha256sum -c -
unzip -q "$TMP/melonds.zip" -d "$VENDOR_ROOT/melonds"
melonds_bin="$(find "$VENDOR_ROOT/melonds" -maxdepth 3 -type f \( -name melonDS -o -name melonds \) -print -quit)"
if [[ -n "$melonds_bin" ]]; then chmod 0755 "$melonds_bin"; ln -sfn "../melonds/${melonds_bin#"$VENDOR_ROOT/melonds/"}" "$VENDOR_ROOT/bin/melonDS"; fi

# LLVM/Clang runtime is packaged as a per-repository release cache because
# libLLVM can exceed GitHub's 100 MiB ordinary Git-blob limit.
LLVM_STAGE="$TMP/llvm-runtime"
mkdir -p "$LLVM_STAGE/bin" "$LLVM_STAGE/lib"
for x in clang ld.lld llvm-objcopy llvm-objdump llvm-readobj llvm-readelf; do
  p="$(command -v "$x" 2>/dev/null || true)"; [[ -n "$p" ]] || continue
  cp -L "$p" "$LLVM_STAGE/bin/$x"
  ldd "$p" 2>/dev/null | awk '/=> \/.* \(/ {print $3} /^\// {print $1}' | while read -r lib; do [[ -f "$lib" ]] && cp -Ln "$lib" "$LLVM_STAGE/lib/$(basename "$lib")" || true; done
done
cat > "$LLVM_STAGE/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$R/bin:$PATH"
export LD_LIBRARY_PATH="$R/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
EOF
chmod 0755 "$LLVM_STAGE/activate.sh"
tar --zstd -cf "$ROOT/nds-llvm-runtime-linux-x86_64.tar.zst" -C "$LLVM_STAGE" .

cat > "$VENDOR_ROOT/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$R/bin:$R/binutils/bin:$PATH"
EOF
chmod 0755 "$VENDOR_ROOT/activate.sh"
printf '# NDS vendored toolchain — Linux x86_64\nGNU binutils %s (arm-none-eabi); melonDS %s. LLVM runtime is stored as this repository’s GitHub Release asset. No ROMs, firmware, keys, NitroSDK, or proprietary matching compiler are included.\n' "$BINUTILS_VERSION" "$MELONDS_VERSION" > "$VENDOR_ROOT/VERSIONS.md"
(cd "$VENDOR_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
"$VENDOR_ROOT/bin/arm-none-eabi-objdump" --version | head -1
rm -rf "$TMP"
