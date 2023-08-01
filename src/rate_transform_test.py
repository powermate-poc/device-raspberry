import time
import unittest

from device import cubic_meters_per_hour


def calculate(seconds: int) -> float:
    rotation_start = time.time_ns()
    # add seconds as nano seconds to the ts
    rotation_end = rotation_start + (seconds * 1_000_000_000)

    return cubic_meters_per_hour(rotation_start, rotation_end)


class TestGasCounter(unittest.TestCase):

    def assert_consumption(self, rotation_s: int, expected: float) -> None:
        gas_consumption_rate = calculate(rotation_s)
        self.assertEqual(gas_consumption_rate, expected)

    def test_sanity_gas_consumption(self):
        rotation_s = 60 * 60
        expected_gas_consumption_rate = 0.01

        self.assert_consumption(rotation_s, expected_gas_consumption_rate)

    def test_minimal_gas_consumption(self):
        rotation_s = 15 * 60
        expected_gas_consumption_rate = 0.04

        self.assert_consumption(rotation_s, expected_gas_consumption_rate)

    def test_maximum_gas_consumption(self):
        rotation_s = 6
        expected_gas_consumption_rate = 6

        self.assert_consumption(rotation_s, expected_gas_consumption_rate)

    def test_middle_gas_consumption(self):
        rotation_s = 45
        expected_gas_consumption_rate = 0.8

        self.assert_consumption(rotation_s, expected_gas_consumption_rate)


if __name__ == '__main__':
    unittest.main()
