# Pokémon Red source inventory tool

`inspect_red_sources.py` reads local `.gb` inputs and writes a metadata-only JSON inventory plus a CSV summary. It records header fields, validates header/global checksums, fingerprints every 16 KiB bank, and reports byte-identical duplicate inputs.

```sh
python3 inspect_red_sources.py /path/to/read-only-roms output
```

The output never contains ROM bytes. Keep all source ROM paths outside the repository and use the generated hashes to select the correct v3 source route.
