# Stage 2 — Silver 16-bit species engine port

## Architecture choice
Do not try to consume all 256 byte values as species IDs. Vanilla G/S uses one-byte species IDs with reserved/sentinel values, including Egg and list terminators. Instead, use a 16-bit logical species ID and an 8-bit transient/storage translation table, following the `pokecrystal16` strategy.

This keeps the change bounded and avoids blindly doubling every party/box/save structure. Any one-byte on-save/transient species token is resolved through a conversion table to the 16-bit logical species ID when game logic needs it.

## Required Silver-specific audit
1. Enumerate every read/write of `MON_SPECIES`, box species arrays, party species arrays and temporary species variables.
2. Add 16-bit load/store wrappers and conversion-table lifecycle/garbage collection.
3. Keep reserved negative/special logical IDs separate from real IDs `1..256`.
4. Convert table lookups to 16-bit-safe indexing and banked pointer tables.
5. Widen Pokédex order and any structure that must directly hold 256 rather than translating transiently.
6. Verify Japanese 30-mon boxes and international/Korean 20-mon boxes independently.
7. Preserve save compatibility where possible; extended species must have deterministic behavior if an old save is loaded.

## HGSS-evolution extension
Add `EVOLVE_MOVE_KNOWN` to Silver's evolution parser. Required rules:

- Yanma + AncientPower (#246) -> Yanmega (#252)
- Aipom + Double Hit (#252) -> Ambipom (#253)
- Lickitung + Rollout (#205) -> Lickilicky (#254)
- Tangela + AncientPower (#246) -> Tangrowth (#255)
- Piloswine + AncientPower (#246) -> Mamoswine (#256)

The check must occur on level-up and obey Everstone/evolution cancellation semantics already used by Silver.

## Double Hit
Gen IV parameters staged for logical move ID 252:
- Normal
- 35 power per strike
- 90% accuracy
- 10 PP
- exactly two hits

Silver already has multi-hit/effect infrastructure, but the move table, name, effect selector, battle animation and learnset reference must all be extended together.

## Compatibility policy
- Normal gameplay on the patched eight-language family: full 256 logical species.
- Time Capsule / unpatched Gen-II link peers: reject or hide extended species rather than serializing an invalid vanilla byte.
- Existing species 1..251 retain their original logical IDs.
