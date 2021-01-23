from dataclasses import dataclass, field
from uuid import uuid4
from typing import Dict
from models.model import Model
from models.store import Store
from libs.request import Request, ItemOutOfStockError


@dataclass(eq=False)
class Item(Model):
    url: str
    store_id: str
    price: float = field(default=None)
    out_of_stock: bool = field(default=False)

    collection: str = field(init=False, default="items")
    _id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        self.store = Store.get_by_id(self.store_id)

    def __repr__(self) -> str:
        return f"<Item store={self.store.url_prefix} >"

    def load_price(self) -> float:
        try:
            self.price = Request.scrape(
                self.url,
                self.store.css_selector,
                self.store.css_selector_out_of_stock
            )
        except ItemOutOfStockError as e:
            print(e)
            self.out_of_stock = True

        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "store_id": self.store_id,
            "price": self.price,
            "out_of_stock": self.out_of_stock,
        }
