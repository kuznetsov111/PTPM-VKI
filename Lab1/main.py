import logging
import os
import math

#создание папки с логами благодоря библитеки os
if not os.path.exists("Logs"):
    os.makedirs("Logs")

# Шаблон строки лога: время | уровень | сообщение
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

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

    #теорема Пифагора
    cx = (b * b + c * c - a * a) / (2 * c)
    # Защита от небольшой ошибки округления, из-за которой под корнем
    # может оказаться чуть меньше нуля
    under_sqrt = b * b - cx * cx
    if under_sqrt < 0:
        under_sqrt = 0
    cy = math.sqrt(under_sqrt)

    #собираем координаты всех трёх точек в список
    points_x = [ax, bx, cx]
    points_y = [ay, by, cy]

    #находим минимальные и максимальные значения
    min_x = min(points_x)
    max_x = max(points_x)
    min_y = min(points_y)
    max_y = max(points_y)

    #находим на сколько нужно масштабировать
    width = max_x - min_x
    height = max_y - min_y

    if width == 0:
        width = 1
    if height == 0:
        height = 1

    scale_x = 100 / width
    scale_y = 100 / height

    #используем наименьший масштаб, чтобы фигура уместилась по обеим осям
    scale = min(scale_x, scale_y)

    #пересчитываем координаты: сдвигаем к нулю и масштабируем
    result = []
    for i in range(3):
        new_x = (points_x[i] - min_x) * scale
        new_y = (points_y[i] - min_y) * scale
        result.append((int(new_x), int(new_y)))

    return result

def process_triangle(str1, str2, str3):
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

# Базовая настройка корневого логгера
logging.basicConfig(
    level=logging.DEBUG, # Минимальный уровень логирования (аналог MinimumLevel.Debug)
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(),    # Настройка логирования в консоль
        logging.FileHandler("Logs/log.txt", encoding="utf-8") # Настройка логирования в файл
    ]
)


def main():
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    print(process_triangle("6", "5", "7"))
    print(process_triangle("5", "5", "7"))
    print(process_triangle("5", "5", "5"))
    print(process_triangle("11", "1", "3"))
    print(process_triangle("7", "2", "привет мир"))

if __name__ == "__main__":
    main()

