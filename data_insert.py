from main_scrap import collect_data
from config import Author,Quote,Tag,db,app
def data_insert():
    data = collect_data()


    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.app_context():
        table_lenght = len(data[1][0])
        i = 0
        while i+1 <= table_lenght:
            author = Author(name = data[1][0][i],
                            about = data[1][1][i],
                            date_of_birth = data[1][2][i],
                            place_of_birth = data[1][3][i])
            uniqe = Author.query.filter_by(name=data[1][0][i]).first()
            if uniqe is None:
                db.session.add(author)
                db.session.commit()
            i+=1

        i=0
        for qoute in data[0]:
            author_id = Author.query.filter_by(name=data[1][0][i]).first().id
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

if __name__ == "__main__": data_insert()