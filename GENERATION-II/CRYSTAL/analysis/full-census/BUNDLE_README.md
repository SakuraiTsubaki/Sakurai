# Full census raw bundle

The complete raw census ledgers and reproducibility scripts are stored as a split Base64-encoded `tar.gz` bundle because the GitHub connector only writes UTF-8 text.

## Parts
Concatenate in lexical order:
- `bundle/crystal_full_census_bundle.tar.gz.b64.part00`
- `bundle/crystal_full_census_bundle.tar.gz.b64.part01`
- `bundle/crystal_full_census_bundle.tar.gz.b64.part02`
- `bundle/crystal_full_census_bundle.tar.gz.b64.part03`
- `bundle/crystal_full_census_bundle.tar.gz.b64.part04`
- `bundle/crystal_full_census_bundle.tar.gz.b64.part05`
- `bundle/crystal_full_census_bundle.tar.gz.b64.part06`

## Reconstruction
```sh
cat bundle/crystal_full_census_bundle.tar.gz.b64.part* > crystal_full_census_bundle.tar.gz.b64
base64 -d crystal_full_census_bundle.tar.gz.b64 > crystal_full_census_bundle.tar.gz
tar -xzf crystal_full_census_bundle.tar.gz
```

## Checksums
- decoded `crystal_full_census_bundle.tar.gz`: `sha256 6ba1334e6d9f0f174dacc72f89ad8849bc9db89514ecafa8afc97fd2e12d9f39`
- concatenated Base64 text: `sha256 7f0e359bf658c41189df9f484ee64b40246e9ceca3e2d2a98c4b597fd25fa601`

The archive contains all generated CSV ledgers, Markdown reports, and the three census Python scripts. It contains **no ROM bytes**.
