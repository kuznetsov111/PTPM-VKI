import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from src.database import DatabaseRepository, MAX_MESSAGE_LENGTH
from src.parser import ForumParser

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "forum_page.html"

# Что мы ожидаем увидеть на сохранённой странице (id, логин)
EXPECTED_POSTS = [
    (12326457, "IceWindDale"),
    (12333689, "crypt"),
    (12336017, "Deleted"),
    (12338799, "crypt"),
    (12338896, "Deleted"),
]


def find_post(posts, post_id):
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


class TestParseHtml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Страница читается один раз на весь класс: тесты её не меняют
        cls.html = FIXTURE_PATH.read_text(encoding="utf-8")

    def setUp(self):
        self.parser = ForumParser()

    def test_parse_html_finds_all_posts(self):
        posts = self.parser.parse_html(self.html)

        self.assertEqual(5, len(posts))

    def test_parse_html_extracts_ids_and_names(self):
        posts = self.parser.parse_html(self.html)

        for post_id, name in EXPECTED_POSTS:
            with self.subTest(id=post_id):
                post = find_post(posts, post_id)
                self.assertIsNotNone(post)
                self.assertEqual(name, post["name"])

    def test_parse_html_extracts_name_of_deleted_user_without_link(self):
        posts = self.parser.parse_html(self.html)

        post = find_post(posts, 12336017)

        self.assertEqual("Deleted", post["name"])

    def test_parse_html_extracts_topic_message_text(self):
        posts = self.parser.parse_html(self.html)

        post = find_post(posts, 12326457)

        self.assertIn("Что думаете?", post["message"])
        self.assertIn("Wraith", post["message"])

    def test_parse_html_keeps_inner_html_markup(self):
        posts = self.parser.parse_html(self.html)

        post = find_post(posts, 12338896)

        self.assertIn("<blockquote>", post["message"])
        self.assertIn("<p>тоже самое покажет", post["message"])

    def test_parse_html_message_has_no_service_blocks(self):
        posts = self.parser.parse_html(self.html)

        post = find_post(posts, 12333689)

        self.assertNotIn("Ответ на", post["message"])
        self.assertNotIn("reactions", post["message"])
        self.assertNotIn("crypt", post["message"])

    def test_parse_html_empty_page_returns_empty_list(self):
        posts = self.parser.parse_html("<html><body></body></html>")

        self.assertEqual([], posts)

    def test_parse_html_ignores_articles_with_unknown_id(self):
        html = (
            '<article class="msg" id="other-1">'
            '<div class="msg-text">text</div>'
            '<div class="sign">ivan</div>'
            "</article>"
        )

        posts = self.parser.parse_html(html)

        self.assertEqual([], posts)

class TestParsePage(unittest.TestCase):
    """parse_page(url): requests.get подменяем, в интернет не ходим."""

    URL = "https://example.test/forum/topic/1"

    @classmethod
    def setUpClass(cls):
        cls.html = FIXTURE_PATH.read_text(encoding="utf-8")

    def setUp(self):
        self.parser = ForumParser()

    def make_response(self):
        response = Mock()
        response.text = self.html
        return response

    def test_parse_page_returns_posts_from_downloaded_page(self):
        with patch("src.parser.requests.get") as mock_get:
            mock_get.return_value = self.make_response()

            posts = self.parser.parse_page(self.URL)

        self.assertEqual(5, len(posts))
        self.assertEqual("IceWindDale", posts[0]["name"])

    def test_parse_page_sends_request_with_user_agent_header(self):
        with patch("src.parser.requests.get") as mock_get:
            mock_get.return_value = self.make_response()

            self.parser.parse_page(self.URL)

        mock_get.assert_called_once()
        self.assertEqual(self.URL, mock_get.call_args.args[0])
        self.assertIn("User-Agent", mock_get.call_args.kwargs["headers"])

    def test_parse_page_raises_error_on_http_error(self):
        response = self.make_response()
        response.raise_for_status.side_effect = requests.HTTPError("403")

        with patch("src.parser.requests.get") as mock_get:
            mock_get.return_value = response

            with self.assertRaises(requests.HTTPError):
                self.parser.parse_page(self.URL)


class TestSaveToDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = FIXTURE_PATH.read_text(encoding="utf-8")
        cls.posts = ForumParser().parse_html(html)

    def setUp(self):
        self.parser = ForumParser()
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    def test_save_to_db_saves_all_posts(self):
        saved = self.parser.save_to_db(self.posts, self.repo)

        self.assertEqual(5, saved)
        self.assertEqual("Deleted", self.repo.get_by_id(12336017)["name"])
        self.assertEqual(2, len(self.repo.get_by_name("crypt")))

    def test_save_to_db_skips_posts_that_already_exist(self):
        self.parser.save_to_db(self.posts, self.repo)

        saved_again = self.parser.save_to_db(self.posts, self.repo)

        self.assertEqual(0, saved_again)
        self.assertEqual(2, len(self.repo.get_by_name("crypt")))

    def test_save_to_db_skips_invalid_posts_and_saves_the_rest(self):
        posts = [
            {"id": 1, "name": "ivan", "message": "m" * (MAX_MESSAGE_LENGTH + 1)},
            {"id": 2, "name": "petr", "message": "ok"},
        ]

        saved = self.parser.save_to_db(posts, self.repo)

        self.assertEqual(1, saved)
        self.assertIsNone(self.repo.get_by_id(1))
        self.assertIsNotNone(self.repo.get_by_id(2))

    def test_save_to_db_calls_repository_add_for_each_post(self):
        repository = Mock()
        posts = [
            {"id": 1, "name": "ivan", "message": "hi"},
            {"id": 2, "name": "petr", "message": "yo"},
        ]

        self.parser.save_to_db(posts, repository)

        self.assertEqual(2, repository.add.call_count)
        repository.add.assert_any_call(1, "ivan", "hi")
        repository.add.assert_any_call(2, "petr", "yo")

    def test_save_to_db_empty_list_saves_nothing(self):
        saved = self.parser.save_to_db([], self.repo)

        self.assertEqual(0, saved)