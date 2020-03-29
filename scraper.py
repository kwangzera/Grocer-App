import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from csv import reader
from pprint import pprint
from random import getrandbits, randint
from urllib.request import urlopen

URL = input("URL: ")
INP = input("CSV INP: ")

with open(INP) as f:
    food_items = {title: f"https://www.walmart.com{link}" for title, link in reader(f)}

continue_amount = 0
for title, url in food_items.items():

    if continue_amount <= 0:
        try:
            continue_amount = int(input("Continue #: "))
        except Exception as e:
            print(repr(e))
            continue_amount = 1

    # Generating item info
    key = getrandbits(63)
    storeId = randint(1, 3)

    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    # Scraping for the price
    for pr in soup.find_all(itemprop="offers"):
        try:
            price = float(pr.span.span.span.span.span.string[1:])
        except AttributeError:
            price = float(pr.span.span.span.span.string[1:])
        break
    else:
        price = 0.0

    # Scraping for the rating and reviews
    for ratrev in soup.find_all(itemprop="aggregateRating"):
        rating = float(ratrev.span.get("aria-label")[:3])
        break
    else:
        rating = 0.0

    # Scraping for the images
    
    for img_link in soup.find_all('img'):
        if "walmartimages.com/asr" in img_link.get('src'):
            imageUrl = f"http:{img_link.get('src')}"
            break
    else:
        imageUrl = ""

    # Inserting the information into a dictonary
    info = {key: {i: eval(i) for i in "title rating price storeId imageUrl".split()}}
    r = requests.post(URL, json=info)

    print("SENT:", info)
    print("RESPONSE:", r.text)

    continue_amount -= 1

