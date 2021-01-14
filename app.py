
import os
import re
from models.item import Item
from models.database import Database
from dotenv import load_dotenv

URL = "https://www.coolblue.nl/product/864424/apple-ipad-pro-2020-12-9-inch-256-gb-wifi-space-gray-pencil-2.html"
TAG_NAME = "strong"
QUERY = {"class": "sales-price__current"}

database = Database(os.environ.get("MONGODB_URI"))
db = database.db

print(list(db.items.find({})))
item = Item(url=URL, tag_name=TAG_NAME, query=QUERY)

print(item.load_price())