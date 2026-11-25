import time
import unittest
from selenium import webdriver
from pages.calculator_page import CalculatorPage


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.page = CalculatorPage(self.driver, delay=1)
        self.page.open()

    def tearDown(self):
        filename = self._testMethodName + ".png"
        self.page.save_screenshot(filename)
        time.sleep(1.5)
        self.driver.quit()

    def test_addition(self):
        # Сложение положительных чисел
        self.page.enter_first_number(5)
        self.page.enter_second_number(3)
        self.page.select_operation("+")

        self.assertEqual("8", self.page.get_result_value())

    def test_subtraction(self):
        # Вычитание
        self.page.enter_first_number(10)
        self.page.enter_second_number(4)
        self.page.select_operation("-")

        self.assertEqual("6", self.page.get_result_value())

    def test_multiplication(self):
        # Умножение
        self.page.enter_first_number(6)
        self.page.enter_second_number(7)
        self.page.select_operation("*")

        self.assertEqual("42", self.page.get_result_value())

    def test_division(self):
        # Деление нацело
        self.page.enter_first_number(20)
        self.page.enter_second_number(4)
        self.page.select_operation("/")

        self.assertEqual("5", self.page.get_result_value())

    def test_division_by_zero(self):
        # Деление на ноль (AngularJS возвращает null)
        self.page.enter_first_number(10)
        self.page.enter_second_number(0)
        self.page.select_operation("/")

        self.assertEqual("null", self.page.get_result_value())

    def test_negative_numbers(self):
        # Работа с отрицательными числами
        self.page.enter_first_number(-5)
        self.page.enter_second_number(-3)
        self.page.select_operation("+")

        self.assertEqual("-8", self.page.get_result_value())

    def test_decimal_numbers(self):
        # Работа с дробными числами (граничный случай)
        self.page.enter_first_number("2.5")
        self.page.enter_second_number("1.5")
        self.page.select_operation("+")

        self.assertEqual("4", self.page.get_result_value())

    def test_zero_multiplication(self):
        # Граничное значение: умножение на ноль
        self.page.enter_first_number(999)
        self.page.enter_second_number(0)
        self.page.select_operation("*")

        self.assertEqual("0", self.page.get_result_value())

    def test_increment_and_decrement_buttons(self):
        # Проверка кнопок +1 и -1 для a и b (по умолчанию a=0, b=0)
        self.page.click_inc_a()
        self.page.click_inc_a()  # a стало 2
        self.page.click_dec_b()  # b стало -1
        self.page.select_operation("+")

        self.assertEqual("1", self.page.get_result_value())

    def test_full_result_string_format(self):
        # Проверка всей строки вывода целиком ("a op b = res")
        self.page.enter_first_number(4)
        self.page.enter_second_number(2)
        self.page.select_operation("*")

        self.assertEqual("4 * 2 = 8", self.page.get_result_text())