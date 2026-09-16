#!/usr/bin/env bash
set -euo pipefail
ROOT="${PROJECT_ROOT:-$PWD}"
VENDOR_ROOT="$ROOT/vendor/toolchain/linux-x86_64"
HACTOOL_COMMIT="${HACTOOL_COMMIT:-1d64a83450e025622f3468c28fc4164dad2c5ef6}"
TMP="$ROOT/_toolbuild"
rm -rf "$TMP" "$VENDOR_ROOT"
mkdir -p "$TMP" "$VENDOR_ROOT/source" "$VENDOR_ROOT/bin" "$VENDOR_ROOT/licenses" "$VENDOR_ROOT/eden"

sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential git curl ca-certificates python3 file

git clone https://github.com/SciresM/hactool.git "$TMP/hactool"
git -C "$TMP/hactool" checkout "$HACTOOL_COMMIT"
git -C "$TMP/hactool" submodule update --init --recursive
git -C "$TMP/hactool" archive --format=tar.gz --output="$VENDOR_ROOT/source/hactool-${HACTOOL_COMMIT}.tar.gz" "$HACTOOL_COMMIT"
cp "$TMP/hactool/config.mk.template" "$TMP/hactool/config.mk"
(cd "$TMP/hactool" && make -j2)
cp "$TMP/hactool/hactool" "$VENDOR_ROOT/bin/hactool"
chmod 0755 "$VENDOR_ROOT/bin/hactool"
find "$TMP/hactool" -maxdepth 2 \( -iname 'LICENSE*' -o -iname 'COPYING*' \) -print -quit | xargs -r -I{} cp '{}' "$VENDOR_ROOT/licenses/hactool-LICENSE"

curl -fsSL https://nightly.eden-emu.dev/latest/release.json -o "$VENDOR_ROOT/eden/release.json"
EDEN_URL="$(python3 - "$VENDOR_ROOT/eden/release.json" <<'PY'
import json,sys
root=json.load(open(sys.argv[1],encoding='utf-8'))
strings=[]
stack=[root]
while stack:
    x=stack.pop()
    if isinstance(x,dict): stack.extend(x.values())
    elif isinstance(x,list): stack.extend(x)
    elif isinstance(x,str): strings.append(x)
choices=[]
for s in strings:
    lo=s.lower()
    if s.startswith('http') and lo.endswith('.appimage') and ('amd64' in lo or 'x86_64' in lo):
        score=(3 if 'pgo' in lo else 0)+(2 if 'amd64' in lo else 0)+(1 if 'standard' in lo else 0)
        choices.append((score,s))
if not choices:
    raise SystemExit('No amd64 AppImage URL found in Eden release JSON')
print(max(choices)[1])
PY
)"
printf '%s\n' "$EDEN_URL" > "$VENDOR_ROOT/eden/DOWNLOAD_URL.txt"
curl -fL --retry 3 "$EDEN_URL" -o "$TMP/Eden.AppImage"
chmod 0755 "$TMP/Eden.AppImage"
sha256sum "$TMP/Eden.AppImage" > "$VENDOR_ROOT/eden/Eden.AppImage.sha256"
# GitHub rejects individual files over 100 MiB; fixed-size chunks keep the emulator itself in Git.
split -b 50m -d -a 3 "$TMP/Eden.AppImage" "$VENDOR_ROOT/eden/Eden.AppImage.part."
cat > "$VENDOR_ROOT/bin/eden" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
H="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
V="$H/../eden"
CACHE_BASE="${XDG_CACHE_HOME:-/tmp}"
CACHE="$CACHE_BASE/sakurai-vendor-eden"
mkdir -p "$CACHE"
APP="$CACHE/Eden.AppImage"
EXPECTED="$(awk '{print $1}' "$V/Eden.AppImage.sha256")"
if [[ ! -x "$APP" ]] || [[ "$(sha256sum "$APP" | awk '{print $1}')" != "$EXPECTED" ]]; then
  cat "$V"/Eden.AppImage.part.* > "$APP"
  chmod 0755 "$APP"
  echo "$EXPECTED  $APP" | sha256sum -c - >/dev/null
fi
export APPIMAGE_EXTRACT_AND_RUN=1
[[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] || export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
exec "$APP" "$@"
EOF
chmod 0755 "$VENDOR_ROOT/bin/eden"
cat > "$VENDOR_ROOT/activate.sh" <<'EOF'
#!/usr/bin/env bash
R="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$R/bin:$PATH"
EOF
chmod 0755 "$VENDOR_ROOT/activate.sh"
printf '# Switch vendored toolchain\nhactool %s; Eden release metadata and Linux amd64 AppImage chunks are tracked. No ROMs/keys/firmware.\n' "$HACTOOL_COMMIT" > "$VENDOR_ROOT/VERSIONS.md"
(cd "$VENDOR_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
"$VENDOR_ROOT/bin/hactool" --help >/dev/null 2>&1 || true
rm -rf "$TMP"
