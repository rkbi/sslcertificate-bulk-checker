import unittest
from checker import get_data


class TestChecker(unittest.TestCase):
    def test_get_data(self):
        self.assertEqual(
            get_data("friendlyshopbd.com"),
            ["friendlyshopbd.com", "Let's Encrypt", "10-Aug-2022 13:26:30", ""],
        )


if __name__ == "__main__":
    unittest.main()
