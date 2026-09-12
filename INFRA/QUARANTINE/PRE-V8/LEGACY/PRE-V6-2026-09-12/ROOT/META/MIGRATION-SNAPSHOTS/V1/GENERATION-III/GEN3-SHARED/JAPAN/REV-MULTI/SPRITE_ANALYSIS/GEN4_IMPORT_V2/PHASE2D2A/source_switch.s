.syntax unified
.cpu arm7tdmi
.thumb
.section .text,"ax",%progbits
.global _start
_start:
    .org 0x34
    b source_helper
    nop
    nop
resume_target:
    .org 0xb0
source_helper:
    adr r2, source_config
    ldrb r2, [r2]
    cmp r2, #2
    bls 1f
    movs r2, #2
1:
    movs r1, #247
    lsls r1, r1, #1
    muls r2, r1
    adds r0, r0, r2
    b resume_target
    .org 0xf0
source_config:
    .byte 2
