# Pocket Monsters Midori (Japan) Rev0 vs Rev A — full revision analysis

## Scope

- Rev0: `Pocket Monsters - Midori (Japan) (SGB Enhanced).gb`
- Rev A: `Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb`
- Both ROMs: 524,288 bytes (512 KiB), 32 × 16 KiB banks, SGB, MBC1+RAM+Battery.
- No ROM image is included in this analysis package.

## Identity / integrity

| Field | Rev0 | Rev A |
|---|---|---|
| SHA-1 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` |
| SHA-256 | `6576b4e0979e93d4a6fa02db893c294b7aeab3b841b1acc8658bc10b3554f33c` | `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816` |
| CRC32 | `BAEACD2B` | `37AE8DC4` |
| Header version byte $014C | `$00` | `$01` |
| Header checksum | `$9C` valid | `$9B` valid |
| Global checksum | `$DDD5` valid | `$F547` valid |

These SHA-1 values match the public `Narishma-gb/pokegreen` disassembly build targets for Japanese Green v1.0 and v1.1 exactly.

## Raw binary diff vs semantic diff

- Raw byte differences: **46,168 bytes** (8.81% of ROM).
- Raw contiguous difference runs: **5,436**.
- This raw number dramatically overstates the amount of rewritten game logic. Deletions/reordering move code, then embedded absolute addresses and pointers change downstream.
- Bank-local sequence alignment gives **8,782 bytes of changed spans per side** in total, rather than 46,168 independently rewritten bytes.

### Highest raw-diff banks

| Bank | Raw differing bytes | % of bank | Aligned changed span | Interpretation |
|---:|---:|---:|---:|---|
| `$0F` | 15,403 | 94.01% | 1,280 | battle core revisions and relocation |
| `$00` | 13,109 | 80.01% | 956 | serial routine deletion/reordering; downstream -18 byte shift |
| `$01` | 11,803 | 72.04% | 1,084 | Cable Club code + corrupted-data text removal; -91/-96 shifts |
| `$07` | 560 | 3.42% | 557 | mostly pointer/garbage/revision-layout effects |
| `$09` | 519 | 3.17% | 161 | 38-byte unused serial function deletion + relocation |
| `$1D` | 425 | 2.59% | 422 | mostly pointer/garbage/revision-layout effects |
| `$12` | 406 | 2.48% | 402 | mostly pointer/garbage/revision-layout effects |
| `$17` | 397 | 2.42% | 393 | mostly pointer/garbage/revision-layout effects |
| `$14` | 379 | 2.31% | 377 | mostly pointer/garbage/revision-layout effects |
| `$03` | 366 | 2.23% | 365 | mostly pointer/garbage/revision-layout effects |
| `$18` | 359 | 2.19% | 356 | mostly pointer/garbage/revision-layout effects |
| `$06` | 348 | 2.12% | 341 | mostly pointer/garbage/revision-layout effects |

Bank `$1B` is the only completely byte-identical bank.

## Confirmed source-level revision changes

### 1. Battle menu Select/swap-state glitch — partial fix

Rev A explicitly clears `wMenuItemToSwap` after returning from the battle item list. In Rev0 the stale swap-selection state can survive and be consumed by later menu code. This is the code-level basis of the known partial “closed-menu Select glitch” fix. It is partial rather than global because the state can still be established by other flows.

### 2. Trapping moves (Wrap-family) and link-battle no-action state

Rev A changes several connected pieces of battle logic:

- When the opponent is using a trapping move and the player cannot act, Rev A writes `CANNOT_MOVE` (`$FF`) into `wPlayerSelectedMove` instead of merely skipping move selection.
- Link battles gain an explicit `LINKBATTLE_NO_ACTION` nybble (`$0D`) alongside `$0E` Struggle and `$0F` Run, and Rev A recognizes/transmits it.
- A Rev0 path tests the opponent-side trapping flag where the player-side flag is required; Rev A tests `wPlayerBattleStatus1` instead.
- Together these changes make “cannot act because trapped” an explicit synchronized state and remove a wrong-side status test.

### 3. Haze + frozen turn handling

At ROM file offset **`0x13F4C`** / CPU **`04:7F4C`**, the immediate mask is directly visible in the two ROMs:

- Rev0: `E6 07` → `and SLP_MASK`
- Rev A: `E6 27` → `and (1 << FRZ) | SLP_MASK`

Haze clears the target status in both versions. Rev0 only notices previous sleep when deciding to invalidate the selected move; Rev A notices sleep **or freeze**, so a Pokémon thawed by Haze does not incorrectly execute a move that turn.

### 4. Link Cable corrupted-data check removed

Rev0 contains a special check after link data exchange: if either trainer name starts with full-width `Ａ`, it prints a “data is corrupted, turn power off” message and enters an endless loop. Rev A removes that test, its strings, and the loop. It also removes the auxiliary `wUnknown_CCE0` usage and sends explicit zero bytes for the associated sync bytes.

Consequences in Bank `$01`:

- `PleaseWaitString`: `01:5368` → `01:530D` (**−0x5B / 91 bytes**).
- `CableClubNPC`: `01:736C` → `01:7311` (**−0x5B / 91 bytes**).
- Inside the receptionist flow another Rev0-only 5-byte store disappears, producing a **−96 byte** downstream displacement.

### 5. Serial routine cleanup / reorder

In Bank `$00`, Rev A removes an 18-byte Rev0-only branch in `Serial_ExchangeBytes.storeReceivedByte` that could redirect the receive destination to `wNameBuffer` in an unused reset-link state. The `serial2.asm` include is also moved to a different position relative to `Serial_ExchangeByte`.

Key symbol movement:

- `Serial_ExchangeBytes.storeReceivedByte` stays at `00:0C14`.
- `Serial_ExchangeByte`: `00:0CAA` → `00:0C1C` (large apparent move caused by reordering).
- `Serial_ExchangeLinkMenuSelection`: `00:0C2E` → `00:0CC9`.
- After the reordering settles, `Serial_ExchangeNybble`: `00:0D57` → `00:0D45`, exactly **18 bytes earlier**, matching the net deletion.

This is why Bank `$00` shows 80% raw byte difference even though its aligned changed span is only 956 bytes.

### 6. 38-byte unused serial function deleted

Rev0 has `UnusedSerialFunction` at **`09:7DCE`** (ROM offset **`0x27DCE`**) immediately before type-printing code. Rev A deletes it. `PrintMonType` therefore moves from `09:7DF4` to `09:7DCE`: exactly **`0x26` = 38 bytes** earlier. The local binary alignment independently detects that exact 38-byte deletion.

The deleted routine manipulated Rev0-only `wUnknownSerialCounter3` / `wUnknownSerialByte` variables and even had a documented fall-through into `PrintMonType`; the corresponding symbolic WRAM members are absent in Rev A while the union allocation preserves layout.

### 7. Equivalent code-size optimizations in battle core

Rev A also rewrites multiple instruction sequences without an intended rules change, for example:

- two `bit` tests → load + masked `and`;
- `bit CONFUSED` → `add a` plus carry test where the relevant bit is bit 7;
- fixed-length nickname indexing via `AddNTimes` → `SkipFixedLengthTextEntries`;
- two direct zero stores → one `HL` sequential store;
- LCD enable bit test → arithmetic carry test;
- instruction ordering changes with equivalent values.

These save/rearrange bytes and amplify address differences in Bank `$0F`; they should not be catalogued as gameplay changes.

### 8. Revision-specific garbage/padding bytes

The disassembly explicitly models separate Rev0/Rev1 `Garbage` sections across many banks. Some are different binary leftovers, and some are tiny explicit values (for example 5 bytes in Garbage 4, a byte in Garbage 11/14, Rev0-only 5 bytes in Bank 15, and a Rev1 `$FF` byte in Bank 26). These explain much of the low-density “confetti” diff outside the core changed banks. They are not normal gameplay tables.

## What does *not* appear to be intentionally revised

The revision-condition search in the matching disassembly is confined to the serial/link/battle/WRAM/garbage areas listed above. The actual game-content source files are shared by both builds. Therefore there is no source-level evidence of an intentional RevA content revision to:

- Pokémon species/base-stat/type/evolution/learnset tables;
- Pokémon front/back graphics, overworld sprites, tilesets;
- map layouts, warps, NPC/story scripts, wild encounter tables;
- trainer parties, normal item/move parameter tables, shops;
- Pokédex descriptions;
- music/SFX;
- ordinary Japanese dialogue/text.

Raw byte differences inside banks containing those assets can still occur when pointers/addresses are regenerated or revision-specific garbage changes. Also, invalid/glitch data can behave differently *because code addresses moved* even when the underlying official content table was not edited.

## Important emergent/glitch behavior

Public glitch documentation reports that Rev A partially fixes the closed-menu Select glitch and that at least one glitch item (“Gold Badge”) changes behavior because internal functions moved. This fits the binary/source result: layout movement itself can alter undefined/glitch behavior even where official content data is unchanged.

## Overall conclusion

**Pokémon Green Rev A (v1.1) is primarily a targeted engine-maintenance revision.** Its meaningful edits cluster in battle-state handling and Game Link Cable code. The enormous raw diff in Banks `$00`, `$01`, and `$0F` is mainly a relocation cascade from deleted/reordered code plus rewritten operands, not a wholesale rewrite of maps, sprites, dialogue, or Pokémon data.

For future reverse-engineering/localization work, **Rev A is the better technical baseline for intended normal gameplay behavior**, while Rev0 should be retained as the historical baseline for bug/glitch archaeology and exact version comparison.

## Generated artifacts

- `midori_rev_analysis.json`: machine-readable hashes, raw diff runs, bank stats, alignment metadata.
- `midori_bank_diff.tsv`: complete 32-bank raw diff table.
- `midori_source_level_changes.tsv`: semantic revision ledger.
- `analyze_midori.py`: reproducible local binary-analysis script.

## External reference used for semantic mapping

- `Narishma-gb/pokegreen`: disassembly with separate `_REV0` / `_REV1` build targets whose Green SHA-1 outputs exactly match these two ROMs.
- Public glitch/version documentation used only to cross-check behavioral interpretation; primary evidence here is the matching binaries plus revision-gated source.
