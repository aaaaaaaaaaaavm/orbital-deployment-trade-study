# Change log / audit record

I record changes here by cause and consequence. The retained FAIL and VOID outcomes are part of
the result, not material to be removed when the repository is cleaned up.

## 0.1.1 — make the corrected evidence state explicit

- Replaced the provisional working-tree provenance with VOLLEY commit `aa22a06`. Every retained
  source file was checked byte-for-byte against that commit before the manifest moved.
- Documented host recoil as a magnitude and made the implementation use that convention for
  either deployment direction. The existing positive-impulse cases do not move.
- Added explicit rejection for non-finite inputs, unbound trajectories and Earth-intersecting
  post-impulse orbits, with tests beside each boundary.
- Expanded the internal-mass comments to keep the peak-rate versus residual-rate correction
  beside the equation that implements it.
- Kept A5 FAIL, A6 VOID, A9 NOT RUN and the unresolved A13 structural/control work visible.

## 0.1.0 — initial public baseline

- Extracted orbital-impulse, phase, recoil and internal-mass screening from VOLLEY.
- Added a standalone interface, a non-VOLLEY case, conservation tests and repository verification.
- Retained the original validation inputs and unresolved evidence limits.
