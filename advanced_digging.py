from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('https://pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html.read(), "lxml")
nameList = bsObj.findAll('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())