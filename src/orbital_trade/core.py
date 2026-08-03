"""Preliminary orbital-deployment and internal-mass trade calculations."""
from __future__ import annotations

import json
import math
from pathlib import Path

MU_EARTH = 3.986004418e14
R_EARTH = 6_378_137.0


def tangential_impulse(altitude_m: float, delta_v_m_s: float, phase_deg: float = 30.0) -> dict[str, float]:
    radius = R_EARTH + float(altitude_m)
    if radius <= R_EARTH: raise ValueError("altitude_m must be positive")
    v0 = math.sqrt(MU_EARTH / radius)
    v1 = v0 + float(delta_v_m_s)
    energy = 0.5 * v1**2 - MU_EARTH / radius
    if energy >= 0: raise ValueError("the post-impulse orbit is not bound")
    a = -MU_EARTH / (2.0 * energy)
    opposite_radius = 2.0 * a - radius
    if opposite_radius <= R_EARTH: raise ValueError("the post-impulse orbit intersects Earth")
    if delta_v_m_s >= 0:
        perigee, apogee = radius, opposite_radius
    else:
        perigee, apogee = opposite_radius, radius
    n0 = math.sqrt(MU_EARTH / radius**3)
    n1 = math.sqrt(MU_EARTH / a**3)
    drift_deg_day = abs(n1 - n0) * 86400.0 * 180.0 / math.pi
    return {
        "initial_circular_velocity_m_s": v0,
        "semi_major_axis_m": a,
        "perigee_altitude_m": perigee - R_EARTH,
        "apogee_altitude_m": apogee - R_EARTH,
        "phase_drift_deg_day": drift_deg_day,
        "days_to_phase": math.inf if drift_deg_day == 0 else abs(phase_deg) / drift_deg_day,
    }


def host_recoil(payload_mass_kg: float, deployment_velocity_m_s: float, host_mass_kg: float) -> float:
    if payload_mass_kg <= 0 or host_mass_kg <= 0: raise ValueError("masses must be positive")
    return payload_mass_kg * deployment_velocity_m_s / host_mass_kg


def internal_move(mass_kg: float, distance_m: float, duration_s: float,
                  lever_arm_m: float, combined_inertia_kg_m2: float) -> dict[str, float]:
    if min(mass_kg, distance_m, duration_s, lever_arm_m, combined_inertia_kg_m2) <= 0:
        raise ValueError("all internal-move inputs must be positive")
    peak_velocity = 2.0 * distance_m / duration_s
    peak_momentum = mass_kg * peak_velocity
    peak_rate = peak_momentum * lever_arm_m / combined_inertia_kg_m2
    attitude_offset = -mass_kg * lever_arm_m * distance_m / combined_inertia_kg_m2
    return {
        "peak_linear_velocity_m_s": peak_velocity,
        "peak_linear_momentum_N_s": peak_momentum,
        "peak_body_rate_deg_s": math.degrees(peak_rate),
        "attitude_offset_deg": math.degrees(attitude_offset),
        "residual_body_rate_deg_s": 0.0,
    }


def evaluate(case: dict) -> dict:
    orbit = tangential_impulse(case["altitude_m"], case["deployment_delta_v_m_s"], case.get("phase_deg", 30.0))
    recoil = host_recoil(case["payload_mass_kg"], case["deployment_delta_v_m_s"], case["host_mass_kg"])
    move = internal_move(**case["internal_move"])
    return {"orbit": orbit, "host_recoil_m_s": recoil, "internal_move": move}


def load_case(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
