import unittest
import random
from mobility_house.pv_simulator import get_pv_value, mean, max_pv

class TestSimulator(unittest.TestCase):
    # Meter Tests


    # PV Simulator Tests
    def test_get_pv_value_below_mean(self):
        time_before_mean = random.randrange(0, mean) # not inclusive
        self.assertTrue(int(get_pv_value(time_before_mean)) < max_pv, "Any PV value before the mean time should be below the max PV.")

    def test_get_pv_value_mean(self):
        self.assertEqual(int(get_pv_value(mean)), max_pv, "The PV value at the mean should be the max PV.")

    def test_get_pv_value_above_mean(self):
        time_after_mean = random.randrange(mean + 1, 24 * 60 * 60) # not inclusive
        self.assertTrue(int(get_pv_value(time_after_mean)) < max_pv, "Any PV value after the mean time should be below the max PV.")

if __name__ == '__main__':
    unittest.main()
