#!/usr/bin/env bash
set -euo pipefail

ROOT="${PROJECT_ROOT:-$PWD}"
VENDOR="$ROOT/vendor/toolchain/linux-x86_64"
TMP="$ROOT/_toolbuild"
CHUNK_SIZE="45m"
HACTOOL_COMMIT="1d64a83450e025622f3468c28fc4164dad2c5ef6"
GHIDRA_VERSION="12.1.3"
GHIDRA_ARCHIVE="ghidra_12.1.3_PUBLIC_20260817.zip"
GHIDRA_SHA256="93a5d11a9ad510622acaaf908c556a7b9b764d338e78a7567f3689bf5081fd54"
SWITCH_LOADER_COMMIT="1f479fc8eb24479f0e5f74ccd4dd4103a10ac24d"
DOTNET_VERSION="10.0.401"
PKNX_COMMIT="d191cd0e5c05f2af81d9a41c1f1d82e6621b351a"
RYUBING_COMMIT="793ca017ff4f6e48b798a62d2486405bfc42ef39"

rm -rf "$TMP" "$VENDOR"
mkdir -p "$TMP" "$VENDOR"/{bin,source,licenses,eden,ghidra,dotnet,aarch64,llvm}

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  build-essential git curl ca-certificates python3 file unzip zip zstd xz-utils \
  openjdk-21-jdk-headless binutils-aarch64-linux-gnu clang llvm lld cmake ninja-build

JAVAC21="$(dpkg -L openjdk-21-jdk-headless | awk '/\/bin\/javac$/ {print; exit}')"
JDK21_HOME="$(dirname "$(dirname "$JAVAC21")")"
test -x "$JDK21_HOME/bin/javac"
"$JDK21_HOME/bin/java" -version

# Keep the decompressor in the repository too; materialization must not require apt.
cp "$(command -v zstd)" "$VENDOR/bin/zstd"
chmod 0755 "$VENDOR/bin/zstd"

split_store() {
  local src="$1" dir="$2" stem="$3"
  mkdir -p "$dir"
  sha256sum "$src" > "$dir/$stem.sha256"
  split -b "$CHUNK_SIZE" -d -a 3 "$src" "$dir/$stem.part."
}

source_archive() {
  local repo="$1" commit="$2" name="$3"
  git clone --filter=blob:none "$repo" "$TMP/$name"
  git -C "$TMP/$name" checkout --detach "$commit"
  git -C "$TMP/$name" archive --format=tar.gz --output="$VENDOR/source/${name}-${commit}.tar.gz" "$commit"
}

cat > "$VENDOR/bin/_materialize" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DIR="$1" STEM="$2" CACHE="$3"
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPECTED="$(awk '{print $1}' "$DIR/$STEM.sha256")"
STAMP="$CACHE/.ready"
if [[ ! -f "$STAMP" ]] || [[ "$(cat "$STAMP" 2>/dev/null || true)" != "$EXPECTED" ]]; then
  rm -rf "$CACHE"; mkdir -p "$CACHE"
  cat "$DIR/$STEM.part."* | "$B/zstd" -d -q | tar -xf - -C "$CACHE"
  printf '%s\n' "$EXPECTED" > "$STAMP"
fi
EOF
chmod 0755 "$VENDOR/bin/_materialize"

# hactool.
git clone https://github.com/SciresM/hactool.git "$TMP/hactool"
git -C "$TMP/hactool" checkout --detach "$HACTOOL_COMMIT"
git -C "$TMP/hactool" submodule update --init --recursive
git -C "$TMP/hactool" archive --format=tar.gz --output="$VENDOR/source/hactool-${HACTOOL_COMMIT}.tar.gz" "$HACTOOL_COMMIT"
cp "$TMP/hactool/config.mk.template" "$TMP/hactool/config.mk"
(cd "$TMP/hactool" && make -j2)
cp "$TMP/hactool/hactool" "$VENDOR/bin/hactool"
chmod 0755 "$VENDOR/bin/hactool"
cp "$TMP/hactool/LICENSE" "$VENDOR/licenses/hactool-LICENSE" 2>/dev/null || true

# Eden emulator AppImage bytes, chunked under GitHub's per-blob limit.
curl -fsSL https://nightly.eden-emu.dev/latest/release.json -o "$VENDOR/eden/release.json"
EDEN_URL="$(python3 - "$VENDOR/eden/release.json" <<'PY'
import json,sys
x=json.load(open(sys.argv[1],encoding='utf-8')); vals=[]; q=[x]
while q:
    v=q.pop()
    if isinstance(v,dict): q.extend(v.values())
    elif isinstance(v,list): q.extend(v)
    elif isinstance(v,str): vals.append(v)
c=[]
for s in vals:
    lo=s.lower()
    if s.startswith('http') and lo.endswith('.appimage') and ('amd64' in lo or 'x86_64' in lo):
        c.append(((3 if 'pgo' in lo else 0)+(2 if 'amd64' in lo else 0),s))
if not c: raise SystemExit('no Linux amd64 Eden AppImage in release metadata')
print(max(c)[1])
PY
)"
printf '%s\n' "$EDEN_URL" > "$VENDOR/eden/DOWNLOAD_URL.txt"
curl -fL --retry 3 "$EDEN_URL" -o "$TMP/Eden.AppImage"
sha256sum "$TMP/Eden.AppImage" > "$VENDOR/eden/Eden.AppImage.sha256"
split -b "$CHUNK_SIZE" -d -a 3 "$TMP/Eden.AppImage" "$VENDOR/eden/Eden.AppImage.part."
cat > "$VENDOR/bin/eden" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; V="$B/../eden"; C="${XDG_CACHE_HOME:-/tmp}/sakurai-eden"; mkdir -p "$C"
A="$C/Eden.AppImage"; E="$(awk '{print $1}' "$V/Eden.AppImage.sha256")"
if [[ ! -x "$A" ]] || [[ "$(sha256sum "$A" 2>/dev/null | awk '{print $1}')" != "$E" ]]; then cat "$V"/Eden.AppImage.part.* > "$A"; chmod 0755 "$A"; echo "$E  $A" | sha256sum -c - >/dev/null; fi
export APPIMAGE_EXTRACT_AND_RUN=1; [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] || export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"; exec "$A" "$@"
EOF
chmod 0755 "$VENDOR/bin/eden"

# Ghidra 12.1.3 + JDK 21 + Switch Loader, preassembled and chunked.
curl -fL --retry 3 "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_${GHIDRA_VERSION}_build/$GHIDRA_ARCHIVE" -o "$TMP/$GHIDRA_ARCHIVE"
echo "$GHIDRA_SHA256  $TMP/$GHIDRA_ARCHIVE" | sha256sum -c -
unzip -q "$TMP/$GHIDRA_ARCHIVE" -d "$TMP/ghidra-unpack"
GHIDRA_HOME="$(find "$TMP/ghidra-unpack" -maxdepth 1 -mindepth 1 -type d -name 'ghidra_*_PUBLIC' | head -n1)"
git clone https://github.com/Adubbz/Ghidra-Switch-Loader.git "$TMP/switch-loader"
git -C "$TMP/switch-loader" checkout --detach "$SWITCH_LOADER_COMMIT"
(cd "$TMP/switch-loader" && JAVA_HOME="$JDK21_HOME" PATH="$JDK21_HOME/bin:$PATH" GHIDRA_INSTALL_DIR="$GHIDRA_HOME" ./gradlew --no-daemon)
LOADER_ZIP="$(find "$TMP/switch-loader/dist" -type f -name '*.zip' | head -n1)"
test -f "$LOADER_ZIP"
mkdir -p "$GHIDRA_HOME/Ghidra/Extensions"
unzip -q "$LOADER_ZIP" -d "$GHIDRA_HOME/Ghidra/Extensions"
git -C "$TMP/switch-loader" archive --format=tar.gz --output="$VENDOR/source/Ghidra-Switch-Loader-${SWITCH_LOADER_COMMIT}.tar.gz" "$SWITCH_LOADER_COMMIT"
READY="$TMP/ghidra-ready"; mkdir -p "$READY"
cp -a "$GHIDRA_HOME" "$READY/ghidra"; cp -a "$JDK21_HOME" "$READY/jdk"
tar -C "$READY" -cf - ghidra jdk | zstd -19 -T0 -q -o "$TMP/ghidra-ready.tar.zst"
split_store "$TMP/ghidra-ready.tar.zst" "$VENDOR/ghidra" ghidra-ready.tar.zst
cat > "$VENDOR/bin/ghidra" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; C="${XDG_CACHE_HOME:-/tmp}/sakurai-ghidra-12.1.3"; "$B/_materialize" "$B/../ghidra" ghidra-ready.tar.zst "$C"; export JAVA_HOME="$C/jdk"; exec "$C/ghidra/ghidraRun" "$@"
EOF
cat > "$VENDOR/bin/ghidra-headless" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; C="${XDG_CACHE_HOME:-/tmp}/sakurai-ghidra-12.1.3"; "$B/_materialize" "$B/../ghidra" ghidra-ready.tar.zst "$C"; export JAVA_HOME="$C/jdk"; exec "$C/ghidra/support/analyzeHeadless" "$@"
EOF
chmod 0755 "$VENDOR/bin/ghidra" "$VENDOR/bin/ghidra-headless"

# .NET 10 SDK + prebuilt Ryubing.
curl -fsSL https://dot.net/v1/dotnet-install.sh -o "$TMP/dotnet-install.sh"
bash "$TMP/dotnet-install.sh" --version "$DOTNET_VERSION" --install-dir "$TMP/dotnet"
git clone https://github.com/Leuconoe/Ryubing.git "$TMP/Ryubing"
git -C "$TMP/Ryubing" checkout --detach "$RYUBING_COMMIT"
git -C "$TMP/Ryubing" submodule update --init --recursive
"$TMP/dotnet/dotnet" build "$TMP/Ryubing" -c Release -o "$TMP/ryubing-build"
git -C "$TMP/Ryubing" archive --format=tar.gz --output="$VENDOR/source/Ryubing-${RYUBING_COMMIT}.tar.gz" "$RYUBING_COMMIT"
READY="$TMP/dotnet-ready"; mkdir -p "$READY"
cp -a "$TMP/dotnet" "$READY/dotnet"; cp -a "$TMP/ryubing-build" "$READY/ryubing"
tar -C "$READY" -cf - dotnet ryubing | zstd -19 -T0 -q -o "$TMP/dotnet-ryubing.tar.zst"
split_store "$TMP/dotnet-ryubing.tar.zst" "$VENDOR/dotnet" dotnet-ryubing.tar.zst
cat > "$VENDOR/bin/dotnet" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; C="${XDG_CACHE_HOME:-/tmp}/sakurai-dotnet-ryubing"; "$B/_materialize" "$B/../dotnet" dotnet-ryubing.tar.zst "$C"; exec "$C/dotnet/dotnet" "$@"
EOF
cat > "$VENDOR/bin/ryubing" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; C="${XDG_CACHE_HOME:-/tmp}/sakurai-dotnet-ryubing"; "$B/_materialize" "$B/../dotnet" dotnet-ryubing.tar.zst "$C"
export DOTNET_ROOT="$C/dotnet"; export PATH="$DOTNET_ROOT:$PATH"
if [[ -x "$C/ryubing/Ryujinx" ]]; then exec "$C/ryubing/Ryujinx" "$@"; fi
DLL="$(find "$C/ryubing" -maxdepth 1 -iname 'Ryujinx*.dll' | head -n1)"; test -n "$DLL"; exec "$C/dotnet/dotnet" "$DLL" "$@"
EOF
chmod 0755 "$VENDOR/bin/dotnet" "$VENDOR/bin/ryubing"

# pkNX exact source snapshot for offline format/data work.
source_archive https://github.com/kwsch/pkNX.git "$PKNX_COMMIT" pkNX

# AArch64 GNU binutils and required host libraries.
READY="$TMP/aarch64-ready"; mkdir -p "$READY/bin" "$READY/lib"
for n in aarch64-linux-gnu-objdump aarch64-linux-gnu-readelf aarch64-linux-gnu-nm aarch64-linux-gnu-objcopy; do
  cp "$(command -v "$n")" "$READY/bin/$n"
  ldd "$(command -v "$n")" 2>/dev/null | awk '/=> \/|^\// {for(i=1;i<=NF;i++) if($i ~ /^\//) print $i}' | while read -r l; do cp -Ln "$l" "$READY/lib/" 2>/dev/null || true; done
done
tar -C "$READY" -cf - bin lib | zstd -19 -T0 -q -o "$TMP/aarch64-tools.tar.zst"
split_store "$TMP/aarch64-tools.tar.zst" "$VENDOR/aarch64" aarch64-tools.tar.zst
for n in objdump readelf nm objcopy; do
cat > "$VENDOR/bin/aarch64-linux-gnu-$n" <<EOF
#!/usr/bin/env bash
set -euo pipefail
B="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"; C="\${XDG_CACHE_HOME:-/tmp}/sakurai-aarch64"; "\$B/_materialize" "\$B/../aarch64" aarch64-tools.tar.zst "\$C"; export LD_LIBRARY_PATH="\$C/lib:\${LD_LIBRARY_PATH:-}"; exec "\$C/bin/aarch64-linux-gnu-$n" "\$@"
EOF
chmod 0755 "$VENDOR/bin/aarch64-linux-gnu-$n"
done

# LLVM/Clang/lld for reconstruction and disassembly.
LLVM_ROOT="$(llvm-config --prefix)"
tar -C "$(dirname "$LLVM_ROOT")" -cf - "$(basename "$LLVM_ROOT")" | zstd -19 -T0 -q -o "$TMP/llvm.tar.zst"
split_store "$TMP/llvm.tar.zst" "$VENDOR/llvm" llvm.tar.zst
for n in clang clang++ llvm-objdump llvm-readelf llvm-nm llvm-objcopy ld.lld; do
cat > "$VENDOR/bin/$n" <<EOF
#!/usr/bin/env bash
set -euo pipefail
B="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"; C="\${XDG_CACHE_HOME:-/tmp}/sakurai-llvm"; "\$B/_materialize" "\$B/../llvm" llvm.tar.zst "\$C"; X="\$(find "\$C" -type f -path '*/bin/$n' | head -n1)"; test -x "\$X"; exec "\$X" "\$@"
EOF
chmod 0755 "$VENDOR/bin/$n"
done
cp "$(command -v ninja)" "$VENDOR/bin/ninja"

cat > "$VENDOR/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; export GEN9_VENDOR_TOOLCHAIN="$R"; export PATH="$R/bin:$PATH"
EOF
chmod 0755 "$VENDOR/activate.sh"

cat > "$VENDOR/VERSIONS.md" <<EOF
# Generation IX vendored Switch toolchain
- hactool: $HACTOOL_COMMIT
- Ghidra: $GHIDRA_VERSION + Ghidra-Switch-Loader $SWITCH_LOADER_COMMIT + bundled JDK 21
- .NET SDK: $DOTNET_VERSION
- pkNX source: $PKNX_COMMIT
- Ryubing: $RYUBING_COMMIT
- Eden: exact release metadata in eden/release.json and AppImage bytes in chunks
- AArch64 GNU binutils: Ubuntu 24.04 runner build
- LLVM/Clang/lld: Ubuntu 24.04 runner build
- zstd: repository-local decompressor used by all chunked launchers

No ROMs, console keys, firmware, NSP/XCI/NCA game content, or decrypted proprietary game binaries are downloaded or committed.
EOF
(cd "$VENDOR" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
rm -rf "$TMP"
