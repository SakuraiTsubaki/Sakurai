# Stage 2 extension. Running this script imports and executes build_stage2.py first.
import build_stage2 as base
from build_stage2 import *

# ---------- battle sprite slot census (6 members per Pokémon/form slot) ----------
sprite_paths = {
    'Diamond_USA': 'poketool/pokegra/pokegra.narc',
    'Pearl_USA': 'poketool/pokegra/pokegra.narc',
    'Platinum_KOR': 'poketool/pokegra/pl_pokegra.narc',
    'HeartGold_KOR': 'a/0/0/4',
    'SoulSilver_KOR': 'a/0/0/4',
}
sprite_rows = []
sprite_group_hashes = {}
for rn, p in sprite_paths.items():
    ms = R[rn].narc_members(p)
    if len(ms) % 6 != 0:
        raise ValueError((rn, p, 'sprite member count not divisible by 6', len(ms)))
    groups = []
    for slot in range(len(ms) // 6):
        g = ms[slot * 6:(slot + 1) * 6]
        group_sha1 = hashlib.sha1(b''.join(g)).hexdigest()
        groups.append(group_sha1)
        sprite_rows.append({
            'rom': rn, 'path': p, 'sprite_slot': slot, 'group_sha1': group_sha1,
            'm0_sha1': hashlib.sha1(g[0]).hexdigest(), 'm1_sha1': hashlib.sha1(g[1]).hexdigest(),
            'm2_sha1': hashlib.sha1(g[2]).hexdigest(), 'm3_sha1': hashlib.sha1(g[3]).hexdigest(),
            'palette0_sha1': hashlib.sha1(g[4]).hexdigest(), 'palette1_sha1': hashlib.sha1(g[5]).hexdigest(),
        })
    sprite_group_hashes[rn] = groups
pd.DataFrame(sprite_rows).to_csv(OUT / 'battle_sprite_slots.csv', index=False)

def compare_slot_hashes(left, right):
    a = sprite_group_hashes[left]
    b = sprite_group_hashes[right]
    n = min(len(a), len(b))
    dif = [i for i in range(n) if a[i] != b[i]]
    return {'slots_compared': n, 'different_slots': len(dif), 'same_slots': n - len(dif), 'different_indices': dif}

sprite_comparisons = {
    'Diamond_USA_vs_Pearl_USA': compare_slot_hashes('Diamond_USA', 'Pearl_USA'),
    'Diamond_USA_vs_Platinum_KOR': compare_slot_hashes('Diamond_USA', 'Platinum_KOR'),
    'Platinum_KOR_vs_HeartGold_KOR': compare_slot_hashes('Platinum_KOR', 'HeartGold_KOR'),
    'HeartGold_KOR_vs_SoulSilver_KOR': compare_slot_hashes('HeartGold_KOR', 'SoulSilver_KOR'),
}
json.dump(sprite_comparisons, open(OUT / 'battle_sprite_comparisons.json', 'w'), indent=2, ensure_ascii=False)

# ---------- compact cross-generation findings ----------
def compact_member_diff(rn1, p1, rn2, p2):
    a = R[rn1].narc_members(p1)
    b = R[rn2].narc_members(p2)
    n = min(len(a), len(b))
    dif = [i for i in range(n) if a[i] != b[i]]
    return {'common': n, 'diff': len(dif), 'indices': dif, 'extra_left': max(0, len(a)-n), 'extra_right': max(0, len(b)-n)}

key_findings = {
    'learnset_diffs': {
        'DP_vs_Pt': compact_member_diff('Diamond_USA', learn_paths['Diamond_USA'], 'Platinum_KOR', learn_paths['Platinum_KOR']),
        'Pt_vs_HGSS': compact_member_diff('Platinum_KOR', learn_paths['Platinum_KOR'], 'HeartGold_KOR', learn_paths['HeartGold_KOR']),
    },
    'message_bank_diffs': {},
    'battle_sprite_slots': sprite_comparisons,
}

def same_diff_counts(rn1, p1, rn2, p2):
    a = R[rn1].narc_members(p1); b = R[rn2].narc_members(p2); n = min(len(a), len(b))
    same = sum(a[i] == b[i] for i in range(n))
    return {'common': n, 'same': same, 'diff': n-same, 'extra_left': max(0,len(a)-n), 'extra_right': max(0,len(b)-n)}

key_findings['message_bank_diffs'] = {
    'Pt_legacy_vs_HGSS_pbr': same_diff_counts('Platinum_KOR','msgdata/msg.narc','HeartGold_KOR','pbr/msg.narc'),
    'Pt_active_vs_HGSS_active': same_diff_counts('Platinum_KOR','msgdata/pl_msg.narc','HeartGold_KOR','a/0/2/7'),
    'HG_vs_SS_active': same_diff_counts('HeartGold_KOR','a/0/2/7','SoulSilver_KOR','a/0/2/7'),
}
json.dump(key_findings, open(OUT / 'key_findings.json', 'w'), indent=2, ensure_ascii=False)

readme = (OUT / 'README.md').read_text(encoding='utf-8')
extra = '''

## Additional cross-generation findings

- D/P main battle-sprite archive: 494 six-member slots; Diamond and Pearl differ in 0 slots.
- Diamond -> Platinum changes 494 of 494 sprite slot groups at the binary level.
- Platinum -> HGSS changes 264 of 494 sprite slot groups; 230 remain identical.
- HeartGold and SoulSilver main battle-sprite slot groups are byte-identical across all 494 slots.
- D/P -> Platinum: 81 of the 501 shared level-up learnset slots change, plus 7 extra Platinum slots. Platinum -> HGSS: 14 of 508 learnset slots change.
- Platinum legacy DP message archive and HGSS pbr legacy archive are byte-identical across all 612 banks. HG/SS active message archives are byte-identical across all 822 banks.
'''
if '## Additional cross-generation findings' not in readme:
    (OUT / 'README.md').write_text(readme + extra, encoding='utf-8')

manifest = []
for p in sorted(OUT.iterdir()):
    if p.is_file():
        b = p.read_bytes()
        manifest.append({'file': p.name, 'size': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
json.dump(manifest, open(OUT / 'ARTIFACT_MANIFEST.json', 'w'), indent=2)
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file():
            z.write(p, arcname=p.name)
print('Stage2 extension complete:', OUT, zpath)
