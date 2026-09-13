# Generation IV → ポケットモンスター — ROM baseline (Structure v5)

Sources locked: 5. Targets locked: 5. Original ROM binaries committed: **no**.

## Source releases
- Diamond: `LIBRARY/GEN-04/DIAMOND/SOURCE/NDS-NTR/CART/ADAE-HV5/` — dump `LGC-a46233d8`
- Pearl: `LIBRARY/GEN-04/PEARL/SOURCE/NDS-NTR/CART/APAE-HV5/` — dump `LGC-99083bf1`
- Platinum: `LIBRARY/GEN-04/PLATINUM/SOURCE/NDS-NTR/CART/CPUK-HV0/` — dump `UPLOAD-f811d9c7`
- HeartGold: `LIBRARY/GEN-04/HEARTGOLD/SOURCE/NDS-NTR/CART/IPKK-HV0/` — dump `UPLOAD-5834fb3a`
- SoulSilver: `LIBRARY/GEN-04/SOULSILVER/SOURCE/NDS-NTR/CART/IPGK-HV0/` — dump `UPLOAD-0330e644`

All five NDS headers have unit code `0x00`, so the source platform profile is `NDS-NTR`.

## Target baseline releases
- Ruby: `LIBRARY/GEN-03/RUBY/SOURCE/GBA/CART/AXVJ-HV0/`
- Sapphire: `LIBRARY/GEN-03/SAPPHIRE/SOURCE/GBA/CART/AXPJ-HV0/`
- Emerald: `LIBRARY/GEN-03/EMERALD/SOURCE/GBA/CART/BPEJ-HV0/`
- FireRed: `LIBRARY/GEN-03/FIRERED/SOURCE/GBA/CART/BPRJ-HV1/`
- LeafGreen: `LIBRARY/GEN-03/LEAFGREEN/SOURCE/GBA/CART/BPGJ-HV0/`

`TARGET` is a project-relative role. The original Japanese GBA releases remain `SOURCE`-owned in `LIBRARY`; the project release lock assigns them as targets.
