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

    i=0
    for qoute in data[0]:
        author_id = Author.query.filter_by(name=data[1][i]).first().id
        quote = Quote(text=qoute, author_id = author_id)
        uniqe = Quote.query.filter_by(text=quote.text).first()
        if uniqe is None:
            db.session.add(quote)
        else:
            quote = uniqe
        for tag in data[2][i]:
            tag = Tag(name = tag)
            uniqe = Tag.query.filter_by(name=tag.name).first()
            if uniqe is None:
                db.session.add(tag)
            else:
                tag = uniqe
            quote.tags.append(tag)
            db.session.commit()
        i += 1

    for quote in Quote.query.all():
        print(quote.text)
        print(Author.query.filter_by(id=quote.author_id).first().name)
        for tag in quote.tags:
            print(tag.name)
        print("\n\n")
