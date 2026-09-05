#!/usr/bin/env python3
"""Build the Generation-III cumulative Pokémon-parameter layer for SILVER.

Source of truth: a local checkout of pret/pokeemerald.
Canonical species identity: National Dex number 252..386.
Pokeemerald's raw species ID is retained only as provenance because its old-Unown
placeholder IDs make Treecko start at raw ID 277 and Chimecho sit after Deoxys.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

GEN3_CONSTANTS = '''
TREECKO GROVYLE SCEPTILE TORCHIC COMBUSKEN BLAZIKEN MUDKIP MARSHTOMP SWAMPERT
POOCHYENA MIGHTYENA ZIGZAGOON LINOONE WURMPLE SILCOON BEAUTIFLY CASCOON DUSTOX
LOTAD LOMBRE LUDICOLO SEEDOT NUZLEAF SHIFTRY TAILLOW SWELLOW WINGULL PELIPPER
RALTS KIRLIA GARDEVOIR SURSKIT MASQUERAIN SHROOMISH BRELOOM SLAKOTH VIGOROTH
SLAKING NINCADA NINJASK SHEDINJA WHISMUR LOUDRED EXPLOUD MAKUHITA HARIYAMA
AZURILL NOSEPASS SKITTY DELCATTY SABLEYE MAWILE ARON LAIRON AGGRON MEDITITE
MEDICHAM ELECTRIKE MANECTRIC PLUSLE MINUN VOLBEAT ILLUMISE ROSELIA GULPIN
SWALOT CARVANHA SHARPEDO WAILMER WAILORD NUMEL CAMERUPT TORKOAL SPOINK GRUMPIG
SPINDA TRAPINCH VIBRAVA FLYGON CACNEA CACTURNE SWABLU ALTARIA ZANGOOSE SEVIPER
LUNATONE SOLROCK BARBOACH WHISCASH CORPHISH CRAWDAUNT BALTOY CLAYDOL LILEEP
CRADILY ANORITH ARMALDO FEEBAS MILOTIC CASTFORM KECLEON SHUPPET BANETTE DUSKULL
DUSCLOPS TROPIUS CHIMECHO ABSOL WYNAUT SNORUNT GLALIE SPHEAL SEALEO WALREIN
CLAMPERL HUNTAIL GOREBYSS RELICANTH LUVDISC BAGON SHELGON SALAMENCE BELDUM
METANG METAGROSS REGIROCK REGICE REGISTEEL LATIAS LATIOS KYOGRE GROUDON RAYQUAZA
JIRACHI DEOXYS
'''.split()
assert len(GEN3_CONSTANTS) == 135
NAT_BY_CONST = {name: 252 + i for i, name in enumerate(GEN3_CONSTANTS)}
CONST_BY_NAT = {v: k for k, v in NAT_BY_CONST.items()}

BASE_FIELDS = [
    'baseHP','baseAttack','baseDefense','baseSpeed','baseSpAttack','baseSpDefense',
    'catchRate','expYield','evYield_HP','evYield_Attack','evYield_Defense',
    'evYield_Speed','evYield_SpAttack','evYield_SpDefense','eggCycles',
    'safariZoneFleeRate',
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def git_head(root: Path) -> str:
    try:
        return subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'], text=True).strip()
    except Exception:
        return 'unknown'


def parse_species_constants(text: str) -> dict[str, int]:
    out = {}
    for name, value in re.findall(r'^#define\s+SPECIES_([A-Z0-9_]+)\s+(\d+)\b', text, re.M):
        out[name] = int(value)
    return out


def parse_scalar(body: str, field: str) -> str:
    m = re.search(rf'\.{re.escape(field)}\s*=\s*([^,\n]+)', body)
    if not m:
        return ''
    val = m.group(1).strip()
    if val == 'STANDARD_FRIENDSHIP':
        return '70'
    return val


def parse_pair(body: str, field: str) -> list[str]:
    m = re.search(rf'\.{re.escape(field)}\s*=\s*\{{\s*([^,}}]+)\s*,\s*([^,}}]+)', body)
    return [m.group(1).strip(), m.group(2).strip()] if m else ['', '']


def parse_species_info(text: str) -> dict[str, dict]:
    pat = re.compile(r'^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\n\s*\{\n(.*?)^\s{4}\},\s*$', re.M | re.S)
    out: dict[str, dict] = {}
    for name, body in pat.findall(text):
        d = {f: parse_scalar(body, f) for f in BASE_FIELDS}
        d['friendship'] = parse_scalar(body, 'friendship')
        d['growthRate'] = parse_scalar(body, 'growthRate')
        d['genderRatio'] = parse_scalar(body, 'genderRatio')
        d['itemCommon'] = parse_scalar(body, 'itemCommon')
        d['itemRare'] = parse_scalar(body, 'itemRare')
        d['bodyColor'] = parse_scalar(body, 'bodyColor')
        d['noFlip'] = parse_scalar(body, 'noFlip')
        d['types'] = parse_pair(body, 'types')
        d['eggGroups'] = parse_pair(body, 'eggGroups')
        d['abilities'] = parse_pair(body, 'abilities')
        out[name] = d
    return out


def parse_evolutions(text: str, raw_ids: dict[str,int]) -> list[dict]:
    starts = list(re.finditer(r'^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*', text, re.M))
    rows = []
    for i, m in enumerate(starts):
        src = m.group(1)
        if src not in NAT_BY_CONST:
            continue
        end = starts[i+1].start() if i+1 < len(starts) else len(text)
        chunk = text[m.end():end]
        for method, param, target in re.findall(r'\{\s*(EVO_[A-Z0-9_]+)\s*,\s*([^,}]+)\s*,\s*SPECIES_([A-Z0-9_]+)\s*\}', chunk):
            target_nat = NAT_BY_CONST.get(target)
            if target_nat is None and raw_ids.get(target, 9999) <= 251:
                target_nat = raw_ids[target]
            rows.append({'from_national_id': NAT_BY_CONST[src], 'from_constant': src, 'method': method, 'parameter': param.strip(), 'to_constant': target, 'to_national_id': target_nat if target_nat is not None else ''})
    return rows


def parse_levelup(learnsets: str, pointers: str) -> list[dict]:
    ptr = dict(re.findall(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*(s[A-Za-z0-9_]+LevelUpLearnset)', pointers))
    blocks = {}
    pat = re.compile(r'static const u16\s+(s[A-Za-z0-9_]+LevelUpLearnset)\[\]\s*=\s*\{(.*?)\n\};', re.S)
    for symbol, body in pat.findall(learnsets):
        blocks[symbol] = [(int(lvl), move) for lvl, move in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*MOVE_([A-Z0-9_]+)\s*\)', body)]
    rows=[]
    for const in GEN3_CONSTANTS:
        symbol = ptr.get(const)
        for level, move in blocks.get(symbol, []):
            rows.append({'national_id':NAT_BY_CONST[const], 'constant':const, 'level':level, 'move':move})
    return rows


def parse_tmhm(text: str) -> list[dict]:
    starts=list(re.finditer(r'^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{\s*\.learnset\s*=\s*\{', text, re.M))
    rows=[]
    for i,m in enumerate(starts):
        const=m.group(1)
        if const not in NAT_BY_CONST:
            continue
        end=starts[i+1].start() if i+1 < len(starts) else len(text)
        chunk=text[m.end():end]
        for move in re.findall(r'^\s*\.([A-Z0-9_]+)\s*=\s*TRUE', chunk, re.M):
            rows.append({'national_id':NAT_BY_CONST[const], 'constant':const, 'machine_move':move})
    return rows


def parse_tutor(text: str) -> list[dict]:
    rows=[]
    starts=list(re.finditer(r'^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*', text, re.M))
    for i,m in enumerate(starts):
        const=m.group(1)
        if const not in NAT_BY_CONST:
            continue
        end=starts[i+1].start() if i+1 < len(starts) else len(text)
        chunk=text[m.end():end]
        moves=set(re.findall(r'TUTOR\(\s*([A-Z0-9_]+)\s*\)', chunk))
        moves.update(re.findall(r'^\s*\.([A-Z0-9_]+)\s*=\s*TRUE', chunk, re.M))
        for move in sorted(moves):
            rows.append({'national_id':NAT_BY_CONST[const], 'constant':const, 'tutor_move':move})
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('pokeemerald_root', type=Path)
    ap.add_argument('output_dir', type=Path)
    args=ap.parse_args()
    root=args.pokeemerald_root.resolve(); out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    files={'species_info': root/'src/data/pokemon/species_info.h','species_constants': root/'include/constants/species.h','evolution': root/'src/data/pokemon/evolution.h','levelup': root/'src/data/pokemon/level_up_learnsets.h','levelup_pointers': root/'src/data/pokemon/level_up_learnset_pointers.h','tmhm': root/'src/data/pokemon/tmhm_learnsets.h','tutor': root/'src/data/pokemon/tutor_learnsets.h'}
    missing=[str(p) for p in files.values() if not p.exists()]
    if missing: raise SystemExit('Missing pokeemerald source files: '+', '.join(missing))
    raw_ids=parse_species_constants(read(files['species_constants']))
    info=parse_species_info(read(files['species_info']))
    base=[]
    for const in GEN3_CONSTANTS:
        if const not in info: raise SystemExit(f'Missing species info: {const}')
        d=info[const]
        row={'national_id':NAT_BY_CONST[const], 'constant':const,'pokeemerald_raw_species_id':raw_ids.get(const,''),'hp':d['baseHP'],'attack':d['baseAttack'],'defense':d['baseDefense'],'speed':d['baseSpeed'],'sp_attack':d['baseSpAttack'],'sp_defense':d['baseSpDefense'],'type1':d['types'][0],'type2':d['types'][1], 'catch_rate':d['catchRate'],'exp_yield':d['expYield'],'ev_hp':d['evYield_HP'],'ev_attack':d['evYield_Attack'],'ev_defense':d['evYield_Defense'],'ev_speed':d['evYield_Speed'],'ev_sp_attack':d['evYield_SpAttack'],'ev_sp_defense':d['evYield_SpDefense'],'item_common':d['itemCommon'],'item_rare':d['itemRare'],'gender_ratio':d['genderRatio'],'egg_cycles':d['eggCycles'],'friendship':d['friendship'],'growth_rate':d['growthRate'],'egg_group1':d['eggGroups'][0],'egg_group2':d['eggGroups'][1],'ability1':d['abilities'][0],'ability2':d['abilities'][1],'safari_flee_rate':d['safariZoneFleeRate'],'body_color':d['bodyColor'],'no_flip':d['noFlip']}
        base.append(row)
    write_csv(out/'gen3_species_parameters.csv',base,list(base[0].keys()))
    evos=parse_evolutions(read(files['evolution']),raw_ids); write_csv(out/'gen3_evolutions.csv',evos,['from_national_id','from_constant','method','parameter','to_constant','to_national_id'])
    level=parse_levelup(read(files['levelup']),read(files['levelup_pointers'])); write_csv(out/'gen3_levelup_learnsets.csv',level,['national_id','constant','level','move'])
    tmhm=parse_tmhm(read(files['tmhm'])); write_csv(out/'gen3_tmhm_learnsets.csv',tmhm,['national_id','constant','machine_move'])
    tutor=parse_tutor(read(files['tutor'])); write_csv(out/'gen3_tutor_learnsets.csv',tutor,['national_id','constant','tutor_move'])
    by_nat={int(r['national_id']):r for r in base}; evo_by={i:[] for i in by_nat}; lvl_by={i:[] for i in by_nat}; tm_by={i:[] for i in by_nat}; tut_by={i:[] for i in by_nat}
    for r in evos: evo_by[int(r['from_national_id'])].append(r)
    for r in level: lvl_by[int(r['national_id'])].append({'level':r['level'],'move':r['move']})
    for r in tmhm: tm_by[int(r['national_id'])].append(r['machine_move'])
    for r in tutor: tut_by[int(r['national_id'])].append(r['tutor_move'])
    bundle=[]
    for nid in range(252,387): bundle.append({'national_id':nid,'species':CONST_BY_NAT[nid],'source_internal_id':by_nat[nid]['pokeemerald_raw_species_id'],'base_parameters':by_nat[nid],'evolutions':evo_by[nid],'level_up':lvl_by[nid],'tm_hm':tm_by[nid],'tutor':tut_by[nid]})
    (out/'gen3_parameter_bundle.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    special={'canonical_range':[252,386],'species_count':135,'canonical_id_rule':'National Dex number; never pokeemerald raw species ID','source_repo':'pret/pokeemerald','source_commit':git_head(root),'special_engine_cases':['Wurmple evolution branch depends on personality value.','Nincada evolution requires special Shedinja creation handling.','Feebas evolves by Beauty; Silver has no native Contest condition.','Generation III adds Abilities and six-stat EV yields.','Generation III adds Erratic and Fluctuating growth curves used by some species.','Deoxys is canonical species #386; form handling must be separated from species identity.'],'source_files':{k:{'path':str(v.relative_to(root)),'sha256':sha256(v)} for k,v in files.items()},'output_files':{}}
    for p in sorted(out.glob('gen3_*')):
        if p.is_file(): special['output_files'][p.name]={'sha256':sha256(p),'bytes':p.stat().st_size}
    (out/'gen3_manifest.json').write_text(json.dumps(special,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert len(base)==135 and [int(r['national_id']) for r in base]==list(range(252,387)); assert len({r['constant'] for r in base})==135
    treecko=base[0]; deoxys=base[-1]; chimecho=base[358-252]
    assert treecko['constant']=='TREECKO' and int(treecko['hp'])==40; assert deoxys['constant']=='DEOXYS' and int(deoxys['attack'])==150; assert chimecho['constant']=='CHIMECHO'; assert int(treecko['pokeemerald_raw_species_id']) != 252
    print(json.dumps({'species':len(base),'evolution_rows':len(evos),'levelup_rows':len(level),'tmhm_rows':len(tmhm),'tutor_rows':len(tutor),'source_commit':special['source_commit'],'output':str(out)}, indent=2))

if __name__=='__main__': main()
