; GREEN 386 canonical identity source-port v1
; Canonical identity: u16 species + u8 form.
; Stock one-byte species fields remain as compatibility proxies for now.

DEF G386_SAVE_VERSION EQU 1
DEF G386_SRAM_BANK EQU 4

G386RuntimeStart::

G386EnableRAM::
	ld a, RAMG_SRAM_ENABLE
	ld [rRAMG], a
	ld a, G386_SRAM_BANK
	ld [rRAMB], a
	ret

G386DisableRAM::
	xor a
	ld [rRAMG], a
	ret

; A = legacy Green internal species ID
; Returns BC = canonical National Dex ID, or $ffff for a non-species ID.
G386MapLegacyToCanonical::
	ld l, a
	ld h, 0
	add hl, hl
	ld de, G386LegacyToCanonicalTable
	add hl, de
	ld a, [hli]
	ld c, a
	ld b, [hl]
	ret

; HL = identity array, A = slot. Returns HL -> u16 species + u8 form.
G386IdentityPtr::
	ld e, a
	add a
	add e
	ld e, a
	ld d, 0
	add hl, de
	ret

; A = box number, C = slot. Returns HL -> working box identity.
G386BoxIdentityPtr::
	push bc
	ld e, a
	ld d, 0
	ld hl, sG386WorkBoxes
	ld bc, MONS_PER_BOX * 3
.boxLoop
	ld a, e
	and a
	jr z, .slot
	add hl, bc
	dec e
	jr .boxLoop
.slot
	pop bc
	ld a, c
	jp G386IdentityPtr

; SRAM bank 4 must be enabled. HL = identity. If zero, derive from proxy A.
; Out: BC species, A form. Zero/zero means unresolved.
G386ResolveRaw::
	push de
	push hl
	ld e, a ; legacy proxy
	ld a, [hli]
	ld c, a
	ld a, [hli]
	ld b, a
	ld a, b
	or c
	jr z, .derive
	ld a, [hl]
	pop hl
	pop de
	ret
.derive
	pop hl
	ld a, e
	call G386MapLegacyToCanonical
	ld a, b
	cp $ff
	jr nz, .store
	ld a, c
	cp $ff
	jr z, .invalid
.store
	ld [hl], c
	inc hl
	ld [hl], b
	inc hl
	xor a
	ld [hl], a
	pop de
	ret
.invalid
	ld bc, 0
	xor a
	pop de
	ret

; BC species, A form. SRAM bank 4 must be enabled.
G386SetCurrentRaw::
	ld [sG386WorkCurrentForm], a
	ld a, c
	ld [sG386WorkCurrentSpecies], a
	ld a, b
	ld [sG386WorkCurrentSpecies + 1], a
	ld a, 1
	ld [sG386WorkOverrideValid], a
	ret

; Called just before LoadMonData's GetMonHeader.
G386PrepareIdentityForLoadMonData::
	call G386EnableRAM
	ld a, [wMonDataLocation]
	cp PLAYER_PARTY_DATA
	jr z, .party
	cp ENEMY_PARTY_DATA
	jr z, .enemy
	cp BOX_DATA
	jr z, .box
	cp DAYCARE_DATA
	jr z, .daycare
	jp G386DisableRAM
.party
	ld hl, sG386WorkParty
	ld a, [wWhichPokemon]
	call G386IdentityPtr
	jr .resolveIndexed
.enemy
	ld hl, sG386WorkEnemyParty
	ld a, [wWhichPokemon]
	call G386IdentityPtr
	jr .resolveIndexed
.box
	ld a, [wCurrentBoxNum]
	and BOX_NUM_MASK
	ld b, a
	ld a, [wWhichPokemon]
	ld c, a
	ld a, b
	call G386BoxIdentityPtr
	jr .resolveIndexed
.daycare
	ld hl, sG386WorkDayCare
.resolveIndexed
	ld a, [wCurPartySpecies]
	call G386ResolveRaw
	call G386SetCurrentRaw
	jp G386DisableRAM

; Queue a canonical mon for the next AddPartyMon.
; BC = canonical species, D = form, A = safe legacy proxy species byte.
G386QueueCanonicalMon::
	ld [wCurPartySpecies], a
	call G386EnableRAM
	ld a, c
	ld [sG386WorkPending], a
	ld a, b
	ld [sG386WorkPending + 1], a
	ld a, d
	ld [sG386WorkPending + 2], a
	jp G386DisableRAM

; Called after stock AddPartyMon has allocated the new slot but before GetMonHeader.
G386PrepareIdentityForAddPartyMon::
	call G386EnableRAM
	ld a, [sG386WorkPending]
	ld c, a
	ld a, [sG386WorkPending + 1]
	ld b, a
	ld a, b
	or c
	jr nz, .pending
	ld a, [wCurPartySpecies]
	call G386MapLegacyToCanonical
	xor a
	jr .have
.pending
	ld a, [sG386WorkPending + 2]
.have
	push af
	push bc
	ld hl, sG386WorkParty
	ld a, [wMonDataLocation]
	and $f
	jr z, .array
	ld hl, sG386WorkEnemyParty
.array
	ldh a, [hNewPartyLength]
	dec a
	call G386IdentityPtr
	pop bc
	pop af
	ld [hl], c
	inc hl
	ld [hl], b
	inc hl
	ld [hl], a
	call G386SetCurrentRaw
	xor a
	ld [sG386WorkPending], a
	ld [sG386WorkPending + 1], a
	ld [sG386WorkPending + 2], a
	jp G386DisableRAM
