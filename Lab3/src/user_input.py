from abc import ABC, abstractmethod


class UserInput(ABC):

    @abstractmethod
    def get_sides(self):
        """Возвращает три стороны треугольника в виде трёх строк."""


class ConsoleUserInput(UserInput):

    def get_sides(self):
        side1 = input("Введите длину первой стороны: ")
        side2 = input("Введите длину второй стороны: ")
        side3 = input("Введите длину третьей стороны: ")
        return side1, side2, side3


