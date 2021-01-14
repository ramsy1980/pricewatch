import re
import requests
from bs4 import BeautifulSoup
from typing import Dict
from uuid import uuid4
from common.database import database

class Item:

    def __init__(self, url: str, tag_name: str, query: Dict, _id: str = None):
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None

        self.collection = "items"
        self._id = _id or uuid4().hex # ensures we have easy to use string

    def __repr__(self) -> str:
        return f"<Item url={self.url} query={self.query} price={self.price}>"

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
    
    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query
        }

    def save_to_db(self):
        database.insert(self.collection, self.json())