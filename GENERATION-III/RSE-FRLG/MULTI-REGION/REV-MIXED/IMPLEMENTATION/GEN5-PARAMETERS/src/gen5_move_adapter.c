#include "global.h"
#include "gen5_personal_adapter.h"
#include "gen5_move_adapter.h"

const struct Gen5MoveRaw *Gen5GetMoveRaw(u16 move)
{
    if (move > GEN5_LAST_MOVE_ID)
        move = 0;

    return &gGen5MoveBw[move];
}

u8 Gen5GetMoveCategory(u16 move)
{
    return Gen5GetMoveRaw(move)->category;
}

u8 Gen5GetMoveTypeGen3(u16 move)
{
    return Gen5TypeToGen3Type(Gen5GetMoveRaw(move)->type);
}

u8 Gen5GetMovePower(u16 move)
{
    return Gen5GetMoveRaw(move)->power;
}

u8 Gen5GetMoveAccuracy(u16 move)
{
    return Gen5GetMoveRaw(move)->accuracy;
}

u8 Gen5GetMovePP(u16 move)
{
    return Gen5GetMoveRaw(move)->pp;
}

s8 Gen5GetMovePriority(u16 move)
{
    return Gen5GetMoveRaw(move)->priority;
}
