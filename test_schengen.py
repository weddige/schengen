import unittest
from datetime import date
from schengen import Visa, VisaError, OverstayWarning


class TestVisa(unittest.TestCase):
    def test_overstay(self):
        visa = Visa(date(2020, 1, 1), date(2021, 1, 1))
        visa.add_trip(date(2020, 1, 1), date(2020, 2, 1))
        with self.assertRaises(VisaError):
            visa.add_trip(date(2020, 3, 1), date(2020, 5, 1))
        with self.assertWarns(OverstayWarning):
            visa.add_trip(date(2020, 3, 1), date(2020, 5, 1), False)
        self.assertFalse(visa.valid)

    def test_max_stay(self):
        visa = Visa(date(2020, 1, 1), date(2021, 1, 1))
        visa.add_trip(date(2020, 1, 1), date(2020, 2, 1))
        visa.add_trip(date(2020, 3, 1), date(2020, 4, 27))
        visa.add_trip(date(2020, 6, 29), date(2020, 7, 30))
        self.assertTrue(visa.valid)


if __name__ == "__main__":
    import warnings

    warnings.simplefilter("ignore")
    unittest.main()
