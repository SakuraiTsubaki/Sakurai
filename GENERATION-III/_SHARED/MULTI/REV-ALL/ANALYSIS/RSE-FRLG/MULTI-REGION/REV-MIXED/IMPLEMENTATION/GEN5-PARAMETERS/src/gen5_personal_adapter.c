#include "global.h"
#include "constants/pokemon.h"
#include "gen5_personal_adapter.h"

/*
 * Gen V type IDs are contiguous 0..16 and omit Gen III's TYPE_MYSTERY slot.
 * Never raw-copy type IDs into a Gen III target.
 */
static const u8 sGen5ToGen3Type[] =
{
    TYPE_NORMAL,
    TYPE_FIGHTING,
    TYPE_FLYING,
    TYPE_POISON,
    TYPE_GROUND,
    TYPE_ROCK,
    TYPE_BUG,
    TYPE_GHOST,
    TYPE_STEEL,
    TYPE_FIRE,
    TYPE_WATER,
    TYPE_GRASS,
    TYPE_ELECTRIC,
    TYPE_PSYCHIC,
    TYPE_ICE,
    TYPE_DRAGON,
    TYPE_DARK,
};

const struct Gen5PersonalRaw *Gen5GetPersonalRaw(u16 species)
{
    if (species > GEN5_NATIONAL_SPECIES_COUNT)
        species = 0;

    return &gGen5PersonalBw[species];
}

u8 Gen5TypeToGen3Type(u8 gen5Type)
{
    if (gen5Type >= ARRAY_COUNT(sGen5ToGen3Type))
        return TYPE_MYSTERY;

    return sGen5ToGen3Type[gen5Type];
}

u16 Gen5GetBaseExp(u16 species)
{
    return Gen5GetPersonalRaw(species)->baseExp;
}

u8 Gen5GetAbilityRaw(u16 species, u8 abilitySlot)
{
    const struct Gen5PersonalRaw *personal = Gen5GetPersonalRaw(species);

    switch (abilitySlot)
    {
    case GEN5_ABILITY_SLOT_1:
        return personal->ability1;
    case GEN5_ABILITY_SLOT_2:
        return personal->ability2;
    case GEN5_ABILITY_SLOT_HIDDEN:
        return personal->abilityHidden;
    default:
        return 0;
    }
}

u16 Gen5GetHeldItemRaw(u16 species, u8 itemSlot)
{
    const struct Gen5PersonalRaw *personal = Gen5GetPersonalRaw(species);

    switch (itemSlot)
    {
    case 0:
        return personal->heldItem1;
    case 1:
        return personal->heldItem2;
    case 2:
        return personal->heldItem3;
    default:
        return 0;
    }
}

bool8 Gen5CanLearnTmHmBit(u16 species, u16 bitIndex)
{
    const struct Gen5PersonalRaw *personal = Gen5GetPersonalRaw(species);
    u16 byteIndex;
    u8 bitMask;

    if (bitIndex >= GEN5_TMHM_BYTES * 8)
        return FALSE;

    byteIndex = bitIndex >> 3;
    bitMask = 1 << (bitIndex & 7);
    return (personal->tmHmCompatibility[byteIndex] & bitMask) != 0;
}

bool8 Gen5CanLearnTutorBit(u16 species, u16 bitIndex)
{
    const struct Gen5PersonalRaw *personal = Gen5GetPersonalRaw(species);
    u16 byteIndex;
    u8 bitMask;

    if (bitIndex >= GEN5_TUTOR_BYTES * 8)
        return FALSE;

    byteIndex = bitIndex >> 3;
    bitMask = 1 << (bitIndex & 7);
    return (personal->tutorCompatibility[byteIndex] & bitMask) != 0;
}
