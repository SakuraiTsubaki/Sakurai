/*
 * Generation IV form-system integration scaffold for Gen III.
 *
 * IMPORTANT:
 * - Do not place form in the encrypted BoxPokemon substruct by stealing ribbon bits.
 * - Persist forms in a save sidecar and move/copy that sidecar whenever a mon changes slot.
 * - Species remains the National Dex base species ID.
 * - This file is a source-integration scaffold, not a drop-in binary patch.
 */

#include "global.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "gen3_form_system.h"
#include "constants/species.h"
#include "constants/items.h"

#define BOX_FORM_COUNT (TOTAL_BOXES_COUNT * IN_BOX_COUNT)
#define BOX_FORM_BYTES ((BOX_FORM_COUNT * FORM_BITS + 7) / 8)
#define PARTY_FORM_COUNT PARTY_SIZE
#define PARTY_FORM_BYTES ((PARTY_FORM_COUNT * FORM_BITS + 7) / 8)

static u8 ReadPacked5(const u8 *data, u16 index)
{
    u16 bit = index * FORM_BITS;
    u16 byte = bit >> 3;
    u8 shift = bit & 7;
    u16 word = data[byte];
    if (shift > 3)
        word |= (u16)data[byte + 1] << 8;
    return (word >> shift) & FORM_MASK;
}

static void WritePacked5(u8 *data, u16 index, u8 form)
{
    u16 bit = index * FORM_BITS;
    u16 byte = bit >> 3;
    u8 shift = bit & 7;
    u16 word = data[byte];
    u16 mask;

    form &= FORM_MASK;
    if (shift > 3)
        word |= (u16)data[byte + 1] << 8;

    mask = (u16)FORM_MASK << shift;
    word = (word & ~mask) | ((u16)form << shift);
    data[byte] = word & 0xFF;
    if (shift > 3)
        data[byte + 1] = word >> 8;
}

/*
 * These pointers must be bound to verified free tails in the save blocks
 * for each R/S/E/FR/LG target. Do not hardcode Emerald offsets for other games.
 */
extern u8 *gGen4PartyFormSidecar; // PARTY_FORM_BYTES (4)
extern u8 *gGen4BoxFormSidecar;   // BOX_FORM_BYTES (263)

u8 GetBoxSlotForm(u8 boxId, u8 slot)
{
    return ReadPacked5(gGen4BoxFormSidecar, boxId * IN_BOX_COUNT + slot);
}

void SetBoxSlotForm(u8 boxId, u8 slot, u8 form)
{
    WritePacked5(gGen4BoxFormSidecar, boxId * IN_BOX_COUNT + slot, form);
}

void MoveBoxSlotForm(u8 srcBox, u8 srcSlot, u8 dstBox, u8 dstSlot)
{
    u8 form = GetBoxSlotForm(srcBox, srcSlot);
    SetBoxSlotForm(dstBox, dstSlot, form);
    ClearBoxSlotForm(srcBox, srcSlot);
}

void ClearBoxSlotForm(u8 boxId, u8 slot)
{
    SetBoxSlotForm(boxId, slot, FORM_DEFAULT);
}

/*
 * Effective-form dispatch.
 * Only persistent forms read the sidecar directly.
 * Dynamic forms are recomputed from original Gen IV conditions.
 */
u8 GetEffectiveMonForm(const struct Pokemon *mon, bool32 inBattle)
{
    u16 species = GetMonData(mon, MON_DATA_SPECIES, NULL);
    u16 item = GetMonData(mon, MON_DATA_HELD_ITEM, NULL);

    switch (species)
    {
    case SPECIES_CASTFORM:
        /* Existing Gen III Forecast/weather path remains authoritative in battle. */
        return 0;

    /* Add canonical National-Dex species constants after ID normalization:
     * DEOXYS 386: persistent
     * BURMY 412: persistent
     * WORMADAM 413: persistent
     * CHERRIM 421: volatile weather form
     * SHELLOS 422: persistent
     * GASTRODON 423: persistent
     * ROTOM 479: persistent
     * GIRATINA 487: conditional (Griseous Orb / field rule)
     * SHAYMIN 492: conditional/volatile
     * ARCEUS 493: held-item-derived
     */
    default:
        return 0;
    }
}
