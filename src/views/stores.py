from flask import Blueprint, render_template, request, redirect, url_for
from src.models import Store, requires_login, requires_admin

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
@requires_login
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores, active="stores")


@store_blueprint.route('/new', methods=["GET", "POST"])
@requires_admin
def new_store():
    if request.method == "POST":
        name = request.form['name']
        currency_symbol = request.form['currency_symbol']
        url_prefix = request.form['url_prefix']
        css_selector = request.form['css_selector']
        css_selector_out_of_stock = request.form['css_selector_out_of_stock']

        if not url_prefix.endswith("/"):
            url_prefix += "/"

        Store(
            name, currency_symbol,
            url_prefix,
            css_selector,
            css_selector_out_of_stock
        ).save_to_db()

        return redirect(url_for('.index'))

    return render_template('stores/new_store.html', store=None)


@store_blueprint.route('/edit/<string:store_id>', methods=["GET", "POST"])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == "POST":
        store.name = request.form['name']
        store.currency_symbol = request.form['currency_symbol']
        store.url_prefix = request.form['url_prefix']
        store.css_selector = request.form['css_selector']
        store.css_selector_out_of_stock = request.form['css_selector_out_of_stock']

        store.save_to_db()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_db()
    return redirect(url_for('.index'))
