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

# Gold/Silver include glue. Do not wholesale replace these top-level files with
# Crystal versions: they also encode game-specific layout and features.
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
# The upstream first-stage table lands in Crystal bank24, but that overflows
# Gold/Silver by $40. Give it an unconstrained ROMX section instead.
needle='INCLUDE "data/pokemon/first_stages.asm"\n'
if needle in s:
    s=s.replace(needle, '')
    s += '\n\nSECTION "First-stage Pokemon", ROMX\n\nINCLUDE "data/pokemon/first_stages.asm"\n'
if 'INCLUDE "engine/16/table_functions.asm"' not in s:
    s += '\n\nSECTION "16-bit ID stuff", ROMX\n\nINCLUDE "engine/16/table_functions.asm"\n'
main.write_text(s)

# The 16-bit branch makes Egg a negative special species. Gold/Silver's old
# palette table stored Egg and padding *after* species 251 and asserted against
# EGG+1; with EGG=-3 that assertion becomes -2. Re-layout only the four legacy
# special palettes to match the new negative-index convention while preserving
# all Gold/Silver 0..251 palette data verbatim.
pal=pg/'data/pokemon/palettes.asm'
s=pal.read_text()
marker='\n; 252\n'
if marker in s and s.startswith('PokemonPalettes:'):
    cut=s.index(marker)
    species=s[:cut].rstrip()+"\n"
    special='''; Special negative species palettes for 16-bit lookup.\n; Egg (-3)\nINCBIN "gfx/pokemon/egg/egg.gbcpal", middle_colors\nINCLUDE "gfx/pokemon/egg/shiny.pal"\n\n; -2\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n; -2 shiny\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n\n; -1\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n; -1 shiny\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n\n'''
    s=special+species
    pal.write_text(s)

# Map-script conversion depends on two new script opcodes that need a deliberate
# Gold/Silver hand-port. Keep vanilla maps during compiler bring-up.
run(['git','checkout','HEAD','--','maps'], pg)

print('phase1 glue installed; palette specials relocated; map script opcodes deferred')
