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

# The expand branch versions of array/copy_name/pokedex_flags/sram were already
# applied mechanically. Keep them: they provide IsInWordArray,
# CopyStringWithTerminator, CountSetBits16, and tracked SRAM-bank semantics.
# Gold/Silver ROM0 is extremely tight, so recover space by relocating two
# self-contained Home routines behind carry/register-safe farcall trampolines.
stone=pg/'home/stone_queue.asm'
stone_romx=stone.read_text().replace('HandleStoneQueue::','_HandleStoneQueue::',1)
stone.write_text('HandleStoneQueue::\n\tfarcall _HandleStoneQueue\n\tret\n')

region=pg/'home/region.asm'
region_text=region.read_text()
region_romx=''
marker='SetXYCompareFlags::'
if marker in region_text:
    prefix, suffix = region_text.split(marker, 1)
    region.write_text(prefix + 'SetXYCompareFlags::\n\tpush hl\n\tfarcall _SetXYCompareFlags\n\tpop hl\n\tret\n')
    region_romx = '_SetXYCompareFlags::' + suffix

home=pg/'home.asm'
s=home.read_text()
if 'INCLUDE "home/indirection.asm"' not in s:
    s += '\nINCLUDE "home/indirection.asm"\nINCLUDE "home/16bit.asm"\n'
home.write_text(s)

# Preserve Gold/Silver HRAM addresses while naming the five-byte scratch prefix
# the 16-bit/SRAM code expects. hFarByte aliases hTempBank as upstream does.
hram=pg/'ram/hram.asm'
s=hram.read_text()
if 'hSRAMBank::' not in s:
    old='SECTION "HRAM", HRAM\n\n\tds 5\n'
    new='SECTION "HRAM", HRAM\n\nhROMBankBackup:: db\nhFarByte::\nhTempBank:: db\nhSRAMBank:: db\n\tds 2\n'
    if old not in s:
        raise SystemExit('could not locate Gold HRAM five-byte scratch prefix')
    s=s.replace(old,new,1)
hram.write_text(s)

# Gold calls the first byte of BaseData wBaseDexNo; for the original 251 this is
# numerically identical to species. Alias the 16-bit port name without changing
# layout. Also carve wTempLoopCounter out of an existing 12-byte unused gap.
wram=pg/'ram/wram.asm'
s=wram.read_text()
if 'wBaseSpecies::' not in s:
    s=s.replace('wCurBaseData::\nwBaseDexNo:: db',
                'wCurBaseData::\nwBaseSpecies::\nwBaseDexNo:: db',1)
if 'wTempLoopCounter::' not in s:
    s=s.replace('wHoursSince:: db\nwDaysSince:: db\n\n\tds 12',
                'wHoursSince:: db\nwDaysSince:: db\n\nwTempLoopCounter:: db\n\tds 11',1)
# Garbage collection needs a contiguous 32-byte bitmap in bank-0 WRAM.
# Keep it as an independent section so RGBDS can place it in available WRAM0.
if 'wConversionTableBitmap::' not in s:
    s += '\n\nSECTION "16-bit conversion bitmap", WRAM0\n\nwConversionTableBitmap:: ds $20\n'
if 'wPokemonIndexTable' not in s:
    s += '\n\nSECTION "16-bit WRAM tables", WRAMX\n\twram_conversion_table wPokemonIndexTable, MON_TABLE\n'
wram.write_text(s)

# Gold/Silver has no Crystal Odd Egg subsystem, so do not invent a fake live
# species variable merely to satisfy the Crystal garbage collector.
tablefunc=pg/'engine/16/table_functions.asm'
s=tablefunc.read_text()
s=s.replace(', wOddEggSpecies, wBaseSpecies', ', wBaseSpecies')
tablefunc.write_text(s)

# breeding.asm was mechanically widened, but evolve.asm is one of the paths
# that does not apply cleanly to pokegold. Supply the far-aware evolution-list
# skipper in the same ROMX section as breeding so its direct CALL is valid.
breeding=pg/'engine/pokemon/breeding.asm'
s=breeding.read_text()
if 'FarSkipEvolutions::' not in s:
    s += '''\n\nFarSkipEvolutions::\n; b:hl points at a far evolution/level-up list.\n\tld a, b\n\tcall GetFarByte\n\tinc hl\n\tand a\n\tret z\n\tcp EVOLVE_STAT\n\tjr nz, .no_extra_skip\n\tinc hl\n.no_extra_skip\n\tinc hl\n\tinc hl\n\tinc hl\n\tjr FarSkipEvolutions\n'''
breeding.write_text(s)

main=pg/'main.asm'
s=main.read_text()
needle='INCLUDE "data/pokemon/first_stages.asm"\n'
if needle in s:
    s=s.replace(needle, '')
    s += '\n\nSECTION "First-stage Pokemon", ROMX\n\nINCLUDE "data/pokemon/first_stages.asm"\n'
if 'INCLUDE "engine/16/table_functions.asm"' not in s:
    s += '\n\nSECTION "16-bit ID stuff", ROMX\n\nINCLUDE "engine/16/table_functions.asm"\n'
if 'SECTION "Relocated Home routines", ROMX' not in s:
    s += '\n\nSECTION "Relocated Home routines", ROMX\n\n' + stone_romx + '\n' + region_romx + '\n'
# evolve.asm failed the mechanical branch patch. Its callers use callfar, so a
# Gold-specific ROMX implementation is safe here and uses the already-added
# FirstEvoStages 16-bit table.
if 'GetLowestEvolutionStage::' not in s:
    s += '''\n\nSECTION "16-bit evolution helpers", ROMX\n\nGetLowestEvolutionStage::\n\tld a, [wCurPartySpecies]\n\tcall GetPokemonIndexFromID\n\tld bc, FirstEvoStages - 2\n\tadd hl, hl\n\tadd hl, bc\n\tld a, BANK(FirstEvoStages)\n\tcall GetFarWord\n\tcall GetPokemonIDFromIndex\n\tld [wCurPartySpecies], a\n\tret\n'''
main.write_text(s)

pal=pg/'data/pokemon/palettes.asm'
s=pal.read_text()
marker='\n; 252\n'
if marker in s and s.startswith('PokemonPalettes:'):
    cut=s.index(marker)
    species=s[:cut].rstrip()+"\n"
    special='''; Special negative species palettes for 16-bit lookup.\n; Egg (-3)\nINCBIN "gfx/pokemon/egg/egg.gbcpal", middle_colors\nINCLUDE "gfx/pokemon/egg/shiny.pal"\n\n; -2\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n; -2 shiny\n\tRGB 30, 26, 11\n\tRGB 23, 16, 00\n\n; -1\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n; -1 shiny\n\tRGB 23, 23, 23\n\tRGB 17, 17, 17\n\n'''
    pal.write_text(special+species)

# Widened evolution targets and save metadata need movable sections in Gold's
# packed layout. Symbolic references follow their linker-selected placement.
layout=pg/'layout.link'
s=layout.read_text()
s=s.replace('\t"Evolutions and Attacks"\n','')
s=s.replace('\t"Backup Save 2"\n','')
layout.write_text(s)

# Compiler bring-up deferrals. These are restored as real 16-bit data/routines
# after the core image links; they are not being discarded.
run(['git','checkout','HEAD','--','maps'], pg)
run(['git','checkout','HEAD','--','engine/events/fish.asm'], pg)
run(['git','checkout','HEAD','--','data/wild/fish.asm'], pg)

print('phase1 glue installed; Home helpers restored; Gold-specific HRAM/WRAM/evolution glue installed')
