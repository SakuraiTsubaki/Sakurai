#!/usr/bin/env python3
import argparse
from pathlib import Path
import hashlib, json, struct, re

GBA = 0x08000000
HOOK_OFF = 0x1805ED0
CREATE_LIST_OFF = 0x0BC8D4
INPUT_OFF = 0x0BC0F8
CREATE_LIST_ARM = 0x09805ED0
EXPECTED_CORE_SHA1 = 'da3aab88a26e20e83c67060a556fa18b2e044079'
EXPECTED_CREATE_ORIG = bytes.fromhex('f0b557464e464546')
EXPECTED_INPUT_ORIG = bytes.fromhex('70b581b00006060e')

def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()
def thumb_to_arm_stub(target):
    return struct.pack('<HHI', 0x4B00, 0x4718, target)

def main():
    ap=argparse.ArgumentParser(description='Patch the BPEE DEX649 core ROM with the L/R banked National Dex UI.')
    ap.add_argument('core_rom', type=Path)
    ap.add_argument('core_manifest', type=Path)
    ap.add_argument('hook_bin', type=Path)
    ap.add_argument('hook_dis', type=Path)
    ap.add_argument('-o','--output', type=Path, required=True)
    ap.add_argument('--manifest-out', type=Path, required=True)
    args=ap.parse_args()

    text=args.hook_dis.read_text(encoding='utf-8', errors='replace')
    m=re.search(r'^([0-9a-fA-F]{8}) <input_hook>:', text, re.M)
    if not m: raise SystemExit('input_hook symbol not found in hook disassembly')
    input_arm=int(m.group(1),16)

    rom=bytearray(args.core_rom.read_bytes())
    got_sha1=sha1(rom)
    if got_sha1 != EXPECTED_CORE_SHA1:
        raise SystemExit(f'wrong core ROM SHA1: {got_sha1}; expected {EXPECTED_CORE_SHA1}')
    core_man=json.loads(args.core_manifest.read_text(encoding='utf-8'))
    alloc=core_man.get('allocation_end')
    if isinstance(alloc,str): alloc=int(alloc,0)
    if alloc != HOOK_OFF:
        raise SystemExit(f"unexpected core allocation_end: {core_man.get('allocation_end')!r}")

    hooks=args.hook_bin.read_bytes()
    if any(x != 0xFF for x in rom[HOOK_OFF:HOOK_OFF+len(hooks)]):
        raise SystemExit('hook allocation is not blank 0xFF space')
    if bytes(rom[CREATE_LIST_OFF:CREATE_LIST_OFF+8]) != EXPECTED_CREATE_ORIG:
        raise SystemExit('CreatePokedexList entry does not match expected BPEE bytes')
    if bytes(rom[INPUT_OFF:INPUT_OFF+8]) != EXPECTED_INPUT_ORIG:
        raise SystemExit('Task_HandlePokedexInput entry does not match expected BPEE bytes')

    create_stub=thumb_to_arm_stub(CREATE_LIST_ARM)
    input_stub=thumb_to_arm_stub(input_arm)
    rom[HOOK_OFF:HOOK_OFF+len(hooks)]=hooks
    rom[CREATE_LIST_OFF:CREATE_LIST_OFF+8]=create_stub
    rom[INPUT_OFF:INPUT_OFF+8]=input_stub

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(rom)

    checks=[]
    def check(name,cond,detail=None):
        checks.append({'name':name,'pass':bool(cond),'detail':detail})
        if not cond: raise AssertionError(f'{name}: {detail}')

    out=args.output.read_bytes()
    check('output_size_32MiB',len(out)==0x2000000,len(out))
    check('create_list_stub_exact',out[CREATE_LIST_OFF:CREATE_LIST_OFF+8]==create_stub,out[CREATE_LIST_OFF:CREATE_LIST_OFF+8].hex())
    check('input_stub_exact',out[INPUT_OFF:INPUT_OFF+8]==input_stub,out[INPUT_OFF:INPUT_OFF+8].hex())
    check('hook_blob_exact',out[HOOK_OFF:HOOK_OFF+len(hooks)]==hooks,len(hooks))
    check('create_list_arm_in_rom',CREATE_LIST_ARM-GBA==HOOK_OFF,hex(CREATE_LIST_ARM))
    check('input_arm_in_hook_blob',HOOK_OFF <= input_arm-GBA < HOOK_OFF+len(hooks),hex(input_arm))
    for name,val in [
        ('view_ptr',0x02039B4C),('getset_arm',0x09805C3C),('list_cont_thumb',0x080BC8DF),
        ('gmain_newkeys',0x030022EE),('handler_cont_thumb',0x080BC101),('create_list_thumb',0x080BC8D5),
        ('clear_sprites_thumb',0x080BDA41),('create_sprites_thumb',0x080BD2B5),('play_se_thumb',0x080A37A5),
        ('bank_state_offset',0x642),('list_count_offset',0x60C),('selected_offset',0x60E),
        ('dex_mode_offset',0x612),('dex_order_offset',0x616),('pokeball_rotation_offset',0x62C),
        ('bank_b_count',263),('bank_b_first_nat',387),('bank_b_end_exclusive',650),('physical_list_slots',387),
    ]:
        check('hook_literal_'+name,struct.pack('<I',val) in hooks,hex(val))
    check('core_getset_stub_preserved',out[0x0C0664:0x0C066C]==bytes.fromhex('004b18473c5c8009'),out[0x0C0664:0x0C066C].hex())
    check('core_count_stub_preserved',out[0x0C07F4:0x0C07FC]==bytes.fromhex('004b18472c5e8009'),out[0x0C07F4:0x0C07FC].hex())
    check('core_nat_to_species_stub_preserved',out[0x06D40C:0x06D414]==bytes.fromhex('004b1847705e8009'),out[0x06D40C:0x06D414].hex())
    check('route101_turtwig_smoke_slot_preserved',out[0x5507E4:0x5507E8]==bytes.fromhex('0202b801'),out[0x5507E4:0x5507E8].hex())

    manifest={
      'target':'Pokemon Emerald (USA, Europe) BPEE rev0',
      'input_core_rom':args.core_rom.name,
      'input_core_sha1':EXPECTED_CORE_SHA1,
      'output_rom':args.output.name,
      'output_size':len(out),
      'output_sha1':sha1(out),
      'output_sha256':sha256(out),
      'ui_mode':'banked National Dex coexistence',
      'bank_a':{'range':'National 001-386','behavior':'vanilla CreatePokedexList path preserved','key':'L'},
      'bank_b':{'range':'National 387-649','entries':263,'behavior':'numerical; all dex numbers listed; unseen names/sprites remain hidden','key':'R'},
      'bank_state':{'storage':'PokedexView filler[0]','offset':0x642,'lifetime':'current Pokedex session; AllocZeroed defaults to Bank A'},
      'hooks':{
        'CreatePokedexList':{'rom_offset':CREATE_LIST_OFF,'original':EXPECTED_CREATE_ORIG.hex(),'stub':create_stub.hex(),'arm_target':hex(CREATE_LIST_ARM)},
        'Task_HandlePokedexInput':{'rom_offset':INPUT_OFF,'original':EXPECTED_INPUT_ORIG.hex(),'stub':input_stub.hex(),'arm_target':hex(input_arm)},
        'arm_blob':{'rom_offset':HOOK_OFF,'gba_address':hex(GBA+HOOK_OFF),'size':len(hooks),'end_offset':HOOK_OFF+len(hooks)}
      },
      'runtime_calls':{
        'GetSetPokedexFlag_ARM':'0x09805C3C','CreatePokedexList_Thumb':'0x080BC8D5',
        'ClearMonSprites_Thumb':'0x080BDA41','CreateMonSpritesAtPos_Thumb':'0x080BD2B5','PlaySE_Thumb':'0x080A37A5'
      },
      'safety':{'PokedexView_size_changed':False,'vanilla_bank_a_overwritten':False,'SELECT_search_repurposed':False,
                'save_layout_shifted':False,'rom_binary_committed_to_github':False,'emulator_boot_tested':False},
      'static_validation':{'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks}
    }
    args.manifest_out.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['output_rom','output_size','output_sha1','output_sha256','ui_mode','bank_a','bank_b']},indent=2))
    print('validation',manifest['static_validation']['passed'],'/',manifest['static_validation']['total'])
    print('INPUT_ARM',hex(input_arm),'hook size',len(hooks),'end',hex(HOOK_OFF+len(hooks)))

if __name__=='__main__': main()
