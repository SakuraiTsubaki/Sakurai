#ifndef GUARD_GEN4_BATTLE_MOVE_EXT_H
#define GUARD_GEN4_BATTLE_MOVE_EXT_H

#include "global.h"

/*
 * Retail Gen III gBattleMoves is physically 12 bytes per record in the ROM.
 * Bytes 0..8 are the original fields. Bytes 9..11 are zero in all 10 uploaded
 * Gen III targets and are reused here without changing the stride.
 */
struct BattleMove
{
    u8 effect;                  /* legacy compatibility mirror */
    u8 power;
    u8 type;
    u8 accuracy;
    u8 pp;
    u8 secondaryEffectChance;
    u8 target;                  /* legacy compatibility mirror */
    s8 priority;
    u8 flags;                   /* shared Gen III low flag bits */
    u8 category;                /* Gen IV physical/special/status */
    u16 effect16;               /* exact Gen IV effect ID */
};

enum Gen4MoveCategory
{
    MOVE_CATEGORY_PHYSICAL = 0,
    MOVE_CATEGORY_SPECIAL  = 1,
    MOVE_CATEGORY_STATUS   = 2,
};

struct Gen4MoveMeta
{
    u16 range;                  /* exact Gen IV 16-bit range */
    u8 flagsB;                  /* exact HGSS byte 0x0B */
    u8 flagsC;                  /* exact HGSS byte 0x0C */
    u8 contestType;
    u8 reserved;
    u16 unkE;
};

extern const struct BattleMove gBattleMoves[];
extern const struct Gen4MoveMeta gGen4MoveMeta[];

u16 GetMoveEffect16(u16 move);
u8 GetMoveCategoryGen4(u16 move);
u16 GetMoveRange16(u16 move);
bool8 IsMovePhysicalGen4(u16 move);
bool8 IsMoveSpecialGen4(u16 move);
bool8 IsMoveStatusGen4(u16 move);

#endif
