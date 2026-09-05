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
needle='INCLUDE "data/pokemon/first_stages.asm"\n'
if needle in s:
    s=s.replace(needle, '')
    s += '\n\nSECTION "First-stage Pokemon", ROMX\n\nINCLUDE "data/pokemon/first_stages.asm"\n'
if 'INCLUDE "engine/16/table_functions.asm"' not in s:
    s += '\n\nSECTION "16-bit ID stuff", ROMX\n\nINCLUDE "engine/16/table_functions.asm"\n'
main.write_text(s)

wram=pg/'ram/wram.asm'
s=wram.read_text()
if 'wPokemonIndexTable' not in s:
    s += '\n\nSECTION "16-bit WRAM tables", WRAMX\n\twram_conversion_table wPokemonIndexTable, MON_TABLE\n'
wram.write_text(s)

pal=pg/'data/pokemon/palettes.asm'
s=pal.read_text()
marker='\n; 252\n'
if marker in s and s.startswith('PokemonPalettes:'):
    cut=s.index(marker)
    species=s[:cut].rstrip()+"\n"
    special='''; Special negative species palettes for 16-bit lookup.\n; Egg (-3)\nINCBIN "gfx/pokemon/egg/egg.gbcpal", middle_colors\nINCLUDE "gfx/pokemon/egg/shiny.pal"\n\n; -2\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n; -2 shiny\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n\n; -1\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n; -1 shiny\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n\n'''
    pal.write_text(special+species)

# Compiler bring-up deferrals. These upstream conversions are functional work
# that must be hand-ported around Gold/Silver's tighter bank/layout rules.
run(['git','checkout','HEAD','--','maps'], pg)
run(['git','checkout','HEAD','--','engine/events/fish.asm'], pg)
# engine/events/fish.asm includes data/wild/fish.asm at its tail. Restoring the
# code alone still leaves the widened u16 fishing records in packed bank24.
# Restore the data too for the compiler-core milestone; it will be relocated and
# re-enabled as a 16-bit table in the later encounter-routing phase.
run(['git','checkout','HEAD','--','data/wild/fish.asm'], pg)

print('phase1 glue installed; WRAM/palette fixed; map/fishing opcode+data work deferred')
