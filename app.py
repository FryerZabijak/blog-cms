from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask("__name__")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

app.secret_key="tentoblogjesuper"

login_manager = LoginManager(app)
login_manager.login_view = '/admin/login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    reviews = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Article %r>" % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=0)
    articles = db.relationship('Article', backref='author', lazy=True)
    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean)

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return "<User %r>" % self.id

@app.route("/")
def index():
    articles = Article.query.order_by(desc(Article.id)).all()
    return render_template("index.html",articles=articles)

@app.route("/article/<int:id>")
def article(id):
    article = Article.query.filter_by(id=id).first()
    article.views=article.views+1
    db.session.commit()
    return render_template("article.html",article=article)


@app.route("/about")
@app.route("/aboutus")
@app.route("/about-us")
@app.route("/o-mne")
@app.route("/omne")
@app.route("/o-nas")
@app.route("/onas")
def about():
    return render_template("about.html")

@app.route("/admin")
def admin():
    return redirect("/admin/login")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        warning=""
        login = request.form["login"]
        password = request.form["password"]
        user = User.query.filter_by(login=login, password=password).first()

        if user:
            login_user(user)
            #user.is_authenticated = True
            return redirect("/admin/articles")
        else:
            warning="Špatné přihlašovací údaje."


        return render_template("admin_login.html",warning=warning)
    else:
        if current_user.is_authenticated:
            return redirect("/admin/articles")
        else:
            return render_template("admin_login.html")

@app.route("/admin/articles")
@login_required
def admin_articles():
    articles = Article.query.order_by(desc(Article.id)).all()
    return render_template("admin_articles.html", articles=articles)

@app.route("/admin/users")
@login_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)

@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect("/")

@app.route("/admin/article/delete=<int:id>")
@login_required
def delete_article(id):
    article = Article.query.filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    return redirect("/admin")

@app.route("/admin/article/edit/<int:id>", methods=["GET","POST"])
@app.route("/admin/article/edit", methods=["GET","POST"])
@login_required
def edit_article(id=None):
    if id:
        article = Article.query.filter_by(id=id).first()
    else:
        article = Article()
    users = User.query.all()
    if request.method == 'GET':
        return render_template("admin_article_edit.html",article=article,users=users)
    elif request.method == "POST":
        article.title = request.form.get("title")
        article.content = request.form.get("content")
        article.author_id = request.form.get("author_id")
        if id:
            db.session.commit()
        else:
            db.session.add(article)
            db.session.commit()
        return redirect("/admin/articles")
