from flask import Flask, render_template, url_for, request, redirect, session, jsonify
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

#
# --- Načte aktuálně přihlášeného uživatele
#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#
# --- Tabulka Článek
#
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categories = db.Column(db.PickleType, default=["uncategorized"])
    likes = db.Column(db.PickleType, default=0)
    dislikes = db.Column(db.PickleType, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    thumbnail = db.Column(db.String)

    def __repr__(self):
        return "<Article %r>" % self.id

#
# --- Tabulka User
#
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

class ArticleRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ArticleRating(user_id={self.user_id}, article_id={self.article_id}, rating={self.rating})"


@app.route("/article/<int:id>/rating", methods=["POST"])
@login_required
def create_rating(id):
    # zkontrolujte, zda uživatel již rating pro tento článek nevytvořil
    existing_rating = ArticleRating.query.filter_by(user_id=current_user.id, article_id=id).first()
    if existing_rating:
        if existing_rating.rating == request.json.get("rating"):
            existing_rating.rating = 0
        else:
            existing_rating.rating = request.json.get("rating")
        
        db.session.commit()
        return jsonify({"message": "Hodnocení úspěšně změněno."}), 200

    # vytvořte nový rating
    rating = request.json.get("rating")
    article_rating = ArticleRating(user_id=current_user.id, article_id=id, rating=rating)
    db.session.add(article_rating)
    db.session.commit()

    # aktualizujte počet likes a dislikes v tabulce Article
    article = Article.query.filter_by(id=id).first()
    likes = ArticleRating.query.filter_by(article_id=id, rating=1).count()
    dislikes = ArticleRating.query.filter_by(article_id=id, rating=-1).count()
    article.likes = likes
    article.dislikes = dislikes
    db.session.commit()

    return jsonify({"message": "Rating úspěšně vytvořen."}), 201


@app.route("/article/<int:id>/rating", methods=["GET"])
def get_ratings(id):
    # získání ratingů pro daný článek
    ratings = ArticleRating.query.filter_by(article_id=id).all()
    rating_dict = {}
    for rating in ratings:
        rating_dict[rating.user_id] = rating.rating
    return jsonify(rating_dict)


#
# --- Domovská stránka s články
#
@app.route("/")
def index():
    articles = Article.query.order_by(desc(Article.id)).all()
    return render_template("index.html",articles=articles)

#
# --- Zobrazí článek podle ID
#
@app.route("/article/<int:id>")
def article(id):
    article = Article.query.filter_by(id=id).first()
    ratings = ArticleRating.query.filter_by(article_id=id).all()

    article.views=article.views+1
    db.session.commit()

    likes = 0
    dislikes = 0
    user_rating = None

    if ArticleRating.query.filter_by(article_id=id).first():
        user_rating = ArticleRating.query.filter_by(article_id=id,user_id=current_user.id).first().rating

        for rating in ratings:
            if rating.rating == 1:
                likes += 1
            elif rating.rating == -1:
                dislikes += 1

    return render_template("article.html",article=article, likes=likes, dislikes=dislikes, user_rating=user_rating)


@app.route("/aboutus")
@app.route("/about-us")
@app.route("/o-mne")
@app.route("/omne")
@app.route("/o-nas")
@app.route("/onas")
@app.route("/oblogu")
@app.route("/about")
def about():
    return render_template("about.html")

#
# --- Pokud se někdo bude snažit do url vecpat admin, automaticky
# --- ho to přehodí buď do login nebo rovnou administrace
# --- záleží jestli je přihlášen nebo ne
#
@app.route("/admin/")
@app.route("/admin")
def admin():
    return redirect("/admin/login")
#
# --- Přihlašování ---
#
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    # Pokus o přihlášení - aktivování post
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
    # Pokud si zobrazí stránku
    else:
        # Pokud je přihlášen - zobrazí se mu administrace
        if current_user.is_authenticated:
            return redirect("/admin/articles")
        # Jinak se mu zobrazí přihlašovací menu
        else:
            return render_template("admin_login.html")
#
# --- Vypsání všech článků ---
#
@app.route("/admin/articles")
@login_required
def admin_articles():
    articles = Article.query.order_by(desc(Article.id)).all()
    return render_template("admin_articles.html", articles=articles)

#
# --- Vypsání všech uživatelů ---
#
@app.route("/admin/users")
@login_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)

#
# --- Odhlášení ---
#
@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect("/")

#
# --- Mazání článku ---
#

@app.route("/admin/article/delete=<int:id>")
@login_required
def delete_article(id):
    article = Article.query.filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    return redirect("/admin")

#
# --- Vytváření a edit článku ---
#

@app.route("/admin/article/edit/<int:id>", methods=["GET","POST"])
@app.route("/admin/article/edit", methods=["GET","POST"])
@login_required
def edit_article(id=None):
    if id:
        article = Article.query.filter_by(id=id).first()
    else:
        article = Article()
    users = User.query.all()
    # Pokud poprvé zobrazuji
    if request.method == 'GET':
        return render_template("admin_article_edit.html",article=article,users=users)
    # Ukládání
    elif request.method == "POST":
        article.title = request.form.get("title")
        article.content = request.form.get("content")
        article.author_id = request.form.get("author_id")
        # Pokud článek existuje, přepíšeme ho
        if id:
            db.session.commit()
        # Pokud ne, vytvoříme nový
        else:
            db.session.add(article)
            db.session.commit()
        return redirect("/admin/articles")
