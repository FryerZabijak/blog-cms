from app import app, db, User, Article
import json
from time import sleep

app.app_context().push()
db.create_all()
user = User(login="Pepa",password="heslo",admin=True)
db.session.add(user)

# načtení dat ze souboru
data = open("basic-articles.json")
data = json.load(data)["articles"]
for article_data in data:
    article = Article(title=article_data["title"], content=article_data["content"], author_id=article_data["author_id"])
    db.session.add(article)
    db.session.commit()
