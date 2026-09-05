# Binary outputs

The deterministic builder produces three non-ROM binary artifacts that are part of this expansion stage:

- `expanded_johto268_parameter_block.bin` — SHA-1 `8b6984805500f2244bada46a7f285354f1ea0f1b`
- `green_expanded_johto268_parameters_rev0.ips` — SHA-1 `2d4265fd539f9ee2a2e4ad8e2908d97fc99ed836`
- `green_expanded_johto268_parameters_reva.ips` — SHA-1 `4bd669ef362be5ad7fe3d5869a82e00cd8fe5c2f`

The ROM binaries themselves are intentionally excluded. These binary artifacts are reproducible from `build_green_johto268.py`; `verify_green_johto268.py` confirms IPS roundtrip identity for both recognized base revisions.
