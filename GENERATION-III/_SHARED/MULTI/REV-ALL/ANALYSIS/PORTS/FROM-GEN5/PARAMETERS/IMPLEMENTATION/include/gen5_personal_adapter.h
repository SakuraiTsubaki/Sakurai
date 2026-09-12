#ifndef GUARD_GEN5_PERSONAL_ADAPTER_H
#define GUARD_GEN5_PERSONAL_ADAPTER_H

#include "global.h"

#define GEN5_NATIONAL_SPECIES_COUNT 649
#define GEN5_BASE_PERSONAL_COUNT    (GEN5_NATIONAL_SPECIES_COUNT + 1)
#define GEN5_PERSONAL_RECORD_SIZE   0x3C
#define GEN5_TMHM_BYTES             0x10
#define GEN5_TUTOR_BYTES            0x04

enum Gen5AbilitySlot
{
    GEN5_ABILITY_SLOT_1 = 0,
    GEN5_ABILITY_SLOT_2 = 1,
    GEN5_ABILITY_SLOT_HIDDEN = 2,
};

/*
 * Canonical BW personal.narc member, /a/0/1/6.
 * Keep this source record intact. Target-ID translation belongs in accessors.
 */
struct __attribute__((packed)) Gen5PersonalRaw
{
    u8 baseHP;
    u8 baseAttack;
    u8 baseDefense;
    u8 baseSpeed;
    u8 baseSpAttack;
    u8 baseSpDefense;
    u8 type1;
    u8 type2;
    u8 catchRate;
    u8 stageAux;
    u16 evYield;
    u16 heldItem1;
    u16 heldItem2;
    u16 heldItem3;
    u8 genderRatio;
    u8 hatchCounter;
    u8 baseFriendship;
    u8 growthRate;
    u8 eggGroup1;
    u8 eggGroup2;
    u8 ability1;
    u8 ability2;
    u8 abilityHidden;
    u8 escapeRate;
    u16 formStatsStart;
    u16 formSpritesStart;
    u8 formCount;
    u8 bodyColor;
    u16 baseExp;
    u16 height;
    u16 weight;
    u8 tmHmCompatibility[GEN5_TMHM_BYTES];
    u8 tutorCompatibility[GEN5_TUTOR_BYTES];
};

typedef char Gen5PersonalRawSizeMustBe60[(sizeof(struct Gen5PersonalRaw) == GEN5_PERSONAL_RECORD_SIZE) ? 1 : -1];

/* Generated locally from a legally supplied BW ROM by tools/extract_gen5_personal.py. */
extern const struct Gen5PersonalRaw gGen5PersonalBw[GEN5_BASE_PERSONAL_COUNT];

const struct Gen5PersonalRaw *Gen5GetPersonalRaw(u16 species);
u8 Gen5TypeToGen3Type(u8 gen5Type);
u16 Gen5GetBaseExp(u16 species);
u8 Gen5GetAbilityRaw(u16 species, u8 abilitySlot);
u16 Gen5GetHeldItemRaw(u16 species, u8 itemSlot);
bool8 Gen5CanLearnTmHmBit(u16 species, u16 bitIndex);
bool8 Gen5CanLearnTutorBit(u16 species, u16 bitIndex);

#endif // GUARD_GEN5_PERSONAL_ADAPTER_H
