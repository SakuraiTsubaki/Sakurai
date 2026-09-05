# Green 386 + Generation III forms — MBC5 runtime scaffold

This is the first ROM-layout baseline for the `#001-386 + Generation III forms` runtime milestone.

## What is already true

- Both Pokémon Green Rev0 and RevA are expanded from 512 KiB to **1 MiB / 64 ROM banks**.
- Cartridge header is migrated from MBC1+RAM+BATTERY to **MBC5+RAM+BATTERY** while retaining 32 KiB SRAM.
- The verified `G386F3` cumulative parameter block is embedded at file offset `0x080000` (MBC5 bank `$20`).
- A 256-entry legacy Green 8-bit internal-ID → canonical `u16 species_id` bridge is embedded at `0x085000` (bank `$21`); exactly 151 original Kanto species are mapped and all non-species/unused legacy IDs resolve to `0xFFFF`.
- A `G386MAP` ABI descriptor is embedded at `0x085200`.
- The long-term identity ABI remains `species_id: u16` + `form_id: u8`.
- IPS generation is deterministic and applying each IPS back to its matching original ROM reproduces the corresponding scaffold ROM byte-for-byte.

## Structural verification

The original 512 KiB region changes at only five header/checksum bytes:

- `0x0147`: cartridge type → `0x1B` (MBC5+RAM+BATTERY)
- `0x0148`: ROM size → `0x05` (1 MiB)
- `0x014D`: header checksum
- `0x014E-014F`: global checksum

No original gameplay/data/code byte is hooked yet.

## Mapper rationale

Green's original banked calls write the ROM bank number through the low ROM-bank register and the stock 512 KiB image only uses banks 0-31. Those writes remain compatible with the low 8-bit MBC5 ROM-bank register. Green's MBC1 `$6000` banking-mode writes are used around SRAM access; MBC5 ignores `$6000`, while `$4000-$5FFF` directly selects the SRAM bank, matching the required save-data behavior for the existing 32 KiB SRAM layout.

This is still a **static scaffold**, not a claim that 386 species are playable yet.

## Next runtime gates

1. Banked `G386F3` loader and canonical lookup ABI.
2. Party and battle working records using `u16 species_id + u8 form_id`.
3. Box/save migration and compatibility policy.
4. Personal-data lookup hook.
5. Wild/trainer/evolution/move/Pokédex hooks.
6. Unown, Castform and Deoxys form rules.
7. Sprite/cry/palette routing and full Rev0/RevA regression testing.

Original ROM binaries are never committed. Only builders, ledgers, manifests, verification reports, parameter blocks and patches are stored here.