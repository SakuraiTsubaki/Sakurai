#ifndef GUARD_GEN5_MOVE_ADAPTER_H
#define GUARD_GEN5_MOVE_ADAPTER_H

#include "global.h"

#define GEN5_LAST_MOVE_ID       559
#define GEN5_MOVE_COUNT         (GEN5_LAST_MOVE_ID + 1)
#define GEN5_MOVE_RECORD_SIZE   0x24

enum Gen5MoveCategory
{
    GEN5_MOVE_CATEGORY_PHYSICAL = 0,
    GEN5_MOVE_CATEGORY_SPECIAL = 1,
    GEN5_MOVE_CATEGORY_STATUS = 2,
};

/* Verified BW /a/0/2/1 36-byte move record. */
struct __attribute__((packed)) Gen5MoveRaw
{
    u8 type;
    u8 effectCategory;
    u8 category;
    u8 power;
    u8 accuracy;
    u8 pp;
    s8 priority;
    u8 hits;
    u16 resultEffect;
    u8 effectChance;
    u8 status;
    u8 minTurns;
    u8 maxTurns;
    u8 critStage;
    u8 flinch;
    u16 effect;
    s8 recoil;
    s8 healing;
    u8 target;
    u8 stat[3];
    s8 magnitude[3];
    u8 statChance[3];
    u8 rawFlags[6];
};

typedef char Gen5MoveRawSizeMustBe36[(sizeof(struct Gen5MoveRaw) == GEN5_MOVE_RECORD_SIZE) ? 1 : -1];

extern const struct Gen5MoveRaw gGen5MoveBw[GEN5_MOVE_COUNT];

const struct Gen5MoveRaw *Gen5GetMoveRaw(u16 move);
u8 Gen5GetMoveCategory(u16 move);
u8 Gen5GetMoveTypeGen3(u16 move);
u8 Gen5GetMovePower(u16 move);
u8 Gen5GetMoveAccuracy(u16 move);
u8 Gen5GetMovePP(u16 move);
s8 Gen5GetMovePriority(u16 move);

#endif // GUARD_GEN5_MOVE_ADAPTER_H
