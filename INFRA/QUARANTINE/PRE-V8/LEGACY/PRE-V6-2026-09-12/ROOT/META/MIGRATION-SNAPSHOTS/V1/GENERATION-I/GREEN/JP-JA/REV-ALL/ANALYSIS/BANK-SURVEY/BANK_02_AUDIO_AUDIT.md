# Pokémon Green JP — Bank 02 deep audit (Rev 0 vs Rev A)

## Scope
- ROM bank: `02` (`0x008000–0x00BFFF` file range; CPU `4000–7FFF` when mapped)
- Rev 0 SHA-1: `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
- Rev A SHA-1: `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`
- Raw differing bytes: **18 / 16384**

## Semantic layout
The exact source/map baseline gives the same Rev 0 and Rev A layout:
- `Audio Engine 1` starts at `4000`
- `Music 1` follows the engine
- `Sound Effects 1`: `6F2E–7F86`
- `Sound Effect Headers 1`: `7F87–7FE3`
- `Garbage 2`: `7FE4–7FFF` (`0x1C` bytes)

No `_REV0`/`_REV1` conditional is present in the bank-02 audio source itself.

## Exhaustive byte-delta classification
Six differences are inside live/semantic bank data. All six are operands that reference HOME routines whose symbols moved after the 18-byte Rev-A serial edit in bank 00:

| CPU address | Rev 0 bytes/context | Rev A bytes/context | Target |
|---|---|---|---|
| `4A49` | `CD 35 0E` | `CD 23 0E` | `PlayMusic` `0E35 → 0E23` |
| `4A67` | `CD 35 0E` | `CD 23 0E` | `PlayMusic` `0E35 → 0E23` |
| `4A8E` | `CD 81 37` | `CD 6F 37` | `Delay3` `3781 → 376F` |
| `4A95` | `CD 35 0E` | `CD 23 0E` | `PlayMusic` `0E35 → 0E23` |
| `6EFD` | `CD 45 0E` | `CD 33 0E` | `PlaySound` `0E45 → 0E33` |
| `6F2C` | `C3 35 0E` | `C3 23 0E` | `PlayMusic` `0E35 → 0E23` |

Each target moved by exactly `-0x12`, matching the bank-00 HOME shrink.

The remaining **12 differing bytes** are at `7FF4–7FFF`, entirely inside `Garbage 2`; they do not alter audio-engine/music/SFX semantics.

## Verdict
- Direct bank-02 revision logic/data edit: **none found**.
- Live differences: **6 bytes, all relocated HOME address operands**.
- Residual differences: **12 bytes, all garbage-tail bytes**.
- Semantic layout/length: **identical** between Rev 0 and Rev A.
- Status: **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
