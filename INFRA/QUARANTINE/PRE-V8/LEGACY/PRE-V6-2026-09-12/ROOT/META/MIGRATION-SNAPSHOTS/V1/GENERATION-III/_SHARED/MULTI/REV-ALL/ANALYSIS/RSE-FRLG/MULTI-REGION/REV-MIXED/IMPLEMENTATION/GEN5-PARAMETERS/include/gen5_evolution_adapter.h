#ifndef GUARD_GEN5_EVOLUTION_ADAPTER_H
#define GUARD_GEN5_EVOLUTION_ADAPTER_H

#include "global.h"

#define GEN5_EVOLUTION_SLOTS       7
#define GEN5_EVOLUTION_RECORD_SIZE 0x2A
#define GEN5_EVOLUTION_SPECIES     650

struct __attribute__((packed)) Gen5EvolutionEntry
{
    u16 method;
    u16 param;
    u16 targetSpecies;
};

struct __attribute__((packed)) Gen5EvolutionRecord
{
    struct Gen5EvolutionEntry entries[GEN5_EVOLUTION_SLOTS];
};

typedef char Gen5EvolutionRecordSizeMustBe42[(sizeof(struct Gen5EvolutionRecord) == GEN5_EVOLUTION_RECORD_SIZE) ? 1 : -1];

extern const struct Gen5EvolutionRecord gGen5EvolutionBw[GEN5_EVOLUTION_SPECIES];

const struct Gen5EvolutionRecord *Gen5GetEvolutionRecord(u16 species);
const struct Gen5EvolutionEntry *Gen5GetEvolutionEntry(u16 species, u8 slot);

#endif // GUARD_GEN5_EVOLUTION_ADAPTER_H
