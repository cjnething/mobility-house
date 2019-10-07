import unittest
import random
from mobility_house.meter import get_period_length, min_period_length, max_period_length
from mobility_house.pv_simulator import get_pv_value, mean, max_pv, std_deviation

class TestSimulator(unittest.TestCase):
    # Meter Tests
    def test_get_period_length(self):
        self.assertTrue(min_period_length <= get_period_length() <= max_period_length, "The meter simulation period length should be between the min and the max.")

    # PV Simulator Tests
    def test_get_pv_value_below_mean(self):
        time_before_mean = random.randrange(0, mean) # not inclusive
        self.assertTrue(int(get_pv_value(time_before_mean)) < max_pv, "Any PV value before the mean time should be below the max PV.")

    def test_get_pv_value_mean(self):
        self.assertEqual(int(get_pv_value(mean)), max_pv, "The PV value at the mean should be the max PV.")

    def test_get_pv_value_above_mean(self):
        time_after_mean = random.randrange(mean + 1, 24 * 60 * 60) # not inclusive
        self.assertTrue(int(get_pv_value(time_after_mean)) < max_pv, "Any PV value after the mean time should be below the max PV.")

    def test_get_pv_value_std_deviation(self):
        time_before_mean = mean - std_deviation
        time_after_mean = mean + std_deviation
        pv_value_before = int(get_pv_value(time_before_mean))
        pv_value_after = int(get_pv_value(time_after_mean))
        self.assertTrue(pv_value_before == pv_value_after, "The PV value for one standard deviation above or below the mean should be the same.")

if __name__ == '__main__':
    unittest.main()
