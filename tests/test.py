import unittest
from mobility_house.pv_simulator import get_pv_value, mean, max_pv

class TestSimulator(unittest.TestCase):

    def test_get_pv_value(self):
        self.assertEqual(int(get_pv_value(mean)), max_pv, "The PV value at the mean should be the max PV.")

if __name__ == '__main__':
    unittest.main()
