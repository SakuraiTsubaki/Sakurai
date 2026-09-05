SECTION "G386 Extended Save", SRAM[$a000], BANK[4]

; Committed state. Only updated by SaveGameData, so quitting without saving
; never corrupts the last committed canonical identities.
sG386CommittedStart::
sG386Magic:: ds 8
sG386Version:: db
sG386CommittedParty:: ds PARTY_LENGTH * 3
sG386CommittedBoxes:: ds NUM_BOXES * MONS_PER_BOX * 3
sG386CommittedDayCare:: ds 3
sG386CommittedDataEnd::
sG386Checksum:: db

; Working persistent state. SRAM is used because stock Green has zero free WRAM0.
sG386WorkParty:: ds PARTY_LENGTH * 3
sG386WorkBoxes:: ds NUM_BOXES * MONS_PER_BOX * 3
sG386WorkDayCare:: ds 3

; Ephemeral working state. Clearing from WorkEnemyParty onward must not erase
; the persistent party/box/daycare identities copied from committed state.
sG386WorkEnemyParty:: ds PARTY_LENGTH * 3
sG386WorkBattle:: ds 3
sG386WorkEnemyBattle:: ds 3
sG386WorkPending:: ds 3
sG386WorkCurrentSpecies:: dw
sG386WorkCurrentForm:: db
sG386WorkOverrideValid:: db
sG386WorkBaseSpAttack:: db
sG386WorkBaseSpDefense:: db
sG386WorkType1Global:: db
sG386WorkType2Global:: db
sG386WorkEnd::

ASSERT sG386WorkEnd - $a000 < $2000
