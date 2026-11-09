import re

import requests
from bs4 import BeautifulSoup

from src.exceptions import DuplicateIdError

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}

# id поста на linux.org.ru: "topic-123" (сообщение темы) или "comment-456"
POST_ID_PATTERN = re.compile(r"^(?:topic|comment)-(\d+)$")


class ForumParser:
    def __init__(self, headers=None, timeout=10):
        if headers is None:
            self.headers = DEFAULT_HEADERS
        else:
            self.headers = headers
        self.timeout = timeout

    def download_page(self, url):
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def parse_page(self, url):
        html = self.download_page(url)
        return self.parse_html(html)

    def parse_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        posts = []
        for article in soup.select("article.msg"):
            post = self.parse_article(article)
            if post is not None:
                posts.append(post)
        return posts

    def parse_article(self, article):
        match = POST_ID_PATTERN.match(article.get("id", ""))
        if match is None:
            return None

        sign = article.select_one("div.sign")
        text_block = article.select_one("div.msg-text")
        if sign is None or text_block is None:
            return None

        # Первая строка блока подписи это логин (и у обычных, и у Deleted)
        name = ""
        for text in sign.stripped_strings:
            name = text
            break
        if name == "":
            return None

        return {
            "id": int(match.group(1)),
            "name": name,
            "message": text_block.decode_contents().strip(),
        }

    def save_to_db(self, parsed_data, repository):
        saved_count = 0
        for post in parsed_data:
            try:
                repository.add(post["id"], post["name"], post["message"])
                saved_count += 1
            except (DuplicateIdError, ValueError, TypeError):
                continue
        return saved_count