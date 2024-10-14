import requests
from bs4 import BeautifulSoup

# Args: Area where you live in
def scrapingPage(area:str) -> list:
    payload = {"m": area}
    req = requests.post("https://www.city.aizuwakamatsu.fukushima.jp/index_php/gomical/index_i.php?typ=p", data=payload)
    req.encoding = req.apparent_encoding
    bsObj = BeautifulSoup(req.text, "html.parser")
    items = bsObj.select("li.tri1")
    return items[5].text