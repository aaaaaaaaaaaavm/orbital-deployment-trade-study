# Orbital Deployment Trade Study

<p align="center"><img src="reference/volley/paper/figures/F04_life.png" alt="Corrected VOLLEY orbital-decay reference" width="100%"></p>

An installable screening calculator for tangential deployment impulses, phase drift, host
recoil and attitude disturbance from a closed internal mass move.

> **Status: preliminary orbital and rigid-body calculations.** This does not perform mission
> conjunction assessment, replace a launch-provider analysis, or establish flight safety.
> The atmosphere, covariance and host-control questions require higher-fidelity tools and data.

## What this demonstrates

- orbital-element changes from a tangential impulse using energy and angular momentum;
- phase-drift time from the change in mean motion;
- host recoil from linear-momentum conservation;
- the corrected internal-mass result: peak body rate and attitude offset, with **zero ideal
  residual rate** after a symmetric closed move;
- limiting-case and conservation tests;
- a non-VOLLEY hosted 6U example.

## Run the calculator

```bash
python -m pip install -e .
orbital-trade cases/hosted_6u_example.json
orbital-trade cases/volley_reference.json --out build/volley_reference.json
```

## Verify the repository

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

## Evidence boundary

The corrected VOLLEY astrodynamics, payload-family, attitude and validation sources remain
under `reference/volley/`. A5 remains **FAIL** because GMAT falsified the claimed solar-activity
invariance. A6 retains **VOID** probability-spread rows and an open covariance problem. A9 is
written but unrun. Correcting A13 removed a false cadence floor; it did not validate structural
settling or a host controller.

See [summary](SUMMARY.md), [validation](docs/VALIDATION.md),
[toolchain](docs/TOOLCHAIN.md), [provenance](docs/PROVENANCE.md), and
[open problems](OPEN_PROBLEMS.md).

## License

MIT. External tools and public orbital data retain their own terms.
