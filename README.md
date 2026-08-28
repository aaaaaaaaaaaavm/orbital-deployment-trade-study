# Orbital Deployment Trade Study

<p align="center"><img src="figures/deployment-trade.svg" alt="Two-body orbital deployment, host recoil and internal-mass screens for two committed cases" width="100%"></p>

[![CI](https://github.com/aaaaaaaaaaaavm/orbital-deployment-trade-study/actions/workflows/ci.yml/badge.svg)](https://github.com/aaaaaaaaaaaavm/orbital-deployment-trade-study/actions/workflows/ci.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Evidence: model only](https://img.shields.io/badge/evidence-model%20only%2C%20unverified-red.svg)](docs/PROVENANCE.md)

An installable preliminary calculator for tangential deployment impulses, phase drift, host
recoil and the rigid-body disturbance from a closed internal mass move.

**Status: two-body and rigid-body trade study.** This does not perform conjunction assessment,
replace a launch-provider analysis or establish flight safety. Atmosphere, covariance,
flexible modes and host control require higher-fidelity tools and mission data.

<p align="center">
  <img src="figures/orbit-envelope.svg" alt="Two-body altitude span and phase drift across a 0 to 20 metre-per-second tangential deployment sweep" width="49%">
  <img src="figures/disturbance-budget.svg" alt="Host recoil, peak body rate and attitude offset for the two committed deployment cases" width="49%">
</p>

<p align="center"><sub>The left sweep separates orbital-energy change from accumulated phase.
The right ledger separates external release recoil from the closed internal-mass disturbance.
All curves and bars are regenerated from the two committed cases.</sub></p>

## Why this exists

VOLLEY's astrodynamics record mixes four questions that do not have the same evidence:

1. what a tangential impulse does to a circular orbit;
2. how mean-motion difference accumulates phase;
3. what linear recoil magnitude the host receives;
4. what ideal angular motion follows an internal mass transfer.

> ### Boundary added 2026-08-14: phase drift is not the cheapest route to phase
>
> Question 2 below computes what it says it computes, and **a VOLLEY analysis has since shown it
> is the wrong comparator for a deployment product.** Satellites released at different times from
> the same host arrive at different true anomalies **in the same orbit**, for no velocity at all:
> at 450 km the in-track rate is **0.0641 °/s**, so **30° costs 468 seconds of waiting** against
> 1.38 days by commanded differential velocity.
>
> **Release timing also gives a better answer, not just a cheaper one.** It sets a static offset;
> a differential sets a **rate** — 21.75 °/day at 10 m/s — that never stops and that a
> propulsion-less satellite cannot null.
>
> **What a differential impulse buys that a clock cannot is a commanded change in orbital energy**:
> +28.8 km of semi-major axis and a 1.602 lifetime multiplier, against 0 m and 1.0000 for timed
> release. *That is a statement about what a deployment interface can command — drag, J<sub>2</sub>
> and solar radiation pressure change orbital elements too, and question 1 below prices none of
> them.* Question 1, not question 2, is where the value is. VOLLEY records this as **P56**.

The first three are useful screening calculations. The fourth is here because a VOLLEY audit
found that peak rate had been mistaken for residual rate. A symmetric closed move returns to
**zero ideal residual body rate** but leaves an attitude offset. That correction removed a
false 18.1 s cadence floor; it did not produce a host-controller or structural-settling model.

<p align="center"><img src="reference/volley/paper/figures/F04_life.png" alt="Corrected VOLLEY orbital-decay reference" width="100%"></p>

<p align="center"><sub>The overview is regenerated from both committed cases by
<code>tools/generate_readme_figure.py</code>. The lifetime plot is retained from the detailed
VOLLEY reference. Both are model output, not flight evidence.</sub></p>

## What the calculator does

- derives the post-impulse ellipse from specific energy and angular momentum;
- computes phase-drift time from the difference in mean motion;
- reports host recoil as a magnitude from linear-momentum conservation;
- separates transient peak rate, attitude offset and ideal residual rate;
- rejects unbound or Earth-intersecting trajectories rather than returning plausible numbers;
- includes one VOLLEY reference case and one independent hosted-6U example.

## Run it

```bash
python -m pip install -e .
orbital-trade cases/hosted_6u_example.json
orbital-trade cases/volley_reference.json --out build/volley_reference.json
```

## Verify it

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```

The tests cover zero impulse, prograde and retrograde geometry, unbound rejection, momentum
conservation, recoil sign convention and the corrected closed internal move.

## Evidence boundary

The committed VOLLEY astrodynamics, payload-family, attitude and validation sources remain
under `reference/volley/`. Their uncomfortable results remain attached:

| Item | Current record |
|---|---|
| A5 | **FAIL** — GMAT falsified the claimed solar-activity invariance |
| A6 | three probability-spread rows remain **VOID**; no operational covariance or CDM |
| A9 | **NOT RUN** against flown public orbital history |
| A13 | corrected zero ideal residual rate; structural settling and control remain open |

NASA GMAT reproduced and challenged numerical claims. NASA did not validate or endorse VOLLEY.

## Repository layout

- `src/orbital_trade/` — two-body, recoil and internal-mass screening functions;
- `cases/` — one VOLLEY case and one non-VOLLEY hosted-6U case;
- `tests/` — limiting cases, conservation checks and rejection paths;
- `reference/volley/` — files retained byte-for-byte from VOLLEY commit `aa22a06`;
- `docs/` — validation boundary, tool versions, provenance, decisions and roadmap.

See [summary](SUMMARY.md), [validation](docs/VALIDATION.md),
[toolchain](docs/TOOLCHAIN.md), [provenance](docs/PROVENANCE.md), and
[open problems](OPEN_PROBLEMS.md).

## Licence

**CC BY 4.0** — full text in [`LICENSE`](LICENSE), attribution form in [`NOTICE`](NOTICE).
Attribution requires credit, a link to the licence, and **an indication of whether changes were
made**.

**Not retroactive:** snapshots taken before this change remain available under the MIT licence
they carried at the time, retained at [`LICENSE-MIT-superseded`](LICENSE-MIT-superseded).

This repository carries copies of VOLLEY analysis code under `reference/volley/`. CC BY 4.0 does
not license patent rights, which is why a patent-granting licence was not used here.
