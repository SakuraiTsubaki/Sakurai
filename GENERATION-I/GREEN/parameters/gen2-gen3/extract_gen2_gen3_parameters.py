#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, re, struct, subprocess, zlib
from pathlib import Path

TYPE_IDS = {
    'NORMAL':0,'FIGHTING':1,'FLYING':2,'POISON':3,'GROUND':4,'ROCK':5,'BUG':6,'GHOST':7,
    'STEEL':8,'FIRE':9,'WATER':10,'GRASS':11,'ELECTRIC':12,'PSYCHIC':13,'ICE':14,'DRAGON':15,'DARK':16,
}
GROWTH_IDS = {
    'GROWTH_MEDIUM_FAST':0,
    'GROWTH_SLIGHTLY_FAST':1,
    'GROWTH_SLIGHTLY_SLOW':2,
    'GROWTH_MEDIUM_SLOW':3,
    'GROWTH_FAST':4,
    'GROWTH_SLOW':5,
    'GROWTH_ERRATIC':6,
    'GROWTH_FLUCTUATING':7,
}
EGG_IDS = {
    'EGG_MONSTER':1,'EGG_WATER_1':2,'EGG_BUG':3,'EGG_FLYING':4,'EGG_GROUND':5,'EGG_FAIRY':6,
    'EGG_PLANT':7,'EGG_HUMANSHAPE':8,'EGG_WATER_3':9,'EGG_MINERAL':10,'EGG_INDETERMINATE':11,
    'EGG_WATER_2':12,'EGG_DITTO':13,'EGG_DRAGON':14,'EGG_NONE':15,
    'EGG_GROUP_MONSTER':1,'EGG_GROUP_WATER_1':2,'EGG_GROUP_BUG':3,'EGG_GROUP_FLYING':4,'EGG_GROUP_FIELD':5,
    'EGG_GROUP_FAIRY':6,'EGG_GROUP_GRASS':7,'EGG_GROUP_HUMAN_LIKE':8,'EGG_GROUP_WATER_3':9,
    'EGG_GROUP_MINERAL':10,'EGG_GROUP_AMORPHOUS':11,'EGG_GROUP_WATER_2':12,'EGG_GROUP_DITTO':13,
    'EGG_GROUP_DRAGON':14,'EGG_GROUP_NO_EGGS_DISCOVERED':15,
}
GEN3_ABILITY_ORDER = [
'stench','drizzle','speed-boost','battle-armor','sturdy','damp','limber','sand-veil','static','volt-absorb',
'water-absorb','oblivious','cloud-nine','compound-eyes','insomnia','color-change','immunity','flash-fire','shield-dust','own-tempo',
'suction-cups','intimidate','shadow-tag','rough-skin','wonder-guard','levitate','effect-spore','synchronize','clear-body','natural-cure',
'lightning-rod','serene-grace','swift-swim','chlorophyll','illuminate','trace','huge-power','poison-point','inner-focus','magma-armor',
'water-veil','magnet-pull','soundproof','rain-dish','sand-stream','pressure','thick-fat','early-bird','flame-body','run-away',
'keen-eye','hyper-cutter','pickup','truant','hustle','cute-charm','plus','minus','forecast','sticky-hold','shed-skin','guts',
'marvel-scale','liquid-ooze','overgrow','blaze','torrent','swarm','rock-head','drought','arena-trap','vital-spirit','white-smoke',
'pure-power','shell-armor','air-lock']
ABILITY_IDS = {'ABILITY_NONE':0}
for i,name in enumerate(GEN3_ABILITY_ORDER,1):
    ABILITY_IDS['ABILITY_' + name.upper().replace('-','_')] = i
NATURES = [
    ('HARDY',None,None),('LONELY','ATK','DEF'),('BRAVE','ATK','SPEED'),('ADAMANT','ATK','SP_ATK'),('NAUGHTY','ATK','SP_DEF'),
    ('BOLD','DEF','ATK'),('DOCILE',None,None),('RELAXED','DEF','SPEED'),('IMPISH','DEF','SP_ATK'),('LAX','DEF','SP_DEF'),
    ('TIMID','SPEED','ATK'),('HASTY','SPEED','DEF'),('SERIOUS',None,None),('JOLLY','SPEED','SP_ATK'),('NAIVE','SPEED','SP_DEF'),
    ('MODEST','SP_ATK','ATK'),('MILD','SP_ATK','DEF'),('QUIET','SP_ATK','SPEED'),('BASHFUL',None,None),('RASH','SP_ATK','SP_DEF'),
    ('CALM','SP_DEF','ATK'),('GENTLE','SP_DEF','DEF'),('SASSY','SP_DEF','SPEED'),('CAREFUL','SP_DEF','SP_ATK'),('QUIRKY',None,None),
]

def repo_sha(path: Path) -> str:
    try:
        return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'], text=True).strip()
    except Exception:
        return 'unknown'

def parse_int(s: str):
    s=s.strip()
    try: return int(s,0)
    except Exception: return None

def pct_gender_value(token: str):
    token=token.strip()
    mapping={'MON_MALE':0,'MON_FEMALE':254,'MON_GENDERLESS':255,'GENDER_UNKNOWN':255}
    if token in mapping:return mapping[token]
    cm={'GENDER_F0':0,'GENDER_F12_5':31,'GENDER_F25':63,'GENDER_F50':127,'GENDER_F75':191,'GENDER_F100':254}
    if token in cm:return cm[token]
    m=re.fullmatch(r'PERCENT_FEMALE\(([-0-9.]+)\)',token)
    if m:
        p=float(m.group(1)); return min(254,int((p*255)//100))
    return None

def norm_type(tok):
    tok=tok.strip()
    if tok.startswith('TYPE_'): tok=tok[5:]
    if tok == 'PSYCHIC_TYPE': tok = 'PSYCHIC'
    return TYPE_IDS[tok]

def norm_growth(tok): return GROWTH_IDS.get(tok.strip(),255)
def norm_egg(tok): return EGG_IDS.get(tok.strip(),255)
def norm_ability(tok): return ABILITY_IDS.get(tok.strip(),255)

def parse_gen2_file(p: Path):
    text=p.read_text(encoding='utf-8')
    lines=text.splitlines()
    m=re.search(r'^\s*db\s+([A-Z0-9_]+)\s*;\s*(\d+)\s*$',text,re.M)
    if not m:return None
    species_token,nat=m.group(1),int(m.group(2))
    if not (152<=nat<=251):return None
    statm=re.search(r'^\s*db\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\n\s*;\s*hp\s+atk\s+def\s+spd\s+sat\s+sdf',text,re.M)
    if not statm: raise ValueError(f'no stats: {p}')
    hp,atk,defn,spd,spa,spd2=map(int,statm.groups())
    typem=re.search(r'^\s*db\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*;\s*type',text,re.M)
    nums=[]
    for ln in lines:
        mm=re.match(r'^\s*db\s+([^;]+)\s*;\s*(.*)$',ln)
        if mm: nums.append((mm.group(1).strip(),mm.group(2).strip().lower()))
    def bycomment(prefix):
        for val,comment in nums:
            if comment.startswith(prefix): return val
        return ''
    itemsm=re.search(r'^\s*db\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*;\s*items',text,re.M)
    genderm=re.search(r'^\s*db\s+([^;]+)\s*;\s*gender ratio',text,re.M)
    hatchm=re.search(r'^\s*db\s+(\d+)\s*;\s*step cycles to hatch',text,re.M)
    growthm=re.search(r'^\s*db\s+(GROWTH_[A-Z0-9_]+)\s*;\s*growth rate',text,re.M)
    eggm=re.search(r'^\s*dn\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*;\s*egg groups',text,re.M)
    tmhm=re.search(r'^\s*tmhm\s*(.*?)\s*$',text,re.M)
    t1,t2=typem.groups()
    item1,item2=itemsm.groups() if itemsm else ('','')
    gender=genderm.group(1).strip() if genderm else ''
    growth=growthm.group(1) if growthm else ''
    e1,e2=eggm.groups() if eggm else ('','')
    return {
        'national_dex':nat,'identifier':p.stem,'source_species_token':species_token,'introduced_generation':2,
        'hp':hp,'attack':atk,'defense':defn,'speed':spd,'sp_attack':spa,'sp_defense':spd2,
        'type1_token':t1,'type2_token':t2,'type1_id':norm_type(t1),'type2_id':norm_type(t2),
        'catch_rate':int(bycomment('catch rate')),'base_exp':int(bycomment('base exp')),
        'held_item_common':item1,'held_item_rare':item2,
        'gender_token':gender,'gender_threshold':pct_gender_value(gender),
        'hatch_cycles':int(hatchm.group(1)) if hatchm else None,
        'friendship':70,
        'growth_token':growth,'growth_id':norm_growth(growth),
        'egg_group1_token':e1,'egg_group2_token':e2,'egg_group1_id':norm_egg(e1),'egg_group2_id':norm_egg(e2),
        'tmhm_tokens':'|'.join(x.strip() for x in (tmhm.group(1).split(',') if tmhm else []) if x.strip()),
        'source_path':str(p).replace('\\','/'),
    }

def parse_gen3_species_info(path: Path):
    text=path.read_text(encoding='utf-8')
    rx=re.compile(r'^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\n\s*\{(.*?)^\s*\},',re.M|re.S)
    blocks=[(name,body) for name,body in rx.findall(text) if name!='NONE']
    names=[n for n,_ in blocks]
    if 'BULBASAUR' not in names or 'CELEBI' not in names or 'TREECKO' not in names or 'DEOXYS' not in names:
        raise ValueError('expected species anchors missing')
    def span(a,b,startdex):
        ia,ib=names.index(a),names.index(b)
        sub=blocks[ia:ib+1]
        return [(startdex+i,n,bod) for i,(n,bod) in enumerate(sub)]
    selected=span('BULBASAUR','CELEBI',1)+span('TREECKO','DEOXYS',252)
    assert len(selected)==386, len(selected)
    def field(body,key):
        m=re.search(r'\.'+re.escape(key)+r'\s*=\s*([^,\n]+)',body)
        return m.group(1).strip() if m else ''
    def pair(body,key):
        m=re.search(r'\.'+re.escape(key)+r'\s*=\s*\{\s*([^,}]+)\s*,\s*([^,}]+)',body)
        return (m.group(1).strip(),m.group(2).strip()) if m else ('','')
    out=[]
    for nat,name,body in selected:
        t1,t2=pair(body,'types'); e1,e2=pair(body,'eggGroups'); a1,a2=pair(body,'abilities')
        gender=field(body,'genderRatio'); fr=field(body,'friendship')
        friendship=70 if fr=='STANDARD_FRIENDSHIP' else parse_int(fr)
        vals={k:parse_int(field(body,k)) for k in ['baseHP','baseAttack','baseDefense','baseSpeed','baseSpAttack','baseSpDefense','catchRate','expYield','evYield_HP','evYield_Attack','evYield_Defense','evYield_Speed','evYield_SpAttack','evYield_SpDefense','eggCycles','safariZoneFleeRate']}
        growth=field(body,'growthRate')
        out.append({
            'national_dex':nat,'identifier':name.lower(),'source_species_token':'SPECIES_'+name,
            'introduced_generation': 1 if nat<=151 else 2 if nat<=251 else 3,
            'hp':vals['baseHP'],'attack':vals['baseAttack'],'defense':vals['baseDefense'],'speed':vals['baseSpeed'],'sp_attack':vals['baseSpAttack'],'sp_defense':vals['baseSpDefense'],
            'type1_token':t1,'type2_token':t2,'type1_id':norm_type(t1),'type2_id':norm_type(t2),
            'catch_rate':vals['catchRate'],'base_exp':vals['expYield'],
            'ev_hp':vals['evYield_HP'],'ev_attack':vals['evYield_Attack'],'ev_defense':vals['evYield_Defense'],'ev_speed':vals['evYield_Speed'],'ev_sp_attack':vals['evYield_SpAttack'],'ev_sp_defense':vals['evYield_SpDefense'],
            'held_item_common':field(body,'itemCommon'),'held_item_rare':field(body,'itemRare'),
            'gender_token':gender,'gender_threshold':pct_gender_value(gender),
            'hatch_cycles':vals['eggCycles'],'friendship':friendship,
            'growth_token':growth,'growth_id':norm_growth(growth),
            'egg_group1_token':e1,'egg_group2_token':e2,'egg_group1_id':norm_egg(e1),'egg_group2_id':norm_egg(e2),
            'ability1_token':a1,'ability2_token':a2,'ability1_id':norm_ability(a1),'ability2_id':norm_ability(a2),
            'safari_flee_rate':vals['safariZoneFleeRate'],'body_color_token':field(body,'bodyColor'),'no_flip_token':field(body,'noFlip'),
            'source_path':str(path).replace('\\','/'),
        })
    return out

def write_csv(rows, path, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def sha1(path):
    h=hashlib.sha1(); h.update(path.read_bytes()); return h.hexdigest()

def build_block(gen2, gen3_all, outpath: Path):
    hs=0x100
    rs=30
    records=[]
    for r in gen3_all:
        flags=1 if r['national_dex']<=251 else 2
        records.append(struct.pack('<H6B2BHH6B2B6B2B',
            r['national_dex'], r['hp'],r['attack'],r['defense'],r['speed'],r['sp_attack'],r['sp_defense'],
            r['type1_id'],r['type2_id'],r['catch_rate'],r['base_exp'],r['gender_threshold'] if r['gender_threshold'] is not None else 255,
            r['hatch_cycles'],r['friendship'] if r['friendship'] is not None else 70,r['growth_id'],r['egg_group1_id'],r['egg_group2_id'],
            r['ability1_id'],r['ability2_id'],r['ev_hp'],r['ev_attack'],r['ev_defense'],r['ev_speed'],r['ev_sp_attack'],r['ev_sp_defense'],
            r['introduced_generation'],flags))
    assert all(len(x)==rs for x in records)
    gen2_snapshot=json.dumps(gen2,separators=(',',':'),ensure_ascii=True).encode()
    header=bytearray(hs); header[:8]=b'GPAR23\0\0'
    struct.pack_into('<HHHHHH',header,8,1,hs,rs,len(gen2),len(gen3_all),386)
    struct.pack_into('<IIII',header,0x20,hs,hs+rs*len(records),len(gen2_snapshot),0)
    header[0x40:0x60]=b'GEN2->GEN3 CUMULATIVE'.ljust(32,b'\0')
    payload=header+b''.join(records)+gen2_snapshot
    crc=zlib.crc32(payload)&0xffffffff
    struct.pack_into('<I',payload,0x2c,crc)
    outpath.parent.mkdir(parents=True,exist_ok=True); outpath.write_bytes(payload)
    return {'record_size':rs,'record_count':len(records),'gen2_native_count':len(gen2),'size':len(payload),'sha1':sha1(outpath),'crc32':f'{crc:08x}'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pokecrystal',type=Path,required=True)
    ap.add_argument('--pokeemerald',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    gen2=[]
    for p in sorted((a.pokecrystal/'data/pokemon/base_stats').glob('*.asm')):
        r=parse_gen2_file(p)
        if r: gen2.append(r)
    gen2.sort(key=lambda r:r['national_dex'])
    assert len(gen2)==100 and [r['national_dex'] for r in gen2]==list(range(152,252))
    gen3_all=parse_gen3_species_info(a.pokeemerald/'src/data/pokemon/species_info.h')
    assert len(gen3_all)==386 and [r['national_dex'] for r in gen3_all]==list(range(1,387))
    gen3_native=[r for r in gen3_all if r['national_dex']>=252]
    assert len(gen3_native)==135
    write_csv(gen2,a.out/'gen2_native_personal_152_251.csv',list(gen2[0].keys()))
    write_csv(gen3_native,a.out/'gen3_native_personal_252_386.csv',list(gen3_all[0].keys()))
    write_csv(gen3_all,a.out/'gen3_personal_overlay_001_386.csv',list(gen3_all[0].keys()))
    ability_rows=[{'ability_id':i,'identifier':n,'generation':3} for i,n in enumerate(GEN3_ABILITY_ORDER,1)]
    write_csv(ability_rows,a.out/'gen3_abilities_001_076.csv',['ability_id','identifier','generation'])
    nature_rows=[{'nature_id':i,'identifier':n.lower(),'up_stat':u or '','down_stat':d or '','generation':3} for i,(n,u,d) in enumerate(NATURES)]
    write_csv(nature_rows,a.out/'gen3_natures_25.csv',['nature_id','identifier','up_stat','down_stat','generation'])
    blockmeta=build_block(gen2,gen3_all,a.out/'green_gen2_gen3_parameter_layer.bin')
    manifest={
        'schema':'green-generation-parameter-stack-v1','order':['GEN1_GREEN','GEN2_CRYSTAL','GEN3_EMERALD'],
        'canonical_species_max_after_gen3':386,
        'gen2_native_species':100,'gen3_native_species':135,'gen3_overlay_species':386,
        'gen2_source':{'repo':'pret/pokecrystal','commit':repo_sha(a.pokecrystal)},
        'gen3_source':{'repo':'pret/pokeemerald','commit':repo_sha(a.pokeemerald)},
        'parameter_block':blockmeta,
        'rules':{
            'gen2':['six_stats','steel_dark','held_items','gender','friendship','breeding','egg_groups','hatch_cycles','growth_rate'],
            'gen3':['abilities','natures','six_independent_ivs','six_ev_yields','new_ev_cap_model','double_battle_ready_personal_schema','erratic_fluctuating_growth_support']
        }
    }
    (a.out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
