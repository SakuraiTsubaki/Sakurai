; Generation V -> Generation II project extension byte 0
;
; Persistent locations:
; - party mon: original party_struct Unused byte
; - boxed mon: repurposed per-slot BoxSpecies[] byte
;
; The boxed-mon record's own MON_SPECIES byte remains the low 8 bits of species.
; BoxSpecies[] is no longer a duplicate species list in the project runtime.
;
; Bit layout:
;   0-1 species ID bits 8-9
;   2-6 form ID bits 0-4
;   7   reserved extension flag
;
; Form IDs:
;   0-27 explicit
;   28-30 reserved
;   31 FORM_AUTO

DEF MONEXT_SPECIES_HI_MASK EQU %00000011
DEF MONEXT_FORM_MASK       EQU %01111100
DEF MONEXT_FORM_SHIFT      EQU 2
DEF MONEXT_FLAG7_MASK      EQU %10000000

DEF PROJECT_FORM_AUTO      EQU 31
DEF PROJECT_FORM_MAX_EXPLICIT EQU 27

; Input: A = extension byte
; Output: A = form id 0..31
Project_GetFormFromExt0::
	and MONEXT_FORM_MASK
	srl a
	srl a
	ret

; Input: A = extension byte
; Output: A = species high two bits
Project_GetSpeciesHiFromExt0::
	and MONEXT_SPECIES_HI_MASK
	ret

; Construction of full species and write-back helpers are intentionally kept
; out of this first file until each target ROM's party/box copy and sBoxSpecies
; users are patched. Do not write a project extension byte into an unpatched
; vanilla box: original routines still interpret BoxSpecies[] as species IDs.
