#ifndef GUARD_GEN5_PARAMETER_ADAPTER_H
#define GUARD_GEN5_PARAMETER_ADAPTER_H

/*
 * Generation V -> Generation III parameter adapter.
 *
 * Design goals:
 * - do not destroy native Gen III tables;
 * - preserve raw BW/B2W2 records;
 * - use explicit data profiles;
 * - keep 16-bit species/move/item IDs end-to-end;
 * - expose fields through accessors so R/S/E/FR/LG revisions can hook the
 *   same logical API while keeping version-specific addresses separate.
 *
 * This header intentionally contains no ROM addresses.
 */

#include <stdint.h>

#define GEN5_NATIONAL_SPECIES_COUNT 649
#define GEN5_PERSONAL_RECORD_SIZE   60
#define GEN5_MOVE_RECORD_SIZE       36
#define GEN5_EVOLUTION_SLOTS        7

/* Profile values are stable project ABI values, not original-game IDs. */
typedef enum Gen5DataProfile
{
    DATA_PROFILE_TARGET_ORIGINAL = 0,
    DATA_PROFILE_BW_ORIGINAL     = 1,
    DATA_PROFILE_B2W2_ORIGINAL   = 2,
    DATA_PROFILE_PROJECT_APPLIED = 3,
} Gen5DataProfile;

#pragma pack(push, 1)
typedef struct Gen5PersonalRecord
{
    uint8_t baseHP;              /* 0x00 */
    uint8_t baseAttack;          /* 0x01 */
    uint8_t baseDefense;         /* 0x02 */
    uint8_t baseSpeed;           /* 0x03 */
    uint8_t baseSpAttack;        /* 0x04 */
    uint8_t baseSpDefense;       /* 0x05 */
    uint8_t type1;               /* 0x06 */
    uint8_t type2;               /* 0x07 */
    uint8_t catchRate;           /* 0x08 */
    uint8_t stageAux;            /* 0x09 */
    uint16_t evYield;            /* 0x0A */
    uint16_t heldItem1;          /* 0x0C */
    uint16_t heldItem2;          /* 0x0E */
    uint16_t heldItem3;          /* 0x10 */
    uint8_t genderRatio;         /* 0x12 */
    uint8_t hatchCounter;        /* 0x13 */
    uint8_t baseFriendship;      /* 0x14 */
    uint8_t growthRate;          /* 0x15 */
    uint8_t eggGroup1;           /* 0x16 */
    uint8_t eggGroup2;           /* 0x17 */
    uint8_t ability1;            /* 0x18 */
    uint8_t ability2;            /* 0x19 */
    uint8_t hiddenAbility;       /* 0x1A */
    uint8_t escapeRate;          /* 0x1B */
    uint16_t formStatsStart;     /* 0x1C */
    uint16_t formSpritesStart;   /* 0x1E */
    uint8_t formCount;           /* 0x20 */
    uint8_t bodyColor;           /* 0x21 */
    uint16_t baseExp;            /* 0x22 */
    uint16_t height;             /* 0x24 */
    uint16_t weight;             /* 0x26 */
    uint8_t tmHmBits[16];        /* 0x28 */
    uint8_t trailingCompat[4];   /* 0x38 */
} Gen5PersonalRecord;

typedef struct Gen5MoveRecord
{
    uint8_t type;                /* 0x00 */
    uint8_t effectCategory;      /* 0x01 */
    uint8_t damageCategory;      /* 0x02 */
    uint8_t power;               /* 0x03 */
    uint8_t accuracy;            /* 0x04 */
    uint8_t pp;                  /* 0x05 */
    int8_t priority;             /* 0x06 */
    uint8_t hitsRaw;             /* 0x07 */
    uint16_t resultEffect;       /* 0x08 */
    uint8_t effectChance;        /* 0x0A */
    uint8_t statusAux;           /* 0x0B */
    uint8_t minTurns;            /* 0x0C */
    uint8_t maxTurns;            /* 0x0D */
    uint8_t critStage;           /* 0x0E */
    uint8_t flinch;              /* 0x0F */
    uint16_t effectId;           /* 0x10 */
    int8_t targetHpChange;       /* 0x12 */
    int8_t userHpChange;         /* 0x13 */
    uint8_t target;              /* 0x14 */
    uint8_t affectedStats[3];    /* 0x15 */
    int8_t statMagnitude[3];     /* 0x18 */
    uint8_t statChance[3];       /* 0x1B */
    uint8_t flagsTail[6];        /* 0x1E; preserve raw until fully decoded */
} Gen5MoveRecord;

typedef struct Gen5EvolutionEntry
{
    uint16_t method;
    uint16_t parameter;
    uint16_t targetSpecies;
} Gen5EvolutionEntry;

typedef struct Gen5EvolutionRecord
{
    Gen5EvolutionEntry slots[GEN5_EVOLUTION_SLOTS];
} Gen5EvolutionRecord;
#pragma pack(pop)

/* Compile-time shape checks for canonical BW records. */
typedef char Gen5PersonalRecord_SizeCheck[(sizeof(Gen5PersonalRecord) == 60) ? 1 : -1];
typedef char Gen5MoveRecord_SizeCheck[(sizeof(Gen5MoveRecord) == 36) ? 1 : -1];
typedef char Gen5EvolutionRecord_SizeCheck[(sizeof(Gen5EvolutionRecord) == 42) ? 1 : -1];

/* Generated canonical corpora. Index zero is retained as the source zero slot. */
extern const Gen5PersonalRecord gGen5BwPersonal[];
extern const Gen5PersonalRecord gGen5B2w2Personal[];
extern const Gen5MoveRecord gGen5BwMoves[];
extern const Gen5MoveRecord gGen5B2w2Moves[];
extern const Gen5EvolutionRecord gGen5BwEvolutions[];
extern const Gen5EvolutionRecord gGen5B2w2Evolutions[];

/* ID adapters: never raw-copy Gen V type/item IDs into Gen III. */
uint8_t Gen5_MapTypeToGen3(uint8_t gen5Type);
uint16_t Gen5_MapItemToProject(uint16_t gen5Item, Gen5DataProfile profile);

/* Personal-data accessors. */
const Gen5PersonalRecord *Gen5_GetPersonal(uint16_t species, uint8_t form, Gen5DataProfile profile);
uint16_t Gen5_GetBaseExp(uint16_t species, uint8_t form, Gen5DataProfile profile);
uint8_t Gen5_GetBaseFriendship(uint16_t species, uint8_t form, Gen5DataProfile profile);
uint8_t Gen5_GetAbility(uint16_t species, uint8_t form, uint8_t abilitySlot, Gen5DataProfile profile);
uint16_t Gen5_GetHeldItem(uint16_t species, uint8_t form, uint8_t itemSlot, Gen5DataProfile profile);

/* Move/evolution accessors. */
const Gen5MoveRecord *Gen5_GetMove(uint16_t move, Gen5DataProfile profile);
const Gen5EvolutionRecord *Gen5_GetEvolutions(uint16_t species, Gen5DataProfile profile);

/* Target hooks to implement per R/S/E/FR/LG revision. */
uint8_t Project_GetResolvedAbilitySlot(const void *boxOrPartyMon);
void Project_SetResolvedAbilitySlot(void *boxOrPartyMon, uint8_t slot);

#endif /* GUARD_GEN5_PARAMETER_ADAPTER_H */
