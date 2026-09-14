# Sprite affine API verification

This directory stores expected per-function SHA-256 fingerprints for the 17-function `sprite.c` block mapped in `config/sprite_affine_api.yml`.

Each CSV was generated from one of the nine verified retail Sapphire references. ROM binaries are not stored in the repository.

Use:

```sh
make analyze-sprite-affine-api ROM=/path/to/reference.gba
```

and compare the emitted function boundaries/hashes with the matching target CSV.
