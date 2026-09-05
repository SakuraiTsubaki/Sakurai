#!/usr/bin/env python3
import pathlib, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: phase1_sram_glue.py POKEGOLD_ROOT')

pg = pathlib.Path(sys.argv[1])
sram_path = pg / 'ram/sram.asm'
s = sram_path.read_text()

if 'sBox1PokemonIndexes::' in s:
    print('16-bit species SRAM storage already present')
    raise SystemExit(0)

# Gold/Silver's two box banks are already packed by the 14 vanilla box structs.
# Keep canonical species indexes in independent SRAM sections so RGBDS can place
# them in genuine free space instead of silently moving/corrupting box data.
# The runtime conversion table is exactly 256 bytes with the current MON_TABLE
# parameters; primary and backup copies remain separate save assets.
extra = r'''

SECTION "Pokemon Index Table Save", SRAM
sPokemonIndexTable:: ds wPokemonIndexTableEnd - wPokemonIndexTable

SECTION "Pokemon Index Table Backup", SRAM
sBackupPokemonIndexTable:: ds wPokemonIndexTableEnd - wPokemonIndexTable

SECTION "Box Pokemon Indexes 1-7", SRAM
sBox1PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox2PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox3PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox4PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox5PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox6PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox7PokemonIndexes:: ds 2 * MONS_PER_BOX

SECTION "Box Pokemon Indexes 8-14", SRAM
sBox8PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox9PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox10PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox11PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox12PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox13PokemonIndexes:: ds 2 * MONS_PER_BOX
sBox14PokemonIndexes:: ds 2 * MONS_PER_BOX
'''

marker = '\nENDSECTION\n'
if marker in s:
    head, tail = s.rsplit(marker, 1)
    s = head + extra + marker + tail
else:
    s += extra

sram_path.write_text(s)
print('installed 1072 bytes of canonical species SRAM storage in four movable sections')
