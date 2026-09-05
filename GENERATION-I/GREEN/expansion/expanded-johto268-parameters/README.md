# Pokémon Green — Expanded Johto Dex 268 parameter architecture

Build date: 2026-09-05 (Asia/Seoul)

## Definition

This is **not** the stock HGSS Johto Pokédex copied verbatim. It is an expanded Johto regional roster built from:

- the exact 256-slot HGSS Johto Pokédex backbone;
- plus the **12 Generation IV evolutions of Generation I/II families that DPPt introduced but HGSS omitted from its regional Johto Pokédex**;
- inserted next to their evolutionary families rather than appended as 257-268.

Final roster size: **268 species**.

The five Generation IV evolutions already present in the HGSS Johto Dex remain where HGSS placed them: Yanmega, Ambipom, Lickilicky, Tangrowth, and Mamoswine. Together with the 12 inserted species, the expanded roster contains all **17 Gen-IV evolutions of Gen-I/II evolutionary families**.

## The 12 inserted DPPt evolutions

| Expanded # | National # | Pokémon | Inserted after |
|---:|---:|---|---|
| 048 | 468 | 토게키스 (`TOGEKISS`) | `TOGETIC` |
| 122 | 462 | 자포코일 (`MAGNEZONE`) | `MAGNETON` |
| 156 | 467 | 마그마번 (`MAGMORTAR`) | `MAGMAR` |
| 161 | 466 | 에레키블 (`ELECTIVIRE`) | `ELECTABUZZ` |
| 194 | 470 | 리피아 (`LEAFEON`) | `UMBREON` |
| 195 | 471 | 글레이시아 (`GLACEON`) | `LEAFEON` |
| 200 | 472 | 글라이온 (`GLISCOR`) | `GLIGAR` |
| 220 | 464 | 거대코뿌리 (`RHYPERIOR`) | `RHYDON` |
| 222 | 430 | 돈크로우 (`HONCHKROW`) | `MURKROW` |
| 228 | 461 | 포푸니라 (`WEAVILE`) | `SNEASEL` |
| 230 | 429 | 무우마직 (`MISMAGIUS`) | `MISDREAVUS` |
| 233 | 474 | 폴리곤Z (`PORYGON_Z`) | `PORYGON2` |

## Internal species-ID architecture

The original Green internal IDs were audited before choosing an expansion format. The 268-species design therefore does **not** convert every species field to 16-bit.

### 1. Kanto species — 151 IDs preserved exactly

All 151 original species retain their original Pokémon Green internal IDs. This protects the largest body of existing battle/map/script/save assumptions.

### 2. Generation II species — 100 reclaimed 8-bit IDs

Green has 39 non-real-species IDs in `01-BE` (36 MissingNo holes plus the three fossil/Ghost pseudo-species IDs) and 64 additional byte values in `BF-FE`. That gives 103 reclaimable non-sentinel byte IDs.

The 100 Generation II species are assigned in National Dex order to the first 100 reclaimable IDs. The old fossil/Ghost pseudo-species behavior must be moved out of the species namespace before `B6-B8` become real Pokémon IDs.

### 3. Generation IV evolutions — 17 extended IDs

All 17 Gen-IV evolutions of Gen-I/II families use a clean extended namespace, assigned in National Dex order:

- canonical extended IDs: `0x100-0x110`;
- storage escape byte: `0xFC`;
- extension selector: `0-16`;
- `0xFD` and `0xFE`: reserved for future expansion;
- `0x00`: remains `NO_MON`;
- `0xFF`: remains the existing list terminator/sentinel.

This deliberately preserves the two most pervasive sentinel semantics instead of forcing a whole-engine `00/FF` rewrite.

### Why `0xFC` is safe to reserve

After assigning the 100 Gen-II species, exactly three reclaimable byte IDs remain: `FC`, `FD`, and `FE`. `FC` becomes the extended-species escape, while `FD/FE` remain spare. No normal Kanto or Johto species uses those values.

## Runtime storage target

For a normal species, the existing one-byte species field remains sufficient. For a Gen-IV extended species, a species byte of `FC` indicates that the real species is selected by a parallel extension selector (`0-16`).

The implementation target is therefore **8-bit legacy storage + a compact sidecar only where the engine stores species lists/mon records**, rather than doubling every species field globally. Party, box, daycare, Hall of Fame, wild and trainer formats still need their individual escape/sidecar hooks before the 17 extended species are playable end-to-end.

## ROM parameter layer installed in this pass

Both supplied Green revisions are expanded from 512 KiB to 1 MiB and migrated from MBC1+RAM+Battery (`03`) to MBC5+RAM+Battery (`1B`) so expansion banks can be selected directly by the existing one-byte bank-number convention.

- parameter bank: `21`
- file offset: `0x084000`
- magic: `HGJX268`
- records: 268
- extended species: 17
- parameter block SHA-1: `8b6984805500f2244bada46a7f285354f1ea0f1b`

The installed block contains expanded regional number, original HGSS regional number (or zero for the 12 inserts), National Dex number, canonical internal ID, HGSS-era type pair, storage byte, extension selector and source flags. Exact HGSS personal/evolution/level-up payloads remain the next import stage rather than being guessed.

## Integrity / verification

- Rev 0 output SHA-1: `dfff4d9475cfa41e6c109a1a650caeeede59730d`
- Rev A output SHA-1: `5488b7509fcce40e300cbf8d3643182945c59da0`
- Rev 0 IPS SHA-1: `2d4265fd539f9ee2a2e4ad8e2908d97fc99ed836`
- Rev A IPS SHA-1: `4bd669ef362be5ad7fe3d5869a82e00cd8fe5c2f`
- header checksum: PASS both revisions
- global checksum: PASS both revisions
- IPS roundtrip: PASS both revisions
- unexpected changes in original 512 KiB region: **0**

Only cartridge type, ROM-size byte and dependent checksums are changed inside the original image in this structural pass. The expansion registry is placed in the new ROM area.

## Files

- `expanded_johto268_registry.csv` — canonical 268-row ledger
- `dppt_12_insertions.csv` — only the 12 newly inserted DPPt evolutions
- `gen4_evolutions_17.csv` — all 17 Gen-IV evolutions in the expanded roster
- `build_green_johto268.py` — deterministic ROM/IPS/registry builder
- `verify_green_johto268.py` — structural and roundtrip verifier
- `MANIFEST.json` / `VERIFICATION.json` — hashes and machine-readable status

ROM binaries are build products and must not be committed to GitHub.
