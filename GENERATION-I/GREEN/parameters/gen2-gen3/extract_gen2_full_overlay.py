#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, re, subprocess
from pathlib import Path

TYPE_IDS = {
    'NORMAL':0,'FIGHTING':1,'FLYING':2,'POISON':3,'GROUND':4,'ROCK':5,'BUG':6,'GHOST':7,
    'STEEL':8,'FIRE':9,'WATER':10,'GRASS':11,'ELECTRIC':12,'PSYCHIC':13,'ICE':14,'DRAGON':15,'DARK':16,
}
GROWTH_IDS = {
    'GROWTH_MEDIUM_FAST':0,'GROWTH_SLIGHTLY_FAST':1,'GROWTH_SLIGHTLY_SLOW':2,'GROWTH_MEDIUM_SLOW':3,
    'GROWTH_FAST':4,'GROWTH_SLOW':5,'GROWTH_ERRATIC':6,'GROWTH_FLUCTUATING':7,
}
EGG_IDS = {
    'EGG_MONSTER':1,'EGG_WATER_1':2,'EGG_BUG':3,'EGG_FLYING':4,'EGG_GROUND':5,'EGG_FAIRY':6,
    'EGG_PLANT':7,'EGG_HUMANSHAPE':8,'EGG_WATER_3':9,'EGG_MINERAL':10,'EGG_INDETERMINATE':11,
    'EGG_WATER_2':12,'EGG_DITTO':13,'EGG_DRAGON':14,'EGG_NONE':15,
}
GENDER = {
    'GENDER_F0':0,'GENDER_F12_5':31,'GENDER_F25':63,'GENDER_F50':127,
    'GENDER_F75':191,'GENDER_F100':254,'GENDER_UNKNOWN':255,
}


def repo_sha(root: Path) -> str:
    return subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'], text=True).strip()


def norm_type(token: str) -> int:
    if token == 'PSYCHIC_TYPE':
        token = 'PSYCHIC'
    return TYPE_IDS[token]


def parse_global_base_happiness(root: Path) -> int:
    text=(root/'constants/pokemon_data_constants.asm').read_text(encoding='utf-8')
    m=re.search(r'^DEF\s+BASE_HAPPINESS\s+EQU\s+(\d+)\s*$', text, re.M)
    if not m:
        raise ValueError('BASE_HAPPINESS not found')
    return int(m.group(1))


def parse_item_ids(root: Path) -> dict[str,int]:
    text=(root/'constants/item_constants.asm').read_text(encoding='utf-8')
    out={name:int(hx,16) for name,hx in re.findall(
        r'^\s*const\s+([A-Z0-9_]+)\s*;\s*([0-9a-fA-F]{2})\s*$', text, re.M)}
    if out.get('NO_ITEM') != 0 or out.get('LEFTOVERS') != 0x92:
        raise ValueError('item constant parse sanity check failed')
    return out


def parse_tmhm_order(root: Path) -> list[str]:
    text=(root/'constants/item_constants.asm').read_text(encoding='utf-8')
    order=[]
    in_macro=False
    for raw in text.splitlines():
        line=raw.strip()
        if line.startswith('MACRO'):
            in_macro=True
            continue
        if in_macro:
            if line == 'ENDM':
                in_macro=False
            continue
        m=re.match(r'add_(?:tm|hm|mt)\s+([A-Z0-9_]+)(?:\s*;.*)?$', line)
        if m:
            order.append(m.group(1))
    if len(order) != 60:
        raise ValueError(f'expected 60 Gen II TM/HM/tutor flags, got {len(order)}')
    if order[:4] != ['DYNAMICPUNCH','HEADBUTT','CURSE','ROLLOUT']:
        raise ValueError('TM order sanity check failed')
    if order[-3:] != ['FLAMETHROWER','THUNDERBOLT','ICE_BEAM']:
        raise ValueError('move tutor order sanity check failed')
    return order


def encode_tmhm_bits(tokens: list[str], order: list[str]) -> str:
    pos={token:i for i,token in enumerate(order)}
    buf=bytearray((len(order)+7)//8)
    for token in tokens:
        if token not in pos:
            raise ValueError(f'unknown TM/HM/tutor token {token}')
        i=pos[token]
        buf[i//8] |= 1 << (i%8)
    return buf.hex()


def parse_file(p: Path, item_ids: dict[str,int], tmhm_order: list[str], base_happiness: int):
    text=p.read_text(encoding='utf-8')
    head=re.search(r'^\s*db\s+([A-Z0-9_]+)\s*;\s*(\d+)\s*$',text,re.M)
    if not head:
        return None
    species_token,nat=head.group(1),int(head.group(2))
    if not 1 <= nat <= 251:
        return None
    stats=re.search(r'^\s*db\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\n\s*;\s*hp\s+atk\s+def\s+spd\s+sat\s+sdf',text,re.M)
    types=re.search(r'^\s*db\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*;\s*type',text,re.M)
    items=re.search(r'^\s*db\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*;\s*items',text,re.M)
    gender=re.search(r'^\s*db\s+([^;]+)\s*;\s*gender ratio',text,re.M)
    hatch=re.search(r'^\s*db\s+(\d+)\s*;\s*step cycles to hatch',text,re.M)
    growth=re.search(r'^\s*db\s+(GROWTH_[A-Z0-9_]+)\s*;\s*growth rate',text,re.M)
    eggs=re.search(r'^\s*dn\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*;\s*egg groups',text,re.M)
    tmhm=re.search(r'^[ \t]*tmhm[ \t]*([^\r\n]*)$',text,re.M)
    if not all([stats,types,items,gender,hatch,growth,eggs]):
        raise ValueError(f'incomplete Crystal base stats: {p}')
    comments={}
    for value,comment in re.findall(r'^\s*db\s+([^;]+?)\s*;\s*([^\n]+)$',text,re.M):
        comments[comment.strip().lower()]=value.strip()
    hp,atk,defn,spd,spa,spdef=map(int,stats.groups())
    t1,t2=types.groups(); i1,i2=items.groups(); e1,e2=eggs.groups(); gt=gender.group(1).strip(); gr=growth.group(1)
    if i1 not in item_ids or i2 not in item_ids:
        raise ValueError(f'{p.name}: unknown held item token(s) {i1}, {i2}')
    tokens=[x.strip() for x in (tmhm.group(1).split(',') if tmhm else []) if x.strip()]
    return {
        'national_dex':nat,'identifier':p.stem,'source_species_token':species_token,
        'introduced_generation':1 if nat<=151 else 2,
        'hp':hp,'attack':atk,'defense':defn,'speed':spd,'sp_attack':spa,'sp_defense':spdef,
        'type1_token':t1,'type2_token':t2,'type1_id':norm_type(t1),'type2_id':norm_type(t2),
        'catch_rate':int(comments['catch rate']),'base_exp':int(comments['base exp']),
        'held_item_common':i1,'held_item_rare':i2,
        'held_item_common_id':item_ids[i1],'held_item_rare_id':item_ids[i2],
        'gender_token':gt,'gender_threshold':GENDER.get(gt,255),
        'hatch_cycles':int(hatch.group(1)),
        'friendship_base':base_happiness,'friendship_source_token':'BASE_HAPPINESS',
        'growth_token':gr,'growth_id':GROWTH_IDS[gr],
        'egg_group1_token':e1,'egg_group2_token':e2,
        'egg_group1_id':EGG_IDS[e1],'egg_group2_id':EGG_IDS[e2],
        'tmhm_tokens':'|'.join(tokens),'tmhm_flag_count':len(tmhm_order),
        'tmhm_bits_hex':encode_tmhm_bits(tokens,tmhm_order),
        'source_path':str(p).replace('\\','/'),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pokecrystal',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    item_ids=parse_item_ids(a.pokecrystal)
    tmhm_order=parse_tmhm_order(a.pokecrystal)
    base_happiness=parse_global_base_happiness(a.pokecrystal)
    rows=[]
    for p in sorted((a.pokecrystal/'data/pokemon/base_stats').glob('*.asm')):
        r=parse_file(p,item_ids,tmhm_order,base_happiness)
        if r: rows.append(r)
    rows.sort(key=lambda r:r['national_dex'])
    assert len(rows)==251, len(rows)
    assert [r['national_dex'] for r in rows]==list(range(1,252))
    assert all(len(bytes.fromhex(r['tmhm_bits_hex']))==8 for r in rows)
    out=a.out/'gen2_personal_overlay_001_251.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    order_rows=[{'flag_number':i+1,'token':token,'byte_index':i//8,'bit_index':i%8} for i,token in enumerate(tmhm_order)]
    with (a.out/'gen2_tmhm_tutor_flag_order.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(order_rows[0].keys())); w.writeheader(); w.writerows(order_rows)
    meta={
        'schema':'green-gen2-full-overlay-v2','source_repo':'pret/pokecrystal',
        'source_commit':repo_sha(a.pokecrystal),'species_count':251,'range':[1,251],
        'gen1_species_represented':151,'gen2_native_species':100,
        'base_happiness':base_happiness,'tm_hm_tutor_flags':len(tmhm_order),
        'tm_hm_tutor_bytes_per_species':8,
        'held_item_ids':'resolved from constants/item_constants.asm',
        'policy':'Crystal Generation II personal state for every National Dex species #001-251; this complete overlay precedes the Generation III overlay.'
    }
    (a.out/'GEN2_FULL_OVERLAY.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps(meta,indent=2))

if __name__=='__main__':
    main()
