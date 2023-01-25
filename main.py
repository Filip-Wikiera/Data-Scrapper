from flask import render_template, request, flash
from config import Quote,app,quotes_on_page,User,db
from sqlalchemy import func,desc
from forms import LoginForm, RegistrationForm, SearchForm
from flask_login import logout_user, login_required, current_user,login_user

with app.app_context():
    max_page = Quote.query.count()/quotes_on_page
@app.route("/")
def index():
    return render_template("index.html",
                           Quote = Quote.query.filter(Quote.id <= quotes_on_page),
                           page_number = 1,
                           max_page = max_page)
@app.route("/page/<int:page_number>/")
def quote_pages(page_number):
    if page_number > max_page: return index()

    quotes = Quote.query.filter(Quote.id > quotes_on_page * (page_number - 1),Quote.id <= quotes_on_page + (page_number - 1) * quotes_on_page)
    return render_template("index.html", Quote = quotes, page_number = page_number, max_page = max_page)
@app.route("/search/",methods =["GET", "POST"])
def search():
    form = SearchForm()
    serach_text = form.text.data
    where_to_search = form.choice.data
    if where_to_search == "Cytat":
        found_quotes = Quote.query.filter(Quote.text.contains(serach_text))
        return render_template("search.html", Quote=found_quotes,form=form)
    elif where_to_search == "Autor":
        found_quotes = []
        for quote in Quote.query.all():
            if serach_text in quote.author.name:
                found_quotes.append(quote)
        if found_quotes != []: return render_template("search.html", Quote=found_quotes, form=form)
    elif where_to_search == "Tag":
        found_quotes = []
        for quote in Quote.query.all():
            for tag in quote.tags:
                if serach_text in tag.name and quote not in found_quotes:
                    found_quotes.append(quote)
        if found_quotes != []: return render_template("search.html", Quote=found_quotes, form=form)
        return render_template("search.html", Quote=found_quotes)
    return render_template("search.html", Quote= "", form=form)
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

@app.route('/login/', methods =["GET", "POST"])
def login(break_loop = True):
    if current_user.is_authenticated:
        return index()
    form = LoginForm()
    if form.validate_on_submit() and break_loop:
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nieprawidlowa nazwa uzytkownika lub haslo')
            return login(False)
        login_user(user, remember=form.remember_me.data)
        return index()
    return render_template('login.html', form=form)
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return index()

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return index()
    form = RegistrationForm()
    if User.query.filter_by(name=form.name.data).first():
        flash("Uzytkownik juz zarejestrowany w systemie")
        return render_template('register.html', form=form)
    if form.validate_on_submit():
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Utworzono konto dla uzytkownika: {user.name}")
        return login()
    return render_template('register.html', form=form)