"""Generate the README deployment-trade figure from the committed cases."""

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


def main() -> None:
    output = ROOT / "figures" / "deployment-trade.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(), encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
