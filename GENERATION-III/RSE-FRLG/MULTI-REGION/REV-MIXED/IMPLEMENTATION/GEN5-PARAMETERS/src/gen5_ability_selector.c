#include "global.h"
#include "constants/pokemon.h"
#include "pokemon.h"
#include "gen5_personal_adapter.h"
#include "gen5_ability_selector.h"

static u8 *GetBoxMonFlagsByte(struct BoxPokemon *boxMon)
{
    return ((u8 *)boxMon) + GEN5_BOXMON_FLAGS_OFFSET;
}

static const u8 *GetBoxMonFlagsByteConst(const struct BoxPokemon *boxMon)
{
    return ((const u8 *)boxMon) + GEN5_BOXMON_FLAGS_OFFSET;
}

bool8 Gen5BoxMonHasHiddenAbility(const struct BoxPokemon *boxMon)
{
    return (*GetBoxMonFlagsByteConst(boxMon) & GEN5_BOXMON_HIDDEN_ABILITY_MASK) != 0;
}

void Gen5SetBoxMonHiddenAbility(struct BoxPokemon *boxMon, bool8 enabled)
{
    u8 *flags = GetBoxMonFlagsByte(boxMon);

    if (enabled)
        *flags |= GEN5_BOXMON_HIDDEN_ABILITY_MASK;
    else
        *flags &= (u8)~GEN5_BOXMON_HIDDEN_ABILITY_MASK;
}

u8 Gen5GetBoxMonAbilitySlot(struct BoxPokemon *boxMon)
{
    if (Gen5BoxMonHasHiddenAbility(boxMon))
        return GEN5_ABILITY_SLOT_HIDDEN;

    /* Three-argument form works with pokeruby and dispatches correctly in FRLG/Emerald. */
    return GetBoxMonData(boxMon, MON_DATA_ABILITY_NUM, NULL)
        ? GEN5_ABILITY_SLOT_2
        : GEN5_ABILITY_SLOT_1;
}

u8 Gen5GetMonAbilitySlot(struct Pokemon *mon)
{
    return Gen5GetBoxMonAbilitySlot(&mon->box);
}

u8 Gen5GetBoxMonAbilityRaw(struct BoxPokemon *boxMon)
{
    u16 species = GetBoxMonData(boxMon, MON_DATA_SPECIES, NULL);
    return Gen5GetAbilityRaw(species, Gen5GetBoxMonAbilitySlot(boxMon));
}

u8 Gen5GetMonAbilityRaw(struct Pokemon *mon)
{
    u16 species = GetMonData(mon, MON_DATA_SPECIES, NULL);
    return Gen5GetAbilityRaw(species, Gen5GetMonAbilitySlot(mon));
}
