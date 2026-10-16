import math
import unittest
from orbital_trade import host_recoil


class FiniteHostTests(unittest.TestCase):
    def test_equal_masses_split_relative_velocity(self):
        self.assertEqual(host_recoil(10, 2, 10), 1)

    def test_momentum_and_relative_velocity_across_mass_ratios(self):
        for payload in (1, 4, 100):
            for host in (1, 500, 10000):
                for relative in (-16, 0, 3):
                    recoil = math.copysign(host_recoil(payload, relative, host), relative)
                    payload_dv = relative - recoil
                    self.assertAlmostEqual(payload * payload_dv - host * recoil, 0, places=9)
                    self.assertAlmostEqual(payload_dv + recoil, relative)

    def test_invalid_inputs(self):
        for args in ((0, 2, 10), (1, 2, 0), (1, math.nan, 10)):
            with self.assertRaises(ValueError):
                host_recoil(*args)


class OrbitStateTests(unittest.TestCase):
    def test_direction_reversal_matches_same_final_speed(self):
        from orbital_trade import tangential_impulse
        from orbital_trade.core import MU_EARTH, R_EARTH
        v0 = math.sqrt(MU_EARTH / (R_EARTH + 500000))
        for change in (-10, 0, 10):
            a = tangential_impulse(500000, change)
            b = tangential_impulse(500000, -2 * v0 - change)
            for key in ('perigee_altitude_m', 'apogee_altitude_m'):
                self.assertAlmostEqual(a[key], b[key], places=5)

    def test_case_delta_v_is_inertial_not_relative(self):
        from orbital_trade import evaluate
        from pathlib import Path
        import json
        for path in (Path(__file__).resolve().parents[1] / 'cases').glob('*.json'):
            c = json.loads(path.read_text())
            result = evaluate(c)
            dv = c['deployment_delta_v_m_s']
            recoil = result['host_recoil_m_s']
            self.assertAlmostEqual(c['payload_mass_kg'] * abs(dv), c['host_mass_kg'] * recoil)
            self.assertAlmostEqual(abs(result['relative_separation_velocity_m_s']), abs(dv) + recoil)
