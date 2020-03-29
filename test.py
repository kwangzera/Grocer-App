"""import requests

# o tru lol. gotta find computer friendly version
# lmao wut test image
# imma find a way to get them images 
# google search banana, photo of a banana
# imma put a test image here
# run it
r = requests.get("https://cdn.mos.cms.futurecdn.net/42E9as7NaTaAi4A6JcuFwG-320-80.jpg")
lol i can alt+click the link tho. click is just click.
wot

click  open file using vbcode  ... -> when you get that error message saying u can't display the photo
boi i cant see banana. its in the folder
with open("banana.png", 'wb') as b:
    b.write(r.content)

"""

import requests, sys, webbrowser, bs4

res = requests.get('https://google.com/search?q=' + ''.join(sys.argv[1:]))
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")
linkElements = soup.select('.r a')
linkToOpen = min(5, len(linkElements))

for i in range(linkToOpen):
    webbrowser.open('https://google.com' + linkElements[i].get('href'))

