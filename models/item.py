import requests
from dataclasses import dataclass, field
from uuid import uuid4
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
from typing import Dict
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float
    _id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        self.price = None

    def __repr__(self) -> str:
        return f"<Item url={self.url} query={self.query} price={self.price}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        self.price = Decimal(sub(r'[^\d.]', '', string_price))

        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query
        }
