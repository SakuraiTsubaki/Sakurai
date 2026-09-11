/*
 * Extended effect dispatcher.
 *
 * Retail Gen III has an 8-bit move-effect field and effect IDs through 213.
 * Official HGSS move data uses higher IDs, including values above 255.
 *
 * All effect dispatch must migrate from:
 *     gBattleMoves[move].effect
 * to:
 *     GetMoveEffect16(move)
 *
 * The legacy byte is not authoritative:
 * - for exact effect <= 255 it mirrors the value;
 * - for exact effect > 255 Phase 10 staging writes 0xFF.
 *
 * 0xFF is only a sentinel. It must never be treated as an implemented effect.
 */
