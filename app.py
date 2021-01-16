import json
from flask import Flask, render_template, request
from models.item import Item

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def new_item():
    if request.method == "POST":

        url = request.form['url']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Item(url, tag_name, query).save_to_db()

    return render_template('new_item.html')

if __name__ == '__main__':
    app.run(debug=True)


# from models.item import Item
# from models.alert import Alert

# URL = "https://www.coolblue.nl/product/864424/apple-ipad-pro-2020-12-9-inch-256-gb-wifi-space-gray-pencil-2.html"
# TAG_NAME = "strong"
# QUERY = {"class": "sales-price__current"}

# # item = Item(url=URL, tag_name=TAG_NAME, query=QUERY)
# # item.save_to_db()

# items_loaded = Item.all()

# print(items_loaded)
# print(items_loaded[0].load_price())

# alert = Alert("1a30a634a609442f92b1a9ff3182a624", 2000)
# alert.save_to_db()