import sys
import os

# Добавляем папку src в список мест, где Python ищет модули для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from unittest.mock import Mock, patch

from controller import Controller
from triangle_calculator import TriangleCalculator
from triangle_database import TriangleDatabase
from user_input import ConsoleUserInput
from result_sender import EmailResultSender


class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        # Заглушка ввода: вместо вопросов в консоли сразу отдаёт готовые стороны
        self.input_stub = Mock()
        # Заглушка отправки: ничего не отправляет, только запоминает вызовы
        self.sender_stub = Mock()
        # Настоящая база данных, но в оперативной памяти
        self.database = TriangleDatabase(":memory:")
        self.controller = Controller(
            self.input_stub,
            TriangleCalculator(),
            self.database,
            self.sender_stub
        )

    def tearDown(self):
        self.database.close()

    def test_new_triangle_is_calculated_and_saved_to_database(self):
        self.input_stub.get_sides.return_value = ("3", "4", "5")

        result = self.controller.run()

        self.assertEqual(result, "Стороны 3, 4, 5: разносторонний")
        self.assertEqual(self.database.get_record("3", "4", "5"), ("разносторонний", ""))

    def test_existing_record_is_taken_from_database(self):
        self.database.add_record("3", "4", "5", "тип из базы", "")
        self.input_stub.get_sides.return_value = ("3", "4", "5")

        result = self.controller.run()

        self.assertEqual(result, "Стороны 3, 4, 5: тип из базы")

    def test_result_is_sent_to_external_service_once(self):
        self.input_stub.get_sides.return_value = ("5", "5", "5")

        result = self.controller.run()

        self.sender_stub.send.assert_called_once_with("Стороны 5, 5, 5: равносторонний")
        self.assertEqual(result, "Стороны 5, 5, 5: равносторонний")

    def test_impossible_triangle_is_saved_with_error_message(self):
        self.input_stub.get_sides.return_value = ("1", "1", "10")

        result = self.controller.run()

        self.assertEqual(result, "Стороны 1, 1, 10: ошибка - стороны не образуют треугольник")
        self.assertEqual(
            self.database.get_record("1", "1", "10"),
            ("не треугольник", "стороны не образуют треугольник")
        )

    def test_non_numeric_input_is_saved_with_error_message(self):
        self.input_stub.get_sides.return_value = ("abc", "4", "5")

        result = self.controller.run()

        self.assertEqual(result, "Стороны abc, 4, 5: ошибка - введены нечисловые данные")
        self.assertEqual(
            self.database.get_record("abc", "4", "5"),
            ("", "введены нечисловые данные")
        )

    def test_same_input_twice_creates_only_one_record(self):
        self.input_stub.get_sides.return_value = ("5", "5", "8")

        first_result = self.controller.run()
        second_result = self.controller.run()

        self.assertEqual(first_result, "Стороны 5, 5, 8: равнобедренный")
        self.assertEqual(second_result, first_result)
        self.assertEqual(self.sender_stub.send.call_count, 2)

    def test_negative_side_is_saved_with_error_message(self):
        self.input_stub.get_sides.return_value = ("-5", "4", "5")

        result = self.controller.run()

        self.assertEqual(result, "Стороны -5, 4, 5: ошибка - стороны не образуют треугольник")

class TestFullScenarioWithPatch(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input")
    def test_full_scenario_with_real_classes(self, input_mock, print_mock):
        input_mock.side_effect = ["3", "4", "5"]
        database = TriangleDatabase(":memory:")
        controller = Controller(
            ConsoleUserInput(),
            TriangleCalculator(),
            database,
            EmailResultSender()
        )

        result = controller.run()

        self.assertEqual(result, "Стороны 3, 4, 5: разносторонний")
        self.assertEqual(input_mock.call_count, 3)
        print_mock.assert_called_once_with(
            "[Имитация email-сервера] Отправлено сообщение: Стороны 3, 4, 5: разносторонний"
        )
        database.close()


class TestControllerIsolated(unittest.TestCase):

    def test_calculator_is_not_called_when_record_exists(self):
        input_stub = Mock()
        input_stub.get_sides.return_value = ("3", "4", "5")
        calculator_stub = Mock()
        database_stub = Mock()
        database_stub.get_record.return_value = ("разносторонний", "")
        sender_stub = Mock()
        controller = Controller(input_stub, calculator_stub, database_stub, sender_stub)

        controller.run()

        calculator_stub.calculate.assert_not_called()
        database_stub.add_record.assert_not_called()


class TestTriangleDatabase(unittest.TestCase):

    def test_deleted_record_is_not_found(self):
        database = TriangleDatabase(":memory:")
        database.add_record("3", "4", "5", "разносторонний", "")

        database.delete_record("3", "4", "5")

        self.assertIsNone(database.get_record("3", "4", "5"))
        database.close()


if __name__ == "__main__":
    unittest.main()