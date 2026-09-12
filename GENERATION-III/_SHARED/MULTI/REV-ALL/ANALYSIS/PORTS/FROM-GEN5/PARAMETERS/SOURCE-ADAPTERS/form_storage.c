#include "global.h"
#include "pokemon.h"
#include "form_storage.h"

/*
 * Persistent 5-bit form storage without increasing sizeof(struct BoxPokemon):
 *   bits 0..3 -> BoxPokemon.unused
 *   bit 4     -> bit 0 of MON_DATA_UNUSED_RIBBONS
 *
 * The high bit is accessed through Get/SetBoxMonData so the secure substruct
 * continues to follow the normal decrypt/checksum/encrypt path.
 */

u8 Project_GetBoxMonForm(struct BoxPokemon *boxMon)
{
    u8 low = boxMon->unused & 0x0F;
    u8 unusedRibbons = (u8)GetBoxMonData(boxMon, MON_DATA_UNUSED_RIBBONS);
    u8 high = (unusedRibbons & 0x01) << 4;

    return (low | high) & PROJECT_FORM_MASK;
}

void Project_SetBoxMonForm(struct BoxPokemon *boxMon, u8 form)
{
    u8 unusedRibbons;

    form &= PROJECT_FORM_MASK;

    boxMon->unused = form & 0x0F;

    unusedRibbons = (u8)GetBoxMonData(boxMon, MON_DATA_UNUSED_RIBBONS);
    unusedRibbons = (unusedRibbons & ~0x01) | ((form >> 4) & 0x01);
    SetBoxMonData(boxMon, MON_DATA_UNUSED_RIBBONS, &unusedRibbons);
}
