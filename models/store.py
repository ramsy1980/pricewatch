import re
from dataclasses import dataclass, field
from uuid import uuid4
from models.model import Model


@dataclass(eq=False)
class Store(Model):
    name: str
    currency_symbol: str
    url_prefix: str
    css_selector: str
    css_selector_out_of_stock: str

    collection: str = field(init=False, default="stores")
    _id: str = field(default_factory=lambda: uuid4().hex)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "currency_symbol": self.currency_symbol,
            "url_prefix": self.url_prefix,
            "css_selector": self.css_selector,
            "css_selector_out_of_stock": self.css_selector_out_of_stock
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
