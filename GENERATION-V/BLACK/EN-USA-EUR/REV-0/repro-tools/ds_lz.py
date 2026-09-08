#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,json

def dec10(src):
    if not src or src[0]!=0x10: raise ValueError('not LZ10')
    size=src[1]|src[2]<<8|src[3]<<16; pos=4; out=bytearray()
    while len(out)<size:
        flags=src[pos];pos+=1
        for bit in range(8):
            if len(out)>=size:break
            if flags&(0x80>>bit):
                b1,b2=src[pos],src[pos+1];pos+=2;ln=(b1>>4)+3;disp=((b1&15)<<8|b2)+1
                if disp>len(out):raise ValueError('bad displacement')
                for _ in range(ln):out.append(out[-disp])
            else:out.append(src[pos]);pos+=1
    return bytes(out[:size])

def dec11(src):
    if not src or src[0]!=0x11: raise ValueError('not LZ11')
    size=src[1]|src[2]<<8|src[3]<<16;pos=4
    if size==0:size=int.from_bytes(src[pos:pos+4],'little');pos+=4
    out=bytearray()
    while len(out)<size:
        flags=src[pos];pos+=1
        for bit in range(8):
            if len(out)>=size:break
            if flags&(0x80>>bit):
                b1=src[pos];hi=b1>>4
                if hi==0:
                    b2,b3=src[pos+1],src[pos+2];pos+=3;ln=((b1&15)<<4|(b2>>4))+0x11;disp=((b2&15)<<8|b3)+1
                elif hi==1:
                    b2,b3,b4=src[pos+1],src[pos+2],src[pos+3];pos+=4;ln=((b1&15)<<12|b2<<4|(b3>>4))+0x111;disp=((b3&15)<<8|b4)+1
                else:
                    b2=src[pos+1];pos+=2;ln=hi+1;disp=((b1&15)<<8|b2)+1
                if disp>len(out):raise ValueError('bad displacement')
                for _ in range(ln):out.append(out[-disp])
            else:out.append(src[pos]);pos+=1
    return bytes(out[:size])

def kind(b):
    t={b'RGCN':'NCGR',b'RLCN':'NCLR',b'RCSN':'NSCR',b'RECN':'NCER',b'RNAN':'NANR',b'BTX0':'BTX0',b'BMD0':'BMD0',b'BCA0':'BCA0',b'BTA0':'BTA0',b'BTP0':'BTP0',b'BMA0':'BMA0',b'BVA0':'BVA0',b'NARC':'NARC'}
    return t.get(b[:4],b[:4].hex().upper())

def run(root):
    root=Path(root);rows=[];errors=[]
    for p in (root/'narc').rglob('*.bin'):
        b=p.read_bytes()
        if not b or b[0] not in (0x10,0x11):continue
        rel=p.relative_to(root/'narc')
        try:d=dec10(b) if b[0]==0x10 else dec11(b)
        except Exception as e:errors.append({'path':rel.as_posix(),'error':str(e)});continue
        q=root/'decompressed'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(d)
        rows.append({'path':rel.as_posix(),'codec':f'LZ{b[0]:02X}','compressed_size':len(b),'decompressed_size':len(d),'type':kind(d),'sha256':hashlib.sha256(d).hexdigest().upper()})
    a=root/'analysis';a.mkdir(exist_ok=True)
    with (a/'lz_decompressed_inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['path','codec','compressed_size','decompressed_size','type','sha256']);w.writeheader();w.writerows(rows)
    with (a/'lz_decompression_errors.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['path','error']);w.writeheader();w.writerows(errors)
    s={'decompressed_files':len(rows),'errors':len(errors),'compressed_bytes':sum(r['compressed_size'] for r in rows),'decompressed_bytes':sum(r['decompressed_size'] for r in rows)}
    (a/'lz_decompression_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('workspace');run(ap.parse_args().workspace)
