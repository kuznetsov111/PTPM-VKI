import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class CalculatorPage:
    URL = "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"

    # Локаторы элементов страницы
    _INPUT_A = (By.CSS_SELECTOR, 'input[ng-model="a"]')
    _INPUT_B = (By.CSS_SELECTOR, 'input[ng-model="b"]')
    _INC_A_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="inca()"]')
    _DEC_A_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="deca()"]')
    _INC_B_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="incb()"]')
    _DEC_B_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="decb()"]')
    _OPERATION_SELECT = (By.CSS_SELECTOR, 'select[ng-model="operation"]')
    _RESULT_TEXT = (By.CLASS_NAME, "result")

    def __init__(self, driver, delay=1):
        self.driver = driver
        self.delay = delay

    def open(self):
        self.driver.get(self.URL)
        time.sleep(self.delay)

    def enter_first_number(self, value):
        field = self.driver.find_element(*self._INPUT_A)
        field.clear()
        field.send_keys(str(value))
        time.sleep(self.delay)

    def enter_second_number(self, value):
        field = self.driver.find_element(*self._INPUT_B)
        field.clear()
        field.send_keys(str(value))
        time.sleep(self.delay)

    def click_inc_a(self):
        self.driver.find_element(*self._INC_A_BUTTON).click()
        time.sleep(self.delay)

    def click_dec_a(self):
        self.driver.find_element(*self._DEC_A_BUTTON).click()
        time.sleep(self.delay)

    def click_inc_b(self):
        self.driver.find_element(*self._INC_B_BUTTON).click()
        time.sleep(self.delay)

    def click_dec_b(self):
        self.driver.find_element(*self._DEC_B_BUTTON).click()
        time.sleep(self.delay)

    def select_operation(self, operation):
        select_element = self.driver.find_element(*self._OPERATION_SELECT)
        Select(select_element).select_by_value(operation)
        time.sleep(self.delay)

    def get_result_text(self):
        return self.driver.find_element(*self._RESULT_TEXT).text

    def get_result_value(self):
        full_text = self.get_result_text()
        parts = full_text.split("=")
        return parts[1].strip()

    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)