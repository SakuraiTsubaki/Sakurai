# RBY source verification — 2026-09-13

Validated 12 local ROM dumps. No ROM binary is committed.

| Game | Platform | Release | Size | Banks | Header ver | CGB | SHA-256 | Checksums |
|---|---|---|---:|---:|---:|---|---|---|
| RED | GB | JP-JA-HV0 | 524288 | 32 | 0 | `0x00` | `392ce450d708c8d127aaed7afc20001a48625bd83a5fa5325be82f5c0972ccfa` | header=OK, global=OK |
| RED | GB | JP-JA-HV1 | 524288 | 32 | 1 | `0x00` | `751abb1fb2b2d6b91dc631fa10ed36bd07f682cb5c3febe6c8f0e3dabc1fae1c` | header=OK, global=OK |
| RED | GB | US-EU-EN-HV0 | 1048576 | 64 | 0 | `0x00` | `5ca7ba01642a3b27b0cc0b5349b52792795b62d3ed977e98a09390659af96b7b` | header=OK, global=OK |
| GREEN | GB | JP-JA-HV0 | 524288 | 32 | 0 | `0x00` | `6576b4e0979e93d4a6fa02db893c294b7aeab3b841b1acc8658bc10b3554f33c` | header=OK, global=OK |
| GREEN | GB | JP-JA-HV1 | 524288 | 32 | 1 | `0x00` | `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816` | header=OK, global=OK |
| BLUE | GB | JP-JA-HV0 | 524288 | 32 | 0 | `0x00` | `71a70e5f77c109177d21c998310ffe01a68e8cd2f41e72e7129093b890c7d3d1` | header=OK, global=OK |
| BLUE | GB | US-EU-EN-HV0 | 1048576 | 64 | 0 | `0x00` | `2a951313c2640e8c2cb21f25d1db019ae6245d9c7121f754fa61afd7bee6452d` | header=OK, global=OK |
| YELLOW | GB | JP-JA-HV0 | 1048576 | 64 | 0 | `0x00` | `09a083624c4f84ccae99165d4091e7c5403aaf9ae44329a9349b4d59b4095436` | header=OK, global=OK |
| YELLOW | GB | JP-JA-HV1 | 1048576 | 64 | 1 | `0x00` | `1acab20d1aa3e19c081abaac3e303c4cf3e582213937acbf25942b31c28aecfe` | header=OK, global=OK |
| YELLOW | GB | JP-JA-HV2 | 1048576 | 64 | 2 | `0x00` | `2c67561f6b2de4ca3a1150f04dc736aead4bf7b5a98ce38196cef899a91be2fd` | header=OK, global=OK |
| YELLOW | GB | JP-JA-HV3 | 1048576 | 64 | 3 | `0x00` | `1349408f328f633b33e059e654edabd19810530df9c883eda03a85d5bb10161a` | header=OK, global=OK |
| YELLOW | GBC | US-EU-EN-HV0 | 1048576 | 64 | 0 | `0x80` | `8cbaa499397e4f1a679c992ea9382a2dd7942ab398b48c19829c2d9529de47bf` | header=OK, global=OK |

The Japanese ROMs are translation originals/build bases. English Red/Blue/Yellow are implementation references only. Green remains independently translated from Japanese Green. English Yellow is canonically routed through `GEN-01/YELLOW/SOURCE/GBC/CART/US-EU-EN-HV0` because its header CGB flag is `0x80`.
