; GREEN G386F3 GetMonHeader hook v1
; Fixed trampoline lives in unused ROM0 RST-vector space.
; Addresses are Rev0/RevA-specific for BankswitchHome/Back.

; Hook replaces final: ld [rROMB], a / ret
; with: jp $0008 / nop

FixedStub_0008:
    push bc
    push de
    push hl
    ld a, $21
    call BankswitchHome
    call $5300 ; legacy u8 -> canonical u16 in BC
    call BankswitchBack
    ld a, $20
    call BankswitchHome
    call $4080 ; G386F3 Kanto-safe overlay
    call BankswitchBack
    pop hl
    pop de
    pop bc
    ret

; Bank $21:$5300
MapLegacySpeciesToCanonical:
    ld a, [wCurSpecies] ; $D092
    ld c, a
    ld b, 0
    ld hl, $5000       ; 256 x u16 map
    add hl, bc
    add hl, bc
    ld a, [hli]
    ld c, a
    ld a, [hl]
    ld b, a
    ret

; Bank $20:$4080, in reserved bytes of G386F3 header.
; BC = canonical National Dex ID.
OverlayGen3KantoSafePersonal:
    ld a, b
    and a
    ret nz
    ld a, c
    and a
    ret z
    cp 152
    ret nc
    dec c
    ld hl, $5D6F       ; Gen3 record #001
    ld de, 30
    ld a, c
    and a
    jr z, .record
.loop
    add hl, de
    dec a
    jr nz, .loop
.record
    inc hl
    inc hl             ; skip canonical u16
    ld de, $D096       ; wMonHBaseHP
    ld b, 4
.copy4
    ld a, [hli]        ; HP/Atk/Def/Speed
    ld [de], a
    inc de
    dec b
    jr nz, .copy4
    inc hl
    inc hl
    inc hl
    inc hl             ; preserve SpA/SpD + types for now
    ld a, [hli]
    ld [$D09D], a      ; catch rate low byte
    inc hl
    ld a, [hli]
    ld [$D09E], a      ; base EXP low byte
    inc hl
    inc hl
    inc hl
    inc hl
    ld a, [hl]
    ld [$D0A8], a      ; growth rate
    ret
