#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${1:-$SCRIPT_DIR/dex649_banked_ui_hooks.s}"
LDS="${2:-$SCRIPT_DIR/dex649_banked_ui.ld}"
OUT_PREFIX="${3:-$SCRIPT_DIR/dex649_banked_ui_hooks}"

CLANG="${CLANG:-clang}"
LD_LLD="${LD_LLD:-ld.lld}"
LLVM_OBJCOPY="${LLVM_OBJCOPY:-llvm-objcopy}"
LLVM_OBJDUMP="${LLVM_OBJDUMP:-llvm-objdump}"

"$CLANG" --target=arm-none-eabi -mcpu=arm7tdmi -marm -c "$SRC" -o "${OUT_PREFIX}.o"
"$LD_LLD" -T "$LDS" -o "${OUT_PREFIX}.elf" "${OUT_PREFIX}.o"
"$LLVM_OBJCOPY" -O binary "${OUT_PREFIX}.elf" "${OUT_PREFIX}.bin"
"$LLVM_OBJDUMP" -d "${OUT_PREFIX}.elf" > "${OUT_PREFIX}.dis"

printf 'Built %s.bin (%s bytes)\n' "$OUT_PREFIX" "$(wc -c < "${OUT_PREFIX}.bin")"
grep -E '<(create_list_hook|input_hook)>:' "${OUT_PREFIX}.dis"
