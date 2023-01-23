from flask import Flask, render_template, request, flash
from sql_init import Quote,app,tags,Tag,db
from sqlalchemy import func,desc
quotes_on_page = 10
@app.route("/")
def index():
    return render_template("index.html",
                           Quote = Quote.query.filter(Quote.id <= quotes_on_page),
                           page_number = 1)
@app.route("/page/<int:page_number>/")
def quote_pages(page_number):
    return render_template("index.html",
                           Quote = Quote.query.filter(Quote.id > quotes_on_page*(page_number-1), Quote.id <= quotes_on_page + (page_number-1)*quotes_on_page),
                           page_number = page_number)
@app.route("/search/",methods =["GET", "POST"])
def search():
    if request.method == "POST":
        serach_text = request.form.get("serach_text")
        where_to_search = request.form.get("choice")
        if where_to_search == "Cytat":
            found_quotes = Quote.query.filter(Quote.text.contains(serach_text))
            return render_template("search.html", Quote=found_quotes)
        elif where_to_search == "Autor":
            found_quotes = []
            for quote in Quote.query.all():
                if serach_text in quote.author.name:
                    found_quotes.append(quote)
            if found_quotes != []: return render_template("search.html", Quote=found_quotes)
        elif where_to_search == "Tag":
            found_quotes = []
            for quote in Quote.query.all():
                for tag in quote.tags:
                    if serach_text in tag.name and quote not in found_quotes:
                        found_quotes.append(quote)
            if found_quotes != []: return render_template("search.html", Quote=found_quotes)
            return render_template("search.html", Quote=found_quotes)
    return render_template("search.html", Quote= "")
@app.route("/statistics/")
def statistics():

    count_tags = {}
    quotes = Quote.query.all()

    for quote in quotes:
        for tag in quote.tags:
            if tag.name in count_tags: count_tags[tag.name] = count_tags[tag.name]+1
            else: count_tags[tag.name] = 1

    count_tags = sorted(count_tags.items(), key=lambda x:x[1], reverse=True)
    converted_dict = dict(count_tags[:3])

    count_authors = {}
    for author in Quote.query.group_by(Quote.author_id).order_by(desc(func.count(Quote.id))).limit(3):

        count_authors[author.author.name] = (Quote.query.filter(Quote.author_id == author.author.id).count())


    return render_template("statistics.html", count_tags = converted_dict,count_authors = count_authors)
