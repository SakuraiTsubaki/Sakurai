; Copy canonical identity alongside _MoveMon. Called after stock data copy, before
; the source is removed. Source proxy is wCurPartySpecies if lazy migration is needed.
G386CopyMoveMonIdentity::
	call G386EnableRAM
	ld a, [wMoveMonType]
	and a
	jr z, .boxToParty
	cp DAYCARE_TO_PARTY
	jr z, .daycareToParty
	cp PARTY_TO_DAYCARE
	jr z, .partyToDaycare
; PARTY_TO_BOX
	ld hl, sG386WorkParty
	ld a, [wWhichPokemon]
	call G386IdentityPtr
	jr .sourceIndexed
.boxToParty
	ld a, [wCurrentBoxNum]
	and BOX_NUM_MASK
	ld b, a
	ld a, [wWhichPokemon]
	ld c, a
	ld a, b
	call G386BoxIdentityPtr
	jr .sourceIndexed
.daycareToParty
	ld hl, sG386WorkDayCare
	jr .sourceReady
.partyToDaycare
	ld hl, sG386WorkParty
	ld a, [wWhichPokemon]
	call G386IdentityPtr
.sourceIndexed
.sourceReady
	ld a, [wCurPartySpecies]
	call G386ResolveRaw
	push af
	push bc
	ld a, [wMoveMonType]
	and a
	jr z, .destParty
	cp DAYCARE_TO_PARTY
	jr z, .destParty
	cp PARTY_TO_DAYCARE
	jr z, .destDaycare
; destination current box
	ld a, [wCurrentBoxNum]
	and BOX_NUM_MASK
	ld b, a
	ld a, [wBoxCount]
	dec a
	ld c, a
	ld a, b
	call G386BoxIdentityPtr
	jr .write
.destParty
	ld hl, sG386WorkParty
	ld a, [wPartyCount]
	dec a
	call G386IdentityPtr
	jr .write
.destDaycare
	ld hl, sG386WorkDayCare
.write
	pop bc
	pop af
	ld [hl], c
	inc hl
	ld [hl], b
	inc hl
	ld [hl], a
	jp G386DisableRAM

; Shift sidecar identities in lockstep with _RemovePokemon. Called before stock shift.
G386RemoveIdentity::
	call G386EnableRAM
	ld a, [wRemoveMonFromBox]
	and a
	jr nz, .box
	ld hl, sG386WorkParty
	ld c, PARTY_LENGTH
	jr .gotBase
.box
	ld a, [wCurrentBoxNum]
	and BOX_NUM_MASK
	ld e, a
	ld d, 0
	ld hl, sG386WorkBoxes
	ld bc, MONS_PER_BOX * 3
.boxBaseLoop
	ld a, e
	and a
	jr z, .boxBaseDone
	add hl, bc
	dec e
	jr .boxBaseLoop
.boxBaseDone
	ld c, MONS_PER_BOX
.gotBase
	ld a, [wWhichPokemon]
	ld b, a
	push bc
	call G386IdentityPtr
	pop bc
	ld d, h
	ld e, l
	inc de
	inc de
	inc de
.shift
	inc b
	ld a, b
	cp c
	jr nc, .clear
	ld a, [de]
	ld [hli], a
	inc de
	ld a, [de]
	ld [hli], a
	inc de
	ld a, [de]
	ld [hli], a
	inc de
	jr .shift
.clear
	xor a
	ld [hli], a
	ld [hli], a
	ld [hl], a
	jp G386DisableRAM

; Copy selected player party identity to active battle identity.
G386SyncPlayerBattleIdentityFromParty::
	call G386EnableRAM
	ld hl, sG386WorkParty
	ld a, [wWhichPokemon]
	call G386IdentityPtr
	ld de, sG386WorkBattle
	ld bc, 3
	call CopyData
	jp G386DisableRAM

; Post-hook for original GetMonHeader. The original call supplies sprite pointers,
; level-1 moves and TM/HM bits from the proxy. This overlays the Gen III personal
; fields that fit the current engine. Special temporarily projects Sp. Atk; Sp. Def
; is retained in the sidecar for the later 6-stat battle phase.
G386OverlayMonHeader::
	call G386EnableRAM
	ld a, [sG386WorkOverrideValid]
	and a
	jr z, .legacy
	xor a
	ld [sG386WorkOverrideValid], a
	ld a, [sG386WorkCurrentSpecies]
	ld c, a
	ld a, [sG386WorkCurrentSpecies + 1]
	ld b, a
	jr .validate
.legacy
	ld a, [wCurSpecies]
	call G386MapLegacyToCanonical
.validate
	ld a, b
	cp HIGH(387)
	jr c, .nonzero
	jr nz, .done
	ld a, c
	cp LOW(387)
	jr nc, .done
.nonzero
	ld a, b
