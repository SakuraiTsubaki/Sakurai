; Generation V personal-data accessor core for a Gen II engine.
;
; This layer intentionally accepts a 16-bit PROJECT species ID in DE.
; It does not pretend the original 8-bit Gen II party/save species fields have
; already been widened. Native Gen II data remains a separate profile.

SECTION "Gen5 Personal Adapter", ROMX

; Gen V type IDs 0..16 -> Gen II numeric type IDs.
; Gen II keeps the historical gap/ordering (BUG=$07, FIRE=$14, etc.).
Gen5ToGen2TypeMap::
	db $00 ; Normal
	db $01 ; Fighting
	db $02 ; Flying
	db $03 ; Poison
	db $04 ; Ground
	db $05 ; Rock
	db $07 ; Bug
	db $08 ; Ghost
	db $09 ; Steel
	db $14 ; Fire
	db $15 ; Water
	db $16 ; Grass
	db $17 ; Electric
	db $18 ; Psychic
	db $19 ; Ice
	db $1a ; Dragon
	db $1b ; Dark

; Read one byte from a columnar species table.
; Input:
;   A  = bank(table)
;   HL = table base + field offset within each entry
;   DE = 16-bit project species ID (0..649)
;   C  = entry stride in bytes (1..16)
; Output:
;   A  = byte value
; Clobbers: HL, C
Gen5ReadSpeciesByte::
	push af
.loop
	add hl, de
	dec c
	jr nz, .loop
	pop af
	jp GetFarByte

; Same addressing rule, returning a little-endian word in HL.
; Input is identical to Gen5ReadSpeciesByte.
; Output: HL = word value
; Clobbers: C
Gen5ReadSpeciesWord::
	push af
.loop
	add hl, de
	dec c
	jr nz, .loop
	pop af
	jp GetFarWord

; ---- Scalar accessors -----------------------------------------------------

Gen5GetCatchRate::
	ld hl, Gen5PersonalCatchRate
	ld a, BANK(Gen5PersonalCatchRate)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetGenderRatio::
	ld hl, Gen5PersonalGenderRatio
	ld a, BANK(Gen5PersonalGenderRatio)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetHatchCounter::
	ld hl, Gen5PersonalHatchCounter
	ld a, BANK(Gen5PersonalHatchCounter)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetBaseFriendship::
	ld hl, Gen5PersonalBaseFriendship
	ld a, BANK(Gen5PersonalBaseFriendship)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetGrowthRate::
	ld hl, Gen5PersonalGrowthRate
	ld a, BANK(Gen5PersonalGrowthRate)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetEscapeRate::
	ld hl, Gen5PersonalEscapeRate
	ld a, BANK(Gen5PersonalEscapeRate)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetBodyColor::
	ld hl, Gen5PersonalBodyColor
	ld a, BANK(Gen5PersonalBodyColor)
	ld c, 1
	jp Gen5ReadSpeciesByte

Gen5GetBaseExp16::
	ld hl, Gen5PersonalBaseExp
	ld a, BANK(Gen5PersonalBaseExp)
	ld c, 2
	jp Gen5ReadSpeciesWord

Gen5GetHeight::
	ld hl, Gen5PersonalHeight
	ld a, BANK(Gen5PersonalHeight)
	ld c, 2
	jp Gen5ReadSpeciesWord

Gen5GetWeight::
	ld hl, Gen5PersonalWeight
	ld a, BANK(Gen5PersonalWeight)
	ld c, 2
	jp Gen5ReadSpeciesWord

; ---- Indexed fields ------------------------------------------------------

; Input: DE=species, B=stat index 0..5. Output A=base stat.
Gen5GetBaseStat::
	ld hl, Gen5PersonalBaseStats
	ld a, b
	ld c, a
	ld b, 0
	add hl, bc
	ld a, BANK(Gen5PersonalBaseStats)
	ld c, 6
	jp Gen5ReadSpeciesByte

; Input: DE=species, B=type slot 0..1. Output A=Gen II type ID.
Gen5GetType::
	ld hl, Gen5PersonalTypes
	ld a, b
	ld c, a
	ld b, 0
	add hl, bc
	ld a, BANK(Gen5PersonalTypes)
	ld c, 2
	call Gen5ReadSpeciesByte
	ld e, a
	ld d, 0
	ld hl, Gen5ToGen2TypeMap
	add hl, de
	ld a, BANK(Gen5ToGen2TypeMap)
	jp GetFarByte

; Input: DE=species, B=ability slot 0 normal1 / 1 normal2 / 2 hidden.
; Output: A=raw Gen V ability ID. Effect engine is a separate subsystem.
Gen5GetAbilityRaw::
	ld hl, Gen5PersonalAbilities
	ld a, b
	ld c, a
	ld b, 0
	add hl, bc
	ld a, BANK(Gen5PersonalAbilities)
	ld c, 3
	jp Gen5ReadSpeciesByte

; Input: DE=species, B=item slot 0..2. Output HL=raw Gen V item ID.
; Raw item IDs must go through the target item-ID map before storage/use.
Gen5GetHeldItemRaw::
	ld hl, Gen5PersonalHeldItems
	ld a, b
	add a
	ld c, a
	ld b, 0
	add hl, bc
	ld a, BANK(Gen5PersonalHeldItems)
	ld c, 6
	jp Gen5ReadSpeciesWord
