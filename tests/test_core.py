import math
import unittest
from orbital_trade import host_recoil, internal_move, tangential_impulse


class OrbitalTradeTests(unittest.TestCase):
    def test_zero_delta_v_preserves_circular_orbit(self):
        result = tangential_impulse(500000.0, 0.0)
        self.assertAlmostEqual(result["perigee_altitude_m"], 500000.0, places=4)
        self.assertAlmostEqual(result["apogee_altitude_m"], 500000.0, places=4)
        self.assertTrue(math.isinf(result["days_to_phase"]))

    def test_prograde_impulse_raises_apogee(self):
        result = tangential_impulse(500000.0, 16.388)
        self.assertGreater(result["apogee_altitude_m"], 500000.0)
        self.assertAlmostEqual(result["perigee_altitude_m"], 500000.0, places=4)

    def test_recoil_conserves_linear_momentum(self):
        recoil = host_recoil(4.0, 16.388, 500.0)
        self.assertAlmostEqual(500.0 * recoil, 4.0 * 16.388, places=12)

    def test_closed_internal_move_has_zero_residual_rate(self):
        result = internal_move(9.445, 1.5, 6.0, 0.166, 329.66843454166667)
        self.assertEqual(result["residual_body_rate_deg_s"], 0.0)
        self.assertAlmostEqual(result["attitude_offset_deg"], -0.4087394686, places=8)
