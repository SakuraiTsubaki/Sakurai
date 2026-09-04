from pathlib import Path
import pandas as pd, struct, hashlib, json, zipfile, collections

BASE = Path('/mnt/data')
ST1 = BASE / 'gen4_census'
OUT = BASE / 'gen4_census_stage2'
OUT.mkdir(exist_ok=True)

ROMS = {
    'Diamond_USA': BASE / 'Pokemon_Diamond_USA_NDS-LGC.nds',
    'Pearl_USA': BASE / 'Pokemon_Pearl_USA_NDS-LGC.nds',
    'Platinum_KOR': BASE / '포켓몬스터Pt 기라티나.nds',
    'HeartGold_KOR': BASE / '포켓몬스터 하트골드.nds',
    'SoulSilver_KOR': BASE / '포켓몬스터 소울실버.nds',
}


class Rom:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.data = path.read_bytes()
        self.files = pd.read_csv(ST1 / f'{name}_files.csv')

    def outer(self, path):
        m = self.files[self.files.path == path]
        if len(m) != 1:
            raise KeyError((self.name, path, len(m)))
        r = m.iloc[0]
        return self.data[int(r.start):int(r.end)]

    def narc_members(self, path):
        b = self.outer(path)
        if b[:4] != b'NARC':
            raise ValueError((self.name, path, b[:4]))
        count = struct.unpack_from('<H', b, 0x18)[0]
        gi = b.find(b'GMIF')
        if gi < 0:
            raise ValueError('GMIF')
        base = gi + 8
        out = []
        for i in range(count):
            a, z = struct.unpack_from('<II', b, 0x1C + 8 * i)
            out.append(b[base + a:base + z])
        return out


R = {k: Rom(k, v) for k, v in ROMS.items()}

# Level-up learnsets: move bits 0-8, level bits 9-15, 0xFFFF terminator.
learn_paths = {
    'Diamond_USA': 'poketool/personal/wotbl.narc',
    'Pearl_USA': 'poketool/personal/wotbl.narc',
    'Platinum_KOR': 'poketool/personal/wotbl.narc',
    'HeartGold_KOR': 'a/0/3/3',
    'SoulSilver_KOR': 'a/0/3/3',
}
learn_rows = []
learn_summary = {}
for rn, p in learn_paths.items():
    members = R[rn].narc_members(p)
    total = 0
    invalid = []
    max_moves = 0
    for slot, b in enumerate(members):
        vals = list(struct.unpack('<' + 'H' * (len(b) // 2), b))
        decoded = []
        terminated = False
        for j, v in enumerate(vals):
            if v == 0xFFFF:
                terminated = True
                break
            level = (v & 0xFE00) >> 9
            move = v & 0x01FF
            if level > 100 or move > 467:
                invalid.append((slot, j, v, level, move))
            decoded.append((level, move, v))
            learn_rows.append({'rom': rn, 'slot': slot, 'entry_index': j, 'level': level, 'move_id': move, 'packed': v})
        total += len(decoded)
        max_moves = max(max_moves, len(decoded))
        if not terminated:
            invalid.append((slot, 'no_term', len(b)))
    learn_summary[rn] = {
        'slots': len(members),
        'total_levelup_entries': total,
        'max_entries_per_slot': max_moves,
        'validation_issues': len(invalid),
    }
pd.DataFrame(learn_rows).to_csv(OUT / 'levelup_learnsets.csv', index=False)

slot_rows = []
for rn, p in learn_paths.items():
    for slot, b in enumerate(R[rn].narc_members(p)):
        vals = struct.unpack('<' + 'H' * (len(b) // 2), b)
        n = next((i for i, v in enumerate(vals) if v == 0xFFFF), len(vals))
        pairs = [(int((v & 0xFE00) >> 9), int(v & 0x1FF)) for v in vals[:n]]
        slot_rows.append({
            'rom': rn,
            'slot': slot,
            'entry_count': len(pairs),
            'raw_size': len(b),
            'sha1': hashlib.sha1(b).hexdigest(),
            'learnset': json.dumps(pairs, separators=(',', ':')),
        })
pd.DataFrame(slot_rows).to_csv(OUT / 'levelup_learnsets_by_slot.csv', index=False)

# Trainer headers and game-specific trainer-party formats.
trainer_paths = {
    'Diamond_USA': ('poketool/trainer/trdata.narc', 'poketool/trainer/trpoke.narc'),
    'Pearl_USA': ('poketool/trainer/trdata.narc', 'poketool/trainer/trpoke.narc'),
    'Platinum_KOR': ('poketool/trainer/trdata.narc', 'poketool/trainer/trpoke.narc'),
    'HeartGold_KOR': ('a/0/5/5', 'a/0/5/6'),
    'SoulSilver_KOR': ('a/0/5/5', 'a/0/5/6'),
}
tr_rows = []
mon_rows = []
tr_summary = {}
for rn, (tdp, tpp) in trainer_paths.items():
    tds = R[rn].narc_members(tdp)
    tps = R[rn].narc_members(tpp)
    assert len(tds) == len(tps)
    type_counts = collections.Counter()
    party_sizes = collections.Counter()
    form_count = custom_moves = held_items = 0
    mismatches = []
    for tid, (td, tp) in enumerate(zip(tds, tps)):
        if len(td) < 20:
            mismatches.append((tid, 'trdata_short', len(td)))
            continue
        typ, cls, unk, npoke = struct.unpack_from('<BBBB', td, 0)
        items = list(struct.unpack_from('<HHHH', td, 4))
        ai, double = struct.unpack_from('<II', td, 12)
        type_counts[typ] += 1
        party_sizes[npoke] += 1
        tr_rows.append({
            'rom': rn, 'trainer_id': tid, 'trainer_type': typ, 'trainer_class': cls,
            'unk2': unk, 'party_count': npoke, 'item1': items[0], 'item2': items[1],
            'item3': items[2], 'item4': items[3], 'ai_flags': ai, 'double_battle': double,
            'trdata_sha1': hashlib.sha1(td).hexdigest(), 'trpoke_sha1': hashlib.sha1(tp).hexdigest(),
            'trpoke_size': len(tp),
        })
        if rn in ('Diamond_USA', 'Pearl_USA'):
            rec_size = {0: 6, 1: 14, 2: 8, 3: 16}.get(typ)
            variant = 'dp'
        elif rn == 'Platinum_KOR':
            rec_size = {0: 8, 1: 16, 2: 10, 3: 18}.get(typ)
            variant = 'pt'
        else:
            rec_size = {0: 8, 1: 16, 2: 10, 3: 18}.get(typ)
            variant = 'hgss'
        if rec_size is None:
            mismatches.append((tid, 'unknown_type', typ))
            continue
        need = rec_size * npoke
        if npoke and len(tp) < need:
            mismatches.append((tid, 'short_party', len(tp), need))
            continue
        off = 0
        for pi in range(npoke):
            if variant == 'hgss':
                diff = tp[off]
                override = tp[off + 1]
                level = struct.unpack_from('<H', tp, off + 2)[0]
                packed = struct.unpack_from('<H', tp, off + 4)[0]
                iv_scale = None
            else:
                iv_scale, level, packed = struct.unpack_from('<HHH', tp, off)
                diff = override = None
            species = packed & 0x03FF
            form = (packed >> 10) & 0x3F
            o = off + 6
            item = 0
            moves = [0, 0, 0, 0]
            if typ in (2, 3):
                item = struct.unpack_from('<H', tp, o)[0]
                o += 2
                held_items += int(item != 0)
            if typ in (1, 3):
                moves = list(struct.unpack_from('<HHHH', tp, o))
                o += 8
                custom_moves += sum(1 for x in moves if x)
            capsule = struct.unpack_from('<H', tp, o)[0] if variant != 'dp' else 0
            form_count += int(form != 0)
            mon_rows.append({
                'rom': rn, 'trainer_id': tid, 'party_index': pi, 'trainer_type': typ,
                'iv_scale': iv_scale, 'difficulty': diff, 'gender_ability_override': override,
                'level': level, 'species_id': species, 'form': form, 'held_item': item,
                'move1': moves[0], 'move2': moves[1], 'move3': moves[2], 'move4': moves[3],
                'capsule': capsule,
            })
            off += rec_size
    tr_summary[rn] = {
        'trainers': len(tds), 'trainer_type_counts': dict(sorted(type_counts.items())),
        'party_size_counts': dict(sorted(party_sizes.items())),
        'party_mons': sum(k * v for k, v in party_sizes.items()),
        'nonzero_form_mons': form_count, 'explicit_custom_move_slots': custom_moves,
        'held_item_mons': held_items, 'validation_issues': len(mismatches),
    }
pd.DataFrame(tr_rows).to_csv(OUT / 'trainers.csv', index=False)
pd.DataFrame(mon_rows).to_csv(OUT / 'trainer_parties.csv', index=False)

# DPPt 424-byte encounter records.
def parse_dppt_enc(b):
    if len(b) != 424:
        raise ValueError(len(b))
    row = {'walk_rate': struct.unpack_from('<I', b, 0)[0]}
    for i in range(12):
        row[f'land{i+1}_level'] = struct.unpack_from('<I', b, 4 + i * 8)[0]
        row[f'land{i+1}_species'] = struct.unpack_from('<I', b, 8 + i * 8)[0]
    names = ['morning1','morning2','day1','day2','night1','night2','radar1','radar2','radar3','radar4','unknown1','unknown2','unknown3','unknown4','unknown5','unknown6','ruby1','ruby2','sapphire1','sapphire2','emerald1','emerald2','firered1','firered2','leafgreen1','leafgreen2']
    for j, n in enumerate(names):
        row[n] = struct.unpack_from('<I', b, 100 + j * 4)[0]
    row['surf_rate'] = struct.unpack_from('<I', b, 204)[0]
    for i in range(5):
        off = 208 + i * 8
        row[f'surf{i+1}_max'] = b[off]
        row[f'surf{i+1}_min'] = b[off + 1]
        row[f'surf{i+1}_species'] = struct.unpack_from('<I', b, off + 4)[0]
    for mode, rateoff, slotoff in [('oldrod',292,296),('goodrod',336,340),('superrod',380,384)]:
        row[f'{mode}_rate'] = struct.unpack_from('<I', b, rateoff)[0]
        for i in range(5):
            off = slotoff + i * 8
            row[f'{mode}{i+1}_max'] = b[off]
            row[f'{mode}{i+1}_min'] = b[off + 1]
            row[f'{mode}{i+1}_species'] = struct.unpack_from('<I', b, off + 4)[0]
    return row

# HGSS 196-byte EncounterData records.
def parse_hgss_enc(b):
    if len(b) != 196:
        raise ValueError(len(b))
    r = {}
    rates = struct.unpack_from('<BBBBBB', b, 0)
    for n, v in zip(['walk_rate','surf_rate','rocksmash_rate','oldrod_rate','goodrod_rate','superrod_rate'], rates):
        r[n] = v
    levels = list(b[8:20])
    morn = struct.unpack_from('<12H', b, 20)
    day = struct.unpack_from('<12H', b, 44)
    nite = struct.unpack_from('<12H', b, 68)
    for i in range(12):
        r[f'land{i+1}_level'] = levels[i]
        r[f'land{i+1}_morn'] = morn[i]
        r[f'land{i+1}_day'] = day[i]
        r[f'land{i+1}_nite'] = nite[i]
    hs = struct.unpack_from('<2H', b, 92)
    ss = struct.unpack_from('<2H', b, 96)
    for i, x in enumerate(hs): r[f'hoenn_sound{i+1}'] = x
    for i, x in enumerate(ss): r[f'sinnoh_sound{i+1}'] = x
    def slots(base, n, prefix):
        for i in range(n):
            mn, mx, sp = struct.unpack_from('<BBH', b, base + 4 * i)
            r[f'{prefix}{i+1}_min'] = mn
            r[f'{prefix}{i+1}_max'] = mx
            r[f'{prefix}{i+1}_species'] = sp
    slots(100, 5, 'surf')
    slots(120, 2, 'rocksmash')
    slots(128, 5, 'oldrod')
    slots(148, 5, 'goodrod')
    slots(168, 5, 'superrod')
    r['land_swarm'], r['surf_swarm'], r['night_fish'], r['fish_swarm'] = struct.unpack_from('<4H', b, 188)
    return r

enc_specs = [
    ('Diamond_USA','diamond','fielddata/encountdata/d_enc_data.narc','dppt'),
    ('Diamond_USA','pearl_embedded','fielddata/encountdata/p_enc_data.narc','dppt'),
    ('Pearl_USA','diamond_embedded','fielddata/encountdata/d_enc_data.narc','dppt'),
    ('Pearl_USA','pearl','fielddata/encountdata/p_enc_data.narc','dppt'),
    ('Platinum_KOR','diamond_embedded','fielddata/encountdata/d_enc_data.narc','dppt'),
    ('Platinum_KOR','pearl_embedded','fielddata/encountdata/p_enc_data.narc','dppt'),
    ('Platinum_KOR','platinum','fielddata/encountdata/pl_enc_data.narc','dppt'),
    ('HeartGold_KOR','gold','a/0/3/7','hgss'), ('HeartGold_KOR','silver_embedded','a/1/3/6','hgss'),
    ('SoulSilver_KOR','gold_embedded','a/0/3/7','hgss'), ('SoulSilver_KOR','silver','a/1/3/6','hgss'),
]
enc_rows = []
enc_summary = {}
for rn, label, p, fmt in enc_specs:
    ms = R[rn].narc_members(p)
    nonzero = 0
    species = set()
    for idx, b in enumerate(ms):
        d = parse_dppt_enc(b) if fmt == 'dppt' else parse_hgss_enc(b)
        enc_rows.append({'rom': rn, 'archive_role': label, 'path': p, 'location_index': idx, **d})
        if d['walk_rate'] or d.get('surf_rate', 0) or d.get('oldrod_rate', 0):
            nonzero += 1
        if fmt == 'dppt':
            vals = [d[f'land{i}_species'] for i in range(1, 13)]
            vals += [d[n] for n in ['morning1','morning2','day1','day2','night1','night2','radar1','radar2','radar3','radar4','ruby1','ruby2','sapphire1','sapphire2','emerald1','emerald2','firered1','firered2','leafgreen1','leafgreen2']]
            vals += [d[f'surf{i}_species'] for i in range(1, 6)]
            for mode in ['oldrod','goodrod','superrod']:
                vals += [d[f'{mode}{i}_species'] for i in range(1, 6)]
        else:
            vals = [d[f'land{i}_{tod}'] for i in range(1, 13) for tod in ['morn','day','nite']]
            vals += [d[f'hoenn_sound{i}'] for i in range(1,3)] + [d[f'sinnoh_sound{i}'] for i in range(1,3)]
            vals += [d[f'surf{i}_species'] for i in range(1,6)] + [d[f'rocksmash{i}_species'] for i in range(1,3)]
            for mode in ['oldrod','goodrod','superrod']:
                vals += [d[f'{mode}{i}_species'] for i in range(1,6)]
            vals += [d['land_swarm'], d['surf_swarm'], d['night_fish'], d['fish_swarm']]
        species.update(int(v) for v in vals if isinstance(v, (int, float)) and 0 < int(v) <= 1023)
    enc_summary[f'{rn}:{label}'] = {
        'locations': len(ms), 'nonzero_locations': nonzero, 'unique_species_ids': len(species),
        'min_species': min(species) if species else 0, 'max_species': max(species) if species else 0,
    }
pd.DataFrame(enc_rows).to_csv(OUT / 'wild_encounters.csv', index=False)

# Message MAT decryption. This mirrors Gen IV game code.
def parse_msg_member(b):
    if len(b) < 4:
        return {'valid': False, 'reason': 'short'}
    count, key = struct.unpack_from('<HH', b, 0)
    if 4 + 8 * count > len(b):
        return {'valid': False, 'reason': 'table_overflow', 'count': count, 'key': key}
    messages = []
    for i in range(count):
        off_enc, len_enc = struct.unpack_from('<II', b, 4 + 8 * i)
        seed = (key * 765 * (i + 1)) & 0xFFFF
        seed32 = seed | (seed << 16)
        off = off_enc ^ seed32
        ln = len_enc ^ seed32
        if off > len(b) or ln > 0x100000 or off + ln * 2 > len(b):
            return {'valid': False, 'reason': 'entry_oob', 'count': count, 'key': key, 'bad_index': i}
        vals = list(struct.unpack_from('<' + 'H' * ln, b, off)) if ln else []
        s = ((i + 1) * 596947) & 0xFFFF
        for j in range(len(vals)):
            vals[j] ^= s
            s = (s + 18749) & 0xFFFF
        messages.append(vals)
    return {'valid': True, 'count': count, 'key': key, 'messages': messages}

msg_specs = [
    ('Diamond_USA','active','msgdata/msg.narc'), ('Pearl_USA','active','msgdata/msg.narc'),
    ('Platinum_KOR','legacy_dp','msgdata/msg.narc'), ('Platinum_KOR','active','msgdata/pl_msg.narc'),
    ('HeartGold_KOR','active','a/0/2/7'), ('HeartGold_KOR','legacy_pbr','pbr/msg.narc'),
    ('SoulSilver_KOR','active','a/0/2/7'), ('SoulSilver_KOR','legacy_pbr','pbr/msg.narc'),
]
msg_bank_rows = []
msg_rows = []
msg_summary = {}
for rn, role, p in msg_specs:
    members = R[rn].narc_members(p)
    valid_banks = total_msgs = total_u16 = 0
    bad = []
    for bank, b in enumerate(members):
        x = parse_msg_member(b)
        if not x['valid']:
            bad.append((bank, x))
            msg_bank_rows.append({'rom':rn,'role':role,'path':p,'bank':bank,'valid':False,'raw_size':len(b),'sha1':hashlib.sha1(b).hexdigest()})
            continue
        valid_banks += 1
        total_msgs += x['count']
        bank_u16 = sum(len(v) for v in x['messages'])
        total_u16 += bank_u16
        msg_bank_rows.append({'rom':rn,'role':role,'path':p,'bank':bank,'valid':True,'raw_size':len(b),'sha1':hashlib.sha1(b).hexdigest(),'message_count':x['count'],'key':x['key'],'total_u16':bank_u16})
        for mi, vals in enumerate(x['messages']):
            raw = struct.pack('<' + 'H' * len(vals), *vals) if vals else b''
            ctrls = sum(1 for v in vals if v >= 0xE000 or v in (0xFFFE, 0xFFFF))
            msg_rows.append({'rom':rn,'role':role,'bank':bank,'message_index':mi,'u16_length':len(vals),'plaintext_sha1':hashlib.sha1(raw).hexdigest(),'first_u16_hex':' '.join(f'{v:04X}' for v in vals[:12]),'last_u16':f'{vals[-1]:04X}' if vals else '','controlish_count':ctrls,'max_u16':max(vals) if vals else 0})
    msg_summary[f'{rn}:{role}'] = {'banks':len(members),'valid_banks':valid_banks,'total_messages':total_msgs,'total_u16_units':total_u16,'invalid_banks':len(bad)}
pd.DataFrame(msg_bank_rows).to_csv(OUT / 'message_banks.csv', index=False)
pd.DataFrame(msg_rows).to_csv(OUT / 'message_entries.csv', index=False)

# Core field archives.
inv_specs = {
    'Diamond_USA': {'scripts':'fielddata/script/scr_seq_release.narc','events':'fielddata/eventdata/zone_event_release.narc','mapmatrix':'fielddata/mapmatrix/map_matrix.narc','land':'fielddata/land_data/land_data_release.narc'},
    'Pearl_USA': {'scripts':'fielddata/script/scr_seq_release.narc','events':'fielddata/eventdata/zone_event_release.narc','mapmatrix':'fielddata/mapmatrix/map_matrix.narc','land':'fielddata/land_data/land_data_release.narc'},
    'Platinum_KOR': {'scripts':'fielddata/script/scr_seq.narc','events':'fielddata/eventdata/zone_event.narc','mapmatrix':'fielddata/mapmatrix/map_matrix.narc','land':'fielddata/land_data/land_data.narc'},
    'HeartGold_KOR': {'scripts':'a/0/1/2','events':'a/0/3/2','mapmatrix':'a/0/4/1','land':'a/0/6/5'},
    'SoulSilver_KOR': {'scripts':'a/0/1/2','events':'a/0/3/2','mapmatrix':'a/0/4/1','land':'a/0/6/5'},
}
inv_rows = []
inv_summary = {}
for rn, cats in inv_specs.items():
    inv_summary[rn] = {}
    for cat, p in cats.items():
        ms = R[rn].narc_members(p)
        sizes = [len(x) for x in ms]
        inv_summary[rn][cat] = {'path':p,'members':len(ms),'total_payload_bytes':sum(sizes),'min_size':min(sizes),'max_size':max(sizes),'zero_size':sum(s == 0 for s in sizes),'unique_sha1':len({hashlib.sha1(x).digest() for x in ms})}
        for i, b in enumerate(ms):
            inv_rows.append({'rom':rn,'category':cat,'path':p,'member_index':i,'size':len(b),'sha1':hashlib.sha1(b).hexdigest(),'first4':b[:4].hex().upper()})
pd.DataFrame(inv_rows).to_csv(OUT / 'map_script_event_land_members.csv', index=False)

# Stage 1 NARC-member signature census and font members.
members_df = pd.read_csv(ST1 / 'all_narc_members.csv')
magic_summary = members_df.groupby(['rom','magic'], dropna=False).agg(members=('member_index','count'), bytes=('size','sum'), unique_sha1=('sha1','nunique')).reset_index()
magic_summary.to_csv(OUT / 'narc_member_magic_summary.csv', index=False)
font_specs = {
    'Diamond_USA':['graphic/font.narc'], 'Pearl_USA':['graphic/font.narc'],
    'Platinum_KOR':['graphic/font.narc','graphic/pl_font.narc'],
    'HeartGold_KOR':['a/0/1/6','pbr/font.narc'], 'SoulSilver_KOR':['a/0/1/6','pbr/font.narc'],
}
font_rows = []
for rn, paths in font_specs.items():
    for p in paths:
        for i, b in enumerate(R[rn].narc_members(p)):
            font_rows.append({'rom':rn,'path':p,'member_index':i,'size':len(b),'sha1':hashlib.sha1(b).hexdigest(),'magic':b[:4].hex().upper()})
pd.DataFrame(font_rows).to_csv(OUT / 'font_archive_members.csv', index=False)

# Exact member comparison helper.
def diff_members(rn1, p1, rn2, p2):
    a = R[rn1].narc_members(p1)
    b = R[rn2].narc_members(p2)
    n = min(len(a), len(b))
    dif = [i for i in range(n) if a[i] != b[i]]
    return {'left_count':len(a),'right_count':len(b),'common_count':n,'different_common_members':len(dif),'different_indices':dif,'extra_left':list(range(n,len(a))),'extra_right':list(range(n,len(b)))}

comparisons = {
    'Diamond_vs_Pearl_learnsets': diff_members('Diamond_USA', learn_paths['Diamond_USA'], 'Pearl_USA', learn_paths['Pearl_USA']),
    'Diamond_vs_Pearl_trainers': diff_members('Diamond_USA','poketool/trainer/trdata.narc','Pearl_USA','poketool/trainer/trdata.narc'),
    'Diamond_vs_Pearl_trainer_parties': diff_members('Diamond_USA','poketool/trainer/trpoke.narc','Pearl_USA','poketool/trainer/trpoke.narc'),
    'Diamond_vs_Pearl_messages': diff_members('Diamond_USA','msgdata/msg.narc','Pearl_USA','msgdata/msg.narc'),
    'HG_vs_SS_learnsets': diff_members('HeartGold_KOR','a/0/3/3','SoulSilver_KOR','a/0/3/3'),
    'HG_vs_SS_trainers': diff_members('HeartGold_KOR','a/0/5/5','SoulSilver_KOR','a/0/5/5'),
    'HG_vs_SS_trainer_parties': diff_members('HeartGold_KOR','a/0/5/6','SoulSilver_KOR','a/0/5/6'),
    'HG_vs_SS_messages': diff_members('HeartGold_KOR','a/0/2/7','SoulSilver_KOR','a/0/2/7'),
    'HG_vs_SS_gold_enc_archive': diff_members('HeartGold_KOR','a/0/3/7','SoulSilver_KOR','a/0/3/7'),
    'HG_vs_SS_silver_enc_archive': diff_members('HeartGold_KOR','a/1/3/6','SoulSilver_KOR','a/1/3/6'),
}
json.dump(comparisons, open(OUT / 'member_level_comparisons.json', 'w'), indent=2, ensure_ascii=False)

summary = {'learnsets':learn_summary,'trainers':tr_summary,'encounters':enc_summary,'messages':msg_summary,'map_script_event_land':inv_summary}
json.dump(summary, open(OUT / 'summary.json', 'w'), indent=2, ensure_ascii=False)

# Manifest and ZIP (analysis only; no ROM bytes).
manifest = []
for p in sorted(OUT.iterdir()):
    if p.is_file():
        b = p.read_bytes()
        manifest.append({'file':p.name,'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
json.dump(manifest, open(OUT / 'ARTIFACT_MANIFEST.json', 'w'), indent=2)

zpath = BASE / 'Generation_IV_ROM_Census_Stage2.zip'
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file():
            z.write(p, arcname=p.name)
print(json.dumps(summary, indent=2, ensure_ascii=False))
print('OUT', OUT, 'ZIP', zpath)
