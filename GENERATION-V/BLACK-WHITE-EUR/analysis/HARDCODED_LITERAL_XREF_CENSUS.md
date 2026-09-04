# Pokémon Black/White EUR — literal-pool xref census

This pass resolves Thumb PC-relative `LDR (literal)` instructions whose computed address lands on each boundary constant, then checks the next five instructions for a register `CMP` consuming the loaded value.

|Constant|LDR xrefs|CMP consumers|Sections|
|---:|---:|---:|---|
|386|7|1|OVL081|
|387|7|1|OVL093|
|493|16|12|ARM9, OVL091, OVL095, OVL123, OVL170, OVL206|
|494|4|0|—|
|649|29|22|ARM9, OVL010, OVL021, OVL091, OVL121, OVL212|
|650|25|10|ARM9, OVL021, OVL092, OVL215|
|651|15|9|ARM9, OVL021, OVL118, OVL119, OVL183|
|652|0|0|—|
|667|3|0|—|
|668|0|0|—|
|669|3|0|—|
|999|29|25|ARM9, OVL010, OVL071, OVL091, OVL105, OVL111, OVL119, OVL131, OVL170, OVL206, OVL212|

Representative consumers: ARM9 `0x02006C04` loads 649 then `CMP r0,r3`; ARM9 `0x0200AF72` loads 651 then `CMP r2,r1`; ARM9 `0x020188E4` loads 650 then `CMP r0,r2`; OVL010 `0x02157F10` loads 649 then compares; OVL021 `0x021CCA8A` loads 650 then compares; OVL183 `0x021DF8C2` loads 651 then compares. `999` has 25 comparison consumers and is executable semantics as well as the Unova-Dex non-member sentinel.

Full rows are reproducible with `scripts/literal_xref_census.py`.