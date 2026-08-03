# Validation record

| Item | Method | Current outcome |
|---|---|---|
| Standalone impulse calculation | zero, prograde and retrograde limiting cases | PASS for declared software tests |
| Orbit validity boundary | unbound and Earth-intersection rejection cases | PASS for declared software tests |
| Host recoil | linear-momentum conservation and sign-convention tests | PASS; output is a magnitude |
| Internal mass move | closed-form angular-momentum result | zero ideal residual rate; attitude offset remains |
| A5 lifetime ratio | NASA GMAT R2022a, independently implemented force model | **FAIL** on claimed activity invariance |
| A6 conjunction screening | Foster 2-D probability with assumed covariance | three original spread rows remain **VOID**; P1 open |
| A9 flown decay | public element-set history | **NOT RUN** |

Model-to-model agreement does not establish flight behavior. A launch-provider conjunction
assessment requires operational ephemerides, covariance and mission-specific screening.
