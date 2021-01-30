from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.models import Alert, Store, Item, User, requires_login
from src.common.display_flash_messages import DisplayFlashMessages
alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@requires_login
def index():
    user = User.find_by_email(session['email'])
    alerts = Alert.find_many_by('user_email', session['email'])
    if user.is_email_verified() and user.phone_number == "":
        DisplayFlashMessages.phone_number_not_verified()

    return render_template('alerts/index.html', alerts=alerts, active="alerts")


@alert_blueprint.route('/new', methods=["GET", "POST"])
@requires_login
def new_alert():
    if request.method == "POST":
        alert_name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.id)

        item.load_price()
        item.save_to_db()

        Alert(alert_name, item.id, price_limit, session['email']).save_to_db()

        return redirect(url_for('.index'))

    return render_template('alerts/new_alert.html', alert=None)


@alert_blueprint.route('/edit/<string:alert_id>', methods=["GET", "POST"])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)

    if request.method == "POST":
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_db()

        return redirect(url_for('.index'))

    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_db()

    return redirect(url_for('.index'))
