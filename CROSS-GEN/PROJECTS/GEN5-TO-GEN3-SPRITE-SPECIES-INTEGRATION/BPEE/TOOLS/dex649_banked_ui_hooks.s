.syntax unified
.cpu arm7tdmi
.arm

.equ VIEW_PTR_ADDR,        0x02039B4C
.equ GMAIN_NEWKEYS,        0x030022EE
.equ GETSET_ARM,           0x09805C3C
.equ CREATE_LIST_THUMB,    0x080BC8D5
.equ CLEAR_SPRITES_THUMB,  0x080BDA41
.equ CREATE_SPRITES_THUMB, 0x080BD2B5
.equ PLAY_SE_THUMB,        0x080A37A5
.equ HANDLE_CONT_THUMB,    0x080BC101
.equ LIST_CONT_THUMB,      0x080BC8DF

.equ OFF_LIST_COUNT,       0x60C
.equ OFF_SELECTED,         0x60E
.equ OFF_DEX_MODE,         0x612
.equ OFF_DEX_ORDER,        0x616
.equ OFF_POKEBALL_ROT,     0x62C
.equ OFF_BANK_STATE,       0x642

.equ DEX_MODE_NATIONAL,    1
.equ KEY_R,                0x0100
.equ KEY_L,                0x0200
.equ SE_SELECT,            5

.global create_list_hook
.type create_list_hook,%function
create_list_hook:
    @ Intercept CreatePokedexList(dexMode=r0, order=r1).
    cmp     r0, #DEX_MODE_NATIONAL
    bne     create_list_original
    ldr     r2, =VIEW_PTR_ADDR
    ldr     r2, [r2]
    ldr     r3, =OFF_BANK_STATE
    ldrb    r3, [r2, r3]
    cmp     r3, #1
    bne     create_list_original

    @ Bank B (#387-649), numerical order. Populate all 263 slots so the
    @ scroll bar denominator can never become zero when only one new species
    @ has been seen. Unseen entries retain dex numbers but their names/sprites
    @ remain hidden by the vanilla rendering path.
    stmdb   sp!, {r4-r11, lr}
    mov     r4, r2                  @ view

    ldr     r0, =OFF_LIST_COUNT
    add     r0, r4, r0
    ldr     r1, =263
    strh    r1, [r0]

    @ Clear all 387 physical list slots to {dexNum=0xFFFF, flags=0}.
    mov     r5, r4
    ldr     r6, =387
    ldr     r7, =0x0000FFFF
1:
    str     r7, [r5], #4
    subs    r6, r6, #1
    bne     1b

    mov     r6, #0                  @ output index
    ldr     r7, =387                @ national number
    ldr     r11, =650               @ end exclusive
2:
    add     r9, r4, r6, lsl #2
    strh    r7, [r9]

    mov     r0, r7
    mov     r1, #0                  @ FLAG_GET_SEEN
    ldr     r3, =GETSET_ARM
    adr     lr, 3f
    bx      r3
3:
    mov     r8, r0

    mov     r0, r7
    mov     r1, #1                  @ FLAG_GET_CAUGHT
    ldr     r3, =GETSET_ARM
    adr     lr, 4f
    bx      r3
4:
    orr     r10, r8, r0, lsl #1
    strh    r10, [r9, #2]

    add     r6, r6, #1
    add     r7, r7, #1
    cmp     r7, r11
    blo     2b

    ldmia   sp!, {r4-r11, lr}
    bx      lr

create_list_original:
    @ Reproduce the overwritten 8-byte Thumb prologue exactly enough to
    @ preserve the original stack/register contract, then resume at +0xA.
    stmdb   sp!, {r4-r7, lr}
    mov     r7, r10
    mov     r6, r9
    mov     r5, r8
    stmdb   sp!, {r5-r7}
    ldr     r3, =LIST_CONT_THUMB
    bx      r3

.global input_hook
.type input_hook,%function
input_hook:
    @ Only handle L/R on the stable main list in National mode.
    ldr     r2, =VIEW_PTR_ADDR
    ldr     r2, [r2]

    ldr     r3, =OFF_DEX_MODE
    ldrh    r3, [r2, r3]
    cmp     r3, #DEX_MODE_NATIONAL
    bne     input_original

    ldr     r3, =GMAIN_NEWKEYS
    ldrh    r3, [r3]
    tst     r3, #(KEY_L | KEY_R)
    beq     input_original

    ldr     r12, =OFF_BANK_STATE
    add     r12, r2, r12
    ldrb    r1, [r12]               @ current bank

    tst     r3, #KEY_R
    movne   r0, #1                  @ R -> Bank B
    moveq   r0, #0                  @ L -> Bank A
    cmp     r0, r1
    beq     input_original

    @ Custom path returns directly to the task runner, so preserve ABI regs/LR.
    stmdb   sp!, {r4-r11, lr}
    mov     r4, r2                   @ view
    strb    r0, [r12]

    @ Reset list cursor and ball position.
    mov     r0, #0
    ldr     r1, =OFF_SELECTED
    strh    r0, [r4, r1]
    ldr     r1, =OFF_POKEBALL_ROT
    mov     r0, #64
    strb    r0, [r4, r1]

    @ Rebuild list through the hooked CreatePokedexList.
    ldr     r1, =OFF_DEX_MODE
    ldrh    r0, [r4, r1]
    ldr     r2, =OFF_DEX_ORDER
    ldrh    r1, [r4, r2]
    ldr     r3, =CREATE_LIST_THUMB
    adr     lr, 6f
    bx      r3
6:
    @ Destroy old list sprites.
    ldr     r3, =CLEAR_SPRITES_THUMB
    adr     lr, 7f
    bx      r3
7:
    @ Repaint the visible 11-row list and top/mid/bottom Pokémon sprites.
    mov     r0, #0
    mov     r1, #0x0E
    ldr     r3, =CREATE_SPRITES_THUMB
    adr     lr, 8f
    bx      r3
8:
    @ Feedback sound.
    mov     r0, #SE_SELECT
    ldr     r3, =PLAY_SE_THUMB
    adr     lr, 9f
    bx      r3
9:
    ldmia   sp!, {r4-r11, lr}
    bx      lr

input_original:
    @ Reproduce overwritten Task_HandlePokedexInput prologue (8 bytes).
    stmdb   sp!, {r4-r6, lr}
    sub     sp, sp, #4
    and     r6, r0, #0xFF
    ldr     r3, =HANDLE_CONT_THUMB
    bx      r3

.ltorg
