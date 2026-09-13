#!/usr/bin/env bash
set -euo pipefail
SRC=${1:-gen5_evolution_ext_hooks.s}
LDS=${2:-gen5_evolution_ext.ld}
OUT=${3:-gen5_evolution_ext_hooks}
CLANG=${CLANG:-clang}
LD_LLD=${LD_LLD:-ld.lld}
OBJCOPY=${OBJCOPY:-llvm-objcopy}
OBJDUMP=${OBJDUMP:-llvm-objdump}
"$CLANG" --target=arm-none-eabi -mcpu=arm7tdmi -marm -c "$SRC" -o "$OUT.o"
"$LD_LLD" -T "$LDS" "$OUT.o" -o "$OUT.elf"
"$OBJCOPY" -O binary "$OUT.elf" "$OUT.bin"
"$OBJDUMP" -d "$OUT.elf" > "$OUT.dis"
sha1sum "$OUT.bin"
sha256sum "$OUT.bin"
