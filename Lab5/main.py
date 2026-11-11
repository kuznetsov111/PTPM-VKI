from src.database import DatabaseRepository
from src.parser import ForumParser

parser = ForumParser()
posts = parser.parse_page("https://www.linux.org.ru/forum/talks/12326457")

for post in posts:
    print(post["id"], post["name"], post["message"][:40])

repository = DatabaseRepository("forum.db")
print("сохранено ", parser.save_to_db(posts, repository))
repository.close()