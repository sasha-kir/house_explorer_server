from bs4 import BeautifulSoup
import requests
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BASE_URL = "http://tipdoma.ru/"

response = requests.get(BASE_URL + "/list1.html")
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

types_cards = soup.find("td", id="frkbl").find(class_="row")

with open(f"{DIR_PATH}/house_types.csv", "w", encoding="utf-8") as fout:
    for card in types_cards:
        card_body = card.find(class_="caption")
        house_type = card_body.find("h4").get_text()
        link = card_body.find(class_="btn btn-primary").get("href")
        fout.write(f"{house_type};{BASE_URL+link}\n")
        # handle types like I-515 (1-515)
        if house_type[0] == "1":
            fout.write(f"I{house_type[1:]};{BASE_URL+link}\n")
