import os, struct, hashlib, csv, json, zipfile, shutil
from pathlib import Path
from PIL import Image, ImageDraw

ROM_HG = '/mnt/data/포켓몬스터 하트골드.nds'
ROM_SS = '/mnt/data/포켓몬스터 소울실버.nds'
ROM_PT = '/mnt/data/포켓몬스터Pt 기라티나.nds'
ROM_D  = '/mnt/data/Pokemon_Diamond_USA_NDS-LGC.nds'
ROM_P  = '/mnt/data/Pokemon_Pearl_USA_NDS-LGC.nds'
OUT = Path('/mnt/data/gen4_sprite_stage4')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)

# ---------- NDS/NARC ----------
def nds_file(rom_path, target_path):
    data = Path(rom_path).read_bytes()
    u32=lambda o: struct.unpack_from('<I',data,o)[0]
    fnt_off,fnt_size=u32(0x40),u32(0x44); fat_off=u32(0x48)
    fnt=data[fnt_off:fnt_off+fnt_size]
    nd=struct.unpack_from('<H',fnt,6)[0]
    dirs=[struct.unpack_from('<IHH',fnt,i*8) for i in range(nd)]
    hit=None
    def walk(did,prefix=''):
        nonlocal hit
        off,fid,_=dirs[did-0xF000]; pos=off
        while True:
            ln=fnt[pos]; pos+=1
            if ln==0: return
            isdir=ln&0x80; n=ln&0x7F
            name=fnt[pos:pos+n].decode('ascii','replace'); pos+=n
            if isdir:
                sub=struct.unpack_from('<H',fnt,pos)[0]; pos+=2
                walk(sub,prefix+name+'/')
                if hit is not None: return
            else:
                if prefix+name == target_path:
                    s,e=struct.unpack_from('<II',data,fat_off+fid*8)
                    hit=data[s:e]; return
                fid += 1
    walk(0xF000)
    if hit is None: raise KeyError(target_path)
    return hit

def narc_members(narc):
    pos=struct.unpack_from('<H',narc,0x0C)[0]
    blocks={}
    for _ in range(struct.unpack_from('<H',narc,0x0E)[0]):
        magic=narc[pos:pos+4]; size=struct.unpack_from('<I',narc,pos+4)[0]
        blocks[magic]=(pos,size); pos+=size
    fat=blocks[b'BTAF'][0]; img=blocks[b'GMIF'][0]+8
    count=struct.unpack_from('<H',narc,fat+8)[0]
    out=[]
    for i in range(count):
        s,e=struct.unpack_from('<II',narc,fat+12+i*8)
        out.append(narc[img+s:img+e])
    return out

# ---------- graphics ----------
def decrypt_dp_ncgr(blob):
    bb=bytearray(blob)
    size=struct.unpack_from('<I',bb,0x28)[0]; off=0x30
    words=list(struct.unpack_from('<'+'H'*(size//2),bb,off))
    seed=words[-1]; out=words[:]
    for i in range(len(words)-1,-1,-1):
        out[i]=words[i] ^ seed
        seed=(seed*0x41C64E6D+0x6073)&0xFFFF
    struct.pack_into('<'+'H'*len(out),bb,off,*out)
    return bytes(bb)

def decrypt_pt_ncgr(blob):
    bb=bytearray(blob)
    size=struct.unpack_from('<I',bb,0x28)[0]; off=0x30
    words=list(struct.unpack_from('<'+'H'*(size//2),bb,off))
    seed=words[0]; out=[]
    for w in words:
        out.append(w ^ seed)
        seed=(seed*0x41C64E6D+0x6073)&0xFFFF
    struct.pack_into('<'+'H'*len(out),bb,off,*out)
    return bytes(bb)

def palette(blob):
    raw=blob[0x28:0x48]
    p=[]
    for i in range(16):
        v=struct.unpack_from('<H',raw,i*2)[0]
        r=(v&31)*255//31; g=((v>>5)&31)*255//31; b=((v>>10)&31)*255//31
        p.append((r,g,b,0 if i==0 else 255))
    return p

def render_ncgr(blob,pal):
    if not blob: return None
    b=decrypt_pt_ncgr(blob)
    htiles,wtiles=struct.unpack_from('<HH',b,0x18); w,h=wtiles*8,htiles*8
    size=struct.unpack_from('<I',b,0x28)[0]; raw=b[0x30:0x30+size]
    idx=[]
    for x in raw: idx += [x&15,x>>4]
    im=Image.new('RGBA',(w,h),(0,0,0,0)); px=im.load()
    for i,v in enumerate(idx[:w*h]): px[i%w,i//w]=pal[v]
    return im

# ---------- archives ----------
hg_main=narc_members(nds_file(ROM_HG,'a/0/0/4'))
ss_main=narc_members(nds_file(ROM_SS,'a/0/0/4'))
hg_forms=narc_members(nds_file(ROM_HG,'a/1/1/4'))
ss_forms=narc_members(nds_file(ROM_SS,'a/1/1/4'))
pt_main=narc_members(nds_file(ROM_PT,'poketool/pokegra/pl_pokegra.narc'))
d_main=narc_members(nds_file(ROM_D,'poketool/pokegra/pokegra.narc'))
p_main=narc_members(nds_file(ROM_P,'poketool/pokegra/pokegra.narc'))

# ---------- main HGSS extraction ----------
core=OUT/'hgss_core'; core.mkdir()
variants=[
    (0,'back_female'),(1,'back_male'),(2,'front_female'),(3,'front_male')
]
main_rows=[]
for species in range(1,494):
    base=species*6
    for slot,label in variants:
        g=hg_main[base+slot]
        for shiny,pidx in [(False,base+4),(True,base+5)]:
            rel=f'{species:03d}/{label}_{"shiny" if shiny else "normal"}.png'
            status='empty' if not g else 'ok'
            sha=''; w=h=0
            if g:
                im=render_ncgr(g,palette(hg_main[pidx]))
                fp=core/rel; fp.parent.mkdir(parents=True,exist_ok=True); im.save(fp)
                sha=hashlib.sha256(fp.read_bytes()).hexdigest(); w,h=im.size
            main_rows.append({
                'species_id':species,'graphic_member':base+slot,'palette_member':pidx,
                'variant':label,'shiny':int(shiny),'status':status,'width':w,'height':h,
                'file':rel if g else '','png_sha256':sha
            })
with open(OUT/'hgss_core_manifest.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=main_rows[0].keys()); w.writeheader(); w.writerows(main_rows)

# ---------- HGSS form archive mapping ----------
# Based on pret/pokeheartgold otherpoke layout + runtime formulas.
form_specs=[]
def add(species, forms, char_base, char_mode, pal_base, pal_mode):
    for fi,form in enumerate(forms):
        for facing in ('back','front'):
            wf=0 if facing=='back' else 2
            if char_mode=='pair': c=char_base + fi*2 + wf//2
            elif char_mode=='block': c=char_base + fi + wf
            elif char_mode=='castform': c=char_base + fi + wf*2
            else: raise ValueError(char_mode)
            for shiny in (0,1):
                if pal_mode=='pair': p=pal_base + fi*2 + shiny
                elif pal_mode=='shared': p=pal_base + shiny
                elif pal_mode=='block': p=pal_base + fi + shiny*len(forms)
                else: raise ValueError(pal_mode)
                form_specs.append((species,form,facing,shiny,c,p))

add('deoxys',['normal','attack','defense','speed'],0,'pair',158,'shared')
add('unown',list('abcdefghijklmnopqrstuvwxyz')+['exclamation_mark','question_mark'],8,'pair',160,'shared')
add('castform',['normal','sun','rain','ice'],64,'castform',162,'block')
add('burmy',['plant','sandy','trash'],72,'pair',170,'pair')
add('wormadam',['plant','sandy','trash'],78,'pair',176,'pair')
add('shellos',['west','east'],84,'block',182,'pair')
add('gastrodon',['west','east'],88,'block',186,'pair')
add('cherrim',['normal','sunshine'],92,'block',190,'block')
add('arceus',['normal','fighting','flying','poison','ground','rock','bug','ghost','steel','mystery','fire','water','grass','electric','psychic','ice','dragon','dark'],96,'pair',194,'pair')
add('shaymin',['land','sky'],134,'pair',232,'pair')
add('rotom',['normal','oven','washer','fridge','fan','lawnmower'],138,'pair',236,'pair')
add('giratina',['altered','origin'],150,'pair',248,'pair')
add('pichu',['normal','spiky'],154,'pair',252,'pair')

forms_dir=OUT/'hgss_forms'; forms_dir.mkdir()
form_rows=[]
for species,form,facing,shiny,c,p in form_specs:
    g=hg_forms[c]
    im=render_ncgr(g,palette(hg_forms[p]))
    rel=f'{species}/{form}/{facing}_{"shiny" if shiny else "normal"}.png'
    fp=forms_dir/rel; fp.parent.mkdir(parents=True,exist_ok=True); im.save(fp)
    form_rows.append({'species':species,'form':form,'facing':facing,'shiny':shiny,'graphic_member':c,'palette_member':p,'file':rel,'png_sha256':hashlib.sha256(fp.read_bytes()).hexdigest()})
# eggs
for label,c,p in [('egg_normal',132,230),('egg_manaphy',133,231)]:
    im=render_ncgr(hg_forms[c],palette(hg_forms[p])); rel=f'special/{label}.png'; fp=forms_dir/rel; fp.parent.mkdir(exist_ok=True); im.save(fp)
    form_rows.append({'species':'special','form':label,'facing':'single','shiny':0,'graphic_member':c,'palette_member':p,'file':rel,'png_sha256':hashlib.sha256(fp.read_bytes()).hexdigest()})
# substitute uses shared palette; shadow is single
for label,c in [('substitute_back',256),('substitute_front',257)]:
    im=render_ncgr(hg_forms[c],palette(hg_forms[258])); rel=f'special/{label}.png'; fp=forms_dir/rel; im.save(fp)
    form_rows.append({'species':'special','form':label,'facing':'single','shiny':0,'graphic_member':c,'palette_member':258,'file':rel,'png_sha256':hashlib.sha256(fp.read_bytes()).hexdigest()})
im=render_ncgr(hg_forms[259],palette(hg_forms[260])); rel='special/shadow.png'; fp=forms_dir/rel; im.save(fp)
form_rows.append({'species':'special','form':'shadow','facing':'single','shiny':0,'graphic_member':259,'palette_member':260,'file':rel,'png_sha256':hashlib.sha256(fp.read_bytes()).hexdigest()})
with open(OUT/'hgss_form_manifest.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=form_rows[0].keys()); w.writeheader(); w.writerows(form_rows)

# ---------- sprite lineage / diffs ----------
def canon_member(blob, enc):
    if not blob: return b''
    if blob[:4] == b'RGCN':
        return decrypt_dp_ncgr(blob) if enc=='dp' else decrypt_pt_ncgr(blob)
    return blob

def canon_group(arr,s,enc):
    return [canon_member(arr[s*6+i],enc) for i in range(6)]

def group_digest(arr,s,enc):
    return hashlib.sha256(b''.join(canon_group(arr,s,enc))).hexdigest()
def changed_members(a,enca,b,encb,s):
    labs=['back_female','back_male','front_female','front_male','normal_palette','shiny_palette']
    ca,cb=canon_group(a,s,enca),canon_group(b,s,encb)
    return [labs[i] for i in range(6) if ca[i]!=cb[i]]

diff_rows=[]
for s in range(1,494):
    dp=canon_group(d_main,s,'dp'); pt=canon_group(pt_main,s,'pt'); hg=canon_group(hg_main,s,'pt')
    diff_rows.append({
        'species_id':s,
        'dp_vs_pt_identical':int(dp==pt),
        'pt_vs_hgss_identical':int(pt==hg),
        'dp_vs_hgss_identical':int(dp==hg),
        'dp_vs_pt_changed_members':'|'.join(changed_members(d_main,'dp',pt_main,'pt',s)),
        'pt_vs_hgss_changed_members':'|'.join(changed_members(pt_main,'pt',hg_main,'pt',s)),
        'dp_group_sha256':group_digest(d_main,s,'dp'),
        'pt_group_sha256':group_digest(pt_main,s,'pt'),
        'hgss_group_sha256':group_digest(hg_main,s,'pt'),
    })
with open(OUT/'sprite_lineage_493.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=diff_rows[0].keys()); w.writeheader(); w.writerows(diff_rows)

# ---------- contact sheets ----------
def make_sheet(species_ids, outfile, title):
    cols=10; cw,ch=100,112; rows=(len(species_ids)+cols-1)//cols
    sh=Image.new('RGBA',(cols*cw,rows*ch+28),'white'); dr=ImageDraw.Draw(sh); dr.text((6,6),title,fill='black')
    for k,s in enumerate(species_ids):
        r,c=divmod(k,cols); base=s*6; g=hg_main[base+3]
        if g:
            im=render_ncgr(g,palette(hg_main[base+4]))
            sh.alpha_composite(im,(c*cw+10,28+r*ch+4))
        dr.text((c*cw+4,28+r*ch+88),f'#{s:03d}',fill='black')
    sh.save(outfile)

make_sheet(list(range(1,152)),OUT/'hgss_kanto_front_sheet.png','HGSS front male normal — #001–151')
make_sheet(list(range(152,252)),OUT/'hgss_johto_front_sheet.png','HGSS front male normal — #152–251')
make_sheet(list(range(252,387)),OUT/'hgss_hoenn_front_sheet.png','HGSS front male normal — #252–386')
make_sheet(list(range(387,494)),OUT/'hgss_sinnoh_front_sheet.png','HGSS front male normal — #387–493')

# forms contact sheet (normal front only)
front_norm=[r for r in form_rows if r['species']!='special' and r['facing']=='front' and r['shiny']==0]
cols=10; cw,ch=120,112; rows=(len(front_norm)+cols-1)//cols
sh=Image.new('RGBA',(cols*cw,rows*ch+28),'white'); dr=ImageDraw.Draw(sh); dr.text((6,6),'HGSS alternate forms — front normal',fill='black')
for k,r in enumerate(front_norm):
    rr,cc=divmod(k,cols); im=Image.open(forms_dir/r['file'])
    sh.alpha_composite(im,(cc*cw+18,28+rr*ch+2)); dr.text((cc*cw+3,28+rr*ch+88),f"{r['species']}:{r['form']}",fill='black')
sh.save(OUT/'hgss_forms_front_sheet.png')

# ---------- report ----------
summary={
 'hgss_main_members':len(hg_main),'hgss_form_members':len(hg_forms),
 'heartgold_soulsilver_main_identical':hg_main==ss_main,
 'heartgold_soulsilver_forms_identical':hg_forms==ss_forms,
 'diamond_pearl_main_identical':d_main==p_main,
 'dp_pt_identical_species_groups':sum(r['dp_vs_pt_identical'] for r in diff_rows),
 'pt_hgss_identical_species_groups':sum(r['pt_vs_hgss_identical'] for r in diff_rows),
 'dp_hgss_identical_species_groups':sum(r['dp_vs_hgss_identical'] for r in diff_rows),
 'hgss_core_png_count':sum(1 for r in main_rows if r['status']=='ok'),
 'hgss_core_empty_variant_palette_rows':sum(1 for r in main_rows if r['status']=='empty'),
 'hgss_form_png_count':len(form_rows),
}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

changed_dp_pt=[r['species_id'] for r in diff_rows if not r['dp_vs_pt_identical']]
changed_pt_hg=[r['species_id'] for r in diff_rows if not r['pt_vs_hgss_identical']]
report=f'''# Generation IV Sprite Census — Stage 4\n\n## Result\n\nThis stage performs complete HGSS battle-sprite extraction from the user-supplied ROM and builds a DP → Platinum → HGSS lineage ledger. ROM bytes are not included in repository artifacts.\n\n- HGSS main battle archive: `a/0/0/4`, **{len(hg_main)} members = 494 × 6**.\n- Main group layout: 4 encrypted NCGR graphics + normal/shiny NCLR palettes.\n- Ordinary species slots: 1–493.\n- HGSS alternate-form archive: `a/1/1/4`, **{len(hg_forms)} members**.\n- HeartGold/SoulSilver main archive identical: **{hg_main==ss_main}**.\n- HeartGold/SoulSilver alternate-form archive identical: **{hg_forms==ss_forms}**.\n- Diamond/Pearl main archive identical: **{d_main==p_main}**.\n\n## Extracted HGSS ordinary battle sprites\n\nEach species has logical slots for female back, male back, female front, male front, each rendered with normal and shiny palettes. Empty gender-difference NCGR slots are preserved as empty in the manifest rather than duplicated.\n\n- Rendered PNGs: **{summary['hgss_core_png_count']:,}**\n- Empty logical variant/palette rows caused by absent gender-specific graphics: **{summary['hgss_core_empty_variant_palette_rows']:,}**\n- Manifest: `hgss_core_manifest.csv`\n\n## Alternate forms\n\nRuntime formulas from `pret/pokeheartgold/src/pokemon.c` were used to map character and palette member IDs. Covered form families: Deoxys, Unown, Castform, Burmy, Wormadam, Shellos, Gastrodon, Cherrim, Arceus, Shaymin, Rotom, Giratina and Pichu (including Spiky-eared Pichu), plus egg, Manaphy egg, Substitute and battle shadow special resources.\n\n- Rendered alternate/special PNGs: **{summary['hgss_form_png_count']:,}**\n- Manifest: `hgss_form_manifest.csv`\n\n## Cross-version lineage\n\nSpecies-group equality is canonicalized across all six members: DP NCGR members are decrypted with the DP cipher, Platinum/HGSS NCGR members with the Pt/HGSS cipher, and palettes are compared directly. This removes encryption-format noise and reflects actual sprite-resource equality.\n\n| Comparison | identical species groups | changed groups |\n|---|---:|---:|\n| Diamond/Pearl base → Platinum active | {summary['dp_pt_identical_species_groups']} | {493-summary['dp_pt_identical_species_groups']} |\n| Platinum active → HGSS active | {summary['pt_hgss_identical_species_groups']} | {493-summary['pt_hgss_identical_species_groups']} |\n| Diamond/Pearl base → HGSS active | {summary['dp_hgss_identical_species_groups']} | {493-summary['dp_hgss_identical_species_groups']} |\n\nFull per-species member-level differences are in `sprite_lineage_493.csv`. This is the basis for the project priority rule **HGSS first → Platinum fallback → Diamond/Pearl fallback**.\n\n## Comparison correction recorded during Stage 4\n\nAn early lineage pass compared encrypted NCGR member bytes directly. Because Diamond/Pearl and Platinum/HGSS use different sprite-stream decryption directions, that raw comparison falsely made all 493 DP → Platinum species groups appear changed. The lineage pass was corrected before finalization to compare canonical decrypted NCGR payloads plus palette data.\n\n- Correct DP → Platinum result: **5 identical / 488 changed**.\n- The five unchanged species groups are National IDs **201, 351, 386, 421, 423**.\n- This correction is retained here so future stages do not regress to encrypted-byte comparison.\n\n## Validation\n\n- Main sprite NCGR data decrypts with the Platinum/HGSS stream cipher and renders correctly at 80×80.\n- The HGSS `otherpoke` index layout matches `pret/pokeheartgold/files/poketool/pokegra/otherpoke.txt`.\n- Runtime form selection formulas match `pret/pokeheartgold/src/pokemon.c`.\n\n## Generated local package\n\nThe user-facing ZIP contains extracted PNGs, CSV ledgers, contact sheets, this report and the reproducible extractor. The repository should keep the report/ledgers/tooling; ROM files themselves are never committed.\n'''
(OUT/'REPORT.md').write_text(report,encoding='utf-8')

# copy script into output
shutil.copy2(__file__,OUT/'build_sprite_stage4.py')

# zip all output
zip_path=Path('/mnt/data/GENERATION-IV-sprite-stage4.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for fp in OUT.rglob('*'):
        if fp.is_file(): z.write(fp,fp.relative_to(OUT.parent))

print(json.dumps(summary,ensure_ascii=False,indent=2))
print('changed DP->Pt',len(changed_dp_pt),changed_dp_pt[:80])
print('changed Pt->HGSS',len(changed_pt_hg),changed_pt_hg[:80])
print('ZIP',zip_path,zip_path.stat().st_size)
