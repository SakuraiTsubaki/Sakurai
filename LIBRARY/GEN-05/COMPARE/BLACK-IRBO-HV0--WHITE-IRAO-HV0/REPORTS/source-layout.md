# Black IRBO-HV0 ↔ White IRAO-HV0 source-layout comparison

Source dumps used for this observation:

- Black: `SWEETNDS-a68b3bed`
- White: `SWEETNDS-f94d4578`

These are exact dump observations, not clean-dump promotion evidence.

## Container-level structure

Both supplied images contain:

- 484 FAT entries
- 237 ARM9 overlay entries/files
- 247 NitroFS files
- 31 NitroFS directories
- 237 NARC containers across NitroFS
- 2 embedded child `.srl` files

The NitroFS top-level file distribution is the same in both images:

- `a/`: 235 files
- `dl_rom/`: 6 files
- `dwc/`: 1 file
- root-level files: 5

## Component comparison

| Component | Result |
|---|---|
| ARM9 | different |
| ARM7 | identical |
| ARM9 overlay table | different |
| FNT | identical |
| FAT | different |
| banner | different |

## FAT-entry equality

- identical: **299 / 484**
- different: **185 / 484**

### ARM9 overlays

- identical: **57 / 237**
- different: **180 / 237**

### NitroFS files

- identical: **242 / 247**
- different: **5 / 247**

The five differing NitroFS paths are:

```text
a/0/2/6
a/0/8/6
a/1/2/6
a/1/7/8
a/2/3/1
```

Do not replace these native path IDs with semantic names in the source tree. Semantic interpretations belong in `DOMAINS` crosswalks and must remain separately verifiable.

## Repository consequence

The result rules out both simplistic storage models:

1. **full physical duplication as the only model** — obscures the very high NitroFS sharing rate;
2. **one merged shared asset tree** — destroys release provenance and hides the very high executable/overlay divergence rate.

v5 therefore keeps release ownership intact and records equality/delta relations here in `COMPARE`. Content-hash equality may be used for deduplication indexes, while source identity remains release-specific.
