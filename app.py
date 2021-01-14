
from models.item import Item

URL = "https://www.coolblue.nl/product/864424/apple-ipad-pro-2020-12-9-inch-256-gb-wifi-space-gray-pencil-2.html"
TAG_NAME = "strong"
QUERY = {"class": "sales-price__current"}

item = Item(url=URL, tag_name=TAG_NAME, query=QUERY)
item.save_to_db()

print(item.load_price())