#include "global.h"
#include "gen5_evolution_adapter.h"

const struct Gen5EvolutionRecord *Gen5GetEvolutionRecord(u16 species)
{
    if (species >= GEN5_EVOLUTION_SPECIES)
        species = 0;

    return &gGen5EvolutionBw[species];
}

const struct Gen5EvolutionEntry *Gen5GetEvolutionEntry(u16 species, u8 slot)
{
    const struct Gen5EvolutionRecord *record = Gen5GetEvolutionRecord(species);

    if (slot >= GEN5_EVOLUTION_SLOTS)
        slot = 0;

    return &record->entries[slot];
}
