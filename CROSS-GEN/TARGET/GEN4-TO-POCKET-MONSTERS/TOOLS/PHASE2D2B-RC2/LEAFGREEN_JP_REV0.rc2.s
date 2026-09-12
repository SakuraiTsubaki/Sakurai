.syntax unified
.cpu arm7tdmi
.thumb
.section .text,"ax",%progbits
.global _start
_start:
    .org 0x000
    b gfx_ext
    .org 0xcc
    cmp r1, #0x7f
    bne set_noncustom
    b set_ext
    .org 0xfe
set_noncustom:
    .org 0x500
gfx_ext:
    push {r4,r5,r6,r7}
    ldr r0, =0x02037012
    ldrh r3, [r0]
    movs r0, #0x80
    lsls r0, r0, #8
    tst r3, r0
    beq packed_ctx
    adds r0, r3, #0
    lsls r0, r0, #22
    lsrs r0, r0, #22
    adds r1, r4, #0
    adds r2, r1, #0
    lsrs r2, r2, #16
    eors r1, r2
    lsls r1, r1, #22
    lsrs r1, r1, #22
    cmp r0, r1
    bne gfx_fallback
    lsrs r4, r3, #10
    movs r0, #31
    ands r4, r0
    cmp r4, #0
    beq gfx_fallback
    b gfx_common
packed_ctx:
    adds r0, r3, #0
    lsrs r0, r0, #5
    cmp r0, r6
    bne gfx_fallback
    movs r4, #31
    ands r4, r3
    cmp r4, #0
    beq gfx_fallback
gfx_common:
    ldr r0, =0x093b6af0
    ldrb r3, [r0]
    cmp r3, #2
    bls 1f
    movs r3, #2
1:
    adds r1, r3, #0
    ldr r2, =549
    muls r1, r2
    adds r1, r1, r6
    lsls r1, r1, #5
    adds r1, r1, r4
    lsls r1, r1, #3
    adds r2, r7, #0
    lsls r2, r2, #1
    adds r1, r1, r2
    ldr r0, =0x093e5100
    ldrh r2, [r0, r1]
    adds r2, #1
    beq gfx_fallback
    subs r2, #1
    adds r1, r3, #0
    ldr r0, =261
    muls r1, r0
    adds r1, r1, r2
    lsls r1, r1, #2
    ldr r0, =0x0944c000
    ldr r0, [r0, r1]
    cmp r0, #0
    beq gfx_fallback
    ldr r2, =0x093e5000
    adds r0, r0, r2
    adds r1, r6, #0
    lsls r1, r1, #5
    adds r1, r1, r4
    ldr r2, =0x02037012
    strh r1, [r2]
    adds r1, r5, #0
    svc #0x11
    pop {r4,r5,r6,r7}
    ldr r3, =0x0800e749
    bx r3
gfx_fallback:
    pop {r4,r5,r6,r7}
    ldr r3, =0x093b6a01
    bx r3

    .org 0x600
set_ext:
    ldrb r3, [r2]
    movs r1, #31
    ands r3, r1
    ldrb r1, [r0, #0x13]
    movs r2, #15
    ands r1, r2
    adds r2, r3, #0
    lsls r2, r2, #28
    lsrs r2, r2, #24
    orrs r1, r2
    strb r1, [r0, #0x13]
    ldrh r1, [r0, #0x1e]
    movs r2, #1
    bics r1, r2
    adds r2, r3, #0
    lsrs r2, r2, #4
    orrs r1, r2
    strh r1, [r0, #0x1e]
    ldr r2, [r0]
    adds r1, r2, #0
    lsrs r1, r1, #16
    eors r2, r1
    lsls r2, r2, #22
    lsrs r2, r2, #22
    adds r1, r3, #0
    lsls r1, r1, #10
    orrs r2, r1
    movs r1, #0x80
    lsls r1, r1, #8
    orrs r2, r1
    ldr r1, =0x02037012
    strh r2, [r1]
    bx lr
