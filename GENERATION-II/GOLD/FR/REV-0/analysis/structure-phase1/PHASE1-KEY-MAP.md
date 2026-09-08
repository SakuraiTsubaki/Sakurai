# Phase 1 Key Map — FR-REV-0

# Structural Survey Phase 1 — FR-REV-0

- Source: `Pokemon - Version Or (France).gbc` (external/read-only; not part of generated corpus)
- Size: 2,097,152 bytes; banks: 128
- SHA-256: `6103cadf2ae505f4b489a8a414c8db27a2307d797ddf8a3a848659b591dd4023`
- Bank 00 reachable instruction starts: 339
- Bank 00 reachable instruction bytes: 588 / 16,384 (3.59%)
- Discovered fixed-bank labels: 46
- CFG edges within Bank 00: 53
- Long `00`/`FF` runs (>=32 bytes): 182
- Pointer-table candidates (heuristic): 1,000
- Immediate-address opcode candidates: 1,407

## Fixed Bank 00 symbols

```text
00:0000 ResetVector
00:0008 FarCall
00:0010 Bankswitch
00:0018 Rst18Trap
00:0020 Rst20Trap
00:0028 JumpTable
00:0038 Rst38Trap
00:0040 VBlankVector
00:0048 LCDVector
00:0050 TimerVector
00:0058 SerialVector
00:0060 JoypadVector
00:0100 Start
00:0150 VBlank
00:032E loc_032e
00:0333 loc_0333
00:041B LCD
00:0430 loc_0430
00:05C6 _Start
00:05CD loc_05cd
00:05CF loc_05cf
00:05F6 loc_05f6
00:0605 loc_0605
00:068E loc_068e
00:0699 loc_0699
00:069E loc_069e
00:06A2 loc_06a2
00:06AA Serial
00:06D2 loc_06d2
00:06D7 loc_06d7
00:06E1 loc_06e1
00:06F0 loc_06f0
00:0700 loc_0700
00:0703 loc_0703
00:070B loc_070b
00:08DF Joypad
00:1EC5 loc_1ec5
00:2E39 FarCall_hl
00:2E5A loc_2e5a
00:2E5B loc_2e5b
00:3111 loc_3111
00:3117 loc_3117
00:315E loc_315e
00:3162 loc_3162
00:3163 loc_3163
00:3CDE loc_3cde
```

## Header constants

```asm
; Declarative cartridge-header metadata. No ROM payload bytes are embedded.
DEF ROM_TITLE EQUS "POKEMON_GLDAAUF"
DEF CGB_FLAG EQU $80
DEF CARTRIDGE_TYPE EQU $10
DEF ROM_SIZE_CODE EQU $06
DEF RAM_SIZE_CODE EQU $03
DEF DESTINATION_CODE EQU $01
DEF MASK_ROM_VERSION EQU $00
DEF HEADER_CHECKSUM EQU $4A
DEF GLOBAL_CHECKSUM EQU $6FC6
```

## Reachable CFG coverage ranges

```csv
start,end,length
0x0000,0x0003,4
0x0008,0x000A,3
0x0010,0x0015,6
0x0018,0x0032,27
0x0038,0x0042,11
0x0048,0x004A,3
0x0050,0x0050,1
0x0058,0x005A,3
0x0060,0x0062,3
0x0100,0x0103,4
0x0150,0x0167,24
0x032E,0x033B,14
0x041B,0x0431,23
0x05C6,0x069C,215
0x069E,0x070F,114
0x08DF,0x08DF,1
0x1EC5,0x1ED0,12
0x2E39,0x2E7D,69
0x3111,0x311B,11
0x315E,0x3169,12
0x3CDE,0x3CF9,28
```

The symbol map contains stable vector semantics plus ROM-local CFG-derived labels. Unknown targets remain `loc_XXXX`; they are not force-named from another localization.
