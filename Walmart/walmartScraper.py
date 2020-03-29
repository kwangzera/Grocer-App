import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from csv import reader
from pprint import pprint
from random import getrandbits, randint
from urllib.request import urlopen

foodItems = defaultdict(str)
finalItems = defaultdict(dict)

with open('c:/Users/boblu/Desktop/Programming/flask_intro/venv/venv/Walmart/allObjects.csv') as csvDataFile:
    csvReader = reader(csvDataFile)
    for row in csvReader:
        foodItems[row[0]] = f"https://www.walmart.com{row[1]}"

skip_ask = 0
for i in foodItems:
    tempItems = {}

    # Generating item info
    title = i
    url = foodItems[i]
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
    for i in "title rating price storeId imageUrl".split():
        tempItems[i] = eval(i)

    finalItems[key] = tempItems

    r = requests.post("http://127.0.0.1:5000/items", json={key: tempItems})
    if skip_ask <= 0:
        try:
            print(r.text)
            skip_ask = int(input("how many to skip"))
        except Exception as e:
            print(repr(e))
            skip_ask = 1

    skip_ask -= 1

    print(tempItems)
    print()
    
# Database items. It has already been made
# print(finalItems)
