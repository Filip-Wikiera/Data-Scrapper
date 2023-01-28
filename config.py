from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'tajne-haslo'

db = SQLAlchemy()
db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'

quotes_on_page = 10
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    quotes = db.relationship("Quote", back_populates="author")
    about = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String)


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('quote_id', db.Integer, db.ForeignKey('quote.id'), primary_key=True)
)
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('quote_id', db.Integer, db.ForeignKey('quote.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'),nullable=False)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('quotes', lazy=True))
    author = db.relationship("Author", back_populates="quotes")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    favorites = db.relationship('Quote', secondary=favorites, backref=db.backref('favorite_user', lazy=True))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
with app.app_context():
    db.create_all()