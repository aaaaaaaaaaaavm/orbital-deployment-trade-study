# Decision log

## D1: correct peak rate without inventing a residual rate

A moving internal mass gives the host a transient counter-rotation. When the mass decelerates
to rest, the ideal closed system returns the angular momentum; residual rate is zero. The host
retains an attitude offset. The old 18.1 s cadence floor depended on confusing those quantities
and is not retained.

## D2: keep conjunction probability outside the standalone interface

Without an operational covariance or CDM, a probability number would be dominated by an
assumed input. The package exposes orbit geometry and drift; the retained A6 record keeps the
covariance limitation and VOID rows visible.

## D3: report recoil as a magnitude

Deployment direction belongs in the orbit geometry. The scalar host-recoil output is named and
documented as a magnitude, so equal prograde and retrograde impulses return equal positive
values rather than allowing a sign convention to leak into a quantity with no axis attached.

## D4: reject trajectories that are not deployment orbits

An unbound result or an ellipse that intersects Earth can still produce finite, precise-looking
numbers. The public function rejects both before reporting phase drift. That is a validity
boundary, not a numerical convenience.
