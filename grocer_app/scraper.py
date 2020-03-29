import requests
from bs4 import BeautifulSoup
from csv import reader
from random import getrandbits, randint
from urllib.request import urlopen

def scrape(num, url, csv):

    with open(csv) as f:
        food_items = {
            title: f"https://www.walmart.com{link}"
            for _, (title, link) in zip(range(num), reader(f))
        }

    for title, link in food_items.items():
    
        r = requests.get(url, title=title)
        if "error" in r.json():
            raise ValueError(r.json()["error"])
        json = r.json()
        if json["data"]:
            continue

        # Generating item info
        id = getrandbits(63)
        storeId = randint(1, 3)
        soup = BeautifulSoup(urlopen(link), "html.parser")

        # Scraping price
        for pr in soup.find_all(itemprop="offers"):
            try:
                price = float(pr.span.span.span.span.span.string[1:])
            except AttributeError:
                price = float(pr.span.span.span.span.string[1:])
            break
        else:
            price = 0.0

        # Scraping rating
        for ratrev in soup.find_all(itemprop="aggregateRating"):
            rating = float(ratrev.span.get("aria-label")[:3])
            break
        else:
            rating = 0.0

        # Scraping images
        for img_link in soup.find_all('img'):
            if "walmartimages.com/asr" in img_link.get('src'):
                imageUrl = f"http:{img_link.get('src')}"
                break
        else:
            imageUrl = ""
            
        title = title

        info = dict(id=id, title=title, rating=rating, price=price, storeId=storeId, imageUrl=imageUrl)
        r = requests.post(url, json=info)
        if "error" in r.json():
            raise ValueError(r.json()["error"])


