class Controller:

    def __init__(self, user_input, calculator, database, sender):
        self.user_input = user_input
        self.calculator = calculator
        self.database = database
        self.sender = sender

    def run(self):
        side1, side2, side3 = self.user_input.get_sides()

        record = self.database.get_record(side1, side2, side3)

        if record is None:
            triangle_type, vertices = self.calculator.calculate(side1, side2, side3)

            error_message = ""
            if triangle_type == "":
                error_message = "введены нечисловые данные"
            elif triangle_type == "не треугольник":
                error_message = "стороны не образуют треугольник"

            self.database.add_record(side1, side2, side3, triangle_type, error_message)
        else:
            triangle_type = record[0]
            error_message = record[1]

        if error_message == "":
            result = f"Стороны {side1}, {side2}, {side3}: {triangle_type}"
        else:
            result = f"Стороны {side1}, {side2}, {side3}: ошибка - {error_message}"

        self.sender.send(result)
        return result

