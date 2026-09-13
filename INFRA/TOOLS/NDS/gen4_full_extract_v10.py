#!/usr/bin/env python3
import argparse,csv,hashlib,json,struct,collections
from pathlib import Path
RELEASES={
'DIAMOND':('ADAE-HV5','US','en'),'PEARL':('APAE-HV5','US','en'),
'PLATINUM':('CPUK-HV0','KR','ko'),'HEARTGOLD':('IPKK-HV0','KR','ko'),
'SOULSILVER':('IPGK-HV0','KR','ko')}
def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def kind(data):
 m=data[:4]; mp={b'NARC':'NARC',b'RGCN':'NCGR',b'RLCN':'NCLR',b'RCSN':'NSCR',b'RECN':'NCER',b'RNAN':'NANR',b'SDAT':'SDAT',b'SSEQ':'SSEQ',b'SSAR':'SSAR',b'SBNK':'SBNK',b'SWAR':'SWAR',b'BMD0':'NSBMD',b'BTX0':'NSBTX',b'BCA0':'NSBCA',b'BTP0':'NSBTP',b'BTA0':'NSBTA',b'BMA0':'NSBMA'}
 if m in mp:return mp[m]
 if data[:1]==b'\x10':return 'LZ10'
 if data[:1]==b'\x11':return 'LZ11'
 return 'BINARY'
def parse_fnt(rom,off,size):
 dcount=u16(rom,off+6); dirs={}
 for i in range(dcount):
  p=off+i*8; dirs[0xF000+i]=(u32(rom,p),u16(rom,p+4),u16(rom,p+6))
 paths={}; seen=set()
 def walk(did,prefix):
  if did in seen or did not in dirs:return
  seen.add(did); sub,first,_=dirs[did]; p=off+sub; fid=first
  while p<off+size:
   n=rom[p]; p+=1
   if n==0:break
   isdir=bool(n&0x80); ln=n&0x7f; name=rom[p:p+ln].decode('ascii','replace'); p+=ln
   if isdir: child=u16(rom,p); p+=2; walk(child,prefix+name+'/')
   else: paths[fid]=prefix+name; fid+=1
 walk(0xF000,''); return paths,dcount
def overlays(rom,off,size):
 out=[]
 if not off or not size:return out
 for i in range(0,size,32):
  if i+32>size:break
  p=off+i; out.append({'overlay_id':u32(rom,p),'ram_address':u32(rom,p+4),'ram_size':u32(rom,p+8),'bss_size':u32(rom,p+12),'static_init_start':u32(rom,p+16),'static_init_end':u32(rom,p+20),'file_id':u32(rom,p+24),'reserved':u32(rom,p+28)})
 return out
def narc_layout(data):
 if data[:4]!=b'NARC' or len(data)<16:return []
 pos=u16(data,12); nsec=u16(data,14); fat=img=None
 for _ in range(nsec):
  if pos+8>len(data):break
  m=data[pos:pos+4]; sz=u32(data,pos+4)
  if sz<8 or pos+sz>len(data):break
  if m in (b'BTAF',b'FATB'):fat=(pos,sz)
  if m in (b'GMIF',b'FIMG'):img=(pos,sz)
  pos+=sz
 if not fat or not img:return []
 p,s=fat; cnt=u16(data,p+8); ep=p+12; base=img[0]+8; out=[]
 for i in range(cnt):
  if ep+8>p+s:break
  st,en=u32(data,ep),u32(data,ep+4); ep+=8; b=data[base+st:base+en]
  out.append({'member_index':i,'start':st,'end':en,'size':len(b),'kind':kind(b)})
 return out
def write_csv(path,rows,fields=None):
 if not rows:return
 fields=fields or list(rows[0]);
 with open(path,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def process(game,path,out):
 release,market,language=RELEASES[game]; rom=Path(path).read_bytes(); sha256=hashlib.sha256(rom).hexdigest(); dump='DUMP-SHA256-'+sha256[:16].upper(); gd=out/game; gd.mkdir(parents=True,exist_ok=True)
 fnt_off,fnt_size=u32(rom,0x40),u32(rom,0x44); fat_off,fat_size=u32(rom,0x48),u32(rom,0x4c); paths,dcount=parse_fnt(rom,fnt_off,fnt_size)
 ov9_off,ov9_size=u32(rom,0x50),u32(rom,0x54); ov7_off,ov7_size=u32(rom,0x58),u32(rom,0x5c)
 fat=[]; narcs=[]; layouts=[]; types=collections.Counter()
 for fid in range(fat_size//8):
  st,en=u32(rom,fat_off+fid*8),u32(rom,fat_off+fid*8+4); b=rom[st:en]; k=kind(b); types[k]+=1
  row={'file_id':fid,'path':paths.get(fid,''),'start':st,'end':en,'size':len(b),'kind':k,'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'magic_hex':b[:8].hex()}; fat.append(row)
  if k=='NARC':
   ms=narc_layout(b); narcs.append({'file_id':fid,'path':row['path'],'size':len(b),'member_count':len(ms),'sha1':row['sha1']})
   for m in ms: layouts.append({'archive_file_id':fid,**m})
 ovs={'arm9':overlays(rom,ov9_off,ov9_size),'arm7':overlays(rom,ov7_off,ov7_size)}
 header={'schema':'sakurai.nds-census.v10','game_id':game,'release_id':release,'dump_id':dump,'market':market,'language':language,'rom_size':len(rom),'title':rom[:12].decode('ascii','replace').rstrip('\0'),'game_code':rom[12:16].decode('ascii','replace'),'maker_code':rom[16:18].decode('ascii','replace'),'unit_code':rom[18],'device_capacity':rom[20],'header_version':rom[30],'fnt':{'offset':fnt_off,'size':fnt_size,'directory_count':dcount,'named_file_count':len(paths)},'fat':{'offset':fat_off,'size':fat_size,'entry_count':fat_size//8},'overlay9':{'offset':ov9_off,'size':ov9_size,'count':len(ovs['arm9'])},'overlay7':{'offset':ov7_off,'size':ov7_size,'count':len(ovs['arm7'])},'narc_count':len(narcs),'narc_member_count':len(layouts),'file_kind_counts':dict(types),'hashes':{'sha1':hashlib.sha1(rom).hexdigest(),'sha256':sha256},'rom_binary_committed':False}
 (gd/'header.json').write_text(json.dumps(header,ensure_ascii=False,indent=2)+'\n'); (gd/'fnt-map.json').write_text(json.dumps({'directory_count':dcount,'paths':paths},ensure_ascii=False,indent=2)+'\n'); (gd/'overlays.json').write_text(json.dumps(ovs,ensure_ascii=False,indent=2)+'\n')
 write_csv(gd/'fat-files.csv',fat); write_csv(gd/'narc-archives.csv',narcs); write_csv(gd/'narc-layout.csv',layouts)
 return header,fat
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('inputs',nargs='+',help='GAME=/path/to/source.nds'); a=ap.parse_args(); out=Path(a.out);out.mkdir(parents=True,exist_ok=True); allfiles=[]; summaries={}
 for item in a.inputs:
  game,path=item.split('=',1); game=game.upper(); h,f=process(game,path,out); summaries[game]=h; allfiles.extend((game,r) for r in f)
 by=collections.defaultdict(list)
 for g,r in allfiles: by[r['sha1']].append({'game':g,'file_id':r['file_id'],'path':r['path'],'size':r['size'],'kind':r['kind']})
 groups=[{'sha1':s,'occurrences':v} for s,v in by.items() if len({x['game'] for x in v})>1]
 (out/'cross-game-identical-files.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n'); (out/'summary.json').write_text(json.dumps({'schema':'gen4.core-five-census.v10','games':summaries,'cross_game_identical_hash_groups':len(groups)},ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
