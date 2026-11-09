import unittest

from src.database import DatabaseRepository, MAX_NAME_LENGTH, MAX_MESSAGE_LENGTH
from src.exceptions import DuplicateIdError, RecordNotFoundError


class RepositoryTestCase(unittest.TestCase):
    """Общая подготовка: у каждого теста своя чистая БД в памяти."""

    def setUp(self):
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()


class TestAdd(RepositoryTestCase):
    def test_add_returns_true_and_saves_record(self):
        # Act
        result = self.repo.add(1, "ivan", "hello")

        # Assert
        self.assertTrue(result)
        self.assertEqual(
            {"id": 1, "name": "ivan", "message": "hello"},
            self.repo.get_by_id(1),
        )

    def test_add_duplicate_id_raises_error(self):
        # Arrange
        self.repo.add(1, "ivan", "hello")

        # Act + Assert
        with self.assertRaises(DuplicateIdError):
            self.repo.add(1, "petr", "other")

    def test_add_duplicate_id_does_not_overwrite_old_record(self):
        # Arrange
        self.repo.add(1, "ivan", "hello")

        # Act
        try:
            self.repo.add(1, "petr", "other")
        except DuplicateIdError:
            pass

        # Assert
        self.assertEqual(
            {"id": 1, "name": "ivan", "message": "hello"},
            self.repo.get_by_id(1),
        )

    def test_add_accepts_maximum_allowed_length(self):
        # Граничное значение: ровно 256 и 8096 символов допустимы
        name = "n" * MAX_NAME_LENGTH
        message = "m" * MAX_MESSAGE_LENGTH

        result = self.repo.add(1, name, message)

        self.assertTrue(result)
        self.assertEqual(message, self.repo.get_by_id(1)["message"])

    def test_add_too_long_name_raises_value_error(self):
        name = "n" * (MAX_NAME_LENGTH + 1)

        with self.assertRaises(ValueError):
            self.repo.add(1, name, "hello")

    def test_add_too_long_message_raises_value_error(self):
        message = "m" * (MAX_MESSAGE_LENGTH + 1)

        with self.assertRaises(ValueError):
            self.repo.add(1, "ivan", message)

    def test_add_wrong_types_raise_type_error(self):
        cases = [
            ("1", "ivan", "hi"),
            (1.5, "ivan", "hi"),
            (True, "ivan", "hi"),
            (None, "ivan", "hi"),
            (1, 123, "hi"),
            (1, None, "hi"),
            (1, "ivan", 123),
            (1, "ivan", None),
        ]

        for comment_id, username, message in cases:
            with self.subTest(id=comment_id, name=username, message=message):
                with self.assertRaises(TypeError):
                    self.repo.add(comment_id, username, message)

    def test_add_invalid_values_raise_value_error(self):
        cases = [
            (0, "ivan", "hi"),
            (-5, "ivan", "hi"),
            (1, "", "hi"),
            (1, "ivan", ""),
        ]

        for comment_id, username, message in cases:
            with self.subTest(id=comment_id, name=username, message=message):
                with self.assertRaises(ValueError):
                    self.repo.add(comment_id, username, message)

class TestGetById(RepositoryTestCase):
    def test_get_by_id_returns_existing_record(self):
        self.repo.add(5, "ivan", "<b>hello</b>")

        result = self.repo.get_by_id(5)

        self.assertEqual({"id": 5, "name": "ivan", "message": "<b>hello</b>"}, result)

    def test_get_by_id_returns_none_if_not_found(self):
        result = self.repo.get_by_id(99)

        self.assertIsNone(result)

    def test_get_by_id_returns_only_requested_record(self):
        self.repo.add(1, "ivan", "first")
        self.repo.add(2, "petr", "second")

        result = self.repo.get_by_id(2)

        self.assertEqual("petr", result["name"])
        self.assertEqual("second", result["message"])

    def test_get_by_id_invalid_id_raises_error(self):
        with self.subTest(case="wrong type"):
            with self.assertRaises(TypeError):
                self.repo.get_by_id("1")
        with self.subTest(case="not positive"):
            with self.assertRaises(ValueError):
                self.repo.get_by_id(0)


class TestGetByName(RepositoryTestCase):
    def test_get_by_name_returns_all_records_of_user(self):
        self.repo.add(1, "ivan", "first")
        self.repo.add(2, "petr", "other user")
        self.repo.add(3, "ivan", "second")

        result = self.repo.get_by_name("ivan")

        self.assertEqual(
            [
                {"id": 1, "name": "ivan", "message": "first"},
                {"id": 3, "name": "ivan", "message": "second"},
            ],
            result,
        )

    def test_get_by_name_returns_empty_list_if_user_unknown(self):
        self.repo.add(1, "ivan", "first")

        result = self.repo.get_by_name("nobody")

        self.assertEqual([], result)

    def test_get_by_name_does_not_return_other_users(self):
        self.repo.add(1, "ivan", "first")
        self.repo.add(2, "petr", "second")

        result = self.repo.get_by_name("petr")

        self.assertEqual(1, len(result))
        self.assertEqual("petr", result[0]["name"])

    def test_get_by_name_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.repo.get_by_name(123)

class TestUpdate(RepositoryTestCase):
    def test_update_changes_message_and_returns_true(self):
        self.repo.add(1, "ivan", "old")

        result = self.repo.update(1, "new")

        self.assertTrue(result)
        self.assertEqual("new", self.repo.get_by_id(1)["message"])

    def test_update_does_not_touch_name_and_other_records(self):
        self.repo.add(1, "ivan", "first")
        self.repo.add(2, "petr", "second")

        self.repo.update(1, "changed")

        self.assertEqual("ivan", self.repo.get_by_id(1)["name"])
        self.assertEqual("second", self.repo.get_by_id(2)["message"])

    def test_update_nonexistent_id_raises_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.repo.update(99, "text")

    def test_update_too_long_message_raises_and_keeps_old_value(self):
        self.repo.add(1, "ivan", "old")
        too_long = "m" * (MAX_MESSAGE_LENGTH + 1)

        with self.assertRaises(ValueError):
            self.repo.update(1, too_long)

        self.assertEqual("old", self.repo.get_by_id(1)["message"])

    def test_update_wrong_types_raise_type_error(self):
        self.repo.add(1, "ivan", "old")
        cases = [
            ("1", "text"),
            (None, "text"),
            (1, 123),
            (1, None),
        ]

        for comment_id, new_message in cases:
            with self.subTest(id=comment_id, message=new_message):
                with self.assertRaises(TypeError):
                    self.repo.update(comment_id, new_message)

    def test_update_invalid_values_raise_value_error(self):
        self.repo.add(1, "ivan", "old")
        cases = [
            (0, "text"),
            (-1, "text"),
            (1, ""),
        ]

        for comment_id, new_message in cases:
            with self.subTest(id=comment_id, message=new_message):
                with self.assertRaises(ValueError):
                    self.repo.update(comment_id, new_message)


class TestDelete(RepositoryTestCase):
    def test_delete_removes_record_and_returns_true(self):
        self.repo.add(1, "ivan", "hello")

        result = self.repo.delete(1)

        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_keeps_other_records(self):
        self.repo.add(1, "ivan", "first")
        self.repo.add(2, "ivan", "second")

        self.repo.delete(1)

        self.assertEqual(
            [{"id": 2, "name": "ivan", "message": "second"}],
            self.repo.get_by_name("ivan"),
        )

    def test_delete_nonexistent_id_raises_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.repo.delete(99)

    def test_delete_same_record_twice_raises_not_found(self):
        self.repo.add(1, "ivan", "hello")
        self.repo.delete(1)

        with self.assertRaises(RecordNotFoundError):
            self.repo.delete(1)

    def test_delete_invalid_id_raises_error(self):
        with self.subTest(case="wrong type"):
            with self.assertRaises(TypeError):
                self.repo.delete("1")
        with self.subTest(case="not positive"):
            with self.assertRaises(ValueError):
                self.repo.delete(0)