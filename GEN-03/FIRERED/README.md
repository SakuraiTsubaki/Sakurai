# FireRed corpus

Canonical structure: repository architecture v11.

Eight supplied FireRed images are independently registered as release/dump observations: `BPRJ-HV0`, `BPRJ-HV1`, `BPRE-HV0`, `BPRE-HV1`, `BPRD-HV0`, `BPRF-HV0`, `BPRI-HV0`, and `BPRS-HV0`.

ROM bytes stay local and are never committed. Hashes, observations, analysis, comparisons, extracted/derived assets, project data, patches, build metadata, tools, reports, and verification are GitHub-tracked according to repository policy.

Legacy `SOURCE/`, `TARGET/`, and `COMPARE/` trees are read-only migration inputs. New work uses `RELEASES/`, `PROJECTS/`, `COMPARES/`, `REFERENCES/`, and `SHARED/`.
