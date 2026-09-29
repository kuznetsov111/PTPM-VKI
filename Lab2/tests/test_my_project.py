import sys
import os

# Добавляем папку src в список мест, где Python ищет модули для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from my_project import get_triangle_type, get_triangle_vertices, process_triangle


class TestGetTriangleType(unittest.TestCase):

    def test_equilateral_triangle(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "равносторонний")

    def test_isosceles_triangle(self):
        self.assertEqual(get_triangle_type(5, 5, 8), "равнобедренный")

    def test_scalene_triangle(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "разносторонний")

    def test_triangle_inequality_violation(self):
        self.assertEqual(get_triangle_type(1, 1, 10), "не треугольник")

    def test_degenerate_triangle_sum_equals_third_side(self):
        # Сумма двух сторон РОВНА третьей - по правилу это уже не треугольник
        self.assertEqual(get_triangle_type(2, 3, 5), "не треугольник")


class TestGetTriangleVertices(unittest.TestCase):

    def test_right_triangle_vertices(self):
        result = get_triangle_vertices(3, 4, 5)
        self.assertEqual(result, [(0, 0), (100, 0), (64, 47)])

    def test_equilateral_triangle_vertices(self):
        result = get_triangle_vertices(5, 5, 5)
        self.assertEqual(result, [(0, 0), (100, 0), (50, 86)])

    def test_vertices_are_integers(self):
        result = get_triangle_vertices(3, 4, 5)
        for point in result:
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)


class TestProcessTriangle(unittest.TestCase):

    def test_valid_triangle_full_result(self):
        result = process_triangle("3", "4", "5")
        self.assertEqual(result, ("разносторонний", [(0, 0), (100, 0), (64, 47)]))

    def test_non_numeric_input(self):
        result = process_triangle("abc", "4", "5")
        self.assertEqual(result, ("", [(-2, -2), (-2, -2), (-2, -2)]))

    def test_negative_side(self):
        result = process_triangle("-5", "4", "5")
        self.assertEqual(result, ("не треугольник", [(-1, -1), (-1, -1), (-1, -1)]))

    def test_zero_side(self):
        result = process_triangle("0", "4", "5")
        self.assertEqual(result, ("не треугольник", [(-1, -1), (-1, -1), (-1, -1)]))

    def test_impossible_triangle_from_strings(self):
        result = process_triangle("1", "1", "10")
        self.assertEqual(result, ("не треугольник", [(-1, -1), (-1, -1), (-1, -1)]))


if __name__ == "__main__":
    unittest.main()