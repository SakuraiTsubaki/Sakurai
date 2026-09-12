# Sapphire source revision differences (v6 identities)

- `AXPE-HV0` → `AXPE-HV1`: **5,638,997 differing bytes**; this is a substantial rebuild/re-layout, not a revision-byte-only change.
- `AXPE-HV1` → `AXPE-HV2`: **4 differing bytes**: `0x0000BC` 01→02, `0x0000BD` 54→53, `0x00919B` DD→DB, `0x0091BF` DC→DA.
- `AXPF-HV0` → `AXPF-HV1`: **4 differing bytes**: `0x0000BC` 00→01, `0x0000BD` 54→53, `0x009367` DD→DB, `0x00938B` DC→DA.
- `AXPI-HV0` → `AXPI-HV1`: **4 differing bytes**: `0x0000BC` 00→01, `0x0000BD` 51→50, `0x009367` DD→DB, `0x00938B` DC→DA.

All nine observed ROM headers passed the GBA complement-check validation. Original ROM binaries are not stored in GitHub.
