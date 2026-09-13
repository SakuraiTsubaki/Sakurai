# Generation I — Pokémon Blue

Canonical architecture: repository v11.

```text
GEN-01/BLUE/
├── RELEASES/GB/CART/<RELEASE-ID>/
├── PROJECTS/<PROJECT-ID>/
├── COMPARES/<COMPARE-ID>/
├── REFERENCES/<REFERENCE-ID>/
└── SHARED/<ARTIFACT-CLASS>/
```

The legacy `SOURCE`, `TARGET`, and `COMPARE` branches under `GEN-01/BLUE` are migration inputs only and receive no new work. New release identity is recorded under `RELEASES`; new cross-release work is recorded under `COMPARES`.

For the current source set, release IDs are `JP-JA-HV0`, `US-EU-EN-HV0`, `EU-DE-HV0`, `EU-ES-HV0`, `EU-FR-HV0`, and `EU-IT-HV0`. Exact dump identity is SHA-256-addressed below each release.

ROM binaries are never committed. Non-ROM outputs are tracked according to the repository-pair contract; Tsubaki is the complete non-ROM superset and Sakurai is the research/control subset.
