#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math, os, shutil, statistics, sys, zlib
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from itertools import combinations
from pathlib import Path

BANK_SIZE = 0x4000
CHUNK_SIZE = 0x1000

ROMS = [
    ("KR", "REV-0", "Pocket Monsters Geum (Korea).gbc"),
    ("JP", "REV-0", "Pocket Monsters Kin (Japan).gbc"),
    ("JP", "REV-A", "Pocket Monsters Kin (Japan) (Rev A).gbc"),
    ("USA-EUROPE", "REV-0", "Pokemon - Gold Version (USA, Europe).gbc"),
    ("DE", "REV-0", "Pokemon - Goldene Edition (Germany).gbc"),
    ("FR", "REV-0", "Pokemon - Version Or (France).gbc"),
    ("IT", "REV-0", "Pokemon - Versione Oro (Italy).gbc"),
    ("ES", "REV-0", "Pokemon - Edicion Oro (Spain).gbc"),
]

ROM_SIZE_CODE = {0x00: 32*1024,0x01:64*1024,0x02:128*1024,0x03:256*1024,0x04:512*1024,0x05:1024*1024,0x06:2*1024*1024,0x07:4*1024*1024,0x08:8*1024*1024,0x52:1152*1024,0x53:1280*1024,0x54:1536*1024}
RAM_SIZE_CODE = {0x00:0,0x01:2*1024,0x02:8*1024,0x03:32*1024,0x04:128*1024,0x05:64*1024}
CART_TYPE = {0x10:"MBC3+TIMER+RAM+BATTERY"}

@dataclass
class RomInfo:
    language: str
    revision: str
    filename: str
    size: int
    md5: str
    sha1: str
    sha256: str
    crc32: str
    title_ascii: str
    cgb_flag: str
    cartridge_type: str
    cartridge_type_code: str
    rom_size_code: str
    declared_rom_size: int | None
    ram_size_code: str
    declared_ram_size: int | None
    destination_code: str
    version_byte: str
    header_checksum_stored: str
    header_checksum_calculated: str
    header_checksum_ok: bool
    global_checksum_stored: str
    global_checksum_calculated: str
    global_checksum_ok: bool
    banks: int
    chunks_4k: int


def digest(data: bytes, alg: str) -> str:
    h = hashlib.new(alg); h.update(data); return h.hexdigest()

def calc_header_checksum(data: bytes) -> int:
    x = 0
    for b in data[0x134:0x14D]: x = (x - b - 1) & 0xFF
    return x

def calc_global_checksum(data: bytes) -> int:
    return (sum(data) - data[0x14E] - data[0x14F]) & 0xFFFF

def safe_title(data: bytes) -> str:
    raw = data[0x134:0x143]
    return ''.join(chr(b) if 32 <= b < 127 else f"\\x{b:02X}" for b in raw).rstrip('\\x00')

def entropy(data: bytes) -> float:
    n=len(data)
    if not n: return 0.0
    c=Counter(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def longest_run(data: bytes, target: int) -> tuple[int,int]:
    best_len=best_start=cur_len=0; cur_start=0
    for i,b in enumerate(data):
        if b==target:
            if cur_len==0: cur_start=i
            cur_len+=1
            if cur_len>best_len: best_len,best_start=cur_len,cur_start
        else: cur_len=0
    return best_start,best_len

def contiguous_diff_ranges(a: bytes, b: bytes):
    n=max(len(a),len(b)); ranges=[]; start=None
    for i in range(n):
        diff = (i>=len(a) or i>=len(b) or a[i]!=b[i])
        if diff and start is None: start=i
        elif not diff and start is not None:
            ranges.append((start,i-1)); start=None
    if start is not None: ranges.append((start,n-1))
    return ranges

def load_info(lang, rev, path: Path):
    data=path.read_bytes()
    stored_g=(data[0x14E]<<8)|data[0x14F]
    calc_g=calc_global_checksum(data)
    stored_h=data[0x14D]; calc_h=calc_header_checksum(data)
    info=RomInfo(
        lang, rev, path.name, len(data), digest(data,'md5'), digest(data,'sha1'), digest(data,'sha256'), f"{zlib.crc32(data)&0xffffffff:08x}",
        safe_title(data), f"0x{data[0x143]:02X}", CART_TYPE.get(data[0x147],f"UNKNOWN_0x{data[0x147]:02X}"), f"0x{data[0x147]:02X}",
        f"0x{data[0x148]:02X}", ROM_SIZE_CODE.get(data[0x148]), f"0x{data[0x149]:02X}", RAM_SIZE_CODE.get(data[0x149]),
        f"0x{data[0x14A]:02X}", f"0x{data[0x14C]:02X}", f"0x{stored_h:02X}", f"0x{calc_h:02X}", stored_h==calc_h,
        f"0x{stored_g:04X}", f"0x{calc_g:04X}", stored_g==calc_g, math.ceil(len(data)/BANK_SIZE), math.ceil(len(data)/CHUNK_SIZE)
    )
    return info,data

def write_csv(path: Path, rows, fieldnames=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    rows=list(rows)
    if fieldnames is None:
        fieldnames=list(rows[0].keys()) if rows else []
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(rows)

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')

def bank_rows(data: bytes):
    rows=[]
    for bank in range(math.ceil(len(data)/BANK_SIZE)):
        start=bank*BANK_SIZE; block=data[start:start+BANK_SIZE]
        c=Counter(block); dom,domn=c.most_common(1)[0]
        zstart,zlen=longest_run(block,0x00); fstart,flen=longest_run(block,0xFF)
        rows.append({
            'bank_dec':bank,'bank_hex':f"0x{bank:02X}",'rom_offset_start':f"0x{start:06X}",'rom_offset_end':f"0x{start+len(block)-1:06X}",
            'length':len(block),'sha1':digest(block,'sha1'),'sha256':digest(block,'sha256'),'crc32':f"{zlib.crc32(block)&0xffffffff:08x}",
            'entropy_bits_per_byte':f"{entropy(block):.6f}",'unique_byte_values':len(c),'dominant_byte':f"0x{dom:02X}",'dominant_count':domn,
            'zero_count':c[0],'ff_count':c[0xFF],'longest_zero_run_offset':f"0x{start+zstart:06X}",'longest_zero_run':zlen,
            'longest_ff_run_offset':f"0x{start+fstart:06X}",'longest_ff_run':flen,'all_zero':len(block)>0 and c[0]==len(block),'all_ff':len(block)>0 and c[0xFF]==len(block)
        })
    return rows

def chunk_rows(data: bytes):
    rows=[]
    for idx in range(math.ceil(len(data)/CHUNK_SIZE)):
        start=idx*CHUNK_SIZE; block=data[start:start+CHUNK_SIZE]
        rows.append({'chunk_dec':idx,'chunk_hex':f"0x{idx:03X}",'rom_offset_start':f"0x{start:06X}",'rom_offset_end':f"0x{start+len(block)-1:06X}",'length':len(block),'sha256':digest(block,'sha256')})
    return rows

def frequency_rows(data: bytes):
    c=Counter(data)
    return [{'byte_dec':b,'byte_hex':f"0x{b:02X}",'count':c[b],'fraction':f"{c[b]/len(data):.10f}"} for b in range(256)]

def header_dict(info: RomInfo):
    d=asdict(info)
    return {k:v for k,v in d.items() if k not in ('md5','sha1','sha256','crc32','banks','chunks_4k')}

def rgbds_rebuild_asm(bank_count: int) -> str:
    lines = [
        '; Byte-exact rebuild scaffold. No ROM bytes are stored here.',
        '; Place the verified source ROM at source.gbc (gitignored).',
        '',
        'SECTION "ROM Bank 00", ROM0[$0000]',
        'INCBIN "source.gbc", $000000, $004000',
    ]
    for bank in range(1, bank_count):
        off = bank * BANK_SIZE
        lines += ['', f'SECTION "ROM Bank {bank:02X}", ROMX[$4000], BANK[${bank:02X}]', f'INCBIN "source.gbc", ${off:06X}, $004000']
    return "\n".join(lines) + "\n"

def bank_constants_inc(bank_count: int) -> str:
    return "\n".join(['; Generated bank constants'] + [f'DEF ROM_BANK_{bank:02X} EQU ${bank:02X}' for bank in range(bank_count)]) + "\n"

def bank_symbols(bank_count: int) -> str:
    lines=[]
    for bank in range(bank_count):
        addr = 0x0000 if bank == 0 else 0x4000
        lines.append(f'{bank:02x}:{addr:04x} ROM_BANK_{bank:02X}_START')
    return "\n".join(lines) + "\n"

def layout_map(bank_count: int) -> str:
    lines=['# ROM bank layout map', '', '| Bank | File offset | CPU window | Size |', '|---:|---:|---:|---:|']
    for bank in range(bank_count):
        off=bank*BANK_SIZE
        cpu='$0000-$3FFF' if bank==0 else '$4000-$7FFF'
        lines.append(f'| `0x{bank:02X}` | `0x{off:06X}-0x{off+BANK_SIZE-1:06X}` | `{cpu}` | `0x4000` |')
    return "\n".join(lines) + "\n"

def md_ident(info: RomInfo, banks):
    blank=[r['bank_hex'] for r in banks if r['all_zero']]
    return f"""# Pokémon Gold — {info.language} — {info.revision} ROM Identification\n\nSource ROM is read-only and is **not stored in this corpus/repository**.\n\n| Field | Value |\n|---|---|\n| Source filename | `{info.filename}` |\n| File size | {info.size:,} bytes |\n| MD5 | `{info.md5}` |\n| SHA-1 | `{info.sha1}` |\n| SHA-256 | `{info.sha256}` |\n| CRC32 | `{info.crc32}` |\n| Header title | `{info.title_ascii}` |\n| CGB flag | `{info.cgb_flag}` |\n| Cartridge type | `{info.cartridge_type_code}` ({info.cartridge_type}) |\n| ROM size code | `{info.rom_size_code}` ({info.declared_rom_size:,} bytes declared) |\n| RAM size code | `{info.ram_size_code}` ({info.declared_ram_size:,} bytes declared) |\n| Destination code | `{info.destination_code}` |\n| Version byte | `{info.version_byte}` |\n| 16 KiB banks | {info.banks} |\n| Header checksum | stored `{info.header_checksum_stored}`, calculated `{info.header_checksum_calculated}` — {'PASS' if info.header_checksum_ok else 'FAIL'} |\n| Global checksum | stored `{info.global_checksum_stored}`, calculated `{info.global_checksum_calculated}` — {'PASS' if info.global_checksum_ok else 'FAIL'} |\n| Fully zero 16 KiB banks | {', '.join(blank) if blank else 'none'} |\n\n## Reproducibility\n\nRun `python tools/build_gold_repro_corpus.py --rom-dir <directory> --out <output>` from the MULTI corpus.\nThe generator recomputes every hash, header field, bank statistic, 4 KiB chunk hash, and comparison table from the local ROMs.\n"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rom-dir',type=Path,default=Path('/mnt/data'))
    ap.add_argument('--out',type=Path,default=Path('/mnt/data/gold_reproducible_corpus'))
    args=ap.parse_args()
    out=args.out
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)

    records=[]; blobs={}; banks_by={}; chunks_by={}
    for lang,rev,name in ROMS:
        path=args.rom_dir/name
        if not path.exists(): raise SystemExit(f"Missing ROM: {path}")
        info,data=load_info(lang,rev,path); records.append(info); blobs[(lang,rev)]=data
        base=out/'GENERATION-II'/'GOLD'/lang/rev/'analysis'
        b=bank_rows(data); c=chunk_rows(data); banks_by[(lang,rev)]=b; chunks_by[(lang,rev)]=c
        base.mkdir(parents=True,exist_ok=True)
        (base/'ROM-IDENTIFICATION.md').write_text(md_ident(info,b),encoding='utf-8')
        write_json(base/'cartridge_header.json',header_dict(info))
        write_csv(base/'bank_map.csv',b)
        write_json(base/'bank_map.json',b)
        write_csv(base/'chunk_hashes_4k.csv',c)
        write_csv(base/'byte_frequency.csv',frequency_rows(data))
        (base/'checksums.txt').write_text(f"MD5 {info.md5}  {info.filename}\nSHA1 {info.sha1}  {info.filename}\nSHA256 {info.sha256}  {info.filename}\nCRC32 {info.crc32}  {info.filename}\n",encoding='utf-8')
        blank=[x for x in b if x['all_zero'] or x['all_ff']]
        write_csv(base/'blank_banks.csv',blank,fieldnames=list(b[0].keys()))
        local_manifest=[{'bank_dec':r['bank_dec'],'bank_hex':r['bank_hex'],'suggested_local_filename':f"bank_{r['bank_dec']:03d}_{r['bank_hex'][2:]}.bin",'sha256':r['sha256']} for r in b]
        write_csv(base/'local_bank_extraction_manifest.csv',local_manifest)
        rebuild=base/'rebuild'
        rebuild.mkdir(parents=True,exist_ok=True)
        (rebuild/'rebuild_exact.asm').write_text(rgbds_rebuild_asm(info.banks),encoding='utf-8')
        (rebuild/'banks.inc').write_text(bank_constants_inc(info.banks),encoding='utf-8')
        (rebuild/'banks.sym').write_text(bank_symbols(info.banks),encoding='utf-8')
        (rebuild/'layout.map.md').write_text(layout_map(info.banks),encoding='utf-8')
        (rebuild/'.gitignore').write_text('source.gbc\nbuilt.gbc\nbuilt.map\nbuilt.sym\n*.o\n',encoding='utf-8')
        readme = (
            f'# Byte-exact rebuild scaffold — {info.language} {info.revision}\n\n'
            'This directory contains no ROM bytes. Put the verified input ROM at `source.gbc` locally.\n\n'
            'The starter `rebuild_exact.asm` maps every 16 KiB bank with RGBDS `INCBIN`. '
            'It is a byte-exact baseline before regions are deliberately replaced by named ASM/data source.\n\n'
            f'Expected input SHA-256: `{info.sha256}`\n\n'
            f'Expected size: `{info.size}` bytes\n\n'
            'Suggested RGBDS flow (when RGBDS is installed):\n\n'
            '```sh\nrgbasm -o built.o rebuild_exact.asm\nrgblink -o built.gbc -m built.map -n built.sym built.o\nsha256sum built.gbc\n```\n\n'
            'The resulting `built.gbc` must match the expected SHA-256 before source replacement begins.\n'
        )
        (rebuild/'README.md').write_text(readme,encoding='utf-8')

    multi=out/'GENERATION-II'/'GOLD'/'MULTI'/'REV-MIXED'/'analysis'
    tools=multi/'tools'; tests=multi/'tests'; comp=multi/'comparison'; manifests=multi/'manifests'
    tools.mkdir(parents=True,exist_ok=True); tests.mkdir(parents=True,exist_ok=True); comp.mkdir(parents=True,exist_ok=True); manifests.mkdir(parents=True,exist_ok=True)

    inv=[asdict(x) for x in records]
    write_csv(manifests/'rom_inventory.csv',inv); write_json(manifests/'rom_inventory.json',inv)

    pairs=[]
    for a,b in combinations(records,2):
        ka=(a.language,a.revision); kb=(b.language,b.revision)
        ba=banks_by[ka]; bb=banks_by[kb]; ca=chunks_by[ka]; cb=chunks_by[kb]
        nbank=min(len(ba),len(bb)); nchunk=min(len(ca),len(cb))
        ib=sum(ba[i]['sha256']==bb[i]['sha256'] for i in range(nbank)); ic=sum(ca[i]['sha256']==cb[i]['sha256'] for i in range(nchunk))
        pairs.append({'a':f"{a.language}/{a.revision}",'b':f"{b.language}/{b.revision}",'bytes_a':a.size,'bytes_b':b.size,'common_bank_positions':nbank,'identical_bank_positions':ib,'common_4k_chunk_positions':nchunk,'identical_4k_chunk_positions':ic})
    write_csv(comp/'pairwise_similarity.csv',pairs); write_json(comp/'pairwise_similarity.json',pairs)

    bank_eq=[]
    maxbanks=max(x.banks for x in records)
    for i in range(maxbanks):
        row={'bank_dec':i,'bank_hex':f"0x{i:02X}"}
        for x in records:
            key=(x.language,x.revision); label=f"{x.language}_{x.revision}"
            row[label]=banks_by[key][i]['sha256'] if i < len(banks_by[key]) else ''
        bank_eq.append(row)
    write_csv(comp/'bank_hash_matrix.csv',bank_eq)

    groups=defaultdict(list)
    for x in records:
        for r in banks_by[(x.language,x.revision)]: groups[r['sha256']].append(f"{x.language}/{x.revision}:{r['bank_hex']}")
    eqrows=[{'sha256':h,'copies':len(v),'locations':' | '.join(v)} for h,v in groups.items() if len(v)>1]
    eqrows.sort(key=lambda r:(-r['copies'],r['sha256']))
    write_csv(comp/'identical_bank_groups.csv',eqrows)

    a=blobs[('JP','REV-0')]; b=blobs[('JP','REV-A')]
    ranges=contiguous_diff_ranges(a,b)
    dr=[]
    for s,e in ranges:
        dr.append({'start_offset':f"0x{s:06X}",'end_offset':f"0x{e:06X}",'length':e-s+1,'start_bank':f"0x{s//BANK_SIZE:02X}",'end_bank':f"0x{e//BANK_SIZE:02X}"})
    write_csv(comp/'jp_rev0_vs_reva_diff_ranges.csv',dr); write_json(comp/'jp_rev0_vs_reva_diff_ranges.json',dr)
    diffbytes=sum(1 for x,y in zip(a,b) if x!=y) + abs(len(a)-len(b))
    (comp/'jp_rev0_vs_reva_summary.md').write_text(f"# JP REV-0 vs REV-A\n\n- Differing bytes: **{diffbytes:,}**\n- Contiguous differing ranges: **{len(ranges):,}**\n- Sizes: {len(a):,} vs {len(b):,} bytes\n- Exact ranges: `jp_rev0_vs_reva_diff_ranges.csv`\n",encoding='utf-8')

    shutil.copy2(Path(__file__),tools/'build_gold_repro_corpus.py')
    (tools/'split_rom_banks.py').write_text('''#!/usr/bin/env python3\nimport argparse,hashlib,math\nfrom pathlib import Path\nBANK=0x4000\nap=argparse.ArgumentParser(); ap.add_argument("rom",type=Path); ap.add_argument("out",type=Path); a=ap.parse_args()\ndata=a.rom.read_bytes(); a.out.mkdir(parents=True,exist_ok=True)\nfor i in range(math.ceil(len(data)/BANK)):\n b=data[i*BANK:(i+1)*BANK]; p=a.out/f"bank_{i:03d}_{i:02X}.bin"; p.write_bytes(b); print(i,hashlib.sha256(b).hexdigest(),p)\n''',encoding='utf-8')
    (tools/'verify_corpus.py').write_text('''#!/usr/bin/env python3\nimport argparse,csv,hashlib\nfrom pathlib import Path\nap=argparse.ArgumentParser(); ap.add_argument("--rom-dir",type=Path,required=True); ap.add_argument("--inventory",type=Path,required=True); a=ap.parse_args()\nfail=0\nwith a.inventory.open(encoding="utf-8") as f:\n for r in csv.DictReader(f):\n  p=a.rom_dir/r["filename"]\n  if not p.exists(): print("MISSING",p); fail+=1; continue\n  data=p.read_bytes(); h=hashlib.sha256(data).hexdigest(); ok=(h==r["sha256"] and len(data)==int(r["size"]))\n  print("PASS" if ok else "FAIL",r["language"],r["revision"],p.name)\n  fail += 0 if ok else 1\nraise SystemExit(1 if fail else 0)\n''',encoding='utf-8')
    (multi/'.gitignore').write_text('rom-derived/\n*.gbc\n*.gb\n*.bin\n',encoding='utf-8')
    (multi/'run_all.sh').write_text('#!/usr/bin/env sh\nset -eu\npython3 tools/build_gold_repro_corpus.py --rom-dir "${1:-/mnt/data}" --out "${2:-./rebuild}"\npython3 tools/verify_corpus.py --rom-dir "${1:-/mnt/data}" --inventory "${2:-./rebuild}/GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/manifests/rom_inventory.csv"\n',encoding='utf-8')
    (tests/'test_plan.md').write_text('''# Reproducibility test plan\n\n1. Verify all eight source ROM filenames exist locally.\n2. Verify file size and SHA-256 against `rom_inventory.csv`.\n3. Recompute Game Boy header checksum and global checksum.\n4. Recompute every 16 KiB bank SHA-256 and statistics.\n5. Recompute every 4 KiB chunk SHA-256.\n6. Regenerate pairwise bank/chunk similarity tables.\n7. Regenerate the JP REV-0 ↔ REV-A exact diff-range table.\n8. Ensure no `.gbc`, `.gb`, or `.bin` is present in the distributable corpus.\n9. Regenerate the complete corpus a second time and require identical path sets and SHA-256 for every generated file.\n10. Keep the RGBDS INCBIN rebuild scaffold external-input-only: `source.gbc` and built ROMs stay gitignored.\n''',encoding='utf-8')
    (multi/'README.md').write_text('''# Pokémon Gold multi-ROM reproducibility corpus\n\nThis corpus covers the eight supplied Pokémon Gold ROM variants: KR, JP REV-0, JP REV-A, USA/EUROPE, DE, FR, IT, and ES.\n\nIt deliberately **does not contain ROM bytes**. Instead it contains enough deterministic metadata and tooling to identify the exact local source ROMs, regenerate bank/chunk maps, compare revisions/localizations, locate blank banks, and verify that future analysis is being performed against the same inputs.\n\n## Included\n\n- ROM inventory with MD5/SHA-1/SHA-256/CRC32\n- Game Boy cartridge/header metadata and checksum verification\n- 16 KiB bank maps with hashes, entropy, fill statistics, and longest 00/FF runs\n- 4 KiB chunk SHA-256 maps for fine-grained change localization\n- Full byte-frequency tables\n- Blank-bank reports\n- Pairwise ROM similarity tables\n- Cross-ROM bank hash matrix and identical-bank groups\n- Exact JP REV-0 vs REV-A contiguous diff ranges\n- Deterministic generator and verifier scripts\n- Per-ROM byte-exact RGBDS rebuild scaffolds (`.asm`, `.inc`, `.sym`, layout map) using local `source.gbc` via `INCBIN`\n- Local-only bank splitter (generated `.bin` files are ignored and must never be committed)\n- Corpus-wide SHA-256 manifest for generated work files\n\n## Repository rule\n\nOriginal ROMs and byte-for-byte ROM-derived binary assets are excluded. To reproduce the corpus, provide the exact local ROMs whose hashes appear in `manifests/rom_inventory.csv`.\n''',encoding='utf-8')

    files=[]
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name!='CORPUS-SHA256SUMS.txt':
            rel=p.relative_to(out).as_posix(); files.append((digest(p.read_bytes(),'sha256'),rel,p.stat().st_size))
    (multi/'CORPUS-SHA256SUMS.txt').write_text(''.join(f"{h}  {rel}\n" for h,rel,_ in files),encoding='utf-8')
    write_csv(manifests/'corpus_files.csv',[{'path':rel,'size':size,'sha256':h} for h,rel,size in files])

    prohibited=[]
    for p in out.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.gbc','.gb','.bin'}: prohibited.append(str(p))
    if prohibited: raise SystemExit('Prohibited binary outputs: '+repr(prohibited))
    print(f"Built {out} with {sum(1 for p in out.rglob('*') if p.is_file())} files")
    for x in records: print(x.language,x.revision,x.size,x.sha256[:16],x.header_checksum_ok,x.global_checksum_ok)

if __name__=='__main__': main()
