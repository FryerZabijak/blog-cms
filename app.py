from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask("__name__")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

app.secret_key="tentoblogjesuper"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Article %r>" % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=0)
    articles = db.relationship('Article', backref='author', lazy=True)

    def __repr__(self):
        return "<User %r>" % self.id

app.app_context().push()
db.create_all()
adminUser = User(login="Pepa",password="heslo",admin=True)
db.session.add(adminUser)
adminUser2 = User(login="Pepo",password="heslo",admin=False)
db.session.add(adminUser2)

article1 = Article(title="Nejlepší článek o programování",content="Kontekt bla bla",author=1)
db.session.add(article1)
article2 = Article(title="Nejhorší článek o programování",content="Kontekt bla bla",author=1)
db.session.add(article2)
db.session.commit()


@app.route("/")
def index():
    articles = Article.query.all()
    return render_template("index.html",articles=articles)


@app.route("/about")
@app.route("/aboutus")
@app.route("/about-us")
@app.route("/o-mne")
@app.route("/omne")
@app.route("/o-nas")
@app.route("/onas")
def about():
    return render_template("about.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":
        warning=""
        login = request.form["login"]
        password = request.form["password"]
        user = User.query.filter_by(login=login, password=password).first()

        if user:
            session["user_id"]=user.id
            return redirect("/admin/articles")
        else:
            warning="Uživatel nebyl nalezen."


        return render_template("admin_login.html",warning=warning)
    else:
        if "user_id" in session:
            return redirect("/admin/articles")
        else:
            return render_template("admin_login.html")

@app.route("/admin/articles")
def admin_articles():
    if "user_id" not in session:
        return redirect("/admin/login")

    user = User.query.filter_by(id=session["user_id"]).first()
    articles = Article.query.all()

    return render_template("admin_articles.html", user=user, articles=articles)

@app.route("/admin/users")
def admin_users():
    return render_template("index.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop('user_id', None)
    return redirect("/admin/login")