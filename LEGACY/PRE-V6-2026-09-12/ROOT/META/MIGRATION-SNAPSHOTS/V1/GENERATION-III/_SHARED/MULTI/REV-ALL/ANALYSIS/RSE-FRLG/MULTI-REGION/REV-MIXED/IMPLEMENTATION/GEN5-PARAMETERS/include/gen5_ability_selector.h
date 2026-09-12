#ifndef GUARD_GEN5_ABILITY_SELECTOR_H
#define GUARD_GEN5_ABILITY_SELECTOR_H

#include "global.h"
#include "pokemon.h"

/*
 * RSE/FRLG BoxPokemon header byte at 0x13:
 * bits 0..2 sanity flags, bit 3 blockBoxRS, bits 4..7 confirmed unused.
 * Reserve bit 4 only. This does not enlarge BoxPokemon or alter secure data.
 */
#define GEN5_BOXMON_FLAGS_OFFSET          0x13
#define GEN5_BOXMON_HIDDEN_ABILITY_MASK   (1 << 4)

bool8 Gen5BoxMonHasHiddenAbility(const struct BoxPokemon *boxMon);
void Gen5SetBoxMonHiddenAbility(struct BoxPokemon *boxMon, bool8 enabled);
u8 Gen5GetBoxMonAbilitySlot(struct BoxPokemon *boxMon);
u8 Gen5GetMonAbilitySlot(struct Pokemon *mon);
u8 Gen5GetBoxMonAbilityRaw(struct BoxPokemon *boxMon);
u8 Gen5GetMonAbilityRaw(struct Pokemon *mon);

#endif // GUARD_GEN5_ABILITY_SELECTOR_H
