# Лабораторная работа 5. Парсинг форума и unittest

Сбор сообщений с форума linux.org.ru (id, логин, текст), сохранение в SQLite
и автоматические тесты на unittest.

## Структура

```
Lab5/
├── requirements.txt
├── src/
│   ├── database.py     # DatabaseRepository: работа с SQLite (таблица comments)
│   ├── exceptions.py   # DuplicateIdError, RecordNotFoundError
│   └── parser.py       # ForumParser: загрузка и разбор страницы форума
└── tests/
    ├── test_database.py  # тесты репозитория БД
    ├── test_parser.py    # тесты парсера
    └── fixtures/
        └── forum_page.html  # сохранённая страница форума для тестов парсера
```

## Установка

Команды выполняются из папки `Lab5`.

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск тестов

```
python -m unittest discover -s tests -t .
```

Тесты парсера не ходят в интернет: они работают с сохранённой страницей
`tests/fixtures/forum_page.html`, а `requests.get` подменяется через `unittest.mock`.

## Покрытие кода

```
coverage run --source=src -m unittest discover -s tests -t .
coverage report -m
```

## Как работает парсер

- `parse_page(url)` скачивает страницу (`requests`, заголовок `User-Agent`) и
  разбирает её (`BeautifulSoup`, `lxml`).
- Каждое сообщение это `<article class="msg">`: id берётся из атрибута
  `id` (`topic-...` или `comment-...`), логин из блока `div.sign`,
  текст из `div.msg-text` (с сохранением HTML-разметки).
- `save_to_db(parsed_data, repository)` добавляет сообщения через
  `DatabaseRepository.add`; дубликаты и некорректные записи пропускаются.