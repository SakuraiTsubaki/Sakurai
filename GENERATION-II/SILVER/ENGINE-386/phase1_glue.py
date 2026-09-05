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

# During compiler bring-up, keep Gold/Silver's existing Home routines and add
# only the new 16-bit core entry points. The mechanically clean changes below
# are functionality work, but together with the new core they overflow ROM0.
# They will be hand-ported after the core image links.
for path in ['home/array.asm','home/copy_name.asm','home/pokedex_flags.asm','home/sram.asm']:
    run(['git','checkout','HEAD','--',path], pg)

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

# Widened evolution targets add one byte per evolution. The original linker
# layout pins the section immediately after bank10, leaving no growth room.
# Likewise the expanded save metadata adds bytes to Backup Save 2. Unpin those
# two sections for the compiler-core image; symbolic BANK()/address references
# can then follow their relocated linker placement.
layout=pg/'layout.link'
s=layout.read_text()
s=s.replace('\t"Evolutions and Attacks"\n','')
s=s.replace('\t"Backup Save 2"\n','')
layout.write_text(s)

# Compiler bring-up deferrals. These upstream conversions are functional work
# that must be hand-ported around Gold/Silver's tighter bank/layout rules.
run(['git','checkout','HEAD','--','maps'], pg)
run(['git','checkout','HEAD','--','engine/events/fish.asm'], pg)
run(['git','checkout','HEAD','--','data/wild/fish.asm'], pg)

print('phase1 glue installed; core layout unpinned; Home/map/fishing feature ports deferred')
