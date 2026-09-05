# Generated IPS patches

The exact raw IPS build products are generated deterministically by `../build_hgss_johto256.py` from the recognized Green base ROM and `../hgss_johto256_registry.csv`.

Expected outputs:

| Base | IPS | SHA-1 | Size |
|---|---|---|---:|
| Rev 0 | `green_hgss_johto256_parameters_rev0.ips` | `24142459e09a489ad101de03b1da7368c85ba25d` | 6,807 bytes |
| Rev A | `green_hgss_johto256_parameters_reva.ips` | `568b76a55380ed4d906ba4e79bcc27493ec6aca5` | 6,807 bytes |

The connected GitHub text-content action cannot commit binary bytes directly, so the binary `.ips` files are not embedded through that action. The committed builder was independently re-run and reproduced both expected IPS SHA-1 values exactly. ROM binaries are intentionally excluded from the repository.
