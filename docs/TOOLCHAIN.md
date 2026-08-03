# Toolchain record

| Tool | Version | License | Role | Settings and output |
|---|---:|---|---|---|
| Python | 3.11.9 | PSF License | corrected reference scripts and rigid-body integration | source hashes in `SOURCE_MANIFEST.json` |
| NumPy | 2.3.5 | BSD-3-Clause | reference propagation and A13 integration | versions and source hash in result JSON |
| SciPy | 1.17.1 | BSD-3-Clause | bounded optimizer in A6 | `xatol=1e-12`, recorded in A6 JSON |
| NASA GMAT | R2022a | Apache-2.0 | independent A5 propagation | MSISE90, 20×20 gravity, RK89, Luna, Sun and SRP; A5 JSON |
| Space-Track public data | not yet acquired | provider terms apply | planned A9 flown-decay comparison | A9 remains unrun |

GMAT inputs and parsers are retained under `reference/volley/validation/gmat/`. Exact copied
file hashes are in `SOURCE_MANIFEST.json`. GMAT is not vendored.
