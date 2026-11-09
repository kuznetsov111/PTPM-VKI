import sqlite3

from src.exceptions import DuplicateIdError, RecordNotFoundError

MAX_NAME_LENGTH = 256
MAX_MESSAGE_LENGTH = 8096


class DatabaseRepository:
    def __init__(self, db_path):
        # db_path: путь к файлу БД или строка ':memory:' (для тестов)
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS comments ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "message TEXT NOT NULL)"
        )
        self.connection.commit()

    def close(self):
        self.connection.close()
    def validate_id(self, comment_id):
        # type(...) is not int отсекает и bool, который в Python считается int
        if type(comment_id) is not int:
            raise TypeError("comment_id должен быть целым числом")
        if comment_id < 1:
            raise ValueError("comment_id должен быть положительным")

    def validate_text(self, value, field_name, max_length):
        if type(value) is not str:
            raise TypeError(field_name + " должно быть строкой")
        if len(value) == 0:
            raise ValueError(field_name + " не может быть пустым")
        if len(value) > max_length:
            raise ValueError(
                field_name + " длиннее " + str(max_length) + " символов"
            )

    def add(self, comment_id, username, message):
        self.validate_id(comment_id)
        self.validate_text(username, "name", MAX_NAME_LENGTH)
        self.validate_text(message, "message", MAX_MESSAGE_LENGTH)

        try:
            self.connection.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise DuplicateIdError(
                "Запись с id " + str(comment_id) + " уже существует"
            )
        return True

    def row_to_dict(self, row):
        # Превращает строку из БД (кортеж) в словарь
        return {"id": row[0], "name": row[1], "message": row[2]}

    def get_by_id(self, comment_id):
        self.validate_id(comment_id)

        cursor = self.connection.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self.row_to_dict(row)

    def get_by_name(self, username):
        self.validate_text(username, "name", MAX_NAME_LENGTH)

        cursor = self.connection.execute(
            "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id",
            (username,),
        )
        result = []
        for row in cursor.fetchall():
            result.append(self.row_to_dict(row))
        return result

    def update(self, comment_id, new_message):
        self.validate_id(comment_id)
        self.validate_text(new_message, "message", MAX_MESSAGE_LENGTH)

        cursor = self.connection.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id),
        )
        self.connection.commit()
        if cursor.rowcount == 0:
            raise RecordNotFoundError(
                "Запись с id " + str(comment_id) + " не найдена"
            )
        return True

    def delete(self, comment_id):
        self.validate_id(comment_id)

        cursor = self.connection.execute(
            "DELETE FROM comments WHERE id = ?",
            (comment_id,),
        )
        self.connection.commit()
        if cursor.rowcount == 0:
            raise RecordNotFoundError(
                "Запись с id " + str(comment_id) + " не найдена"
            )
        return True