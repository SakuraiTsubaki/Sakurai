# BANK 01 integrated audit + disassembly map — Pokémon Silver multi-region

## Scope
- ROM offset: `0x004000–0x007FFF`
- CPU-visible window while bank 01 is selected: `$4000–$7FFF`
- Method: original-ROM byte audit and semantic disassembly are performed in the same pass. Linear opcode listings are evidence only; data/text/pointer regions override mechanical decoding.

## Bank statistics
| Build | SHA-1 | Entropy | Non-zero bytes | Last non-zero |
|---|---|---:|---:|---|
| KR | `ba4b431fdd955dcdb737d67dcf37345efdc19241` | 5.9783 | 12,163 | `$75ED` |
| JP0 | `d867e843bb8f83b6bd70bbed0c698b36f4b229a0` | 6.8886 | 14,670 | `$7FCD` |
| JPA | `0d5d2abae58e8b9f1b1d638ec9e3a59deefee46c` | 6.8618 | 14,567 | `$7F63` |
| EN | `c40bb790434b1f5437964a948164a130ac6646c9` | 5.9274 | 11,956 | `$7513` |
| DE | `433e10c3c846cae709538069108da188a61e38d5` | 5.9493 | 12,010 | `$754C` |
| FR | `2391a968e51162079d4c40562498425995ee2d77` | 5.9596 | 12,005 | `$7546` |
| IT | `782cb365bf42980902c100049fab677900f3bbc7` | 5.9492 | 12,003 | `$7545` |
| ES | `7cbb0e27172fb10752b48373bb35f40746ee1c71` | 5.9585 | 12,025 | `$755C` |

## Confirmed semantic boundaries
| Label / section | KR | JP0 | JPA | EN | DE | FR | IT | ES | Type |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `PlaceWaitingText` | `$4000` | `$4000` | `$4000` | `$4000` | `$4000` | `$4000` | `$4000` | `$4000` | CODE |
| `WriteOAMDMACodeToHRAM` | `$4034` | `$4032` | `$4032` | `$4032` | `$4033` | `$4032` | `$4031` | `$4030` | CODE |
| `OAMDMACode` | `$4042` | `$4040` | `$4040` | `$4040` | `$4041` | `$4040` | `$403F` | `$403E` | CODE copied to HRAM |
| `Facings` | `$404C` | `$404A` | `$404A` | `$404A` | `$404B` | `$404A` | `$4049` | `$4048` | POINTER+OAM DATA |
| `SpriteMovementData` | `$4276` | `$4274` | `$4274` | `$4274` | `$4275` | `$4274` | `$4273` | `$4272` | DATA |
| `DeleteMapObject` | `$435A` | `$4358` | `$4358` | `$4358` | `$4359` | `$4358` | `$4357` | `$4356` | CODE / map_objects |
| `MainMenu` | `$5A5B` | `$5A4D` | `$5A4D` | `$5A4D` | `$5A4E` | `$5A4D` | `$5A4C` | `$5A4B` | CODE+TEXT/DATA |
| `NewGame` | `$5C4B` | `$5C1A` | `$5C1A` | `$5C1E` | `$5C3C` | `$5C35` | `$5C38` | `$5C3D` | CODE+TEXT/DATA / intro_menu |
| `ReanchorBGMap_NoOAMUpdate` | `$65F0` | `$6718` | `$6718` | `$6517` | `$654F` | `$654C` | `$6549` | `$6561` | CODE / init_map |
| `LearnMove` | `$6686` | `$67AE` | `$67AE` | `$65AD` | `$65E5` | `$65E2` | `$65DF` | `$65F7` | CODE+text commands |
| `CorrectNickErrors` | `$681D` | `$6A36` | `$6A36` | `$6744` | `$677C` | `$6779` | `$6776` | `$678E` | CODE+validation table |
| `_Multiply` | `$685D` | `$6A75` | `$6A75` | `$6783` | `$67BB` | `$67B8` | `$67B5` | `$67CD` | CODE / math |
| `ItemAttributes` | `$6940` | `$6B58` | `$6B58` | `$6866` | `$689E` | `$689B` | `$6898` | `$68B0` | DATA 256x7 bytes |
| `CanObjectMoveInDirection` | `$7040` | `$79B0` | `$79B0` | `$6F66` | `$6F9E` | `$6F9B` | `$6F98` | `$6FB0` | CODE / npc_movement |
| `GetFirstPokemonHappiness` | `$730C` | `$7C7C` | `$7C7C` | `$7232` | `$726A` | `$7267` | `$7264` | `$727C` | CODE+DATA / happiness_egg |
| `GiveShuckle` | `$7481` | `$7DF1` | `$7DF1` | `$73A7` | `$73DF` | `$73DC` | `$73D9` | `$73F1` | CODE+TEXT / shuckle |
| `BillsGrandfather` | `$756B` | `$7EE1` | `$7EE1` | `$7491` | `$74CA` | `$74C4` | `$74C3` | `$74DA` | CODE+DATA / haircut |
| `LastNonZero` | `$75ED` | `$7FCD` | `$7F63` | `$7513` | `$754C` | `$7546` | `$7545` | `$755C` | END |

## Front-of-bank disassembly, verified against the KR source
The first bank routine is not guessed from a linear decoder. The actual KR bytes map to the existing semantic source as follows:

```asm
; KR BANK $01
PlaceWaitingText:          ; $4000
    ld hl, $c457
    ld b, $02
    ld c, $0b
    ld a, [$d1d3]
    and a
    jr z, $4012
    call $0f12
    jr $4017
    ld a, $10
    call $2ed0
    ld hl, $c482
    ld de, $4025
    call $0f6f
    ld c, $32
    jp $033c

.Waiting:                ; $4025-$4032
    ; Korean encoded string: "통신 대기중!@"

DummyPredef1:             ; $4033
    ret

WriteOAMDMACodeToHRAM:    ; $4034
    ld c, $80
    ld b, $0a
    ld hl, $4042
.copy
    ld a, [hli]
    ldh [c], a
    inc c
    dec b
    jr nz, .copy
    ret

OAMDMACode:               ; $4042-$404b
    ld a, $c3
    ldh [$46], a
    ld a, $28
.wait
    dec a
    jr nz, .wait
    ret
```

At `$404C` the bytes stop being instructions: they are the `Facings` pointer table and OAM-facing records. Treating `$404C` as code produces illegal/meaningless opcodes, which is exactly why the semantic pass must accompany bank auditing.

### Data boundaries established from structure
- `Facings`: KR `$404C–$4275` (554 bytes total: 66-byte pointer table + 488 bytes of OAM-facing records).
- `SpriteMovementData`: KR `$4276–$4359` (228 bytes = 38 records × 6 bytes).
- `DeleteMapObject` begins at KR `$435A`, proving the exact DATA→CODE transition.
- `ItemAttributes`: KR `$6940–$703F`; exactly `0x700` bytes = 256 item records × 7 bytes. `CanObjectMoveInDirection` starts immediately at `$7040`.

## Localization-induced relocation
All eight builds retain the same broad semantic sequence, but variable-length localized strings shift later addresses. Even in the first 0x50 bytes: KR `Facings=$404C`, EN/JP=`$404A`, DE=`$404B`, IT=`$4049`, ES=`$4048`. Therefore same-index byte comparison alone is insufficient; label-to-label mapping is required.

## Korean-specific code
`CorrectNickErrors` starts at KR `$681D`. Unlike the non-Korean routine, it counts both remaining bytes and remaining characters, detects two-byte Hangul characters (`cp $0c` branch), and prevents truncation in the middle of a two-byte character. This is a true localization-engine code change, not merely translated data.

## JP Rev0 → RevA
BANK 01 has 103 changed bytes, concentrated in four spans:
- `$7F64–$7F6B` (8 changed bytes)
- `$7F6D–$7FBD` (81 changed bytes)
- `$7FBF–$7FC9` (11 changed bytes)
- `$7FCB–$7FCD` (3 changed bytes)

Rev A has zero padding from `$7F64` onward while Rev0 retains a second block through `$7FCD`. The retained Rev0 bytes strongly resemble an extra/duplicate tail routine/data block and are marked **revision-specific residue candidate** until cross-reference analysis proves whether it is reachable. Do not label it a bug fix yet.

## Disassembly state
- Full 16 KiB LR35902 *mechanical* listings have been generated for all 8 BANK 01 images.
- Confirmed CODE/DATA/TEXT boundaries above supersede the mechanical listing in those ranges.
- Remaining BANK 01 work is symbol-by-symbol naming and reachability analysis inside each confirmed source section; no blind linear decode will be promoted to final source.
- Completion gate for this bank: all `$4000–$7FFF` bytes classified, semantic source emitted, no opaque original-ROM include, and reconstructed bank SHA-1 matches the corresponding source ROM.
