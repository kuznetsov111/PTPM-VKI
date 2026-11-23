# Лабораторная работа 6. Автоматизированное UI-тестирование (Page Object Model)

Автоматизированные UI-тесты для веб-приложения Simple Calculator
(`https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/`)
с использованием паттерна Page Object Model (POM), Selenium WebDriver и unittest.

## Структура

```text
Lab6/
├── README.md
├── requirements.txt
├── pages/
│   ├── __init__.py
│   └── calculator_page.py    # CalculatorPage: локаторы и методы работы со страницей
└── tests/
    ├── __init__.py
    └── test_calculator.py    # TestCalculator: набор UI-тестов на unittest