	or c
	jr z, .done
	dec bc
	ld h, b
	ld l, c
	add hl, hl
	push hl
	add hl, hl
	add hl, hl
	add hl, hl
	add hl, hl
	pop de
	ld a, l
	sub e
	ld l, a
	ld a, h
	sbc d
	ld h, a ; *30
	ld de, G386Gen3PersonalTable
	add hl, de
	inc hl
	inc hl
	ld de, wMonHBaseHP
	ld b, 4
.copy4
	ld a, [hli]
	ld [de], a
	inc de
	dec b
	jr nz, .copy4
	ld a, [hli] ; SpA
	ld [sG386WorkBaseSpAttack], a
	ld [wMonHBaseSpecial], a
	ld a, [hli] ; SpD
	ld [sG386WorkBaseSpDefense], a
	ld a, [hli] ; type1 global
	ld [sG386WorkType1Global], a
	ld a, [hli] ; type2 global
	ld [sG386WorkType2Global], a
	ld a, [hli] ; catch low
	ld [wMonHCatchRate], a
	inc hl       ; catch high
	ld a, [hli] ; base EXP low
	ld [wMonHBaseEXP], a
	inc hl       ; base EXP high
	inc hl       ; gender
	inc hl       ; hatch
	inc hl       ; friendship
	ld a, [hl]   ; growth
	cp 6
	jr c, .growthOK
	ld a, GROWTH_MEDIUM_FAST ; Erratic/Fluctuating deferred to growth phase
.growthOK
	ld [wMonHGrowthRate], a
.done
	jp G386DisableRAM

; Local checksum equivalent to stock CalcCheckSum, avoiding a cross-ROMX direct call.
G386CalcChecksum::
	ld d, 0
.loop
	ld a, [hli]
	add d
	ld d, a
	dec bc
	ld a, b
	or c
	jr nz, .loop
	ld a, d
	cpl
	ret

G386ClearWorking::
	ld hl, sG386WorkParty
	ld bc, sG386WorkEnd - sG386WorkParty
	xor a
	jp FillMemory

; Called after vanilla save data has loaded.
G386LoadExtended::
	call G386EnableRAM
	ld hl, sG386Magic
	ld de, G386SaveMagic
	ld b, 8
.magic
	ld a, [de]
	cp [hl]
	jr nz, .invalid
	inc de
	inc hl
	dec b
	jr nz, .magic
	ld a, [sG386Version]
	cp G386_SAVE_VERSION
	jr nz, .invalid
