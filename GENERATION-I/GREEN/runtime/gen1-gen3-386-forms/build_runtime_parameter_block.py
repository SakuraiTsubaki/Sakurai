#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, struct, zlib
from pathlib import Path

HEADER_SIZE = 0x100
GEN2_RECORD_SIZE = 29
GEN3_RECORD_SIZE = 30
FORM_RECORD_SIZE = 8

TRIGGER_IDS = {
    'personality-derived':1,
    'clear-or-nontrigger-weather':2,
    'harsh-sunlight':3,
    'rain':4,
    'hail':5,
    'explicit-form':6,
}
SCOPE_IDS = {'gen2-gen3':1, 'gen3':2}


def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def i(row, key):
    return int(row[key])


def sha1_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def pack_gen2(row):
    tm = bytes.fromhex(row['tmhm_bits_hex'])
    if len(tm) != 8:
        raise ValueError(f"Gen2 #{row['national_dex']} TMHM bitset is not 8 bytes")
    out = bytearray()
    out += struct.pack('<H', i(row,'national_dex'))
    out += bytes(i(row,k) for k in ('hp','attack','defense','speed','sp_attack','sp_defense'))
    out += bytes((i(row,'type1_id'), i(row,'type2_id'), i(row,'catch_rate'), i(row,'base_exp')))
    out += bytes((i(row,'held_item_common_id'), i(row,'held_item_rare_id')))
    out += bytes((i(row,'gender_threshold'), i(row,'hatch_cycles'), i(row,'friendship_base'), i(row,'growth_id')))
    out += bytes((i(row,'egg_group1_id'), i(row,'egg_group2_id')))
    out += tm
    out += bytes((i(row,'introduced_generation'),))
    if len(out) != GEN2_RECORD_SIZE:
        raise AssertionError(len(out))
    return bytes(out)


def pack_gen3(row):
    out = struct.pack(
        '<H6B2BHH6B2B6B2B',
        i(row,'national_dex'),
        i(row,'hp'), i(row,'attack'), i(row,'defense'), i(row,'speed'), i(row,'sp_attack'), i(row,'sp_defense'),
        i(row,'type1_id'), i(row,'type2_id'),
        i(row,'catch_rate'), i(row,'base_exp'),
        i(row,'gender_threshold'), i(row,'hatch_cycles'), i(row,'friendship'), i(row,'growth_id'),
        i(row,'egg_group1_id'), i(row,'egg_group2_id'),
        i(row,'ability1_id'), i(row,'ability2_id'),
        i(row,'ev_hp'), i(row,'ev_attack'), i(row,'ev_defense'), i(row,'ev_speed'), i(row,'ev_sp_attack'), i(row,'ev_sp_defense'),
        i(row,'introduced_generation'),
        1 if i(row,'national_dex') <= 251 else 2,
    )
    if len(out) != GEN3_RECORD_SIZE:
        raise AssertionError(len(out))
    return out


def yes(value):
    return value.strip().lower() == 'yes'


def pack_form(row):
    flags = 0
    persistence = row['persistence'].strip().lower()
    if persistence == 'persistent': flags |= 0x01
    if persistence == 'battle-only': flags |= 0x02
    if persistence == 'base/outside-battle': flags |= 0x04
    if yes(row['personal_override']): flags |= 0x08
    if yes(row['learnset_override']): flags |= 0x10
    if yes(row['sprite_variant']): flags |= 0x20
    trigger = TRIGGER_IDS[row['trigger']]
    scope = SCOPE_IDS[row['scope']]
    out = struct.pack('<HBBBBBB', int(row['species_id']), int(row['form_id']), flags, trigger, scope, 0, 0)
    if len(out) != FORM_RECORD_SIZE:
        raise AssertionError(len(out))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gen2', type=Path, required=True)
    ap.add_argument('--gen3', type=Path, required=True)
    ap.add_argument('--forms', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    gen2 = read_csv(args.gen2)
    gen3 = read_csv(args.gen3)
    forms = read_csv(args.forms)

    assert len(gen2) == 251
    assert [int(r['national_dex']) for r in gen2] == list(range(1,252))
    assert len(gen3) == 386
    assert [int(r['national_dex']) for r in gen3] == list(range(1,387))
    assert len(forms) == 36
    assert sum(1 for r in forms if int(r['species_id']) == 201) == 28
    assert sum(1 for r in forms if int(r['species_id']) == 351) == 4
    assert sum(1 for r in forms if int(r['species_id']) == 386) == 4

    gen2_blob = b''.join(pack_gen2(r) for r in gen2)
    gen3_blob = b''.join(pack_gen3(r) for r in gen3)
    form_blob = b''.join(pack_form(r) for r in forms)

    off_gen2 = HEADER_SIZE
    off_gen3 = off_gen2 + len(gen2_blob)
    off_forms = off_gen3 + len(gen3_blob)
    end = off_forms + len(form_blob)

    header = bytearray(HEADER_SIZE)
    header[0:8] = b'G386F3\0\0'
    struct.pack_into('<HHHHHHH', header, 0x08, 2, HEADER_SIZE, 386, 419, 251, 386, 36)
    struct.pack_into('<IIII', header, 0x20, off_gen2, off_gen3, off_forms, end)
    struct.pack_into('<HHH', header, 0x34, GEN2_RECORD_SIZE, GEN3_RECORD_SIZE, FORM_RECORD_SIZE)
    header[0x40:0x60] = b'GREEN 386 + GEN3 FORMS ABI V2'.ljust(32,b'\0')

    payload = header + gen2_blob + gen3_blob + form_blob
    crc = zlib.crc32(payload) & 0xffffffff
    struct.pack_into('<I', payload, 0x60, crc)

    out = args.out_dir/'green_386_forms_runtime_parameter_block.bin'
    out.write_bytes(payload)
    manifest = {
        'schema':'green-386-forms-runtime-block-v2',
        'magic':'G386F3',
        'identity_abi':{'species_id':'u16','form_id':'u8'},
        'canonical_species_max':386,
        'species_form_combinations':419,
        'gen2_overlay':{'count':251,'record_size':GEN2_RECORD_SIZE,'offset':off_gen2},
        'gen3_overlay':{'count':386,'record_size':GEN3_RECORD_SIZE,'offset':off_gen3},
        'form_descriptors':{'count':36,'record_size':FORM_RECORD_SIZE,'offset':off_forms},
        'size':len(payload),
        'crc32':f'{crc:08x}',
        'sha1':sha1_bytes(payload),
        'runtime_status':'parameter scaffold only; Green engine hooks/party/box/save/battle migration are separate and not yet claimed complete',
    }
    (args.out_dir/'RUNTIME_BLOCK_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__ == '__main__':
    main()
