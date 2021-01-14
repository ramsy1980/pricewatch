import re
import requests
from bs4 import BeautifulSoup
from typing import Dict

class Item:

    def __init__(self, url: str, tag_name: str, query: Dict):
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None

    def __repr__(self) -> str:
        return "<Item url={self.url} query={self.query} price={self.price}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+\.?\d*,?\d*)")
        match = pattern.search(string_price)
        found_price = match.group(1)

        without_dots = found_price.replace(".","")
        if without_dots.endswith(","): without_dots = without_dots.replace(",","")

        self.price = float(without_dots)
        return self.price