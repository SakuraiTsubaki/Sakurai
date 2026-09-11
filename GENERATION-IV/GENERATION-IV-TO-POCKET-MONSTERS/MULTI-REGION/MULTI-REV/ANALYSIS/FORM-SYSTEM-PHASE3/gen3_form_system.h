#ifndef GEN4_FORM_SYSTEM_H
#define GEN4_FORM_SYSTEM_H

#include "global.h"

#define FORM_BITS 5
#define FORM_MASK 0x1F
#define FORM_DEFAULT 0

enum FormStorageClass
{
    FORM_STORAGE_DERIVED,
    FORM_STORAGE_PERSISTENT,
    FORM_STORAGE_VOLATILE,
    FORM_STORAGE_CONDITIONAL,
};

u8 GetStoredMonForm(const struct Pokemon *mon);
void SetStoredMonForm(struct Pokemon *mon, u8 form);
u8 GetEffectiveMonForm(const struct Pokemon *mon, bool32 inBattle);

u8 GetBoxSlotForm(u8 boxId, u8 slot);
void SetBoxSlotForm(u8 boxId, u8 slot, u8 form);
void MoveBoxSlotForm(u8 srcBox, u8 srcSlot, u8 dstBox, u8 dstSlot);
void ClearBoxSlotForm(u8 boxId, u8 slot);

#endif
