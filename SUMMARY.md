# Orbital Deployment Trade Study: one page

The package answers a bounded preliminary question: what does a tangential deployment impulse
do to a circular orbit, how quickly does mean-motion difference accumulate phase, what recoil
magnitude does the host receive, and what ideal rigid-body motion follows an internal mass
transfer?

The calculation keeps four outputs separate:

| Output | Meaning |
|---|---|
| Post-impulse perigee and apogee | two-body geometry at the impulse point |
| Phase-drift time | mean-motion difference, not a propagated conjunction |
| Host recoil | magnitude from linear-momentum conservation |
| Internal-mass response | transient peak rate, attitude offset and zero ideal residual rate |

The corrected internal-mass result matters because VOLLEY once treated peak rate during sled
return as rate left after the sled stopped. A symmetric closed move ends with zero ideal
residual body rate but leaves an attitude offset. Flexible modes, damping, controller behavior
and restoration time remain open.

The retained record keeps A5 FAIL, A6 VOID rows and A9 NOT RUN visible. NASA GMAT reproduced
and challenged claims; NASA did not validate or endorse the design. This is a trade calculator,
not a conjunction product or flight-dynamics certification.
