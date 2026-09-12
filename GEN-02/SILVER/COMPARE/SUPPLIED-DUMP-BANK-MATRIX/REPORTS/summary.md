# Silver supplied-ROM comparison

All eight currently supplied Silver ROM images were re-read directly from the project files. Header and global checksums validate for all eight. No ROM binary is committed.

- Japan `AAXJ-HV0` -> `AAXJ-HV1`: 19,150 differing bytes out of 1,048,576 (1.826286%); 48/64 same-position 16 KiB banks are byte-identical.
- English `AAXE-HV0` vs Korean `AAXK-HV0`: 882,326 differing bytes out of 2,097,152 (42.072582%); 29/128 same-position banks are byte-identical.
- Korean `AAXK-HV0` uses CGB flag `0xC0` and SGB flag `0x00`; the other supplied releases use CGB `0x80` and SGB `0x03`.

These are dump-level observations only; they do not by themselves prove source-code ancestry or preservation-set canonicality.
