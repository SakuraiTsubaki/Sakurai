# Pokémon Crystal Original ROM Limit Audit

Direct measurements from the seven project ROM images. Originals were read only.

## Common hard limits

- ROM image: 2 MiB, 128 x 16 KiB banks on every source ROM.

- International SRAM header: 32 KiB (4 x 8 KiB). Japanese SRAM header: 64 KiB (8 x 8 KiB).

- Species identity is 8-bit in the original mon structures and core routines. Vanilla valid species are 1..251; $FD is EGG.

- BaseData: 251 records x 32 bytes = 8,032 bytes. Extracted BaseData is byte-identical in all seven ROMs (SHA-1 33b3dad88e67289252d419cc56248dfbf4ae7887).

- Pokedex seen/caught: 251-bit arrays (32 bytes each). 1025 species require 129 bytes each.

- ROM bank identity is 8-bit in the engine, so the natural existing-engine bank namespace is 256 banks = 4 MiB. Going beyond that requires a bank-addressing redesign.

- BoxMon structure is 32 bytes. International box = 0x450 bytes, 20 mons; 7 boxes use 7,728 of 8,192 bytes in one SRAM bank. A single combined 16-bit mon/entity ID can fit after widening; separate Species16+Form16 does not fit the same 7-box packing without further changes.

- Pokemon display name budget in the international engine is 10 characters (MON_NAME_LENGTH 11 including terminator/storage convention). Dex number UI is three digits.

- Move and item IDs are 8-bit. Gen II has 251 moves; $FF is used as a special move value. TM/HM/tutor compatibility occupies 8 bytes in each 32-byte BaseData record (60 defined flags).

- Base stats, catch rate, base EXP, held item IDs, gender, egg cycles, growth index are byte-sized. In the original 251 records HP already reaches 255 (Blissey) and base EXP reaches 255 (Chansey/Blissey).


## ROM-specific measurements


| Build | SRAM | BaseData offset | GetBaseData | Fully zero banks | trailing-zero planning slack* |
|---|---:|---:|---:|---|---:|
| EN v1.1 | 32 KiB | 0x51424 | 0x3856 | 75 76 79 7A | 427.0 KiB |
| JP v1.0 | 64 KiB | 0x514BA | 0x3826 | 60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B 7C | 600.0 KiB |
| ES v1.0 | 32 KiB | 0x5142D | 0x3840 | 7A | 421.5 KiB |
| DE v1.0 | 32 KiB | 0x5140E | 0x3840 | 7A | 388.2 KiB |
| EN v1.0 | 32 KiB | 0x51424 | 0x3856 | 75 76 79 7A | 427.0 KiB |
| FR v1.0 | 32 KiB | 0x51417 | 0x3843 | 7A | 444.4 KiB |
| IT v1.0 | 32 KiB | 0x51433 | 0x3844 | 7A | 436.1 KiB |


\* Planning metric only: sum of bank-tail zero runs >=256 bytes. Do not treat every byte as safe free space until pointer/reference mapping confirms it.


## Storage arithmetic for the 1025 / 1351 / 1579 design

- 1025 Species Seen flags: ceil(1025/8) = 129 bytes; Caught = another 129 bytes. Increase vs original pair = 194 bytes.

- Current save and backup areas each have 0x18A (394) bytes of explicit padding after game data in the disassembly layout, so the Species-only 1025-bit dex expansion can fit by consuming padding.

- Original international box: 1104 bytes. With a 16-bit combined entity ID both in the box list and BoxMon records: 1145 bytes; 7 boxes = 8015 bytes, leaving 177 bytes in an 8 KiB SRAM bank.

- Adding a separate 16-bit form field would make a box 1185 bytes; 7 boxes = 8295 bytes, 103 bytes over one SRAM bank.
