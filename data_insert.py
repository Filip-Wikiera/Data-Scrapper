from main_scrap import collect_data
from config import Author,Quote,Tag,db,app

data = collect_data()


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
        print(quote.author.name)
        for tag in quote.tags:
            print(tag.name)
        print("\n\n")
