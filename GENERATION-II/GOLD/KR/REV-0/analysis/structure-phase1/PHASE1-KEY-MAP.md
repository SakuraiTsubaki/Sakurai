# Phase 1 Key Map — KR-REV-0

# Structural Survey Phase 1 — KR-REV-0

- Source: `Pocket Monsters Geum (Korea).gbc` (external/read-only; not part of generated corpus)
- Size: 2,097,152 bytes; banks: 128
- SHA-256: `9c273e86e6120c6a038160ccb0153b8b20425b84fc08a496281c1d1bcac492f6`
- Bank 00 reachable instruction starts: 318
- Bank 00 reachable instruction bytes: 567 / 16,384 (3.46%)
- Discovered fixed-bank labels: 45
- CFG edges within Bank 00: 51
- Long `00`/`FF` runs (>=32 bytes): 208
- Pointer-table candidates (heuristic): 1,000
- Immediate-address opcode candidates: 1,476

## Fixed Bank 00 symbols

```text
00:0000 ResetVector
00:0008 FarCall
00:0010 Bankswitch
00:0018 Rst18Trap
00:001E loc_001e
00:0020 Rst20Trap
00:0028 JumpTable
00:0038 Rst38Trap
00:003B loc_003b
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
00:0434 loc_0434
00:05CA _Start
00:05D3 loc_05d3
00:05DC loc_05dc
00:0603 loc_0603
00:0612 loc_0612
00:068D loc_068d
00:0698 Serial
00:06C0 loc_06c0
00:06C5 loc_06c5
00:06CF loc_06cf
00:06DE loc_06de
00:06EE loc_06ee
00:06F1 loc_06f1
00:06F9 loc_06f9
00:08D2 Joypad
00:1F10 loc_1f10
00:2EAE FarCall_hl
00:2ECF loc_2ecf
00:2ED0 loc_2ed0
00:31A7 loc_31a7
00:31AD loc_31ad
00:31F4 loc_31f4
00:31F8 loc_31f8
00:31F9 loc_31f9
00:3D1A loc_3d1a
```

## Header constants

```asm
; Declarative cartridge-header metadata. No ROM payload bytes are embedded.
DEF ROM_TITLE EQUS "POKEMON_GLDAAUK"
DEF CGB_FLAG EQU $C0
DEF CARTRIDGE_TYPE EQU $10
DEF ROM_SIZE_CODE EQU $06
DEF RAM_SIZE_CODE EQU $03
DEF DESTINATION_CODE EQU $01
DEF MASK_ROM_VERSION EQU $00
DEF HEADER_CHECKSUM EQU $08
DEF GLOBAL_CHECKSUM EQU $778A
```

## Reachable CFG coverage ranges

```csv
start,end,length
0x0000,0x0003,4
0x0008,0x000A,3
0x0010,0x0015,6
0x0018,0x0024,13
0x0028,0x0032,11
0x0038,0x003E,7
0x0040,0x0042,3
0x0048,0x004A,3
0x0050,0x0050,1
0x0058,0x005A,3
0x0060,0x0062,3
0x0100,0x0103,4
0x0150,0x0167,24
0x032E,0x033B,14
0x041B,0x0435,27
0x05CA,0x06FD,308
0x08D2,0x08D2,1
0x1F10,0x1F1B,12
0x2EAE,0x2EF2,69
0x31A7,0x31B1,11
0x31F4,0x31FF,12
0x3D1A,0x3D35,28
```

The symbol map contains stable vector semantics plus ROM-local CFG-derived labels. Unknown targets remain `loc_XXXX`; they are not force-named from another localization.
