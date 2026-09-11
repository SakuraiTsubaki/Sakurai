/*
 * Generation IV form-change rules backported to the Gen III-style engine.
 * Prerequisites: canonical species IDs 1..493, persisted form accessors,
 * Gen IV move expansion, and Gen IV item/hold-effect translation.
 */
#include "global.h"
#include "pokemon.h"
#include "gen3_gen4_forms.h"
#include "gen4_form_rules.h"
#include "constants/moves.h"

#ifndef MOVE_NONE
#define MOVE_NONE 0
#endif

static const u16 sRotomFormMoves[ROTOM_FORM_COUNT] = {
    MOVE_NONE, MOVE_OVERHEAT, MOVE_HYDRO_PUMP, MOVE_BLIZZARD,
    MOVE_AIR_SLASH, MOVE_LEAF_STORM,
};

bool8 Gen4_SetRotomForm(struct Pokemon *mon, u8 form, u8 fallbackMoveSlot)
{
    u16 newMove;
    u8 i, j;
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) != 479 || form >= ROTOM_FORM_COUNT)
        return FALSE;
    newMove = sRotomFormMoves[form];
    for (i = 0; i < MAX_MON_MOVES; i++) {
        u16 move = GetMonData(mon, MON_DATA_MOVE1 + i, NULL);
        for (j = 1; j < ROTOM_FORM_COUNT; j++) {
            if (move != MOVE_NONE && move == sRotomFormMoves[j]) {
                if (newMove != MOVE_NONE) {
                    SetMonMoveSlot(mon, newMove, i);
                    newMove = MOVE_NONE;
                } else {
                    DeleteMonMoveSlotAndShift(mon, i);
                    i--;
                }
                break;
            }
        }
    }
    if (newMove != MOVE_NONE) {
        for (i = 0; i < MAX_MON_MOVES; i++) {
            if (GetMonData(mon, MON_DATA_MOVE1 + i, NULL) == MOVE_NONE) {
                SetMonMoveSlot(mon, newMove, i);
                break;
            }
        }
        if (i == MAX_MON_MOVES)
            SetMonMoveSlot(mon, newMove, fallbackMoveSlot);
    }
    if (GetMonData(mon, MON_DATA_MOVE1, NULL) == MOVE_NONE)
        SetMonMoveSlot(mon, MOVE_THUNDER_SHOCK, 0);
    SetMonForm(mon, form);
    CalculateMonStats(mon);
    RefreshMonAbilityFromForm(mon);
    return TRUE;
}

s8 Gen4_UpdateGiratinaForm(struct Pokemon *mon, bool8 inDistortionWorld)
{
    u16 item;
    u8 form;
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) != 487)
        return -1;
    item = GetMonData(mon, MON_DATA_HELD_ITEM, NULL);
    form = (inDistortionWorld || item == ITEM_GRISEOUS_ORB)
         ? GIRATINA_FORM_ORIGIN : GIRATINA_FORM_ALTERED;
    SetMonForm(mon, form);
    RefreshMonAbilityFromForm(mon);
    CalculateMonStats(mon);
    return form;
}

bool8 Gen4_CanShayminUseGracidea(const struct Pokemon *mon, u8 hour)
{
    u32 status;
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) != 492)
        return FALSE;
    if (GetMonForm(mon) != SHAYMIN_FORM_LAND)
        return FALSE;
    if (GetMonData(mon, MON_DATA_HP, NULL) == 0)
        return FALSE;
    if (!GetMonData(mon, MON_DATA_MODERN_FATEFUL_ENCOUNTER, NULL))
        return FALSE;
    status = GetMonData(mon, MON_DATA_STATUS, NULL);
    if (status & STATUS1_FREEZE)
        return FALSE;
    return hour >= 4 && hour < 20;
}

void Gen4_SetShayminLandForm(struct Pokemon *mon)
{
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) == 492) {
        SetMonForm(mon, SHAYMIN_FORM_LAND);
        RefreshMonAbilityFromForm(mon);
        CalculateMonStats(mon);
    }
}

void Gen4_SetShayminSkyForm(struct Pokemon *mon)
{
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) == 492) {
        SetMonForm(mon, SHAYMIN_FORM_SKY);
        RefreshMonAbilityFromForm(mon);
        CalculateMonStats(mon);
    }
}

u8 Gen4_GetArceusFormFromHoldEffect(u16 effect)
{
    switch (effect) {
    case GEN4_HOLD_ARCEUS_FIGHTING: return 1;
    case GEN4_HOLD_ARCEUS_FLYING: return 2;
    case GEN4_HOLD_ARCEUS_POISON: return 3;
    case GEN4_HOLD_ARCEUS_GROUND: return 4;
    case GEN4_HOLD_ARCEUS_ROCK: return 5;
    case GEN4_HOLD_ARCEUS_BUG: return 6;
    case GEN4_HOLD_ARCEUS_GHOST: return 7;
    case GEN4_HOLD_ARCEUS_STEEL: return 8;
    case GEN4_HOLD_ARCEUS_FIRE: return 10;
    case GEN4_HOLD_ARCEUS_WATER: return 11;
    case GEN4_HOLD_ARCEUS_GRASS: return 12;
    case GEN4_HOLD_ARCEUS_ELECTRIC: return 13;
    case GEN4_HOLD_ARCEUS_PSYCHIC: return 14;
    case GEN4_HOLD_ARCEUS_ICE: return 15;
    case GEN4_HOLD_ARCEUS_DRAGON: return 16;
    case GEN4_HOLD_ARCEUS_DARK: return 17;
    default: return 0;
    }
}

void Gen4_UpdateArceusForm(struct Pokemon *mon, u16 effect)
{
    u8 form;
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) != 493)
        return;
    if (GetMonAbility(mon) != ABILITY_MULTITYPE)
        return;
    form = Gen4_GetArceusFormFromHoldEffect(effect);
    SetMonForm(mon, form);
}

bool8 Gen4_BlockSpikyEarPichuEvolution(const struct Pokemon *mon)
{
    return GetMonData(mon, MON_DATA_SPECIES, NULL) == 172
        && GetMonForm(mon) == PICHU_FORM_SPIKY_EAR;
}
