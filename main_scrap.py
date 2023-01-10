import requests
from bs4 import BeautifulSoup
i = 1
while i < 11:
    web_page = requests.get(f"https://quotes.toscrape.com/page/{i}")
    soup = BeautifulSoup(web_page.text,features="html.parser")


    def extract_text(input_soup: BeautifulSoup, searched_class: str, type: str):
        text = input_soup.find_all(type, limit=1, class_=searched_class)
        text = BeautifulSoup(str(text), features="html.parser")
        text = text.getText()[1:-1]
        return text


    for quote in soup.find_all("div", class_="quote"):
        quote_text = extract_text(quote,"text","span")
        print(quote_text)

        quote_author = extract_text(quote, "author", "small")
        print(quote_author)

        tags = BeautifulSoup(str(quote),features="html.parser")
        quote_tags = []
        for tag in tags.find_all("a",class_ = "tag"):
            tag = str(tag)
            tag = tag.split(">")[1]
            tag = tag.split("<")[0]
            quote_tags.append(tag)
        print(quote_tags)
        print("\n------\n")
    i+=1