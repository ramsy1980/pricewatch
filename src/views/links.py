from flask import Blueprint, redirect, url_for, session, flash
from src.models.user import requires_login
from src.models.item import Item

link_blueprint = Blueprint('links', __name__)


@link_blueprint.route('<string:item_id>')
@requires_login
def get_item_by_id(item_id):
    try:
        item = Item.get_by_id(item_id)
        return redirect(item.url)
    except Exception:
        flash("Invalid link", 'red')
        return redirect("/")
