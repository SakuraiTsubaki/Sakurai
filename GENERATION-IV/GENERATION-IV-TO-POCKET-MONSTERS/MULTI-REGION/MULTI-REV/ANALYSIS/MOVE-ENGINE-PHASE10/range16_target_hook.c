/*
 * Exact Generation IV targeting/range hook.
 *
 * HGSS range constants:
 * 0x000 SINGLE_TARGET
 * 0x001 SINGLE_TARGET_SPECIAL
 * 0x002 RANDOM_OPPONENT
 * 0x004 ADJACENT_OPPONENTS
 * 0x008 ALL_ADJACENT
 * 0x010 USER
 * 0x020 USER_SIDE
 * 0x040 FIELD
 * 0x080 OPPONENT_SIDE
 * 0x100 ALLY
 * 0x200 SINGLE_TARGET_USER_SIDE
 * 0x400 FRONT
 *
 * Retail Gen III target is only one byte and is not equivalent.
 * All target selection / multi-target loops must consult GetMoveRange16().
 *
 * Two immediate hard blockers:
 * - Acupressure (#367) uses 0x200
 * - Me First (#382) uses 0x400
 */
