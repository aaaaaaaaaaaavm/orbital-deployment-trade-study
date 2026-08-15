# Change log / audit record

I record changes here by cause and consequence. The retained FAIL and VOID outcomes are part of
the result, not material to be removed when the repository is cleaned up.

## 0.1.3 — the reference impulse, and the comparator phase drift is not

- VOLLEY applied a depth-resolved thrust constant on 2026-08-13. The reference case here still
  carried the superseded impulse: **16.388 → 16.029 m/s**. No test asserts a velocity, so nothing
  else moved.
- **Recorded a boundary the calculator did not have.** Question 2 — phase accumulated from a
  mean-motion difference — computes what it says it computes, and a VOLLEY analysis has since
  shown it is **the wrong comparator for a deployment product**. Satellites released at different
  times from the same host reach different true anomalies **in the same orbit** for no velocity:
  at 450 km, **30° costs 468 s of waiting** against 1.38 days by commanded differential.
- **Release timing is also the better answer.** It sets an offset; a differential sets a rate —
  **21.75 °/day at 10 m/s** — that never stops and that a propulsion-less satellite cannot null.
- What a differential impulse buys that a clock cannot is **the orbit**: +28.8 km of semi-major
  axis and a 1.602 lifetime multiplier against 0 m and 1.0000. **Question 1 is where the value
  is.** VOLLEY records the correction as P56; nothing in this calculator is withdrawn.

## 0.1.2 — hash the committed source state consistently

- Recomputed the source manifest from the retained blobs in VOLLEY commit `aa22a06`, not
  from platform-specific working-tree line endings.
- Made repository verification hash committed blobs while separately rejecting any retained
  source file that differs from the current commit. A source archive normalizes text line endings
  before hashing because no Git metadata is present; binary files remain byte-exact.
- Kept every model result, FAIL, VOID, NOT RUN and unresolved risk unchanged. This is a
  provenance portability fix, not new orbital evidence.

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
