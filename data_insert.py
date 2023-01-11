from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main_scrap import collect_data

data = collect_data()

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('quote.id'), primary_key=True)
)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'),nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('quotes', lazy=True))


with app.app_context():
    db.create_all()

with app.app_context():
    for author in data[1]:
        author = Author(name = author)
        uniqe = Author.query.filter_by(name=author.name).first()
        if uniqe is None:
            db.session.add(author)
            db.session.commit()

    for autor in Author.query.all():
        print(autor.name)