#!/usr/bin/env python3
import pathlib, subprocess, sys

if len(sys.argv) != 3:
    raise SystemExit('usage: phase1_glue.py POKEGOLD_ROOT POKECRYSTAL16_ROOT')
pg = pathlib.Path(sys.argv[1])
pc = pathlib.Path(sys.argv[2])

def run(args, cwd, check=True):
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)

def source(path):
    return run(['git','show',f'origin/expand-mon-ID:{path}'], pc).stdout

def sync(path):
    dst=pg/path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(source(path))

# These files are new infrastructure on the 16-bit branch and can be carried
# over without replacing Gold/Silver game-content files.
for path in [
    'macros/wram_16bit.asm',
    'macros/indirection.asm',
    'macros/lists.asm',
    'constants/16_bit_translation_constants.asm',
    'constants/16_bit_locking_constants.asm',
    'home/indirection.asm',
    'home/16bit.asm',
    'engine/16/macros.asm',
    'engine/16/table_functions.asm',
]:
    sync(path)

# Gold/Silver include glue. Do not wholesale replace includes.asm/home.asm/main.asm
# with Crystal versions: those files also describe game-specific layout.
inc=pg/'includes.asm'
s=inc.read_text()
anchor='INCLUDE "macros/vc.asm"\n'
extra='INCLUDE "macros/wram_16bit.asm"\nINCLUDE "macros/indirection.asm"\nINCLUDE "macros/lists.asm"\n'
if 'INCLUDE "macros/indirection.asm"' not in s:
    s=s.replace(anchor, anchor+extra)
anchor='INCLUDE "constants/type_constants.asm"\n'
extra='INCLUDE "constants/16_bit_translation_constants.asm"\nINCLUDE "constants/16_bit_locking_constants.asm"\n'
if 'INCLUDE "constants/16_bit_translation_constants.asm"' not in s:
    s=s.replace(anchor, anchor+extra)
inc.write_text(s)

home=pg/'home.asm'
s=home.read_text()
if 'INCLUDE "home/indirection.asm"' not in s:
    s += '\nINCLUDE "home/indirection.asm"\nINCLUDE "home/16bit.asm"\n'
home.write_text(s)

main=pg/'main.asm'
s=main.read_text()
if 'INCLUDE "engine/16/table_functions.asm"' not in s:
    s += '\n\nSECTION "16-bit ID stuff", ROMX\n\nINCLUDE "engine/16/table_functions.asm"\n'
main.write_text(s)

# Map-script conversion on the upstream branch depends on two new script
# opcodes that need a deliberate Gold/Silver hand-port. Keep vanilla maps for
# this compiler bring-up so the 16-bit core can be advanced independently.
run(['git','checkout','HEAD','--','maps'], pg)

print('phase1 glue installed; map script opcode conversion deferred')
