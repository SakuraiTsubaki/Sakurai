; Generation IV form-rule bridge for Gen II
; Requires Phase 4 species bit8 + form[4:0] storage.
; Requires separate 9-bit MOVE ID migration before all Rotom appliance moves work.

DEF ROTOM_BASE  EQU 0
DEF ROTOM_HEAT  EQU 1
DEF ROTOM_WASH  EQU 2
DEF ROTOM_FROST EQU 3
DEF ROTOM_FAN   EQU 4
DEF ROTOM_MOW   EQU 5

DEF GIRATINA_ALTERED EQU 0
DEF GIRATINA_ORIGIN  EQU 1
DEF SHAYMIN_LAND EQU 0
DEF SHAYMIN_SKY  EQU 1
DEF PICHU_NORMAL    EQU 0
DEF PICHU_SPIKY_EAR EQU 1

; Arceus Gen IV form ids mirror type ids.
DEF ARCEUS_NORMAL   EQU 0
DEF ARCEUS_FIGHTING EQU 1
DEF ARCEUS_FLYING   EQU 2
DEF ARCEUS_POISON   EQU 3
DEF ARCEUS_GROUND   EQU 4
DEF ARCEUS_ROCK     EQU 5
DEF ARCEUS_BUG      EQU 6
DEF ARCEUS_GHOST    EQU 7
DEF ARCEUS_STEEL    EQU 8
DEF ARCEUS_MYSTERY  EQU 9 ; original unused/inaccessible ???-type slot
DEF ARCEUS_FIRE     EQU 10
DEF ARCEUS_WATER    EQU 11
DEF ARCEUS_GRASS    EQU 12
DEF ARCEUS_ELECTRIC EQU 13
DEF ARCEUS_PSYCHIC  EQU 14
DEF ARCEUS_ICE      EQU 15
DEF ARCEUS_DRAGON   EQU 16
DEF ARCEUS_DARK     EQU 17

; Runtime policy:
; - Rotom: stored form + 9-bit move replacement
; - Giratina: Origin if Griseous Orb or Platinum-style Distortion World flag
; - Shaymin: Sky only if fateful, alive, not frozen, 04:00-19:59;
;            force Land on storage/trade-style hooks and night transition
; - Arceus: synchronize form from held-item hold effect + Multitype
; - Spiky-ear Pichu (HGSS): form=1, block evolution
;
; Hooks are inserted after species9/move9 lookup migration is live.
