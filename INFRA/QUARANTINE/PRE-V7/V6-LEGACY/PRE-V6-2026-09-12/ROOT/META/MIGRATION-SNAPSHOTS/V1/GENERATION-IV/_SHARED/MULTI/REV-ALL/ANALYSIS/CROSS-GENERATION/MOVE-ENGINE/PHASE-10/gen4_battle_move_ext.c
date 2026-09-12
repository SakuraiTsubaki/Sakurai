#include "global.h"
#include "gen4_battle_move_ext.h"

u16 GetMoveEffect16(u16 move)
{
    return gBattleMoves[move].effect16;
}

u8 GetMoveCategoryGen4(u16 move)
{
    return gBattleMoves[move].category;
}

u16 GetMoveRange16(u16 move)
{
    return gGen4MoveMeta[move].range;
}

bool8 IsMovePhysicalGen4(u16 move)
{
    return GetMoveCategoryGen4(move) == MOVE_CATEGORY_PHYSICAL;
}

bool8 IsMoveSpecialGen4(u16 move)
{
    return GetMoveCategoryGen4(move) == MOVE_CATEGORY_SPECIAL;
}

bool8 IsMoveStatusGen4(u16 move)
{
    return GetMoveCategoryGen4(move) == MOVE_CATEGORY_STATUS;
}
