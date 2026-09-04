from pathlib import Path
from collections import defaultdict, Counter
import hashlib, zlib, json, difflib, math

p0=Path('/mnt/data/Pocket Monsters - Midori (Japan) (SGB Enhanced).gb')
p1=Path('/mnt/data/Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb')
a=p0.read_bytes(); b=p1.read_bytes()
BANK=0x4000

def hdr(d):
    title=d[0x134:0x144].split(b'\0')[0].decode('ascii','replace')
    return {
      'title':title,'cgb':d[0x143],'new_licensee':d[0x144:0x146].decode('ascii','replace'),
      'sgb':d[0x146], 'cart_type':d[0x147], 'rom_size':d[0x148], 'ram_size':d[0x149],
      'destination':d[0x14A], 'old_licensee':d[0x14B], 'version':d[0x14C],
      'header_checksum_stored':d[0x14D], 'global_checksum_stored':int.from_bytes(d[0x14E:0x150],'big'),
    }

def hchk(d):
    x=0
    for i in range(0x134,0x14D): x=(x-d[i]-1)&0xff
    return x

def gchk(d): return (sum(d)-d[0x14E]-d[0x14F])&0xffff

def diff_runs(x,y,base=0):
    runs=[]; s=None
    for i,(u,v) in enumerate(zip(x,y)):
      if u!=v and s is None:s=i
      if u==v and s is not None:
        runs.append((base+s,base+i,i-s));s=None
    if s is not None:runs.append((base+s,base+len(x),len(x)-s))
    return runs

out={}
out['files']={
 'rev0':{'size':len(a),'sha1':hashlib.sha1(a).hexdigest(),'sha256':hashlib.sha256(a).hexdigest(),'crc32':f'{zlib.crc32(a)&0xffffffff:08x}','header':hdr(a),'calc_header_checksum':hchk(a),'calc_global_checksum':gchk(a)},
 'revA':{'size':len(b),'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','header':hdr(b),'calc_header_checksum':hchk(b),'calc_global_checksum':gchk(b)} }

out['total_diff_bytes']=sum(x!=y for x,y in zip(a,b))
runs=diff_runs(a,b)
out['total_diff_runs']=len(runs)
out['largest_runs']=sorted(runs,key=lambda t:t[2], reverse=True)[:100]

banks=[]
for bank in range(len(a)//BANK):
    x=a[bank*BANK:(bank+1)*BANK]; y=b[bank*BANK:(bank+1)*BANK]
    n=sum(u!=v for u,v in zip(x,y)); rr=diff_runs(x,y,bank*BANK)
    banks.append({'bank':bank,'diff_bytes':n,'diff_pct':n/BANK*100,'runs':len(rr),
                  'first_diff':rr[0][0] if rr else None,'last_diff':rr[-1][1]-1 if rr else None,
                  'largest_run':max((z for _,_,z in rr),default=0),
                  'sha1_rev0':hashlib.sha1(x).hexdigest(),'sha1_revA':hashlib.sha1(y).hexdigest()})
out['banks']=banks

# SequenceMatcher per bank, autojunk=False. Identify non-equal opcodes and equal matching blocks.
seqbanks=[]
for bank in range(32):
    x=a[bank*BANK:(bank+1)*BANK]; y=b[bank*BANK:(bank+1)*BANK]
    sm=difflib.SequenceMatcher(None,x,y,autojunk=False)
    ops=sm.get_opcodes()
    change=[]
    for tag,i1,i2,j1,j2 in ops:
      if tag!='equal':
        change.append({'tag':tag,'a0':bank*BANK+i1,'a1':bank*BANK+i2,'b0':bank*BANK+j1,'b1':bank*BANK+j2,'alen':i2-i1,'blen':j2-j1})
    matches=[m for m in sm.get_matching_blocks() if m.size]
    seqbanks.append({'bank':bank,'ratio':sm.ratio(),'opcode_changes':len(change),
                     'changed_a_span':sum(c['alen'] for c in change),'changed_b_span':sum(c['blen'] for c in change),
                     'largest_equal_blocks':sorted([{'a':bank*BANK+m.a,'b':bank*BANK+m.b,'size':m.size,'delta':m.b-m.a} for m in matches],key=lambda q:q['size'],reverse=True)[:20],
                     'changes':change[:2000]})
out['sequence']=seqbanks

# Byte pair differences, helpful for pointer byte patterns
pairs=Counter((u,v) for u,v in zip(a,b) if u!=v)
out['top_byte_substitutions']=[{'from':u,'to':v,'count':c} for (u,v),c in pairs.most_common(100)]

Path('/mnt/data/midori_rev_analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))

# TSV summaries
with open('/mnt/data/midori_bank_diff.tsv','w') as f:
    f.write('bank\tdiff_bytes\tdiff_pct\truns\tfirst_diff\tlast_diff\tlargest_run\n')
    for z in banks:
      f.write(f"{z['bank']:02X}\t{z['diff_bytes']}\t{z['diff_pct']:.4f}\t{z['runs']}\t{'' if z['first_diff'] is None else f'{z['first_diff']:05X}'}\t{'' if z['last_diff'] is None else f'{z['last_diff']:05X}'}\t{z['largest_run']}\n")

print('total diff',out['total_diff_bytes'],'runs',out['total_diff_runs'])
for z in sorted(banks,key=lambda q:q['diff_bytes'],reverse=True):
    print(f"bank {z['bank']:02X}: diff {z['diff_bytes']:5d} {z['diff_pct']:6.2f}% runs {z['runs']:4d} largest {z['largest_run']:5d} first {z['first_diff']} last {z['last_diff']}")
print('largest diff runs:')
for r in out['largest_runs'][:30]: print(tuple(hex(v) if k<2 else v for k,v in enumerate(r)))
