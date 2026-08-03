"""Preliminary orbital-deployment and internal-mass trade calculations.

WHY THESE CALCULATIONS STOP HERE
--------------------------------
A two-body impulse is useful for rejecting a deployment trade before a propagator is needed.
It is not a conjunction product. No atmosphere, J2, covariance, CDM, flexible mode or host
controller enters this module.

The internal-mass calculation keeps peak rate, attitude offset and residual rate separate.
VOLLEY once treated transient return-sled rate as rate left after the sled stopped. Angular
momentum does not support that conclusion: a symmetric closed move returns the ideal rigid body
to zero residual rate while retaining an attitude offset.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


MU_EARTH = 3.986004418e14
R_EARTH = 6_378_137.0


def _finite(**values: float) -> None:
    """Reject undefined inputs before they become plausible orbital outputs."""
    invalid = sorted(name for name, value in values.items() if not math.isfinite(value))
    if invalid:
        raise ValueError("non-finite inputs: " + ", ".join(invalid))


def tangential_impulse(
    altitude_m: float,
    delta_v_m_s: float,
    phase_deg: float = 30.0,
) -> dict[str, float]:
    """Apply a tangential impulse to a circular orbit.

    Positive delta-v places the impulse point at perigee; negative delta-v places it at
    apogee. Unbound and Earth-intersecting results are rejected because neither belongs in
    a deployment trade presented as an orbit.
    """
    altitude_m = float(altitude_m)
    delta_v_m_s = float(delta_v_m_s)
    phase_deg = float(phase_deg)
    _finite(
        altitude_m=altitude_m,
        delta_v_m_s=delta_v_m_s,
        phase_deg=phase_deg,
    )
    if altitude_m <= 0.0:
        raise ValueError("altitude_m must be positive")

    radius = R_EARTH + altitude_m
    initial_velocity = math.sqrt(MU_EARTH / radius)
    post_impulse_velocity = initial_velocity + delta_v_m_s
    specific_energy = 0.5 * post_impulse_velocity**2 - MU_EARTH / radius
    if specific_energy >= 0.0:
        raise ValueError("the post-impulse orbit is not bound")

    semi_major_axis = -MU_EARTH / (2.0 * specific_energy)
    opposite_radius = 2.0 * semi_major_axis - radius
    if opposite_radius <= R_EARTH:
        raise ValueError("the post-impulse orbit intersects Earth")

    if delta_v_m_s >= 0.0:
        perigee, apogee = radius, opposite_radius
    else:
        perigee, apogee = opposite_radius, radius

    initial_mean_motion = math.sqrt(MU_EARTH / radius**3)
    final_mean_motion = math.sqrt(MU_EARTH / semi_major_axis**3)
    drift_deg_day = (
        abs(final_mean_motion - initial_mean_motion)
        * 86400.0
        * 180.0
        / math.pi
    )

    return {
        "initial_circular_velocity_m_s": initial_velocity,
        "semi_major_axis_m": semi_major_axis,
        "perigee_altitude_m": perigee - R_EARTH,
        "apogee_altitude_m": apogee - R_EARTH,
        "phase_drift_deg_day": drift_deg_day,
        "days_to_phase": (
            math.inf if drift_deg_day == 0.0 else abs(phase_deg) / drift_deg_day
        ),
    }


def host_recoil(
    payload_mass_kg: float,
    deployment_velocity_m_s: float,
    host_mass_kg: float,
) -> float:
    """Return host recoil delta-v magnitude from linear-momentum conservation."""
    payload_mass_kg = float(payload_mass_kg)
    deployment_velocity_m_s = float(deployment_velocity_m_s)
    host_mass_kg = float(host_mass_kg)
    _finite(
        payload_mass_kg=payload_mass_kg,
        deployment_velocity_m_s=deployment_velocity_m_s,
        host_mass_kg=host_mass_kg,
    )
    if payload_mass_kg <= 0.0 or host_mass_kg <= 0.0:
        raise ValueError("masses must be positive")
    return abs(payload_mass_kg * deployment_velocity_m_s / host_mass_kg)


def internal_move(
    mass_kg: float,
    distance_m: float,
    duration_s: float,
    lever_arm_m: float,
    combined_inertia_kg_m2: float,
) -> dict[str, float]:
    """Screen the rigid-body response to a symmetric closed internal move."""
    values = {
        "mass_kg": float(mass_kg),
        "distance_m": float(distance_m),
        "duration_s": float(duration_s),
        "lever_arm_m": float(lever_arm_m),
        "combined_inertia_kg_m2": float(combined_inertia_kg_m2),
    }
    _finite(**values)
    non_positive = sorted(name for name, value in values.items() if value <= 0.0)
    if non_positive:
        raise ValueError("inputs must be positive: " + ", ".join(non_positive))

    peak_velocity = 2.0 * values["distance_m"] / values["duration_s"]
    peak_momentum = values["mass_kg"] * peak_velocity
    peak_rate = (
        peak_momentum
        * values["lever_arm_m"]
        / values["combined_inertia_kg_m2"]
    )
    attitude_offset = (
        -values["mass_kg"]
        * values["lever_arm_m"]
        * values["distance_m"]
        / values["combined_inertia_kg_m2"]
    )

    return {
        "peak_linear_velocity_m_s": peak_velocity,
        "peak_linear_momentum_N_s": peak_momentum,
        "peak_body_rate_deg_s": math.degrees(peak_rate),
        "attitude_offset_deg": math.degrees(attitude_offset),
        # The mass ends at rest. In the ideal rigid-body system there is no angular
        # momentum left to support a residual rate; controller and flexible-mode behavior
        # remain outside this calculation.
        "residual_body_rate_deg_s": 0.0,
    }


def evaluate(case: dict) -> dict:
    """Evaluate the three independent screens in one case file."""
    orbit = tangential_impulse(
        case["altitude_m"],
        case["deployment_delta_v_m_s"],
        case.get("phase_deg", 30.0),
    )
    recoil = host_recoil(
        case["payload_mass_kg"],
        case["deployment_delta_v_m_s"],
        case["host_mass_kg"],
    )
    move = internal_move(**case["internal_move"])
    return {
        "orbit": orbit,
        "host_recoil_m_s": recoil,
        "internal_move": move,
    }


def load_case(path: str | Path) -> dict:
    """Load a UTF-8 JSON case without mission-specific defaults."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
