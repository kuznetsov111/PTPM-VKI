import logging
import math


def get_triangle_type(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"

    if a == b and b == c:
        return "равносторонний"

    if a == b or b == c or a == c:
        return "равнобедренный"

    return "разносторонний"


def get_triangle_vertices(a, b, c):
    ax = 0
    ay = 0

    bx = c
    by = 0

    cx = (b * b + c * c - a * a) / (2 * c)
    under_sqrt = b * b - cx * cx
    if under_sqrt < 0:
        under_sqrt = 0
    cy = math.sqrt(under_sqrt)

    points_x = [ax, bx, cx]
    points_y = [ay, by, cy]

    min_x = min(points_x)
    max_x = max(points_x)
    min_y = min(points_y)
    max_y = max(points_y)

    width = max_x - min_x
    height = max_y - min_y

    if width == 0:
        width = 1
    if height == 0:
        height = 1

    scale_x = 100 / width
    scale_y = 100 / height
    scale = min(scale_x, scale_y)

    result = []
    for i in range(3):
        new_x = (points_x[i] - min_x) * scale
        new_y = (points_y[i] - min_y) * scale
        result.append((int(new_x), int(new_y)))

    return result


class TriangleCalculator:

    def calculate(self, str1, str2, str3):
        try:
            a = float(str1)
            b = float(str2)
            c = float(str3)
        except ValueError:
            logging.error(f"Некорректные (нечисловые) данные: {str1}, {str2}, {str3}")
            return "", [(-2, -2), (-2, -2), (-2, -2)]

        if a <= 0 or b <= 0 or c <= 0:
            logging.warning(f"Стороны должны быть положительными: {a}, {b}, {c}")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

        triangle_type = get_triangle_type(a, b, c)

        if triangle_type == "не треугольник":
            logging.warning(f"Невозможный треугольник: {a}, {b}, {c}")
            return triangle_type, [(-1, -1), (-1, -1), (-1, -1)]

        vertices = get_triangle_vertices(a, b, c)
        logging.info(f"Успешный расчёт: стороны = ({a}, {b}, {c}), тип = {triangle_type}, вершины = {vertices}")

        return triangle_type, vertices
