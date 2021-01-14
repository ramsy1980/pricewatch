from typing import Dict, List
from models.item import Item
from uuid import uuid4
from common.database import database

class Alert:
    def __init__(self, item_id: str, price_limit: float, _id: str = None):
        self.item_id = item_id
        self.item = Item.get_by_id(item_id)
        self.price_limit = price_limit
        self.collection = "alerts"
        self._id = _id or uuid4().hex

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "item_id": self.item_id
        }

    def save_to_db(self):
        database.insert(self.collection, self.json())

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached price under {self.price_limit}. Latest price: {self.item.price}")

    @classmethod
    def all(cls) -> List:
        return [cls(**alert) for alert in database.find("alerts", {})]
