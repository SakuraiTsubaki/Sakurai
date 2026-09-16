#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
REPO_NAME="$(basename "$ROOT_DIR")"
TOOLS_DIR="${TOOLS_DIR:-$ROOT_DIR/.tools}"
BIN_DIR="$TOOLS_DIR/bin"
SRC_DIR="$TOOLS_DIR/src"
EMU_DIR="$TOOLS_DIR/emulators"
mkdir -p "$BIN_DIR" "$SRC_DIR" "$EMU_DIR"

if [[ -d "$ROOT_DIR/.git" ]]; then
  touch "$ROOT_DIR/.git/info/exclude"
  grep -qxF '.tools/' "$ROOT_DIR/.git/info/exclude" || echo '.tools/' >> "$ROOT_DIR/.git/info/exclude"
fi

log() { printf '[toolchain] %s\n' "$*"; }
warn() { printf '[toolchain] WARNING: %s\n' "$*" >&2; }

if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=()
elif command -v sudo >/dev/null 2>&1; then
  SUDO=(sudo)
else
  SUDO=()
fi

apt_install() {
  command -v apt-get >/dev/null 2>&1 || return 0
  "${SUDO[@]}" apt-get update || { warn 'apt-get update failed; continuing with existing packages'; return 0; }
  DEBIAN_FRONTEND=noninteractive "${SUDO[@]}" apt-get install -y --no-install-recommends "$@" \
    || warn "some apt packages could not be installed: $*"
}

install_common() {
  apt_install ca-certificates curl git make cmake ninja-build python3 python3-venv pkg-config build-essential \
    unzip xz-utils p7zip-full file patch libssl-dev zlib1g-dev
}

latest_asset_url() {
  local repo="$1" pattern="$2"
  curl -fsSL "https://api.github.com/repos/$repo/releases/latest" | \
    python3 -c 'import json,re,sys; d=json.load(sys.stdin); p=re.compile(sys.argv[1],re.I); print(next((a.get("browser_download_url","") for a in d.get("assets",[]) if p.search(a.get("name",""))), ""))' "$pattern"
}

download_latest_asset() {
  local repo="$1" pattern="$2" dest="$3" url
  url="$(latest_asset_url "$repo" "$pattern" || true)"
  [[ -n "$url" ]] || { warn "no matching release asset for $repo / $pattern"; return 1; }
  log "downloading $(basename "$dest") from $repo"
  curl -fL --retry 3 --retry-delay 2 "$url" -o "$dest"
  chmod +x "$dest" 2>/dev/null || true
}

link_bin() {
  local src="$1" name="$2"
  [[ -e "$src" ]] && ln -sfn "$src" "$BIN_DIR/$name"
}

install_rgbds() {
  local version='1.0.3'
  [[ -f "$ROOT_DIR/.rgbds-version" ]] && version="$(tr -d '[:space:]' < "$ROOT_DIR/.rgbds-version")"
  [[ -x "$TOOLS_DIR/rgbds/bin/rgbasm" ]] && { log "RGBDS $version already installed"; return 0; }
  apt_install bison flex libpng-dev
  rm -rf "$SRC_DIR/rgbds-$version"
  log "installing RGBDS $version"
  git clone --depth 1 --branch "v$version" https://github.com/gbdev/rgbds.git "$SRC_DIR/rgbds-$version"
  cmake -S "$SRC_DIR/rgbds-$version" -B "$SRC_DIR/rgbds-$version/build" \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$TOOLS_DIR/rgbds"
  cmake --build "$SRC_DIR/rgbds-$version/build" -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)"
  cmake --install "$SRC_DIR/rgbds-$version/build"
  for t in rgbasm rgblink rgbfix rgbgfx; do link_bin "$TOOLS_DIR/rgbds/bin/$t" "$t"; done
}

install_mgba() {
  command -v mgba-qt >/dev/null 2>&1 && { log 'mGBA already available system-wide'; return 0; }
  [[ -x "$EMU_DIR/mGBA.AppImage" ]] && { log 'mGBA AppImage already installed'; return 0; }
  download_latest_asset mgba-emu/mgba 'appimage-(x64|x86_64).*\.appimage$' "$EMU_DIR/mGBA.AppImage" || true
}

install_arm_toolchain() {
  apt_install gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi
  command -v arm-none-eabi-gcc >/dev/null 2>&1 && link_bin "$(command -v arm-none-eabi-gcc)" arm-none-eabi-gcc
}

install_agbcc() {
  [[ -d "$SRC_DIR/agbcc/.git" ]] || git clone --depth 1 https://github.com/pret/agbcc.git "$SRC_DIR/agbcc"
  (cd "$SRC_DIR/agbcc" && make -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)") || warn 'agbcc build did not complete on this host'
}

install_ndstool() {
  command -v ndstool >/dev/null 2>&1 && { log 'ndstool already available'; return 0; }
  [[ -d "$SRC_DIR/ndstool/.git" ]] || git clone --depth 1 https://github.com/devkitPro/ndstool.git "$SRC_DIR/ndstool"
  cmake -S "$SRC_DIR/ndstool" -B "$SRC_DIR/ndstool/build" -DCMAKE_BUILD_TYPE=Release || return 0
  cmake --build "$SRC_DIR/ndstool/build" -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)" || return 0
  local f
  f="$(find "$SRC_DIR/ndstool/build" -type f -name ndstool -perm -111 | head -n1 || true)"
  [[ -n "$f" ]] && link_bin "$f" ndstool
}

install_melonds() {
  [[ -x "$EMU_DIR/melonDS.AppImage" ]] && { log 'melonDS AppImage already installed'; return 0; }
  download_latest_asset melonDS-emu/melonDS 'melonDS.*(x86_64|x64).*\.AppImage$' "$EMU_DIR/melonDS.AppImage" || true
}

install_3ds_tools() {
  apt_install libcurl4-openssl-dev libssl-dev
  if [[ ! -x "$BIN_DIR/3dstool" ]]; then
    [[ -d "$SRC_DIR/3dstool/.git" ]] || git clone --depth 1 https://github.com/dnasdw/3dstool.git "$SRC_DIR/3dstool"
    cmake -S "$SRC_DIR/3dstool" -B "$SRC_DIR/3dstool/build" -DUSE_DEP=OFF -DCMAKE_BUILD_TYPE=Release || true
    cmake --build "$SRC_DIR/3dstool/build" -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)" || true
    local f
    f="$(find "$SRC_DIR/3dstool/build" -type f -name 3dstool -perm -111 | head -n1 || true)"
    [[ -n "$f" ]] && link_bin "$f" 3dstool
  fi
  if [[ ! -x "$BIN_DIR/ctrtool" || ! -x "$BIN_DIR/makerom" ]]; then
    [[ -d "$SRC_DIR/Project_CTR/.git" ]] || git clone --depth 1 https://github.com/3DSGuy/Project_CTR.git "$SRC_DIR/Project_CTR"
    (cd "$SRC_DIR/Project_CTR" && make -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)") || warn 'Project_CTR build did not complete'
    for t in ctrtool makerom; do
      local f
      f="$(find "$SRC_DIR/Project_CTR" -type f -name "$t" -perm -111 | head -n1 || true)"
      [[ -n "$f" ]] && link_bin "$f" "$t"
    done
  fi
}

install_azahar() {
  [[ -x "$EMU_DIR/Azahar.AppImage" ]] && { log 'Azahar AppImage already installed'; return 0; }
  download_latest_asset azahar-emu/azahar 'linux.*(x86_64|x64).*\.AppImage$|\.AppImage$' "$EMU_DIR/Azahar.AppImage" || true
}

install_switch_tools() {
  apt_install dotnet-sdk-8.0 llvm clang lld
  if [[ ! -x "$BIN_DIR/hactool" ]]; then
    [[ -d "$SRC_DIR/hactool/.git" ]] || git clone --depth 1 https://github.com/SciresM/hactool.git "$SRC_DIR/hactool"
    (cd "$SRC_DIR/hactool" && make -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)") || warn 'hactool build did not complete'
    [[ -x "$SRC_DIR/hactool/hactool" ]] && link_bin "$SRC_DIR/hactool/hactool" hactool
  fi
}

install_eden() {
  [[ -x "$EMU_DIR/Eden.AppImage" ]] && { log 'Eden AppImage already installed'; return 0; }
  local url
  url="$(curl -fsSL https://nightly.eden-emu.dev/latest/release.json 2>/dev/null | python3 -c '
import json, sys
root = json.load(sys.stdin)
stack = [root]
urls = []
while stack:
    item = stack.pop()
    if isinstance(item, dict):
        stack.extend(item.values())
    elif isinstance(item, list):
        stack.extend(item)
    elif isinstance(item, str):
        urls.append(item)
for s in urls:
    low = s.lower()
    if s.startswith("http") and low.endswith(".appimage") and ("amd64" in low or "x86_64" in low) and "pgo" in low:
        print(s)
        break
' 2>/dev/null || true)"
  if [[ -n "$url" ]]; then
    log 'downloading latest Eden nightly AppImage'
    curl -fL --retry 3 "$url" -o "$EMU_DIR/Eden.AppImage" && chmod +x "$EMU_DIR/Eden.AppImage"
  else
    warn 'could not resolve Eden nightly AppImage automatically'
  fi
}

install_common

case "$REPO_NAME" in
  Sakurai|Tsubaki)
    log 'umbrella repository: installing all common reverse-engineering toolchains and emulators'
    install_rgbds || true
    install_arm_toolchain || true
    install_agbcc || true
    install_ndstool || true
    install_3ds_tools || true
    install_switch_tools || true
    install_mgba || true
    install_melonds || true
    install_azahar || true
    install_eden || true
    ;;
  pokegold-kr|PocketMonsters-Pikachu-Disassembly|PocketMonsters-Midori-Disassembly|PocketMonsters-Aka-Disassembly|PocketMonsters-Ao-Disassembly|PocketMonsters-Gin-Disassembly|PocketMonsters-Kin-Disassembly|PocketMonsters-Crystal-Disassembly)
    install_rgbds
    install_mgba
    ;;
  PocketMonsters-Ruby-Disassembly|PocketMonsters-Sapphire-Disassembly|PocketMonsters-Emerald-Disassembly|PocketMonsters-FireRed-Disassembly|PocketMonsters-LeafGreen-Disassembly|PocketMonsters-Ruby-Decompilation|PocketMonsters-Sapphire-Decompilation|PocketMonsters-Emerald-Decompilation|PocketMonsters-FireRed-Decompilation|PocketMonsters-LeafGreen-Decompilation)
    install_arm_toolchain
    install_agbcc
    install_mgba
    ;;
  PocketMonsters-Diamond-Decompilation|PocketMonsters-Pearl-Decompilation|PocketMonsters-Platinum-Decompilation|PocketMonsters-HeartGold-Decompilation|PocketMonsters-SoulSilver-Decompilation|PocketMonsters-Black-Decompilation|PocketMonsters-White-Decompilation|PocketMonsters-Black2-Decompilation|PocketMonsters-White2-Decompilation)
    install_arm_toolchain
    install_ndstool
    install_melonds
    ;;
  PocketMonsters-X-Decompilation|PocketMonsters-Y-Decompilation|PocketMonsters-OmegaRuby-Decompilation|PocketMonsters-AlphaSapphire-Decompilation|PocketMonsters-Sun-Decompilation|PocketMonsters-Moon-Decompilation|PocketMonsters-UltraSun-Decompilation|PocketMonsters-UltraMoon-Decompilation)
    install_arm_toolchain
    install_3ds_tools
    install_azahar
    ;;
  PocketMonsters-LetsGoPikachu-Decompilation|PocketMonsters-LetsGoEevee-Decompilation|PocketMonsters-Sword-Decompilation|PocketMonsters-Shield-Decompilation|PocketMonsters-BrilliantDiamond-Decompilation|PocketMonsters-ShiningPearl-Decompilation|PokemonLegends-Arceus-Decompilation|PocketMonsters-Scarlet-Decompilation|PocketMonsters-Violet-Decompilation|PokemonLegends-Z-A-Decompilation|PocketMonsters-Winds-Decompilation|PocketMonsters-Waves-Decompilation)
    install_switch_tools
    install_eden
    ;;
  *)
    warn "unknown repository class: $REPO_NAME; installed common tools only"
    ;;
esac

cat > "$TOOLS_DIR/activate.sh" <<ACTIVATE
export PATH="$BIN_DIR:\$PATH"
ACTIVATE

log "done for $REPO_NAME"
log "add tools to this shell with: source '$TOOLS_DIR/activate.sh'"
log 'ROMs, firmware and console keys are never downloaded by this script; supply only your own dumps when an emulator/tool requires them.'
