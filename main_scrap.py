import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

#locale.setlocale(locale.LC_ALL, 'en_US')
def collect_data():
    start_page = 1
    end_page = 10
    collectet_data = [[],[[],[],[],[]],[]]

    #[cytat,[autor,opis,data urodzenia,miejce urodzenia],tagi]

    i = start_page
    while i < end_page+1:
        web_page = requests.get(f"https://quotes.toscrape.com/page/{i}")
        soup = BeautifulSoup(web_page.text,features="html.parser")

        def extract_text(input_soup: BeautifulSoup, searched_class: str, type: str):
            text = input_soup.find_all(type, limit=1, class_=searched_class)
            text = BeautifulSoup(str(text), features="html.parser")
            text = text.getText()[1:-1]
            return text


        for quote in soup.find_all("div", class_="quote"):
            quote_text = extract_text(quote,"text","span")
            collectet_data[0].append(quote_text)

            quote_author = extract_text(quote, "author", "small")
            collectet_data[1][0].append(quote_author)

            tags = BeautifulSoup(str(quote),features="html.parser")
            quote_tags = []
            for tag in tags.find_all("a",class_ = "tag"):
                tag = str(tag)
                tag = tag.split(">")[1]
                tag = tag.split("<")[0]
                quote_tags.append(tag)
            collectet_data[2].append(quote_tags)

        i+=1
    for author in collectet_data[1][0]:

        author_replace = author.replace(".","-")
        author_replace = author_replace.replace("- ","-")
        author_replace = author_replace.replace(" ", "-")
        author_replace = author_replace.replace("é","e")
        author_replace = author_replace.replace("'", "")
        if author_replace[-1] == "-": author_replace = author_replace[:len(author_replace)-1]

        web_page = requests.get(f"https://quotes.toscrape.com/author/{author_replace}/")
        soup = BeautifulSoup(web_page.text, features="html.parser")

        about_author = extract_text(soup,"author-description","div")
        collectet_data[1][1].append(about_author)

        birthdate = extract_text(soup,"author-born-date","span")
        #September 20, 1948
        birthdate = datetime.strptime(birthdate,'%B %d, %Y')
        collectet_data[1][2].append(birthdate)


        birthplace = extract_text(soup, "author-born-location", "span")
        birthplace = birthplace.replace("in ","")
        collectet_data[1][3].append(birthplace)





    return collectet_data