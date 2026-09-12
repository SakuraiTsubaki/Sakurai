#ifndef GUARD_PROJECT_FORM_STORAGE_H
#define GUARD_PROJECT_FORM_STORAGE_H

#include "global.h"

#define PROJECT_FORM_BITS 5
#define PROJECT_FORM_MASK ((1 << PROJECT_FORM_BITS) - 1)
#define PROJECT_FORM_AUTO 31
#define PROJECT_FORM_EXPLICIT_MAX 27

struct BoxPokemon;

u8 Project_GetBoxMonForm(struct BoxPokemon *boxMon);
void Project_SetBoxMonForm(struct BoxPokemon *boxMon, u8 form);

#endif // GUARD_PROJECT_FORM_STORAGE_H
