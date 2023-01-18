import requests
from bs4 import BeautifulSoup

def collect_data():
    start_page = 1
    end_page = 10
    collectet_data = [[],[],[]]

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
            collectet_data[1].append(quote_author)

            tags = BeautifulSoup(str(quote),features="html.parser")
            quote_tags = []
            for tag in tags.find_all("a",class_ = "tag"):
                tag = str(tag)
                tag = tag.split(">")[1]
                tag = tag.split("<")[0]
                quote_tags.append(tag)
            collectet_data[2].append(quote_tags)

        i+=1

    return collectet_data