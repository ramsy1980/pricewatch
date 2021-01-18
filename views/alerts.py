from flask import Blueprint, render_template, request
from models.alert import Alert
from models.store import Store
from models.item import Item

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    alerts = Alert.all()
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=["GET", "POST"])
def new_alert():
    if request.method == "POST":

        alert_name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)

        item.load_price()
        item.save_to_db()

        Alert(alert_name, item._id, price_limit).save_to_db()

    return render_template('alerts/new_alert.html')
