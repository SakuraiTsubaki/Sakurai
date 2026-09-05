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

stone=pg/'home/stone_queue.asm'
stone_romx=stone.read_text().replace('HandleStoneQueue::','_HandleStoneQueue::',1)
stone.write_text('HandleStoneQueue::\n\tfarcall _HandleStoneQueue\n\tret\n')

region=pg/'home/region.asm'
region_text=region.read_text()
region_romx=''
marker='SetXYCompareFlags::'
if marker in region_text:
    prefix, suffix = region_text.split(marker, 1)
    region.write_text(prefix + 'SetXYCompareFlags::\n\tfarcall _SetXYCompareFlags\n\tret\n')
    region_romx = '_SetXYCompareFlags::' + suffix

home=pg/'home.asm'
s=home.read_text()
if 'INCLUDE "home/indirection.asm"' not in s:
    s += '\nINCLUDE "home/indirection.asm"\nINCLUDE "home/16bit.asm"\n'
home.write_text(s)

hram=pg/'ram/hram.asm'
s=hram.read_text()
if 'hSRAMBank::' not in s:
    old='SECTION "HRAM", HRAM\n\n\tds 5\n'
    new='SECTION "HRAM", HRAM\n\nhROMBankBackup:: db\nhFarByte::\nhTempBank:: db\nhSRAMBank:: db\n\tds 2\n'
    if old not in s:
        raise SystemExit('could not locate Gold HRAM five-byte scratch prefix')
    s=s.replace(old,new,1)
hram.write_text(s)

wram=pg/'ram/wram.asm'
s=wram.read_text()
if 'wBaseSpecies::' not in s:
    s=s.replace('wCurBaseData::\nwBaseDexNo:: db',
                'wCurBaseData::\nwBaseSpecies::\nwBaseDexNo:: db',1)
if 'wTempLoopCounter::' not in s:
    s=s.replace('wHoursSince:: db\nwDaysSince:: db\n\n\tds 12',
                'wHoursSince:: db\nwDaysSince:: db\n\nwTempLoopCounter:: db\n\tds 11',1)
if 'wConversionTableBitmap::' not in s:
    s += '\n\nSECTION "16-bit conversion bitmap", WRAM0\n\nwConversionTableBitmap:: ds $20\n'
if 'wPokemonIndexTable' not in s:
    s += '\n\nSECTION "16-bit WRAM tables", WRAMX\n\twram_conversion_table wPokemonIndexTable, MON_TABLE\n'
wram.write_text(s)

tablefunc=pg/'engine/16/table_functions.asm'
s=tablefunc.read_text()
s=s.replace(', wOddEggSpecies, wBaseSpecies', ', wBaseSpecies')
tablefunc.write_text(s)

breeding=pg/'engine/pokemon/breeding.asm'
s=breeding.read_text()
if 'FarSkipEvolutions::' not in s:
    s += '''\n\nFarSkipEvolutions::\n; b:hl points at a far evolution/level-up list.\n\tld a, b\n\tcall GetFarByte\n\tinc hl\n\tand a\n\tret z\n\tcp EVOLVE_STAT\n\tjr nz, .no_extra_skip\n\tinc hl\n.no_extra_skip\n\tinc hl\n\tinc hl\n\tinc hl\n\tjr FarSkipEvolutions\n'''
breeding.write_text(s)

main=pg/'main.asm'
s=main.read_text()
if 'INCLUDE "data/pokemon/first_stages.asm"' in s:
    s=s.replace('INCLUDE "data/pokemon/first_stages.asm"\n', '')
if 'SECTION "First-stage Pokemon", ROMX' not in s:
    s += '\n\nSECTION "First-stage Pokemon", ROMX\n\nINCLUDE "data/pokemon/first_stages.asm"\n'
if 'INCLUDE "engine/16/table_functions.asm"' not in s:
    s += '\n\nSECTION "16-bit ID stuff", ROMX\n\nINCLUDE "engine/16/table_functions.asm"\n'
if 'SECTION "Relocated Home routines", ROMX' not in s:
    s += '\n\nSECTION "Relocated Home routines", ROMX\n\n' + stone_romx + '\n' + region_romx + '\n'
if 'GetLowestEvolutionStage::' not in s:
    s += '''\n\nSECTION "16-bit evolution helpers", ROMX\n\nGetLowestEvolutionStage::\n\tld a, [wCurPartySpecies]\n\tcall GetPokemonIndexFromID\n\tld bc, FirstEvoStages - 2\n\tadd hl, hl\n\tadd hl, bc\n\tld a, BANK(FirstEvoStages)\n\tcall GetFarWord\n\tcall GetPokemonIDFromIndex\n\tld [wCurPartySpecies], a\n\tret\n'''
if 'GetBoxMonPokemonIndexPointer::' not in s:
    s += '''\n\nSECTION "16-bit box index helpers", ROMX\n\nGetBoxMonPokemonIndexPointer::\n; in: b = slot, c = zero-based saved box\n; out: b = SRAM bank, hl = little-endian u16 canonical species index\n\tpush de\n\tld e, c\n\tld d, 0\n\tld hl, SilverBoxIndexAddresses\n\tadd hl, de\n\tadd hl, de\n\tadd hl, de\n\tld a, [hli]\n\tpush af\n\tld a, [hli]\n\tld h, [hl]\n\tld l, a\n\tld e, b\n\tld d, 0\n\tadd hl, de\n\tadd hl, de\n\tpop af\n\tld b, a\n\tpop de\n\tret\n\nSilverBoxIndexAddresses:\n\tdba sBox1PokemonIndexes\n\tdba sBox2PokemonIndexes\n\tdba sBox3PokemonIndexes\n\tdba sBox4PokemonIndexes\n\tdba sBox5PokemonIndexes\n\tdba sBox6PokemonIndexes\n\tdba sBox7PokemonIndexes\n\tdba sBox8PokemonIndexes\n\tdba sBox9PokemonIndexes\n\tdba sBox10PokemonIndexes\n\tdba sBox11PokemonIndexes\n\tdba sBox12PokemonIndexes\n\tdba sBox13PokemonIndexes\n\tdba sBox14PokemonIndexes\n'''
main.write_text(s)

pal=pg/'data/pokemon/palettes.asm'
s=pal.read_text()
marker='\n; 252\n'
if marker in s and s.startswith('PokemonPalettes:'):
    cut=s.index(marker)
    species=s[:cut].rstrip()+"\n"
    special='''; Special negative species palettes for 16-bit lookup.\n; Egg (-3)\nINCBIN "gfx/pokemon/egg/egg.gbcpal", middle_colors\nINCLUDE "gfx/pokemon/egg/shiny.pal"\n\n; -2\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n; -2 shiny\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n\n; -1\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n; -1 shiny\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n\n'''
    pal.write_text(special+species)

layout=pg/'layout.link'
s=layout.read_text()
s=s.replace('\t"Evolutions and Attacks"\n','')
s=s.replace('\t"Backup Save 2"\n','')
layout.write_text(s)

run(['git','checkout','HEAD','--','maps'], pg)
run(['git','checkout','HEAD','--','engine/events/fish.asm'], pg)
run(['git','checkout','HEAD','--','data/wild/fish.asm'], pg)

print('phase1 glue installed; Gold/Silver saved-box u16 address table linked')
