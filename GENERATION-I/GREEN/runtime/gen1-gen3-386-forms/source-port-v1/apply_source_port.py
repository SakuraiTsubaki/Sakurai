#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, shutil, struct
from pathlib import Path

POKEGREEN_COMMIT='953f41b34108621b2bf13c3b1e53abfc9c3e5aec'

def replace_once(path:Path, old:str, new:str):
    text=path.read_text(encoding='utf-8')
    n=text.count(old)
    if n!=1: raise RuntimeError(f'{path}: expected 1 match, got {n}: {old[:80]!r}')
    path.write_text(text.replace(old,new,1),encoding='utf-8')

def append_once(path:Path, marker:str, addition:str):
    text=path.read_text(encoding='utf-8')
    if marker not in text:
        path.write_text(text.rstrip()+'\n\n'+addition.rstrip()+'\n',encoding='utf-8')

def extract_gen3(runtime:bytes)->bytes:
    if runtime[:8]!=b'G386F3\0\0': raise RuntimeError('bad G386F3 magic')
    _,off3,offf,_=struct.unpack_from('<IIII',runtime,0x20)
    _,rs3,_=struct.unpack_from('<HHH',runtime,0x34)
    if rs3!=30: raise RuntimeError(f'bad record size {rs3}')
    blob=runtime[off3:offf]
    if len(blob)!=386*30: raise RuntimeError(f'bad table size {len(blob)}')
    for i in range(386):
        rec=blob[i*30:(i+1)*30]
        if struct.unpack_from('<H',rec)[0]!=i+1: raise RuntimeError(f'bad natdex at {i}')
        if rec[11] or rec[13]: raise RuntimeError(f'byte projection overflow at #{i+1}')
    return blob

def patch(pg:Path):
    replace_once(pg/'Makefile','RGBFIXFLAGS += -sv -k 01 -l 0x33 -m MBC1+RAM+BATTERY -r 03 -p 0','RGBFIXFLAGS += -sv -k 01 -l 0x33 -m MBC5+RAM+BATTERY -r 04 -p 0')
    append_once(pg/'ram.asm','INCLUDE "ram/g386.asm"','INCLUDE "ram/g386.asm"')
    append_once(pg/'main.asm','SECTION "G386 Runtime"','SECTION "G386 Runtime", ROMX\n\nINCLUDE "engine/g386/runtime.asm"')
    layout=pg/'layout.link'
    replace_once(layout,'ROMX $1F\n\t"Audio Engine 3"\n\t"Music 3"\n\t"Sound Effect Headers 3"\n\t"Music Headers 3"\n\t"Sound Effects 3"\n\t"Garbage 31"\nWRAM0','ROMX $1F\n\t"Audio Engine 3"\n\t"Music 3"\n\t"Sound Effect Headers 3"\n\t"Music Headers 3"\n\t"Sound Effects 3"\n\t"Garbage 31"\nROMX $20\n\t"G386 Runtime"\nWRAM0')
    replace_once(layout,'SRAM $3\n\t"Saved Boxes 2"\nHRAM','SRAM $3\n\t"Saved Boxes 2"\nSRAM $4\n\t"G386 Extended Save"\nHRAM')
    replace_once(pg/'home/pokemon.asm','.done\n\tld a, [wCurSpecies]\n\tld [wMonHIndex], a','.done\n\tfarcall G386OverlayMonHeader\n\tld a, [wCurSpecies]\n\tld [wMonHIndex], a')
    replace_once(pg/'engine/pokemon/load_mon_data.asm','\tld a, [wCurPartySpecies]\n\tld [wCurSpecies], a\n\tcall GetMonHeader','\tld a, [wCurPartySpecies]\n\tld [wCurSpecies], a\n\tfarcall G386PrepareIdentityForLoadMonData\n\tcall GetMonHeader')
    add=pg/'engine/pokemon/add_mon.asm'
    replace_once(add,'\tld a, [wCurPartySpecies]\n\tld [wCurSpecies], a\n\tcall GetMonHeader','\tld a, [wCurPartySpecies]\n\tld [wCurSpecies], a\n\tfarcall G386PrepareIdentityForAddPartyMon\n\tcall GetMonHeader')
    replace_once(add,'\tld bc, BOXMON_STRUCT_LENGTH\n\tcall CopyData\n\tpop de\n\tpop hl\n\tld a, [wMoveMonType]','\tld bc, BOXMON_STRUCT_LENGTH\n\tcall CopyData\n\tpop de\n\tpop hl\n\tfarcall G386CopyMoveMonIdentity\n\tld a, [wMoveMonType]')
    replace_once(pg/'engine/pokemon/remove_mon.asm','_RemovePokemon::\n\tld hl, wPartyCount','_RemovePokemon::\n\tfarcall G386RemoveIdentity\n\tld hl, wPartyCount')
    core=pg/'engine/battle/core.asm'
    replace_once(core,'\tld de, wBattleMonPP\n\tld bc, NUM_MOVES\n\tcall CopyData\n\tld de, wBattleMonLevel','\tld de, wBattleMonPP\n\tld bc, NUM_MOVES\n\tcall CopyData\n\tfarcall G386SyncPlayerBattleIdentityFromParty\n\tld de, wBattleMonLevel')
    save=pg/'engine/menus/save.asm'
    replace_once(save,'\tcall LoadPartyAndDexData\n\tjr c, .badsum\n\tld a, $2 ; good checksum','\tcall LoadPartyAndDexData\n\tjr c, .badsum\n\tfarcall G386LoadExtended\n\tld a, $2 ; good checksum')
    replace_once(save,'SaveGameData::\n\tcall SaveMainData\n\tcall SaveCurrentBoxData\n\tjp SavePartyAndDexData','SaveGameData::\n\tcall SaveMainData\n\tcall SaveCurrentBoxData\n\tcall SavePartyAndDexData\n\tfarcall G386CommitExtended\n\tret')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pokegreen',type=Path,required=True); ap.add_argument('--sakurai',type=Path,required=True); ap.add_argument('--assets',type=Path,required=True); a=ap.parse_args()
    runtime=(a.sakurai/'GENERATION-I/GREEN/runtime/gen1-gen3-386-forms/generated/green_386_forms_runtime_parameter_block.bin').read_bytes()
    legacy=(a.sakurai/'GENERATION-I/GREEN/runtime/gen1-gen3-386-forms/getmonheader-hook-v1/generated/green_legacy8_to_canonical16_map.bin').read_bytes()
    if len(legacy)!=512: raise RuntimeError('legacy map size')
    gen3=extract_gen3(runtime)
    data=a.pokegreen/'data/g386'; data.mkdir(parents=True,exist_ok=True)
    (data/'gen3_personal.bin').write_bytes(gen3); (data/'legacy_map.bin').write_bytes(legacy)
    (a.pokegreen/'engine/g386').mkdir(parents=True,exist_ok=True)
    parts=sorted(a.assets.glob('runtime_g386_part*.asm'))
    if not parts: raise RuntimeError('runtime parts missing')
    (a.pokegreen/'engine/g386/runtime.asm').write_text(''.join(x.read_text(encoding='utf-8') for x in parts),encoding='utf-8')
    shutil.copyfile(a.assets/'ram_g386.asm',a.pokegreen/'ram/g386.asm')
    patch(a.pokegreen)
    print({'base':POKEGREEN_COMMIT,'gen3_sha1':hashlib.sha1(gen3).hexdigest(),'legacy_sha1':hashlib.sha1(legacy).hexdigest(),'wram_added':0,'sram_bank':4})
if __name__=='__main__': main()
