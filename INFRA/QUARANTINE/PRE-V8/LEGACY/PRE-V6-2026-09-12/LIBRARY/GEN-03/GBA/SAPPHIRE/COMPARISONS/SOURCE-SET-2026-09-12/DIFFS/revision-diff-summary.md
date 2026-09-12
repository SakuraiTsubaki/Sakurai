# Sapphire revision-diff summary

Byte-for-byte comparisons among supplied releases sharing the same GBA game code.

## AXPE

- `AXPE-R0` → `AXPE-R1`: **5,638,997 differing bytes**.
- `AXPE-R1` → `AXPE-R2`: **4 differing bytes**.
  - `0x0000BC`: `0x01` → `0x02`
  - `0x0000BD`: `0x54` → `0x53`
  - `0x00919B`: `0xDD` → `0xDB`
  - `0x0091BF`: `0xDC` → `0xDA`

## AXPF

- `AXPF-R0` → `AXPF-R1`: **4 differing bytes**.
  - `0x0000BC`: `0x00` → `0x01`
  - `0x0000BD`: `0x54` → `0x53`
  - `0x009367`: `0xDD` → `0xDB`
  - `0x00938B`: `0xDC` → `0xDA`

## AXPI

- `AXPI-R0` → `AXPI-R1`: **4 differing bytes**.
  - `0x0000BC`: `0x00` → `0x01`
  - `0x0000BD`: `0x51` → `0x50`
  - `0x009367`: `0xDD` → `0xDB`
  - `0x00938B`: `0xDC` → `0xDA`

## Key observation

`AXPE-R1 → AXPE-R2`, `AXPF-R0 → AXPF-R1`, and `AXPI-R0 → AXPI-R1` each differ at only four bytes in the supplied images: the GBA header revision/checksum pair plus two nearby program bytes. `AXPE-R0` is structurally much farther from `AXPE-R1/R2` and must not be treated as the same byte layout with only a revision-byte change.
