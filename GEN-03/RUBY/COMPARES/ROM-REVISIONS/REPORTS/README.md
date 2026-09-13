# Pokémon Ruby ROM revision comparison

13 local ROM inputs were fingerprinted; ROM binaries are not committed.

- AXVS HV0↔HV1: 4 differing bytes.
- AXVD retail HV0↔HV1: 4 differing bytes.
- AXVF HV0↔HV1: 4 differing bytes.
- AXVI HV0↔HV1: 4 differing bytes.
- AXVE HV1↔HV2: 4 differing bytes.
- AXVE HV0↔HV1: 5,744,535 differing bytes.
- AXVE HV0↔HV2: 5,744,537 differing bytes.
- AXVD DEBUG HV0↔retail HV0: 6,751,723 differing bytes.
- AXVD DEBUG HV0↔retail HV1: 6,751,725 differing bytes.

All 13 inputs pass the standard GBA header complement check. The German debug image is therefore tracked as a separate release identity, not merely another revision label.
