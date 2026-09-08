# Phase 1 Key Map — JP-REV-A

# Structural Survey Phase 1 — JP-REV-A

- Source: `Pocket Monsters Kin (Japan) (Rev A).gbc` (external/read-only; not part of generated corpus)
- Size: 1,048,576 bytes; banks: 64
- SHA-256: `27a07a1d3faf9c6a0b1b60d5e88ee3a4159a751a47b4c46ab09f1202d52bac3e`
- Bank 00 reachable instruction starts: 339
- Bank 00 reachable instruction bytes: 588 / 16,384 (3.59%)
- Discovered fixed-bank labels: 46
- CFG edges within Bank 00: 53
- Long `00`/`FF` runs (>=32 bytes): 105
- Pointer-table candidates (heuristic): 1,000
- Immediate-address opcode candidates: 1,381

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
00:05C5 _Start
00:05CC loc_05cc
00:05CE loc_05ce
00:05F5 loc_05f5
00:0604 loc_0604
00:068D loc_068d
00:0698 loc_0698
00:069D loc_069d
00:06A1 loc_06a1
00:06A9 Serial
00:06D1 loc_06d1
00:06D6 loc_06d6
00:06E0 loc_06e0
00:06EF loc_06ef
00:06FF loc_06ff
00:0702 loc_0702
00:070A loc_070a
00:08DE Joypad
00:1E60 loc_1e60
00:2DE3 FarCall_hl
00:2E04 loc_2e04
00:2E05 loc_2e05
00:30BB loc_30bb
00:30C1 loc_30c1
00:3108 loc_3108
00:310C loc_310c
00:310D loc_310d
00:3C70 loc_3c70
```

## Header constants

```asm
; Declarative cartridge-header metadata. No ROM payload bytes are embedded.
DEF ROM_TITLE EQUS "POKEMON_GLDAAUJ"
DEF CGB_FLAG EQU $80
DEF CARTRIDGE_TYPE EQU $10
DEF ROM_SIZE_CODE EQU $05
DEF RAM_SIZE_CODE EQU $03
DEF DESTINATION_CODE EQU $00
DEF MASK_ROM_VERSION EQU $01
DEF HEADER_CHECKSUM EQU $47
DEF GLOBAL_CHECKSUM EQU $8460
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
0x05C5,0x069B,215
0x069D,0x070E,114
0x08DE,0x08DE,1
0x1E60,0x1E6B,12
0x2DE3,0x2E27,69
0x30BB,0x30C5,11
0x3108,0x3113,12
0x3C70,0x3C8B,28
```

The symbol map contains stable vector semantics plus ROM-local CFG-derived labels. Unknown targets remain `loc_XXXX`; they are not force-named from another localization.
