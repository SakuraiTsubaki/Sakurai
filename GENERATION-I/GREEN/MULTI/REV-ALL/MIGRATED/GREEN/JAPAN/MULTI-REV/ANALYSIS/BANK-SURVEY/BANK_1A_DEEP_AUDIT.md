# Pokémon Green JP — Bank 1A deep audit (Rev 0 vs Rev A)

- Role: Version GFX, Tilesets 2, Battle Engine 12.
- Raw differences: **2**.
- `7FF4`: HOME call target `3AD1 → 3ABF` (`-0x12`) — relocation only.
- `7FFF`: `00 → FF`; Rev 0 map has one byte of free/empty space here while Rev A occupies it as revision residual/garbage.
- Direct bank-1A revision edit: **none found**.

**Verdict:** one live relocation byte + one final residual byte. **DEEP-AUDITED / NO-DIRECT-SEMANTIC-DELTA**.
