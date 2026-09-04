#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,math
from pathlib import Path
from collections import Counter,defaultdict
from difflib import SequenceMatcher

BANK=0x4000
PAGE=0x100

# Generation I Japanese charmap subset used for discovery scans.
JP={
0x05:'ガ',0x06:'ギ',0x07:'グ',0x08:'ゲ',0x09:'ゴ',0x0a:'ザ',0x0b:'ジ',0x0c:'ズ',0x0d:'ゼ',0x0e:'ゾ',0x0f:'ダ',0x10:'ヂ',0x11:'ヅ',0x12:'デ',0x13:'ド',
0x19:'バ',0x1a:'ビ',0x1b:'ブ',0x1c:'ボ',0x26:'が',0x27:'ぎ',0x28:'ぐ',0x29:'げ',0x2a:'ご',0x2b:'ざ',0x2c:'じ',0x2d:'ず',0x2e:'ぜ',0x2f:'ぞ',0x30:'だ',0x31:'ぢ',0x32:'づ',0x33:'で',0x34:'ど',
0x3a:'ば',0x3b:'び',0x3c:'ぶ',0x3d:'べ',0x3e:'ぼ',0x40:'パ',0x41:'ピ',0x42:'プ',0x43:'ポ',0x44:'ぱ',0x45:'ぴ',0x46:'ぷ',0x47:'ぺ',0x48:'ぽ',
0x49:'<PAGE>',0x4a:'<PKMN>',0x4b:'<_CONT>',0x4c:'<SCROLL>',0x4e:'<NEXT>',0x4f:'<LINE>',0x50:'@',0x51:'<PARA>',0x52:'<PLAYER>',0x53:'<RIVAL>',0x54:'#',0x55:'<CONT>',0x56:'<……>',0x57:'<DONE>',0x58:'<PROMPT>',0x59:'<TARGET>',0x5a:'<USER>',0x5b:'<PC>',0x5c:'<TM>',0x5d:'<TRAINER>',0x5e:'<ROCKET>',0x5f:'<DEXEND>',
0x70:'「',0x71:'」',0x73:'』',0x75:'⋯',0x7f:'　',0xe3:'ー',0xe4:'ﾟ',0xe5:'ﾞ',0xe6:'？',0xe7:'！',0xe8:'。',0xf0:'円',0xf2:'．',0xf3:'／',0xf4:'ォ',
0xf6:'０',0xf7:'１',0xf8:'２',0xf9:'３',0xfa:'４',0xfb:'５',0xfc:'６',0xfd:'７',0xfe:'８',0xff:'９'}
kat='アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフホマミムメモヤユヨラルレロワヲンッャュョィ'
for i,ch in enumerate(kat): JP[0x80+i]=ch
hira='あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんっゃゅょ'
for i,ch in enumerate(hira): JP[0xb1+i]=ch
GLYPH=set(JP)-{0x50}|{0x1f,0x22,0x23,0x24,0x25,0x35,0x36,0x37,0x4a,0x54}
TEXT_ALLOWED=GLYPH|set(range(0x49,0x60))

def entropy(bs:bytes)->float:
    if not bs:return 0.0
    c=Counter(bs);n=len(bs)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def h(x,n=6):return f'{x:0{n}X}'
def hashes(bs):return {'md5':hashlib.md5(bs).hexdigest(),'sha1':hashlib.sha1(bs).hexdigest(),'sha256':hashlib.sha256(bs).hexdigest()}

def parse_header(b):
    chk=0
    for i in range(0x134,0x14D):chk=(chk-b[i]-1)&255
    g=(sum(b)-b[0x14E]-b[0x14F])&0xffff
    return {'entry_point_hex':b[0x100:0x104].hex().upper(),'title':b[0x134:0x144].rstrip(b'\0').decode('ascii','replace'),'cgb_flag':b[0x143],'new_licensee_hex':b[0x144:0x146].hex().upper(),'sgb_flag':b[0x146],'cartridge_type':b[0x147],'rom_size_code':b[0x148],'ram_size_code':b[0x149],'destination_code':b[0x14A],'old_licensee_code':b[0x14B],'mask_rom_version':b[0x14C],'header_checksum':b[0x14D],'header_checksum_valid':chk==b[0x14D],'global_checksum':int.from_bytes(b[0x14E:0x150],'big'),'global_checksum_valid':g==int.from_bytes(b[0x14E:0x150],'big')}

def diff_runs(a,b):
    rows=[];i=0
    while i<len(a):
        if a[i]==b[i]:i+=1;continue
        s=i
        while i<len(a) and a[i]!=b[i]:i+=1
        rows.append((s,i))
    return rows

def fill_runs(b,minlen=16):
    rows=[];i=0
    while i<len(b):
        v=b[i];j=i+1
        while j<len(b) and b[j]==v:j+=1
        if j-i>=minlen:rows.append((i,j,v))
        i=j
    return rows

def decode_text(bs):return ''.join(JP.get(x,f'<{x:02X}>') for x in bs)

def candidate_texts(b,max_back=160,minlen=4):
    out=[];seen=set();kana_extra=set(range(5,0x14))|set(range(0x19,0x1d))|set(range(0x26,0x35))|set(range(0x3a,0x49))
    for end,x in enumerate(b):
        if x!=0x50:continue
        s=end-1;floor=max(-1,end-max_back-1)
        while s>floor and b[s] in TEXT_ALLOWED and b[s]!=0x50:s-=1
        start=s+1
        if start>=end or (start,end) in seen:continue
        raw=b[start:end]
        if len(raw)<minlen:continue
        glyph=sum(x in GLYPH for x in raw);kana=sum((0x80<=x<=0xe2) or x in kana_extra for x in raw);controls=sum(x in range(0x49,0x60) for x in raw)
        if glyph/len(raw)<0.72 or kana<3 or controls>max(4,len(raw)//3):continue
        seen.add((start,end));out.append((start,end+1,raw+b'\x50',glyph,kana,controls))
    return out

def cpu_addr(off):
    bank=off//BANK;ib=off%BANK
    return ib if bank==0 else 0x4000+ib

def vector_summary(b):
    names={0x00:'RST00',0x08:'RST08',0x10:'RST10',0x18:'RST18',0x20:'RST20',0x28:'RST28',0x30:'RST30',0x38:'RST38',0x40:'VBlank',0x48:'LCD_STAT',0x50:'Timer',0x58:'Serial',0x60:'Joypad',0x100:'Entry'}
    rows=[]
    for off,name in names.items():
        chunk=b[off:off+8];op=chunk[0];desc=''
        if op==0xC3:desc=f'JP ${int.from_bytes(chunk[1:3],"little"):04X}'
        elif op==0xD9:desc='RETI'
        elif op==0xFF:desc='RST $38'
        elif op==0x00:desc='NOP'
        else:desc=f'opcode ${op:02X}'
        rows.append({'name':name,'offset_hex':h(off,4),'first_opcode_hex':f'{op:02X}','decoded_first_instruction':desc,'first_8_sha256':hashlib.sha256(chunk).hexdigest()})
    return rows

def write_csv(path,rows):
    if not rows:path.write_text('',encoding='utf-8');return
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rev0',type=Path);ap.add_argument('reva',type=Path);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    a=args.rev0.read_bytes();b=args.reva.read_bytes();out=args.out;out.mkdir(parents=True,exist_ok=True)
    if len(a)!=len(b) or len(a)%BANK:raise SystemExit('ROM size mismatch')
    banks=len(a)//BANK
    meta={}
    for key,p,bs in [('rev_0',args.rev0,a),('rev_a',args.reva,b)]:meta[key]={'file_label':p.name,'size_bytes':len(bs),'banks_16k':banks,'hashes':hashes(bs),'header':parse_header(bs),'entropy':round(entropy(bs),6),'unique_bytes':len(set(bs))}
    dr=diff_runs(a,b);diffn=sum(e-s for s,e in dr)
    meta['comparison']={'different_bytes':diffn,'different_percent':round(diffn/len(a)*100,6),'contiguous_diff_runs':len(dr),'first_diff_hex':h(dr[0][0]) if dr else None,'last_diff_hex':h(dr[-1][1]-1) if dr else None}
    (out/'rom_overview.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_csv(out/'vectors_rev0.csv',vector_summary(a));write_csv(out/'vectors_reva.csv',vector_summary(b))
    diffrows=[]
    for s,e in dr:diffrows.append({'bank_hex':f'{s//BANK:02X}','start_hex':h(s),'end_hex':h(e-1),'length':e-s,'start_in_bank_hex':h(s%BANK,4),'end_in_bank_hex':h((e-1)%BANK,4),'rev0_region_sha256':hashlib.sha256(a[s:e]).hexdigest(),'reva_region_sha256':hashlib.sha256(b[s:e]).hexdigest()})
    write_csv(out/'revision_diff_runs.csv',diffrows)
    for label,bs in [('rev0',a),('reva',b)]:
        rows=[]
        for s,e,v in fill_runs(bs,16):rows.append({'bank_hex':f'{s//BANK:02X}','start_hex':h(s),'end_hex':h(e-1),'length':e-s,'byte_hex':f'{v:02X}','padding_or_garbage_candidate':v in (0,0xff)})
        write_csv(out/f'fill_runs_{label}.csv',rows)
    texts=candidate_texts(a);text_starts_by_bank=defaultdict(set);word_counts=Counter(int.from_bytes(a[i:i+2],'little') for i in range(len(a)-1));text_rows=[]
    for s,e,raw,glyph,kana,controls in texts:
        bank=s//BANK;addr=cpu_addr(s);text_starts_by_bank[bank].add(addr)
        text_rows.append({'bank_hex':f'{bank:02X}','start_hex':h(s),'end_hex':h(e-1),'cpu_address_hex':f'{addr:04X}','length_bytes':e-s,'glyph_bytes':glyph,'kana_bytes':kana,'control_bytes':controls,'pointer_value_occurrences':word_counts[addr],'decoded':decode_text(raw)})
    write_csv(out/'jp_text_candidates_rev0.csv',text_rows)
    ptrtables=[]
    for bank in range(banks):
        chunk=a[bank*BANK:(bank+1)*BANK];targets=text_starts_by_bank.get(bank,set());i=0
        while targets and i<=len(chunk)-6:
            j=i;vals=[]
            while j+1<len(chunk):
                v=int.from_bytes(chunk[j:j+2],'little')
                if v not in targets:break
                vals.append(v);j+=2
            if len(vals)>=3:ptrtables.append({'bank_hex':f'{bank:02X}','start_hex':h(bank*BANK+i),'end_hex':h(bank*BANK+j-1),'pointer_count':len(vals),'first_target_hex':f'{vals[0]:04X}','last_target_hex':f'{vals[-1]:04X}'});i=j
            else:i+=1
    write_csv(out/'jp_text_pointer_table_candidates_rev0.csv',ptrtables)
    bankrows=[];pagerows=[];alignrows=[];text_by=Counter(s//BANK for s,_,*rest in texts);diff_by=Counter();diffruns_by=Counter();largest=Counter()
    for s,e in dr:bank=s//BANK;diff_by[bank]+=e-s;diffruns_by[bank]+=1;largest[bank]=max(largest[bank],e-s)
    for bank in range(banks):
        s=bank*BANK;e=s+BANK;x=a[s:e];y=b[s:e];sm=SequenceMatcher(None,x,y,autojunk=True);ops=sm.get_opcodes();edits=[z for z in ops if z[0]!='equal'];eq=sum(i2-i1 for tag,i1,i2,j1,j2 in ops if tag=='equal')
        bankrows.append({'bank_hex':f'{bank:02X}','start_hex':h(s),'end_hex':h(e-1),'rev0_entropy':round(entropy(x),6),'reva_entropy':round(entropy(y),6),'rev0_unique_bytes':len(set(x)),'reva_unique_bytes':len(set(y)),'rev0_zero_bytes':x.count(0),'rev0_ff_bytes':x.count(255),'reva_zero_bytes':y.count(0),'reva_ff_bytes':y.count(255),'raw_different_bytes':diff_by[bank],'raw_difference_percent':round(diff_by[bank]/BANK*100,6),'raw_diff_runs':diffruns_by[bank],'largest_raw_diff_run':largest[bank],'sequence_similarity_ratio':round(sm.ratio(),6),'aligned_equal_bytes':eq,'sequence_edit_opcodes':len(edits),'jp_text_candidates_rev0':text_by[bank]})
        alignrows.append({'bank_hex':f'{bank:02X}','sequence_similarity_ratio':round(sm.ratio(),6),'matching_bytes_via_sequence_alignment':eq,'non_equal_opcode_count':len(edits),'raw_different_bytes':diff_by[bank]})
        for po in range(s,e,PAGE):
            xx=a[po:po+PAGE];yy=b[po:po+PAGE];pagerows.append({'bank_hex':f'{bank:02X}','page_in_bank_hex':f'{(po-s)//PAGE:02X}','start_hex':h(po),'end_hex':h(po+PAGE-1),'rev0_entropy':round(entropy(xx),6),'reva_entropy':round(entropy(yy),6),'rev0_unique_bytes':len(set(xx)),'reva_unique_bytes':len(set(yy)),'different_bytes':sum(u!=v for u,v in zip(xx,yy))})
    write_csv(out/'bank_stats.csv',bankrows);write_csv(out/'page_stats_256b.csv',pagerows);write_csv(out/'revision_sequence_alignment_by_bank.csv',alignrows)
    summary={'banks':banks,'rev0_text_candidate_count':len(texts),'rev0_text_candidate_bytes':sum(e-s for s,e,*_ in texts),'rev0_text_pointer_table_candidate_count':len(ptrtables),'raw_diff_run_count':len(dr),'largest_raw_diff_runs':sorted([{'length':e-s,'start_hex':h(s),'end_hex':h(e-1),'bank_hex':f'{s//BANK:02X}'} for s,e in dr],key=lambda z:z['length'],reverse=True)[:30]}
    (out/'census_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
