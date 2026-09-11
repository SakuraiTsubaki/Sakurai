; Generation IV form-system scaffold for Generation II
; -----------------------------------------------------------
; Gold/Silver:
;   The native BoxMon layout has two skipped bytes after MON_POKERUS.
;   Preserve struct size and assign the first skipped byte as MON_EXT0:
;
;       bit 0    species ID bit 8
;       bits 1-5 stored form (0..31)
;       bits 6-7 reserved
;
;   The second skipped byte remains reserved for later engine expansion.
;
; Crystal:
;   DO NOT use those bytes. Crystal uses them for MON_CAUGHTDATA.
;   Use a packed 6-bit sidecar in verified save padding instead.
;
; This file is a source-integration scaffold, not a blind ROM patch.

DEF EXT_SPECIES_HIGH_BIT EQU 0
DEF EXT_FORM_SHIFT       EQU 1
DEF EXT_FORM_MASK        EQU %00111110

; A = ext0
GetFormFromExt0::
    and EXT_FORM_MASK
    srl a
    ret

; A = form (0..31), B = old ext0
; Returns A = new ext0
SetFormInExt0::
    and %00011111
    sla a
    ld c, a
    ld a, b
    and %11000001
    or c
    ret

; A = species high bit (0/1), B = old ext0
; Returns A = new ext0
SetSpeciesHighInExt0::
    and 1
    ld c, a
    ld a, b
    and %11111110
    or c
    ret

; A = ext0
; Returns A = species high bit (0/1)
GetSpeciesHighFromExt0::
    and 1
    ret

; Crystal sidecar entry:
; 6 bits per mon = species high bit + form[4:0].
; Party + boxes must be indexed through helpers so swaps/moves/trades
; move the sidecar entry together with the Pokémon.
