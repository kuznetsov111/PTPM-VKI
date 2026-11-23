from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class CalculatorPage:
    URL = "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"

    # Локаторы элементов страницы (защищённые кортежи By, как требует ТЗ)
    _INPUT_A = (By.CSS_SELECTOR, 'input[ng-model="a"]')
    _INPUT_B = (By.CSS_SELECTOR, 'input[ng-model="b"]')
    _INC_A_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="inca()"]')
    _DEC_A_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="deca()"]')
    _INC_B_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="incb()"]')
    _DEC_B_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="decb()"]')
    _OPERATION_SELECT = (By.CSS_SELECTOR, 'select[ng-model="operation"]')
    _RESULT_TEXT = (By.CLASS_NAME, "result")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def enter_first_number(self, value):
        field = self.driver.find_element(*self._INPUT_A)
        field.clear()
        field.send_keys(str(value))

    def enter_second_number(self, value):
        field = self.driver.find_element(*self._INPUT_B)
        field.clear()
        field.send_keys(str(value))

    def click_inc_a(self):
        self.driver.find_element(*self._INC_A_BUTTON).click()

    def click_dec_a(self):
        self.driver.find_element(*self._DEC_A_BUTTON).click()

    def click_inc_b(self):
        self.driver.find_element(*self._INC_B_BUTTON).click()

    def click_dec_b(self):
        self.driver.find_element(*self._DEC_B_BUTTON).click()

    def select_operation(self, operation):
        select_element = self.driver.find_element(*self._OPERATION_SELECT)
        Select(select_element).select_by_value(operation)

    def get_result_text(self):
        # Вернёт строку вида "2 + 3 = 5"
        return self.driver.find_element(*self._RESULT_TEXT).text

    def get_result_value(self):
        # Разделяет строку "2 + 3 = 5" по знаку "=" и берёт правую часть ("5")
        full_text = self.get_result_text()
        parts = full_text.split("=")
        return parts[1].strip()