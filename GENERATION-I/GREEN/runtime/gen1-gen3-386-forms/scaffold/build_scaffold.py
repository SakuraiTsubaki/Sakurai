#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, struct, zlib
from pathlib import Path

ROM_SIZE = 0x100000
RUNTIME_OFFSET = 0x080000
LEGACY_MAP_OFFSET = 0x085000
DESCRIPTOR_OFFSET = 0x085200
RUNTIME_EXPECTED_SHA1 = '2ce3ef33a991d52135dbf43080787a51995cc908'
RUNTIME_EXPECTED_SIZE = 19403


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

def header_checksum(rom: bytearray) -> int:
    x=0
    for b in rom[0x134:0x14D]:
        x=(x-b-1)&0xff
    return x

def global_checksum(rom: bytearray) -> int:
    return (sum(rom[:0x14E])+sum(rom[0x150:])) & 0xffff

def set_checksums(rom: bytearray):
    rom[0x14D]=header_checksum(rom)
    rom[0x14E]=0
    rom[0x14F]=0
    g=global_checksum(rom)
    rom[0x14E]=(g>>8)&0xff
    rom[0x14F]=g&0xff

def verify_checksums(rom: bytes):
    b=bytearray(rom)
    assert b[0x14D] == header_checksum(b)
    stored=(b[0x14E]<<8)|b[0x14F]
    assert stored == global_checksum(b)

def make_legacy_map(registry: Path):
    table=[0xffff]*256
    rows=list(csv.DictReader(registry.open(encoding='utf-8',newline='')))
    kanto=[r for r in rows if int(r['national_dex'])<=151 and r['id_class']=='KANTO_LEGACY']
    assert len(kanto)==151
    for r in kanto:
        legacy=int(r['legacy_green_internal_id'])
        nat=int(r['national_dex'])
        assert 1<=legacy<=255 and 1<=nat<=151
        assert table[legacy]==0xffff
        table[legacy]=nat
    vals=sorted(v for v in table if v!=0xffff)
    assert vals==list(range(1,152))
    return b''.join(struct.pack('<H',v) for v in table), kanto

def build_descriptor(runtime: bytes, mapping: bytes):
    d=bytearray([0]*0x100)
    d[0:8]=b'G386MAP\0'
    struct.pack_into('<HH',d,0x08,1,0x100)
    struct.pack_into('<II',d,0x0C,RUNTIME_OFFSET,len(runtime))
    struct.pack_into('<II',d,0x14,LEGACY_MAP_OFFSET,len(mapping))
    struct.pack_into('<HHH',d,0x1C,386,419,151)
    d[0x22]=0x1B
    d[0x23]=0x05
    d[0x24]=0x03
    d[0x28:0x3C]=hashlib.sha1(runtime).digest()
    d[0x3C:0x50]=hashlib.sha1(mapping).digest()
    d[0x60:0x80]=b'GREEN 386+FORMS SCAFFOLD'.ljust(32,b'\0')
    crc=zlib.crc32(d[:0xFC])&0xffffffff
    struct.pack_into('<I',d,0xFC,crc)
    return bytes(d)

def build_rom(original: bytes, runtime: bytes, mapping: bytes, descriptor: bytes):
    assert len(original)==0x80000
    rom=bytearray([0xff])*ROM_SIZE
    rom[:len(original)]=original
    rom[0x147]=0x1B
    rom[0x148]=0x05
    rom[0x149]=0x03
    assert RUNTIME_OFFSET+len(runtime) <= LEGACY_MAP_OFFSET
    rom[RUNTIME_OFFSET:RUNTIME_OFFSET+len(runtime)]=runtime
    rom[LEGACY_MAP_OFFSET:LEGACY_MAP_OFFSET+len(mapping)]=mapping
    rom[DESCRIPTOR_OFFSET:DESCRIPTOR_OFFSET+len(descriptor)]=descriptor
    set_checksums(rom)
    return bytes(rom)

def ips_record(offset:int, data:bytes):
    out=bytearray()
    while data:
        chunk=data[:0xffff]; data=data[len(chunk):]
        out += offset.to_bytes(3,'big') + len(chunk).to_bytes(2,'big') + chunk
        offset += len(chunk)
    return bytes(out)

def ips_rle(offset:int, length:int, value:int):
    out=bytearray()
    while length:
        n=min(length,0xffff)
        out += offset.to_bytes(3,'big') + b'\x00\x00' + n.to_bytes(2,'big') + bytes([value])
        offset += n; length -= n
    return bytes(out)

def make_ips(original: bytes, target: bytes):
    assert len(original)==0x80000 and len(target)==ROM_SIZE
    out=bytearray(b'PATCH')
    i=0
    while i<len(original):
        if original[i]==target[i]:
            i+=1; continue
        start=i
        buf=bytearray()
        while i<len(original) and original[i]!=target[i] and len(buf)<0xffff:
            buf.append(target[i]); i+=1
        out += ips_record(start,bytes(buf))
    out += ips_rle(0x80000,0x80000,0xff)
    i=0x80000
    while i<len(target):
        if target[i]==0xff:
            i+=1; continue
        start=i; buf=bytearray()
        while i<len(target) and target[i]!=0xff and len(buf)<0xffff:
            buf.append(target[i]); i+=1
        out += ips_record(start,bytes(buf))
    out += b'EOF' + len(target).to_bytes(3,'big')
    return bytes(out)

def apply_ips(original: bytes, patch: bytes):
    assert patch[:5]==b'PATCH'
    out=bytearray(original); p=5
    while patch[p:p+3] != b'EOF':
        off=int.from_bytes(patch[p:p+3],'big'); p+=3
        size=int.from_bytes(patch[p:p+2],'big'); p+=2
        if size==0:
            n=int.from_bytes(patch[p:p+2],'big'); p+=2
            val=patch[p]; p+=1
            need=off+n
            if len(out)<need: out.extend(b'\x00'*(need-len(out)))
            out[off:off+n]=bytes([val])*n
        else:
            data=patch[p:p+size]; p+=size
            need=off+size
            if len(out)<need: out.extend(b'\x00'*(need-len(out)))
            out[off:off+size]=data
    p+=3
    if p+3<=len(patch):
        trunc=int.from_bytes(patch[p:p+3],'big')
        if trunc:
            if len(out)<trunc: out.extend(b'\x00'*(trunc-len(out)))
            else: del out[trunc:]
    return bytes(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rev0',type=Path,required=True)
    ap.add_argument('--reva',type=Path,required=True)
    ap.add_argument('--runtime',type=Path,required=True)
    ap.add_argument('--registry',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    runtime=a.runtime.read_bytes()
    assert len(runtime)==RUNTIME_EXPECTED_SIZE
    assert sha1(runtime)==RUNTIME_EXPECTED_SHA1
    assert runtime[:8]==b'G386F3\0\0'
    mapping,kanto=make_legacy_map(a.registry)
    descriptor=build_descriptor(runtime,mapping)
    (a.out/'green_legacy8_to_canonical16_map.bin').write_bytes(mapping)
    (a.out/'green_386_forms_scaffold_descriptor.bin').write_bytes(descriptor)
    with (a.out/'green_legacy8_to_canonical16_map.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['legacy_internal_id','legacy_internal_id_hex','canonical_species_id','national_dex'])
        for legacy in range(256):
            v=struct.unpack_from('<H',mapping,legacy*2)[0]
            w.writerow([legacy,f'0x{legacy:02X}','' if v==0xffff else v,'' if v==0xffff else v])
    expected={'rev0':'82c0eef40a5e2423699d9fd8ba15dfaa8b51d196','reva':'4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b'}
    manifests={}
    for tag,path in [('rev0',a.rev0),('reva',a.reva)]:
        orig=path.read_bytes(); assert sha1(orig)==expected[tag]
        target=build_rom(orig,runtime,mapping,descriptor)
        verify_checksums(target)
        diffs=[i for i in range(len(orig)) if orig[i]!=target[i]]
        allowed={0x147,0x148,0x14d,0x14e,0x14f}
        assert set(diffs)==allowed, (tag,diffs)
        assert target[RUNTIME_OFFSET:RUNTIME_OFFSET+len(runtime)]==runtime
        assert target[LEGACY_MAP_OFFSET:LEGACY_MAP_OFFSET+len(mapping)]==mapping
        assert target[DESCRIPTOR_OFFSET:DESCRIPTOR_OFFSET+len(descriptor)]==descriptor
        outrom=a.out/f'Pocket Monsters - Midori (Japan) - 386 Forms Runtime Scaffold ({tag}).gb'
        outrom.write_bytes(target)
        patch=make_ips(orig,target)
        ipsp=a.out/f'green_386_forms_runtime_scaffold_{tag}.ips'; ipsp.write_bytes(patch)
        reapplied=apply_ips(orig,patch)
        assert reapplied==target
        manifests[tag]={
          'original_sha1':sha1(orig),'output_sha1':sha1(target),'output_md5':md5(target),
          'output_size':len(target),'ips_sha1':sha1(patch),'ips_size':len(patch),
          'original_region_changed_offsets':[f'0x{x:06X}' for x in diffs],
          'header':{'cartridge_type':target[0x147],'rom_size_code':target[0x148],'ram_size_code':target[0x149],
                    'header_checksum':target[0x14d],'global_checksum':f'{(target[0x14e]<<8|target[0x14f]):04x}'},
          'ips_roundtrip':'PASS','static_checksum_verification':'PASS'
        }
    manifest={
      'schema':'green-386-forms-mbc5-scaffold-v1',
      'status':'static parameter scaffold; runtime engine hooks are NOT active yet',
      'mapper':'MBC5+RAM+BATTERY','rom_size':ROM_SIZE,'rom_banks':64,'sram_size':'32 KiB (unchanged)',
      'runtime_block':{'offset':RUNTIME_OFFSET,'bank':RUNTIME_OFFSET//0x4000,'size':len(runtime),'sha1':sha1(runtime)},
      'legacy_map':{'offset':LEGACY_MAP_OFFSET,'bank':LEGACY_MAP_OFFSET//0x4000,'size':len(mapping),'mapped_species':151,'sha1':sha1(mapping)},
      'descriptor':{'offset':DESCRIPTOR_OFFSET,'size':len(descriptor),'sha1':sha1(descriptor)},
      'identity_abi':{'species_id':'u16','form_id':'u8'},
      'canonical_species_max':386,'species_form_combinations':419,
      'roms':manifests,
      'boot_test':'NOT_RUN_NO_EMULATOR_AVAILABLE',
      'next_runtime_work':['banked G386F3 loader','party/battle species_id+form_id working records','box/save migration','personal lookup hook','wild/trainer/evolution/move/Pokedex hooks','form rules']
    }
    (a.out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    verify=[]
    verify += ['GREEN 386 + GEN III FORMS / MBC5 STATIC SCAFFOLD VERIFICATION','']
    verify += [f'Runtime block: {len(runtime)} bytes SHA1 {sha1(runtime)}',f'Legacy map: 512 bytes / 151 mapped Kanto species',f'ROM: 1 MiB / MBC5+RAM+BATTERY / 64 banks','']
    for tag,m in manifests.items():
        verify += [f'{tag}: output SHA1 {m["output_sha1"]}',f'{tag}: IPS SHA1 {m["ips_sha1"]}',f'{tag}: header/global checksum PASS',f'{tag}: IPS roundtrip PASS',f'{tag}: original 512 KiB changes only {", ".join(m["original_region_changed_offsets"])}','']
    verify += ['IMPORTANT: This proves structural embedding and deterministic patching only.','No engine hook is active yet, and no emulator boot/play test has been performed.']
    (a.out/'VERIFY.txt').write_text('\n'.join(verify)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
