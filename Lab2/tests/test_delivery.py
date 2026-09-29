import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from delivery_service import calculate_delivery_cost


class TestCalculateDeliveryCost(unittest.TestCase):

    def test_standard_delivery_base_cost(self):
        result = calculate_delivery_cost(2, 100, "обычный", False)
        self.assertEqual(result, (700, "2026-09-04"))

    def test_light_weight_surcharge(self):
        result = calculate_delivery_cost(10, 100, "обычный", False)
        self.assertEqual(result, (840, "2026-09-04"))

    def test_heavy_weight_surcharge(self):
        result = calculate_delivery_cost(25, 100, "обычный", False)
        self.assertEqual(result, (1050, "2026-09-04"))

    def test_weight_boundary_five_kg_no_surcharge(self):
        result = calculate_delivery_cost(5.0, 100, "обычный", False)
        self.assertEqual(result, (700, "2026-09-04"))

    def test_fragile_package_surcharge(self):
        result = calculate_delivery_cost(2, 100, "хрупкий", False)
        self.assertEqual(result, (1000, "2026-09-04"))

    def test_dangerous_package_surcharge(self):
        result = calculate_delivery_cost(2, 100, "опасный", False)
        self.assertEqual(result, (1700, "2026-09-04"))

    def test_weight_above_maximum_returns_error(self):
        result = calculate_delivery_cost(51, 100, "обычный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_distance_above_maximum_returns_error(self):
        result = calculate_delivery_cost(2, 5001, "обычный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_invalid_package_type_returns_error(self):
        result = calculate_delivery_cost(2, 100, "секретный", False)
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_express_delivery_should_cost_more_than_standard(self):
        standard = calculate_delivery_cost(2, 100, "обычный", False)
        express = calculate_delivery_cost(2, 100, "обычный", True)
        # Экспресс-доставка должна быть ДОРОЖЕ обычной, а не дешевле
        self.assertGreater(express[0], standard[0])


if __name__ == "__main__":
    unittest.main()