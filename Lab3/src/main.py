import logging

from controller import Controller
from triangle_calculator import TriangleCalculator
from triangle_database import TriangleDatabase
from user_input import ConsoleUserInput
from result_sender import EmailResultSender


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(levelname)-7s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    database = TriangleDatabase("triangles.db")
    controller = Controller(
        ConsoleUserInput(),
        TriangleCalculator(),
        database,
        EmailResultSender()
    )

    result = controller.run()
    print(f"Результат: {result}")

    database.close()


if __name__ == "__main__":
    main()