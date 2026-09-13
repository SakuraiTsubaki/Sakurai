.syntax unified
.cpu arm7tdmi

.equ GET_MON_DATA_THUMB,          0x0806A519
.equ GET_HOLD_EFFECT_THUMB,       0x080D74DD
.equ ORIGINAL_CONT_THUMB,         0x0806D0A1
.equ PLAYER_PARTY_COUNT_ADDR,     0x020244E9
.equ PLAYER_PARTY_ADDR,           0x020244EC
.equ SPECIES_INFO_ADDR,           0x090E3710

.equ MON_DATA_PERSONALITY,        0
.equ MON_DATA_SPECIES,            11
.equ MON_DATA_HELD_ITEM,          12
.equ MON_DATA_MOVE1,              13
.equ MON_DATA_IS_EGG,             45
.equ MON_DATA_LEVEL,              56

.equ ITEM_EVERSTONE,              0xAF
.equ HOLD_EFFECT_PREVENT_EVOLVE,  0x26

.equ METHOD_KNOW_MOVE,            21
.equ METHOD_PARTY_SPECIES,        22
.equ METHOD_LEVEL_MALE,           23
.equ METHOD_LEVEL_FEMALE,         24

.arm
.global evolution_ext_hook
.type evolution_ext_hook,%function
evolution_ext_hook:
    stmdb   sp!, {r4-r11, lr}
    mov     r4, r0
    mov     r5, r1
    mov     r6, r2

    ldr     r3, =original_trampoline
    adr     lr, 1f
    bx      r3
1:
    cmp     r0, #0
    bne     hook_done
    cmp     r5, #0
    bne     hook_zero

    mov     r0, r4
    mov     r1, #MON_DATA_HELD_ITEM
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 2f
    bx      r3
2:
    mov     r8, r0
    cmp     r8, #ITEM_EVERSTONE
    beq     hook_zero
    mov     r0, r8
    ldr     r3, =GET_HOLD_EFFECT_THUMB
    adr     lr, 3f
    bx      r3
3:
    cmp     r0, #HOLD_EFFECT_PREVENT_EVOLVE
    beq     hook_zero

    mov     r0, r4
    mov     r1, #MON_DATA_SPECIES
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 4f
    bx      r3
4:
    mov     r7, r0
    mov     r0, r4
    mov     r1, #MON_DATA_LEVEL
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 5f
    bx      r3
5:
    mov     r8, r0
    ldr     r9, =ext_evolution_records
record_loop:
    ldr     r0, =ext_evolution_records_end
    cmp     r9, r0
    bhs     hook_zero
    ldrh    r0, [r9, #0]
    cmp     r0, r7
    bne     next_record
    ldrh    r11, [r9, #2]
    cmp     r11, #METHOD_KNOW_MOVE
    beq     eval_known_move
    cmp     r11, #METHOD_PARTY_SPECIES
    beq     eval_party_species
    cmp     r11, #METHOD_LEVEL_MALE
    beq     eval_level_male
    cmp     r11, #METHOD_LEVEL_FEMALE
    beq     eval_level_female
    b       next_record

eval_known_move:
    ldrh    r10, [r9, #4]
    mov     r11, #MON_DATA_MOVE1
move_loop:
    mov     r0, r4
    mov     r1, r11
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 6f
    bx      r3
6:
    cmp     r0, r10
    beq     return_target
    add     r11, r11, #1
    cmp     r11, #(MON_DATA_MOVE1 + 4)
    blo     move_loop
    b       next_record

eval_party_species:
    ldrh    r10, [r9, #4]
    ldr     r0, =PLAYER_PARTY_COUNT_ADDR
    ldrb    r11, [r0]
    cmp     r11, #0
    beq     next_record
    mov     r5, #0
party_loop:
    mov     r0, r5, lsl #6
    add     r0, r0, r5, lsl #5
    add     r0, r0, r5, lsl #2
    ldr     r1, =PLAYER_PARTY_ADDR
    add     r0, r1, r0
    mov     r6, r0
    mov     r1, #MON_DATA_IS_EGG
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 7f
    bx      r3
7:
    cmp     r0, #0
    bne     party_next
    mov     r0, r6
    mov     r1, #MON_DATA_SPECIES
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 8f
    bx      r3
8:
    cmp     r0, r10
    beq     return_target
party_next:
    add     r5, r5, #1
    cmp     r5, r11
    blo     party_loop
    b       next_record

eval_level_male:
    ldrh    r0, [r9, #4]
    cmp     r8, r0
    blo     next_record
    bl      determine_female
    cmp     r0, #0
    beq     return_target
    b       next_record

eval_level_female:
    ldrh    r0, [r9, #4]
    cmp     r8, r0
    blo     next_record
    bl      determine_female
    cmp     r0, #1
    beq     return_target
    b       next_record

determine_female:
    stmdb   sp!, {r1-r3, lr}
    mov     r0, r4
    mov     r1, #MON_DATA_PERSONALITY
    mov     r2, #0
    ldr     r3, =GET_MON_DATA_THUMB
    adr     lr, 9f
    bx      r3
9:
    and     r1, r0, #0xFF
    ldr     r2, =SPECIES_INFO_ADDR
    mov     r3, r7, lsl #5
    sub     r3, r3, r7, lsl #2
    add     r2, r2, r3
    ldrb    r2, [r2, #0x10]
    cmp     r2, #0
    moveq   r0, #0
    beq     gender_done
    cmp     r2, #0xFE
    moveq   r0, #1
    beq     gender_done
    cmp     r2, #0xFF
    moveq   r0, #2
    beq     gender_done
    cmp     r2, r1
    movhi   r0, #1
    movls   r0, #0
gender_done:
    ldmia   sp!, {r1-r3, lr}
    bx      lr

return_target:
    ldrh    r0, [r9, #6]
    b       hook_done
next_record:
    add     r9, r9, #8
    b       record_loop
hook_zero:
    mov     r0, #0
hook_done:
    ldmia   sp!, {r4-r11, lr}
    bx      lr

.align 2
ext_evolution_records:
    .hword 108, METHOD_KNOW_MOVE,     205, 516
    .hword 114, METHOD_KNOW_MOVE,     246, 518
    .hword 193, METHOD_KNOW_MOVE,     246, 522
    .hword 221, METHOD_KNOW_MOVE,     246, 526
    .hword 491, METHOD_KNOW_MOVE,     102, 185
    .hword 492, METHOD_KNOW_MOVE,     102, 122
    .hword 465, METHOD_LEVEL_FEMALE,   20, 466
    .hword 465, METHOD_LEVEL_MALE,     20, 467
    .hword 468, METHOD_LEVEL_FEMALE,   21, 469
    .hword 511, METHOD_PARTY_SPECIES, 223, 226
ext_evolution_records_end:

.ltorg

.thumb
.align 2
.global original_trampoline
.type original_trampoline,%function
.thumb_func
original_trampoline:
    push    {r4-r7, lr}
    mov     r7, r10
    mov     r6, r9
    mov     r5, r8
    ldr     r3, =ORIGINAL_CONT_THUMB
    bx      r3
