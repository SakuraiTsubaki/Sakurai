from pathlib import Path
import csv, itertools

ROOT=Path('/mnt/data')
WORK=ROOT/'crystal_work'
ROMS={
'JP0': ROOT/'Pocket Monsters - Crystal Version (Japan).gbc',
'EN0': ROOT/'Pokemon - Crystal Version (USA, Europe).gbc',
'EN1': ROOT/'Pokemon - Crystal Version (USA, Europe) (Rev A).gbc',
'ES0': ROOT/'Pokemon - Edicion Cristal (Spain).gbc',
'DE0': ROOT/'Pokemon - Kristall-Edition (Germany).gbc',
'FR0': ROOT/'Pokemon - Version Cristal (France).gbc',
'IT0': ROOT/'Pokemon - Versione Cristallo (Italy).gbc',
}
BANK=0x4000
raw={k:p.read_bytes() for k,p in ROMS.items()}
with open(WORK/'bank_diff_matrix.csv',encoding='utf-8',newline='') as f:
    base=list(csv.DictReader(f))

def diff(a,b,bank):
    s=bank*BANK;e=s+BANK
    return sum(x!=y for x,y in zip(raw[a][s:e],raw[b][s:e]))

def classify(label, bank):
    if bank in (0x75,0x76,0x79): return 'map-script (EU relocation)'
    if bank==0x7A: return 'unused/zero'
    l=label.lower()
    if 'map script' in l: return 'map-script'
    if 'map block' in l: return 'map-block'
    if 'pokedex entries' in l: return 'text/dex'
    if 'text' in l: return 'text'
    if 'pic' in l or 'sprite' in l or 'font' in l or 'gfx' in l or 'tileset' in l or 'roof' in l: return 'graphics/data'
    if 'song' in l or 'audio' in l or 'sound' in l or 'cries' in l: return 'audio'
    if 'mobile' in l or 'battle tower' in l or 'crystal events' in l or 'stadium' in l: return 'mobile/special'
    if 'battle' in l or 'effect' in l or 'enemy trainers' in l: return 'battle/code-data'
    if 'phone' in l: return 'phone/script-text'
    if 'unmapped' in l: return 'unmapped'
    return 'engine/mixed'

special={0x75:'Map Scripts 26 (ES/FR exact; DE/IT EU-localized)',0x76:'Map Scripts 27 (ES/FR exact; DE/IT EU-localized)',0x79:'Map Scripts 28 (ES/FR exact; DE/IT EU-localized)',0x7A:'Unused / all-zero in all seven ROMs'}
anchors=['EN0','JP0','ES0','FR0']
out=[]
for r in base:
    b=int(r['bank'],16)
    label=special.get(b,r['semantic_label_en'])
    nearest={}
    for target in ['DE0','IT0']:
        vals=[(diff(target,a,b),a) for a in anchors]
        vals.sort()
        nearest[target]=vals
    def fmt_near(target):
        d,a=nearest[target][0]
        ties=[x for x in nearest[target] if x[0]==d]
        names='/'.join(x[1] for x in ties)
        return f'{names} ({d} bytes)'
    same_pairs=[]
    for a,c in itertools.combinations(ROMS,2):
        if diff(a,c,b)==0: same_pairs.append((a,c))
    all7=all(diff('EN0',k,b)==0 for k in ROMS if k!='EN0')
    eu_extra = b in (0x75,0x76,0x79)
    enrev=diff('EN0','EN1',b)
    de_exact=[a for a in anchors if diff('DE0',a,b)==0]
    it_exact=[a for a in anchors if diff('IT0',a,b)==0]
    if all7:
        status='Shared byte-identical across all 7; semantic lift once.'
    elif b==0x7A:
        status='All-zero unused bank.'
    elif eu_extra:
        status='EU-only map-script expansion; ES/FR exact source anchors, DE/IT need symbol/address lifting.'
    else:
        bits=[]
        if enrev: bits.append(f'EN Rev0→RevA changes: {enrev} B')
        bits.append('DE '+('exact '+','.join(de_exact) if de_exact else 'reconstruct'))
        bits.append('IT '+('exact '+','.join(it_exact) if it_exact else 'reconstruct'))
        status='; '.join(bits)+'.'
    if b in (0x75,0x76,0x79): priority='A'
    elif enrev: priority='A' if enrev>=64 else 'B'
    elif all7: priority='D'
    elif de_exact and it_exact: priority='D'
    else:
        cls=classify(label,b)
        priority='B' if cls in {'map-script','phone/script-text','text','text/dex','engine/mixed','battle/code-data','mobile/special'} else 'C'
    out.append({
        'bank':f'{b:02X}','semantic_role':label,'class':classify(label,b),
        'all7_identical':'yes' if all7 else 'no','en_rev_diff_bytes':enrev,
        'de_nearest_anchor':fmt_near('DE0'),'it_nearest_anchor':fmt_near('IT0'),
        'priority':priority,'status':status,
    })

with open(WORK/'semantic_bank_status.csv','w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)

from collections import Counter
classes=Counter(x['class'] for x in out)
pri=Counter(x['priority'] for x in out)
all7=[x['bank'] for x in out if x['all7_identical']=='yes']
rev=[x for x in out if x['en_rev_diff_bytes']]

def rows_for(start,end):
    lines=[]
    for x in out[start:end]:
        lines.append(f"|{x['bank']}|{x['semantic_role']}|{x['class']}|{x['en_rev_diff_bytes']}|{x['de_nearest_anchor']}|{x['it_nearest_anchor']}|{x['priority']}|")
    return '\n'.join(lines)

md=[]
md.append('# Pokémon Crystal 7-ROM Semantic Bank Census')
md.append('')
md.append('This is the second-pass bank census: it keeps the 128-bank byte survey, but adds semantic role, reconstruction status, nearest exact-source anchor for German/Italian, and work priority. English roles are anchored to pret/pokecrystal; Japanese to PikalaxALT/pokekuristaru; Spanish to erosunica/pokecrystal-es; French to qwilvove/pokecrystal-fr. Banks 75/76/79 are confirmed EU map-script expansions from the exact Spanish and French layouts.')
md.append('')
md.append('## Executive findings')
md.append('')
md.append(f'- 128 banks × 7 ROMs = 896 bank images surveyed.')
md.append(f'- All-seven byte-identical banks ({len(all7)}): ' + ', '.join(all7))
md.append(f'- English Rev0→RevA changed banks ({len(rev)}): ' + ', '.join(f"{x['bank']}({x['en_rev_diff_bytes']}B)" for x in rev))
md.append('- EU-only expansion: 75 = Map Scripts 26, 76 = Map Scripts 27, 79 = Map Scripts 28; 7A is all-zero in all seven.')
md.append('- DE/IT have no exact semantic source repository confirmed in this survey, so per-bank nearest-anchor matching is used to prioritize reconstruction.')
md.append('- Priority: A = relocation/revision-critical; B = code/script/text semantic reconstruction; C = graphics/audio/data alignment; D = byte-identical or directly reusable structure.')
md.append('')
md.append('## Class counts')
md.append('')
for k,v in sorted(classes.items()): md.append(f'- {k}: {v}')
md.append('')
md.append('## Full 00–7F status')
md.append('')
md.append('|Bank|Semantic role|Class|EN0→EN1 diff|DE nearest exact-source anchor|IT nearest exact-source anchor|Priority|')
md.append('|---:|---|---|---:|---|---|:---:|')
md.append(rows_for(0,128))
md.append('')
md.append('## Interpretation')
md.append('')
md.append('A nearest-anchor byte count is not a claim that the target bank is derived from that language; it is a reconstruction heuristic. Exact source repos provide semantic boundaries and labels, while local DE/IT ROM bytes remain the authority for their final addresses and content.')
md.append('')
md.append('The next deep pass should begin with Bank 00 (vectors/header/home code) and, in parallel, Banks 75/76/79 because they expose the European relocation model needed to understand later pointer movement.')
(WORK/'SEMANTIC_BANK_CENSUS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

print('wrote',WORK/'semantic_bank_status.csv')
print('wrote',WORK/'SEMANTIC_BANK_CENSUS.md')
print('priorities',dict(pri))
print('classes',dict(classes))
print('all7',all7)
print('rev',[(x['bank'],x['en_rev_diff_bytes']) for x in rev])
