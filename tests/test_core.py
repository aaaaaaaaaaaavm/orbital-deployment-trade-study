import math
import unittest

from orbital_trade import host_recoil, internal_move, tangential_impulse


class OrbitalTradeTests(unittest.TestCase):
    def test_zero_delta_v_preserves_circular_orbit(self):
        result = tangential_impulse(500_000.0, 0.0)
        self.assertAlmostEqual(result["perigee_altitude_m"], 500_000.0, places=4)
        self.assertAlmostEqual(result["apogee_altitude_m"], 500_000.0, places=4)
        self.assertTrue(math.isinf(result["days_to_phase"]))

    def test_prograde_impulse_raises_apogee(self):
        result = tangential_impulse(500_000.0, 16.388)
        self.assertGreater(result["apogee_altitude_m"], 500_000.0)
        self.assertAlmostEqual(result["perigee_altitude_m"], 500_000.0, places=4)

    def test_retrograde_impulse_lowers_perigee(self):
        result = tangential_impulse(500_000.0, -16.388)
        self.assertLess(result["perigee_altitude_m"], 500_000.0)
        self.assertAlmostEqual(result["apogee_altitude_m"], 500_000.0, places=4)

    def test_unbound_impulse_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not bound"):
            tangential_impulse(500_000.0, 10_000.0)

    def test_earth_intersection_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "intersects Earth"):
            tangential_impulse(200_000.0, -500.0)

    def test_recoil_conserves_linear_momentum(self):
        recoil = host_recoil(4.0, 16.388, 500.0)
        self.assertAlmostEqual(500.0 * recoil, 4.0 * 16.388, places=12)

    def test_recoil_is_reported_as_a_magnitude(self):
        self.assertEqual(
            host_recoil(4.0, -16.388, 500.0),
            host_recoil(4.0, 16.388, 500.0),
        )

    def test_closed_internal_move_has_zero_residual_rate(self):
        result = internal_move(
            9.445,
            1.5,
            6.0,
            0.166,
            329.66843454166667,
        )
        self.assertEqual(result["residual_body_rate_deg_s"], 0.0)
        self.assertAlmostEqual(result["attitude_offset_deg"], -0.4087394686, places=8)

    def test_non_finite_internal_move_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "mass_kg"):
            internal_move(
                math.inf,
                1.5,
                6.0,
                0.166,
                329.66843454166667,
            )
