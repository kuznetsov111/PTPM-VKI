import sqlite3


class TriangleDatabase:

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 TEXT,
                side2 TEXT,
                side3 TEXT,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self.connection.commit()

    def add_record(self, side1, side2, side3, triangle_type, error_message):
        self.connection.execute(
            "INSERT INTO triangles VALUES (?, ?, ?, ?, ?)",
            (side1, side2, side3, triangle_type, error_message)
        )
        self.connection.commit()

    def get_record(self, side1, side2, side3):
        cursor = self.connection.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (side1, side2, side3)
        )
        return cursor.fetchone()

    def delete_record(self, side1, side2, side3):
        self.connection.execute(
            "DELETE FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (side1, side2, side3)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()

