	ld hl, sG386Version
	ld bc, sG386CommittedDataEnd - sG386Version
	call G386CalcChecksum
	ld b, a
	ld a, [sG386Checksum]
	cp b
	jr nz, .invalid
	ld hl, sG386CommittedParty
	ld de, sG386WorkParty
	ld bc, PARTY_LENGTH * 3
	call CopyData
	ld hl, sG386CommittedBoxes
	ld de, sG386WorkBoxes
	ld bc, NUM_BOXES * MONS_PER_BOX * 3
	call CopyData
	ld hl, sG386CommittedDayCare
	ld de, sG386WorkDayCare
	ld bc, 3
	call CopyData
	ld hl, sG386WorkEnemyParty
	ld bc, sG386WorkEnd - sG386WorkEnemyParty
	xor a
	call FillMemory
	jp G386DisableRAM
.invalid
	call G386ClearWorking
; Migrate the loaded party immediately; boxes migrate lazily by proxy when used.
	ld a, [wPartyCount]
	ld b, a
	xor a
	ld c, a
.partyLoop
	ld a, c
	cp b
	jr nc, .done
	push bc
	ld hl, wPartySpecies
	ld e, c
	ld d, 0
	add hl, de
	ld a, [hl]
	push af
	ld hl, sG386WorkParty
	ld a, c
	call G386IdentityPtr
	pop af
	call G386ResolveRaw
	pop bc
	inc c
	jr .partyLoop
.done
	jp G386DisableRAM

; Called only when vanilla SaveGameData succeeds. Commits working persistent state.
G386CommitExtended::
	call G386EnableRAM
	ld hl, G386SaveMagic
	ld de, sG386Magic
	ld bc, 8
	call CopyData
	ld a, G386_SAVE_VERSION
	ld [sG386Version], a
	ld hl, sG386WorkParty
	ld de, sG386CommittedParty
	ld bc, PARTY_LENGTH * 3
	call CopyData
	ld hl, sG386WorkBoxes
	ld de, sG386CommittedBoxes
	ld bc, NUM_BOXES * MONS_PER_BOX * 3
	call CopyData
	ld hl, sG386WorkDayCare
	ld de, sG386CommittedDayCare
	ld bc, 3
	call CopyData
	ld hl, sG386Version
	ld bc, sG386CommittedDataEnd - sG386Version
	call G386CalcChecksum
	ld [sG386Checksum], a
	jp G386DisableRAM

G386SaveMagic:
	db "G386SV1", 0

G386LegacyToCanonicalTable::
	INCBIN "data/g386/legacy_map.bin"
G386LegacyToCanonicalTableEnd::
	ASSERT G386LegacyToCanonicalTableEnd - G386LegacyToCanonicalTable == 512

G386Gen3PersonalTable::
	INCBIN "data/g386/gen3_personal.bin"
G386Gen3PersonalTableEnd::
	ASSERT G386Gen3PersonalTableEnd - G386Gen3PersonalTable == 386 * 30

G386RuntimeEnd::
