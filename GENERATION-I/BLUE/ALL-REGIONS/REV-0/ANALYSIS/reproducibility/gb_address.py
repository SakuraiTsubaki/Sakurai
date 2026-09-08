#!/usr/bin/env python3
"""Convert Game Boy ROM file offsets <-> banked CPU addresses."""
import argparse
BANK=0x4000

def offset_to_bank_addr(off):
    if off < 0: raise ValueError('offset must be >= 0')
    bank=off//BANK
    return bank, off if bank==0 else 0x4000+(off%BANK)

def bank_addr_to_offset(bank,addr):
    if bank < 0: raise ValueError('bank must be >= 0')
    if bank==0:
        if not 0 <= addr < 0x4000: raise ValueError('bank 0 address must be 0000-3FFF')
        return addr
    if not 0x4000 <= addr < 0x8000: raise ValueError('switchable bank address must be 4000-7FFF')
    return bank*BANK+(addr-0x4000)

def num(s): return int(s,0)
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('offset'); a.add_argument('offset',type=num)
    b=sub.add_parser('address'); b.add_argument('bank',type=num); b.add_argument('address',type=num)
    x=p.parse_args()
    if x.cmd=='offset':
        bank,addr=offset_to_bank_addr(x.offset); print(f'bank=0x{bank:02X} address=0x{addr:04X}')
    else:
        off=bank_addr_to_offset(x.bank,x.address); print(f'offset=0x{off:06X} ({off})')
if __name__=='__main__': main()
