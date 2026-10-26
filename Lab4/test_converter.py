import unittest

from converter import Converter


class TestConverter(unittest.TestCase):

    def test_big_positive_returns_1000(self):
        # Arrange
        x = 150.0
        # Act
        result = Converter.do(x)
        # Assert
        self.assertEqual(result, 1000)

    def test_middle_positive_returns_int_part(self):
        x = 65.7
        result = Converter.do(x)
        self.assertEqual(result, 65)

    def test_small_negative_returns_int_part_minus_5(self):
        x = -10.5
        result = Converter.do(x)
        self.assertEqual(result, -15)

    def test_big_negative_returns_minus_2000(self):
        x = -94.5
        result = Converter.do(x)
        self.assertEqual(result, -2000)

    def test_boundary_100_7_returns_1000(self):
        x = 100.7
        result = Converter.do(x)
        self.assertEqual(result, 1000)

    def test_boundary_100_6_returns_100(self):
        x = 100.6
        result = Converter.do(x)
        self.assertEqual(result, 100)

    def test_boundary_0_1_returns_0(self):
        x = 0.1
        result = Converter.do(x)
        self.assertEqual(result, 0)

    def test_boundary_minus_0_1_returns_minus_5(self):
        x = -0.1
        result = Converter.do(x)
        self.assertEqual(result, -5)

    def test_boundary_minus_30_4_returns_minus_35(self):
        x = -30.4
        result = Converter.do(x)
        self.assertEqual(result, -35)

    def test_boundary_minus_30_5_returns_minus_2000(self):
        x = -30.5
        result = Converter.do(x)
        self.assertEqual(result, -2000)

    def test_zero_raises_value_error(self):
        x = 0.0
        with self.assertRaises(ValueError):
            Converter.do(x)



if __name__ == "__main__":
    unittest.main()