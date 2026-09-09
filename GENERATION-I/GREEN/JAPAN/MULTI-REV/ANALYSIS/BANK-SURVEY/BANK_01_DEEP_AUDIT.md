# Bank 01 deep audit — title / link / menu / overworld core

## Revision structure

- Rev 0 `bank1`: `$4000-$7FFA` = `$3FFB` bytes; residual = 5 bytes.
- Rev A `bank1`: `$4000-$7F9A` = `$3F9B` bytes; residual = `$65` (101) bytes.
- Semantic bank1 body shrinks exactly `$60` (96) bytes in Rev A.

## Direct revision edits and exact size accounting

| Change | Rev A size effect |
|---|---:|
| remove `wUnknown_CCE0` initialization in `CableClub_DoBattleOrTrade` | -3 |
| simplify synchronization-zero handling | -5 |
| remove Rev-0-only link data-corruption runtime checker | -33 |
| remove associated `DataCorruptedText`, `MyString`, `PartnersString` | -50 |
| remove Rev-0-only `wUnknown_CCE0` initialization in `CableClubNPC` | -5 |
| **Total** | **-96** |

The map-size delta and revision-conditioned source delta match exactly.

## Link corruption checker removed in Rev A

Rev 0 contains a post-transfer sanity check that tests whether the first character of the player's or peer trainer name is `'Ａ'`. If matched, it copies a self/partner label, prints a data-corruption warning, and enters an endless loop. This entire checker and its warning strings are absent from Rev A.

This is recorded as a factual revision difference; no historical motive is inferred.

## Address cascade

| Symbol | Rev 0 | Rev A |
|---|---:|---:|
| `CableClub_DoBattleOrTrade` | `01:5115` | `01:5115` |
| `CableClub_DoBattleOrTradeAgain` | `01:5146` | `01:5143` |
| `.finishedPatchingPlayerData` | `01:51B3` | `01:51B0` |
| `.trading` | `01:532D` | `01:5304` |
| `PleaseWaitString` | `01:5368` | `01:530D` |

The 11,803 raw byte differences are therefore dominated by downstream shifts and changed addresses rather than 11.8 KiB of unrelated new code.

## Shared bug candidate

The cable-club source has a cross-revision comment at the enemy-party buffer clear: `ld bc, $13b ; bug? This does not reach wTrainerHeaderPtr, leaving data in the buffer`.

Keep this as a candidate for emulator/test-ROM validation because it is outside the revision conditionals.
