#ifndef GUARD_GEN4_FORM_RULES_H
#define GUARD_GEN4_FORM_RULES_H

#include "global.h"
#include "pokemon.h"

enum { FORM_BASE = 0 };

enum {
    ROTOM_FORM_BASE,
    ROTOM_FORM_HEAT,
    ROTOM_FORM_WASH,
    ROTOM_FORM_FROST,
    ROTOM_FORM_FAN,
    ROTOM_FORM_MOW,
    ROTOM_FORM_COUNT
};

enum { GIRATINA_FORM_ALTERED, GIRATINA_FORM_ORIGIN };
enum { SHAYMIN_FORM_LAND, SHAYMIN_FORM_SKY };
enum { PICHU_FORM_NORMAL, PICHU_FORM_SPIKY_EAR };

enum Gen4ArceusHoldEffect {
    GEN4_HOLD_NONE,
    GEN4_HOLD_ARCEUS_FIGHTING,
    GEN4_HOLD_ARCEUS_FLYING,
    GEN4_HOLD_ARCEUS_POISON,
    GEN4_HOLD_ARCEUS_GROUND,
    GEN4_HOLD_ARCEUS_ROCK,
    GEN4_HOLD_ARCEUS_BUG,
    GEN4_HOLD_ARCEUS_GHOST,
    GEN4_HOLD_ARCEUS_STEEL,
    GEN4_HOLD_ARCEUS_FIRE,
    GEN4_HOLD_ARCEUS_WATER,
    GEN4_HOLD_ARCEUS_GRASS,
    GEN4_HOLD_ARCEUS_ELECTRIC,
    GEN4_HOLD_ARCEUS_PSYCHIC,
    GEN4_HOLD_ARCEUS_ICE,
    GEN4_HOLD_ARCEUS_DRAGON,
    GEN4_HOLD_ARCEUS_DARK
};

bool8 Gen4_SetRotomForm(struct Pokemon *mon, u8 form, u8 fallbackMoveSlot);
s8 Gen4_UpdateGiratinaForm(struct Pokemon *mon, bool8 inDistortionWorld);
bool8 Gen4_CanShayminUseGracidea(const struct Pokemon *mon, u8 hour);
void Gen4_SetShayminLandForm(struct Pokemon *mon);
void Gen4_SetShayminSkyForm(struct Pokemon *mon);
u8 Gen4_GetArceusFormFromHoldEffect(u16 holdEffect);
void Gen4_UpdateArceusForm(struct Pokemon *mon, u16 holdEffect);
bool8 Gen4_BlockSpikyEarPichuEvolution(const struct Pokemon *mon);

#endif
