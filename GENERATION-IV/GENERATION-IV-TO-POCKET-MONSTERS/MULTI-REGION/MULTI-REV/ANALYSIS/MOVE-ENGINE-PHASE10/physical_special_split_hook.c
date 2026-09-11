/*
 * Generation IV physical/special split hook.
 *
 * Retail Gen III:
 *     physical/special is decided from move TYPE.
 *
 * Generation IV:
 *     physical/special/status is decided per MOVE.
 *
 * Replace every battle-semantic use of:
 *     IS_TYPE_PHYSICAL(type)
 *     IS_TYPE_SPECIAL(type)
 * with the move-category equivalent where Generation IV does so.
 *
 * Core damage selection:
 *
 * switch (GetMoveCategoryGen4(move))
 * {
 * case MOVE_CATEGORY_PHYSICAL:
 *     attack  = attacker->attack;
 *     defense = defender->defense;
 *     break;
 * case MOVE_CATEGORY_SPECIAL:
 *     attack  = attacker->spAttack;
 *     defense = defender->spDefense;
 *     break;
 * default:
 *     return 0;
 * }
 *
 * Move TYPE still controls STAB, type effectiveness, immunities, etc.
 */
