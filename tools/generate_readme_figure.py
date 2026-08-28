"""Generate the README visual set from the committed deployment cases."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from orbital_trade.core import evaluate  # noqa: E402


BG, PANEL, INK, MUTED = "#07111b", "#0c1d2a", "#e8f0f7", "#8fa7ba"
CYAN, VIOLET, AMBER, RED = "#38d6e8", "#9b8cff", "#ffb454", "#ff6b6b"


def txt(x: float, y: float, value: str, size: int, colour: str = INK, weight: int = 400,
        anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{colour}" font-family="Inter,Segoe UI,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def box(x: float, y: float, w: float, h: float, fill: str = PANEL, stroke: str = "#17384b",
        radius: int = 18) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def load(name: str) -> tuple[dict, dict]:
    case = json.loads((ROOT / "cases" / name).read_text(encoding="utf-8"))
    return case, evaluate(case)


def render() -> str:
    cases = [
        ("VOLLEY REFERENCE", *load("volley_reference.json"), CYAN),
        ("HOSTED 6U EXAMPLE", *load("hosted_6u_example.json"), VIOLET),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="920" viewBox="0 0 1600 920">',
        f'<rect width="1600" height="920" fill="{BG}"/>',
        txt(72, 78, "ORBITAL DEPLOYMENT TRADE STUDY", 24, CYAN, 700),
        txt(72, 124, "One case file, three questions that should not be collapsed into one.", 34, INK, 600),
        txt(72, 162, "Two-body orbit geometry · host recoil · closed internal-mass disturbance", 19, MUTED),
    ]

    for i, (label, case, result, colour) in enumerate(cases):
        x = 72 + i * 744
        y = 214
        orbit = result["orbit"]
        move = result["internal_move"]
        out += [box(x, y, 704, 390, stroke=colour), txt(x + 28, y + 46, label, 18, colour, 700)]
        perigee = orbit["perigee_altitude_m"] / 1000.0
        apogee = orbit["apogee_altitude_m"] / 1000.0
        out += [
            txt(x + 28, y + 88, f"{case['deployment_delta_v_m_s']:.3f} m/s tangential release", 25, INK, 650),
            txt(x + 28, y + 124, f"{perigee:.1f} km perigee", 16, MUTED),
            txt(x + 676, y + 124, f"{apogee:.1f} km apogee", 16, MUTED, 400, "end"),
        ]
        # An altitude scale, not a to-scale Earth-orbit drawing.
        scale_x, scale_y, scale_w = x + 28, y + 156, 648
        lo, hi = min(perigee, apogee), max(perigee, apogee)
        out.append(f'<line x1="{scale_x}" y1="{scale_y}" x2="{scale_x + scale_w}" y2="{scale_y}" stroke="#294a5d" stroke-width="8" stroke-linecap="round"/>')
        out.append(f'<line x1="{scale_x}" y1="{scale_y}" x2="{scale_x + scale_w}" y2="{scale_y}" stroke="{colour}" stroke-width="8" stroke-linecap="round"/>')
        out += [txt(scale_x, scale_y + 30, f"Δ altitude {hi - lo:.1f} km", 14, colour, 650), txt(scale_x + scale_w, scale_y + 30, "altitude span", 13, MUTED, 400, "end")]
        metrics = [
            ("PHASE DRIFT", f"{orbit['phase_drift_deg_day']:.2f}° / day"),
            ("HOST RECOIL", f"{result['host_recoil_m_s'] * 1000:.2f} mm/s"),
            ("PEAK BODY RATE", f"{move['peak_body_rate_deg_s']:.4f}°/s"),
            ("IDEAL RESIDUAL RATE", f"{move['residual_body_rate_deg_s']:.1f}°/s"),
        ]
        for row, (name, value) in enumerate(metrics):
            yy = y + 236 + row * 38
            out += [txt(x + 28, yy, name, 12, MUTED, 650), txt(x + 676, yy, value, 19, INK, 650, "end")]

    out += [
        box(72, 646, 1452, 188, fill="#091720", stroke="#21465b"),
        txt(104, 694, "THE USEFUL SEPARATION", 15, CYAN, 700),
        txt(104, 736, "A clock can create phase offset. A commanded release impulse changes orbital energy.", 25, INK, 600),
        txt(104, 780, "This screen prices neither conjunction risk nor the atmosphere, J₂, covariance, flexible modes or host control.", 19, MUTED),
        txt(1494, 878, "PRELIMINARY MODEL OUTPUT · NOT FLIGHT-SAFETY ANALYSIS", 15, RED, 650, "end"),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def orbit_envelope() -> str:
    source_cases = [
        ("VOLLEY · 500 km", *load("volley_reference.json"), CYAN),
        ("HOSTED 6U · 550 km", *load("hosted_6u_example.json"), VIOLET),
    ]
    series = []
    for label, case, _result, colour in source_cases:
        rows = []
        for delta_v in range(0, 21):
            value = evaluate({**case, "deployment_delta_v_m_s": float(delta_v)})["orbit"]
            rows.append((delta_v, (value["apogee_altitude_m"] - value["perigee_altitude_m"]) / 1000.0, value["phase_drift_deg_day"]))
        series.append((label, rows, colour))
    max_span = max(row[1] for _label, rows, _colour in series for row in rows)
    max_drift = max(row[2] for _label, rows, _colour in series for row in rows)
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="860" viewBox="0 0 1600 860">',
        f'<rect width="1600" height="860" fill="{BG}"/>',
        txt(72, 78, "DEPLOYMENT-IMPULSE ENVELOPE", 24, CYAN, 700),
        txt(72, 124, "A tangential impulse changes orbital energy and accumulates phase drift.", 34, INK, 600),
        txt(72, 162, "Two-body sweep from 0–20 m/s at each committed starting altitude.", 19, MUTED),
    ]
    panels = [("ALTITUDE SPAN", 1, max_span, "km"), ("PHASE DRIFT", 2, max_drift, "° / day")]
    for panel_index, (title, value_index, ymax, unit) in enumerate(panels):
        x, y, w, h = 72 + panel_index * 744, 218, 704, 500
        left, top, plot_w, plot_h = x + 82, y + 76, 570, 326
        out += [box(x, y, w, h), txt(x + 28, y + 44, title, 16, CYAN, 700)]
        for tick in range(5):
            yy = top + plot_h * tick / 4
            value = ymax * (1 - tick / 4)
            out += [
                f'<line x1="{left}" y1="{yy:.1f}" x2="{left + plot_w}" y2="{yy:.1f}" stroke="#17384b"/>',
                txt(left - 12, yy + 5, f"{value:.1f}", 12, MUTED, 400, "end"),
            ]
        for tick in range(0, 21, 5):
            xx = left + plot_w * tick / 20
            out += [f'<line x1="{xx}" y1="{top}" x2="{xx}" y2="{top + plot_h}" stroke="#122a39"/>', txt(xx, top + plot_h + 28, str(tick), 12, MUTED, 400, "middle")]
        for series_index, (label, rows, colour) in enumerate(series):
            points = []
            for row in rows:
                xx = left + plot_w * row[0] / 20
                yy = top + plot_h * (1 - row[value_index] / ymax)
                points.append(f"{xx:.1f},{yy:.1f}")
            dash = ' stroke-dasharray="10 8"' if series_index else ""
            out.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{colour}" stroke-width="4"{dash}/>')
        out += [
            txt(left, top - 16, unit, 13, MUTED),
            f'<line x1="{x + 30}" y1="{y + 458}" x2="{x + 70}" y2="{y + 458}" stroke="{CYAN}" stroke-width="4"/>',
            txt(x + 80, y + 464, series[0][0], 13, INK),
            f'<line x1="{x + 360}" y1="{y + 458}" x2="{x + 400}" y2="{y + 458}" stroke="{VIOLET}" stroke-width="4" stroke-dasharray="10 8"/>',
            txt(x + 410, y + 464, series[1][0], 13, INK),
        ]
    out += [txt(1494, 818, "TWO-BODY SCREEN · NO ATMOSPHERE, J₂ OR COVARIANCE", 15, RED, 650, "end"), "</svg>"]
    return "\n".join(out) + "\n"


def disturbance_budget() -> str:
    cases = [
        ("VOLLEY", *load("volley_reference.json"), CYAN),
        ("HOSTED 6U", *load("hosted_6u_example.json"), VIOLET),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="760" viewBox="0 0 1600 760">',
        f'<rect width="1600" height="760" fill="{BG}"/>',
        txt(72, 78, "HOST DISTURBANCE LEDGER", 24, CYAN, 700),
        txt(72, 124, "Release recoil and an internal mass move are different host problems.", 34, INK, 600),
        txt(72, 162, "Each metric is independently scaled; exact model outputs remain on the bars.", 19, MUTED),
    ]
    metrics = [
        ("HOST RECOIL", lambda result: result["host_recoil_m_s"] * 1000, "mm/s"),
        ("PEAK BODY RATE", lambda result: result["internal_move"]["peak_body_rate_deg_s"], "°/s"),
        ("ATTITUDE OFFSET", lambda result: abs(result["internal_move"]["attitude_offset_deg"]), "°"),
    ]
    for metric_index, (title, getter, unit) in enumerate(metrics):
        x, y, w, h = 72 + metric_index * 500, 226, 452, 350
        values = [(label, getter(result), colour) for label, _case, result, colour in cases]
        vmax = max(value for _label, value, _colour in values)
        out += [box(x, y, w, h), txt(x + 26, y + 44, title, 15, CYAN, 700), txt(x + 426, y + 44, unit, 13, MUTED, 500, "end")]
        for row, (label, value, colour) in enumerate(values):
            yy = y + 94 + row * 104
            out += [
                txt(x + 26, yy, label, 14, INK, 650),
                f'<rect x="{x + 26}" y="{yy + 20}" width="{360 * value / vmax:.1f}" height="28" rx="14" fill="{colour}"/>',
                txt(x + 426, yy + 42, f"{value:.4f}", 15, INK, 650, "end"),
            ]
    out += [
        box(72, 620, 1452, 76, fill="#091720", stroke="#21465b"),
        txt(102, 652, "IDEAL CLOSED MOVE", 14, AMBER, 700),
        txt(102, 678, "Residual body rate returns to 0°/s; the attitude offset does not. Flexible modes and host control remain outside the model.", 17, INK, 550),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    outputs = {
        ROOT / "figures" / "deployment-trade.svg": render(),
        ROOT / "figures" / "orbit-envelope.svg": orbit_envelope(),
        ROOT / "figures" / "disturbance-budget.svg": disturbance_budget(),
    }
    for output, body in outputs.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(body, encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
